from datetime import datetime
import csv
import io
import xlwt
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render, resolve_url
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import CreateView, UpdateView, ListView
from django.db.models import Q
from .models import Contrato, BMF, ItemBm, QtdBM,Aprovador,DMS,BMS,FRS
from .forms import ContratoForm, BmfForm, ItemForm, QtdForm,AprovadorForm,DmsForm,BmsForm,FrsForm
from django.db.models import Sum
from django.contrib.auth.models import User
from romaneio.models import Area, Solicitante 

def contrato_add(request):
    template_name = 'contrato.html'
    contrato_form = Contrato()
    objects = Contrato.objects.all()
    if request.method == 'POST' and request.POST.get('edit-form'):
        pk = request.POST.get('edit-form')
        contrato = request.POST.get('main-contrato')
        Contrato.objects.filter(pk=pk).update(contrato=contrato)
        url = '#'
        return HttpResponseRedirect(url)
    elif request.method == 'POST':
        form=ContratoForm(request.POST, instance=contrato_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=ContratoForm(instance=contrato_form, prefix='main')
    context={'form':form,'objects_list': objects}
    return render(request, template_name, context)

def aprovador_add(request):
    template_name = 'aprovador.html'
    aprovador_form = Aprovador()
    objects = Aprovador.objects.all()
    if request.method == 'POST' and request.POST.get('edit-form'):
        pk = request.POST.get('edit-form')
        aprovador = request.POST.get('main-aprovador')
        Aprovador.objects.filter(pk=pk).update(aprovador=aprovador)
        url = '#'
        return HttpResponseRedirect(url)
    elif request.method == 'POST':
        form=AprovadorForm(request.POST, instance=aprovador_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=AprovadorForm(instance=aprovador_form, prefix='main')
    context={'form':form,'objects_list': objects}
    return render(request, template_name, context)

def itembm_add(request):
    template_name = 'itembm.html'
    item_form = ItemBm()
    search = request.GET.get('search')
    objects = ItemBm.objects.all()
    if search:
        objects = objects.filter(item_ref__icontains=search)
    else:
        objects = objects.filter(pk=1)
    if request.method == 'POST' and request.POST.get('edit-form'):
        pk = request.POST.get('edit-form')
        item_to_update = ItemBm.objects.get(pk=pk)
        form=ItemForm(request.POST, instance=item_to_update, prefix='main')
        if form.is_valid():
            item = form.save(commit=False)
            item.contrato = form.cleaned_data['contrato']
            item.item_ref = form.cleaned_data['item_ref']
            item.disciplina = form.cleaned_data['disciplina']
            item.descricao = form.cleaned_data['descricao']
            item.und = form.cleaned_data['und']
            item.preco_item = form.cleaned_data['preco_item']
            item.save()
            url = '#'
            return HttpResponseRedirect(url)
        
    elif request.method == 'POST':
        form=ItemForm(request.POST, instance=item_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=ItemForm(instance=item_form, prefix='main')
    context={'form':form,'objects_list': objects, 'limitador':'limit'}
    return render(request, template_name, context)

class BmfList(ListView):
    model = BMF
    template_name = 'bmf_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'
    def get_queryset(self):
        queryset = super(BmfList, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(bmf__icontains=search) |
                Q(solicitante__solicitante__icontains=search) |
                Q(unidade__area__icontains=search)|
                Q(status__icontains=search)
            )
        return queryset
class DmsList(ListView):
    model = DMS
    template_name = 'dms_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'
 
class BmsList(ListView):
    model = BMS
    template_name = 'bms_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'

class FrsList(ListView):
    model = FRS
    template_name = 'frs_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'

class BmfCreate(CreateView):
    model = BMF
    template_name = 'bmf_form.html'
    form_class = BmfForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.funcionario = self.request.user
        obj.save()  
        self.object = obj      
        return HttpResponseRedirect(self.get_success_url())
 
class BmfUpdate(UpdateView):
    model = BMF
    template_name = 'bmf_form.html'
    form_class = BmfForm

class DMSCreate(CreateView):
    model = DMS
    template_name = 'bmf_form.html'
    form_class = DmsForm
 
class DMSUpdate(UpdateView):
    model = DMS
    template_name = 'bmf_form.html'
    form_class = DmsForm

class BmsCreate(CreateView):
    model = BMS
    template_name = 'bmf_form.html'
    form_class = BmsForm
 
class BmsUpdate(UpdateView):
    model = BMS
    template_name = 'bmf_form.html'
    form_class = BmsForm

class FRSCreate(CreateView):
    model = FRS
    template_name = 'bmf_form.html'
    form_class = FrsForm
 
class FRSUpdate(UpdateView):
    model = FRS
    template_name = 'bmf_form.html'
    form_class = FrsForm
############## jsonitens
def json_itens(request, ref):
    data = list(ItemBm.objects.values().filter(item_ref=ref))
    return JsonResponse({'data':data})
def json_fat_uni(request,begin,end):
    data_inicial = begin
    data__final = end
    data = list(BMF.objects.filter(data_periodo__range=[data_inicial, data__final]).values('unidade__area').annotate(Sum('valor')))
    return JsonResponse({'data':data})
def json_fat_sol(request,begin,end):
    data_inicial = begin
    data__final = end
    data = list(BMF.objects.filter(data_periodo__range=[data_inicial, data__final]).values('solicitante__solicitante').annotate(Sum('valor')))
    return JsonResponse({'data':data})
def json_fat_tipo(request,begin,end):
    data_inicial = begin
    data__final = end
    data = list(BMF.objects.filter(data_periodo__range=[data_inicial, data__final]).values('tipo').annotate(Sum('valor')))
    return JsonResponse({'data':data})
def json_fat_dms(request,begin,end,status):
    data_inicial = begin
    data__final = end
    status = status
    data = list(DMS.objects.filter(created__range=[data_inicial, data__final],status=status).values('aprovador__aprovador').annotate(Sum('valor')))
    return JsonResponse({'data':data})


###############
def bmf_detail(request, pk):
    template_name = 'bmf_detail.html'
    obj = BMF.objects.get(pk=pk)
    qtdbm = QtdBM.objects.filter(bmf=pk)
    item_form = QtdBM()
    if request.method == 'POST':
        form=QtdForm(request.POST, instance=item_form, prefix='main')
        itembm = request.POST.get('hashid')
        if form.is_valid():
            obj.item_bm.add(itembm)
            form=form.save(commit=False)
            form.bmf = obj
            form.save()
            qtdbm = QtdBM.objects.filter(bmf=pk)
            valor_total = 0
            for item in qtdbm:
                valor_total += item.total
            BMF.objects.filter(pk=pk).update(valor=valor_total)
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=QtdForm(instance=item_form, prefix='main')
 
    context = {'object': obj, 'form':form, 'qtdbm':qtdbm}
    return render(request, template_name, context)

def delete_item(request, pk, id, ind):
    item = ItemBm.objects.get(pk=pk)
    qtd = QtdBM.objects.get(pk=id)
    obj = BMF.objects.get(pk=ind)
    qtd.delete()
    obj.item_bm.remove(item)
    qtdbm = QtdBM.objects.filter(bmf=ind)
    valor_total = 0
    for x in qtdbm:
        valor_total += x.total
    BMF.objects.filter(pk=ind).update(valor=valor_total)
    return HttpResponseRedirect(resolve_url('financeiro:bmf_detail',obj.pk))

def dms_detail(request, pk):    
    template_name = 'dms_detail.html'
    obj = DMS.objects.get(pk=pk)
    itens = BMF.objects.filter(dms=None)
    if request.method == 'POST':
        bmf = request.POST.get('bmf')
        BMF.objects.filter(pk=bmf).update(dms=pk)
        qtditem = BMF.objects.filter(dms=pk)
        valor_total = 0
        for item in qtditem:
            valor_total += item.valor
        DMS.objects.filter(pk=pk).update(valor=valor_total)
        url='#'
        return HttpResponseRedirect(url)
    context = {'object': obj, 'itens':itens}
    return render(request, template_name, context)

def dmsitem_delete(request, pk, id):
    BMF.objects.filter(pk=pk).update(dms=None)
    qtditem = BMF.objects.filter(dms=id)
    valor_total = 0
    for item in qtditem:
        valor_total += item.valor
    DMS.objects.filter(pk=id).update(valor=valor_total)
    return HttpResponseRedirect(resolve_url('financeiro:dms_detail',id))

def bms_detail(request, pk):    
    template_name = 'bms_detail.html'
    obj = BMS.objects.get(pk=pk)
    itens = DMS.objects.filter(bms=None)
    if request.method == 'POST':
        dms = request.POST.get('dms')
        DMS.objects.filter(pk=dms).update(bms=pk)
        qtditem = DMS.objects.filter(bms=pk)
        valor_total = 0
        for item in qtditem:
            valor_total += item.valor
        BMS.objects.filter(pk=pk).update(valor=valor_total)
        url='#'
        return HttpResponseRedirect(url)
    context = {'object': obj, 'itens':itens}
    return render(request, template_name, context)

def bmsitem_delete(request, pk, id):
    DMS.objects.filter(pk=pk).update(bms=None)
    qtditem = DMS.objects.filter(bms=id)
    valor_total = 0
    for item in qtditem:
        valor_total += item.valor
    BMS.objects.filter(pk=id).update(valor=valor_total)
    return HttpResponseRedirect(resolve_url('financeiro:bms_detail',id))

def frs_detail(request, pk):    
    template_name = 'frs_detail.html'
    obj = FRS.objects.get(pk=pk)
    itens = BMS.objects.filter(frs=None)
    if request.method == 'POST':
        bms = request.POST.get('bms')
        BMS.objects.filter(pk=bms).update(frs=pk)
        qtditem = BMS.objects.filter(frs=pk)
        valor_total = 0
        for item in qtditem:
            valor_total += item.valor
        FRS.objects.filter(pk=pk).update(valor=valor_total)
        url='#'
        return HttpResponseRedirect(url)
    context = {'object': obj, 'itens':itens}
    return render(request, template_name, context)

def frsitem_delete(request, pk, id):
    BMS.objects.filter(pk=pk).update(frs=None)
    qtditem = BMS.objects.filter(frs=id)
    valor_total = 0
    for item in qtditem:
        valor_total += item.valor
    FRS.objects.filter(pk=id).update(valor=valor_total)
    return HttpResponseRedirect(resolve_url('financeiro:frs_detail',id))


######################### importações e exportações

def save_data(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:
        contrato = 1
        item_ref = item.get('item_ref')
        disciplina = item.get('disciplina')
        descricao = item.get('descricao')
        und = item.get('und')
        preco_item = item.get('preco_item')
        obj = ItemBm(
                contrato = Contrato.objects.get(pk=contrato),
                item_ref = item_ref,
                disciplina = disciplina,
                descricao = descricao,
                und = und,
                preco_item = preco_item,
        )
        aux.append(obj)
    ItemBm.objects.bulk_create(aux)
def import_csv(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data(data)
        return HttpResponseRedirect(reverse('financeiro:bmf_list'))

    template_name = 'itemcontrato_import.html'
    return render(request, template_name)


def export_xlsx(model, filename, queryset, columns):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    default_style = xlwt.XFStyle()

    rows = queryset
    for row, rowdata in enumerate(rows):
        row_num += 1
        for col, val in enumerate(rowdata):
            ws.write(row_num, col, val, default_style)

    wb.save(response)
    return response


def export_xlsx_func_bmf(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'BMF'
    filename = 'bmf_exportados.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = BMF.objects.all().values_list('bmf','funcionario__username','data_periodo','unidade__area','solicitante__solicitante','auth_serv',
                                             'escopo','local','id_serv','tipo','valor','status','dms__dms_n','dms__aprovador__aprovador',
                                             'dms__data_aprov','dms__status','dms__bms__bms_n','dms__bms__status',
                                             'dms__bms__aprovador__aprovador','dms__bms__frs__frs_n','dms__bms__frs__status_frs',
                                             'dms__bms__frs__data_aprov','dms__bms__frs__nf','dms__bms__frs__data_emissão',
                                             'dms__bms__frs__status_nf')

    columns = ('bmf','Planejador/Medidor','data_periodo','unidade','solicitante','AS/ASE',
                'escopo','local','id_serv','tipo','valor','status','dms','dms__aprovador',
                'dms__data_aprov','dms__status','bms','bms__status',
                'bms__aprovador','frs','status_frs',
                'frs__data_aprov','nf','data_emissão',
                'status_nf')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response

###############################################################################
def save_data_bmf(data):
    aux = []
    for item in data:
        funcionario = 1
        data_periodo = item.get('data_periodo')
        rev = item.get('rev')
        unidade = item.get('unidade')
        solicitante = item.get('solicitante')
        contrato = item.get('contrato')
        auth_serv = item.get('auth_serv')
        escopo = item.get('escopo')
        local = item.get('local')
        id_serv = item.get('id_serv')
        tipo = item.get('tipo')
        valor = float(item.get('valor'))
        status = True if item.get('status') == 'True' else False
        obj = BMF(
                funcionario = User.objects.get(pk=funcionario),
                data_periodo = datetime.strptime(data_periodo, '%d/%m/%Y').date(),
                rev = rev,
                unidade = Area.objects.get(pk=unidade),
                solicitante = Solicitante.objects.get(pk=solicitante),
                contrato = Contrato.objects.get(pk=contrato),
                auth_serv = auth_serv,
                escopo = escopo,
                local = local,
                id_serv = id_serv,
                tipo = tipo,
                valor = valor,
                status = status,
        )
        aux.append(obj)
    BMF.objects.bulk_create(aux)
def import_csv_bmf(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data_bmf(data)
        return HttpResponseRedirect(reverse('financeiro:bmf_list'))

    template_name = 'itemcontrato_import.html'
    return render(request, template_name)

def save_data_dms(data):
    aux = []
    for item in data:
        dms_n = item.get('dms_n')
        status = item.get('status')
        data_aprov = item.get('data_aprov')
        aprovador = int(item.get('aprovador'))
        valor = item.get('valor')
        obj = DMS(
                dms_n = dms_n,
                status = status,
                data_aprov = datetime.strptime(data_aprov, '%d/%m/%Y').date(),
                aprovador = Aprovador.objects.get(pk=aprovador),
                valor = valor,
                
        )
        aux.append(obj)
    DMS.objects.bulk_create(aux)
def import_csv_dms(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data_dms(data)
        return HttpResponseRedirect(reverse('financeiro:bmf_list'))

    template_name = 'itemcontrato_import.html'
    return render(request, template_name)


def save_data_aprovador(data):
    aux = []
    for item in data:
        aprovador = item.get('aprovador')
        obj = Aprovador(
                aprovador = aprovador,
        )
        aux.append(obj)
    Aprovador.objects.bulk_create(aux)
def import_csv_aprovador(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data_aprovador(data)
        return HttpResponseRedirect(reverse('financeiro:bmf_list'))

    template_name = 'itemcontrato_import.html'
    return render(request, template_name)

def save_data_solicitante(data):
    aux = []
    for item in data:
        area = item.get('area')
        obj = Area(
                area = area,
        )
        aux.append(obj)
    Area.objects.bulk_create(aux)
def import_csv_solicitante(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data_solicitante(data)
        return HttpResponseRedirect(reverse('financeiro:bmf_list'))

    template_name = 'itemcontrato_import.html'
    return render(request, template_name)