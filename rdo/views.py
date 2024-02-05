from datetime import datetime
import csv
import io
import xlwt
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, resolve_url, redirect,get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import CreateView, UpdateView, ListView
from django.db.models import Q, F
from rdo.models import Contrato, RDO, ItemBm, QtdBM, QtdAS,AprovadorDMS,AprovadorBMS,BoletimMedicao,FRS, AssinaturaDigital, ProjetoCodigo, Area, Solicitante, AS
from .forms import ContratoForm, RdoForm, ItemForm, QtdForm, QtdASForm, AprovadorDMSForm,AprovadorBMSForm, BoletimForm, AssinaturadigitalForm, ProjetoForm, AreaForm, SolicitanteForm, FrsForm,AsForm
from django.db.models import Sum, Count, Case, When
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from usuarios.decorators import manager_required, superuser_required
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import View
import base64
from django.core.files.base import ContentFile
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

# Create your views here.
@login_required
@manager_required
def area_add(request):
    template_name = 'area_add.html'
    area_form = Area()
    objects = Area.objects.all()
    if request.method == 'POST' and request.POST.get('edit-form'):
        pk = request.POST.get('edit-form')
        area = request.POST.get('main-area')
        Area.objects.filter(pk=pk).update(area=area)
        url = '#'
        return HttpResponseRedirect(url)
    elif request.method == 'POST':
        form=AreaForm(request.POST, instance=area_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=AreaForm(instance=area_form, prefix='main')
    context={'form':form,'objects_list': objects}
    return render(request, template_name, context)

@login_required
@manager_required
def delete_area(request,pk):
    area = Area.objects.get(pk=pk)
    area.delete()
    url = '#'
    return HttpResponseRedirect(url)

@login_required
@manager_required
def solicitante_add(request):
    template_name = 'solicitante_add.html'
    solicitante_form = Solicitante()
    objects = Solicitante.objects.all()
    if request.method == 'POST' and request.POST.get('edit-form'):
        pk = request.POST.get('edit-form')
        solicitante = request.POST.get('main-solicitante')
        Solicitante.objects.filter(pk=pk).update(solicitante=solicitante)
        url = '#'
        return HttpResponseRedirect(url)
    elif request.method == 'POST':
        form=SolicitanteForm(request.POST, instance=solicitante_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=SolicitanteForm(instance=solicitante_form, prefix='main')
    context={'form':form,'objects_list': objects}
    return render(request, template_name, context)

@login_required
@manager_required
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

@login_required
@manager_required
def aprovadordms_add(request):
    template_name = 'aprovador.html'
    aprovador_form = AprovadorDMS()
    objects = AprovadorDMS.objects.all()
    if request.method == 'POST' and request.POST.get('edit-form'):
        pk = request.POST.get('edit-form')
        aprovador = request.POST.get('main-aprovador')
        AprovadorDMS.objects.filter(pk=pk).update(aprovador=aprovador)
        url = '#'
        return HttpResponseRedirect(url)
    elif request.method == 'POST':
        form=AprovadorDMSForm(request.POST, instance=aprovador_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=AprovadorDMSForm(instance=aprovador_form, prefix='main')
    context={'form':form,'objects_list': objects}
    return render(request, template_name, context)

@login_required
@manager_required
def aprovadorbms_add(request):
    template_name = 'aprovador.html'
    aprovador_form = AprovadorBMS()
    objects = AprovadorBMS.objects.all()
    if request.method == 'POST' and request.POST.get('edit-form'):
        pk = request.POST.get('edit-form')
        aprovador = request.POST.get('main-aprovador')
        AprovadorBMS.objects.filter(pk=pk).update(aprovador=aprovador)
        url = '#'
        return HttpResponseRedirect(url)
    elif request.method == 'POST':
        form=AprovadorBMSForm(request.POST, instance=aprovador_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=AprovadorBMSForm(instance=aprovador_form, prefix='main')
    context={'form':form,'objects_list': objects}
    return render(request, template_name, context)

@login_required
@manager_required
def projeto_add(request):
    template_name = 'projeto_codigo.html'
    projeto_form = ProjetoCodigo()
    objects = ProjetoCodigo.objects.all()
    if request.method == 'POST' and request.POST.get('edit-form'):
        pk = request.POST.get('edit-form')
        projeto_nome = request.POST.get('main-projeto_nome')
        ProjetoCodigo.objects.filter(pk=pk).update(projeto_nome=projeto_nome)
        url = '#'
        return HttpResponseRedirect(url)
    elif request.method == 'POST':
        form=ProjetoForm(request.POST, instance=projeto_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=ProjetoForm(instance=projeto_form, prefix='main')
    context={'form':form,'objects_list': objects}
    return render(request, template_name, context)

@login_required
@manager_required
def itembm_add(request):
    template_name = 'itembm.html'
    item_form = ItemBm()
    search = request.GET.get('q')
    objects = ItemBm.objects.all()
    if search:
        objects = objects.filter(descricao__icontains=search)
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


class RdoCreate(CreateView):
    model = RDO
    template_name = 'rdo_form.html'
    form_class = RdoForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.funcionario = self.request.user
        obj.save()  
        self.object = obj      
        return HttpResponseRedirect(self.get_success_url())

@has_role_decorator('rdo')
@login_required
def rdo_edit(request, slug):
    template_name = 'rdo_form.html'
    if request.method == "GET":
        objeto = RDO.objects.filter(slug=slug).first()
        if objeto is None:
            return redirect('rdo:rdo_list')
        form = RdoForm(instance=objeto)
        context={'form':form}
        return render(request, template_name, context)
    if request.method == "POST":
        objeto = RDO.objects.filter(slug=slug).first()
        if objeto is None:
            return redirect('rdo:rdo_list')
        form = RdoForm(request.POST, request.FILES, instance=objeto)
        if form.is_valid():
            modelo = form.save()
            modelo.save()
            url='rdo:rdo_detail'
            return HttpResponseRedirect(resolve_url(url,modelo.slug))
        else:
            context={'form':form}
            return render(request, template_name, context)

class RdoList(ListView):
    model = RDO
    template_name = 'rdo_list.html'
    paginate_by = 15
    context_object_name = 'objects_list'
    def get_queryset(self):
        queryset = super(RdoList, self).get_queryset()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(disciplina__icontains=search) |
                Q(rdo__icontains=search) |
                Q(solicitante__solicitante__icontains=search) |
                Q(unidade__area__icontains=search)
            )
        return queryset
    
class RdoListFiscal(ListView):
    model = RDO
    template_name = 'rdo_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'
    def get_queryset(self):
        queryset = super(RdoListFiscal, self).get_queryset()
        search = self.request.GET.get('q')
        logged_in_user_first_name = self.request.user.first_name
        if search:
            queryset = queryset.filter(
                Q(bmf__icontains=search) |
                Q(solicitante__solicitante__icontains=search) |
                Q(unidade__area__icontains=search)|
                Q(status__icontains=search)
            )
        return queryset.filter(solicitante__solicitante=logged_in_user_first_name)

@has_role_decorator('rdodetail')   
@login_required
def rdo_detail(request, slug):
    template_name = 'rdo_detail.html'
    obj = RDO.objects.get(slug=slug)
    qtdbm = QtdBM.objects.filter(bmf=obj.pk)
    total = QtdBM.objects.filter(bmf=obj.pk).aggregate(Sum("total"))['total__sum'] or 0
    assinatura = AssinaturaDigital.objects.filter(rdo=obj).first()
    assinatura_binario = base64.b64encode(assinatura.assinatura_digital).decode('utf-8') if assinatura else None
    if request.method == 'POST':
        form=QtdForm(request.POST)
        itembm = request.POST.get('id_itembm')
        id_qtdas = request.POST.get('id_qtdas')
        if form.is_valid():
            form=form.save(commit=False)
            form.bmf = obj
            if id_qtdas != '':
                qtdas = QtdAS.objects.get(pk=id_qtdas)
                saldo = qtdas.qtd_consumida if qtdas.qtd_consumida is not None else 0
                novo_saldo = saldo + form.qtd
                QtdAS.objects.filter(pk=id_qtdas).update(qtd_consumida=novo_saldo)
                
                
            if itembm != '':
                item_bm = ItemBm.objects.get(pk=itembm)
                form.valor = item_bm
            if form.montagem == 'DESMONTAGEM':
                form.qtd_t = form.qtd_t * -1 if form.qtd_t != None else 0
                form.qtd_e = form.qtd_e * -1 if form.qtd_e != None else 0
                form.qtd_pranchao = form.qtd_pranchao * -1 if form.qtd_pranchao != None else 0
                form.qtd_piso = form.qtd_piso * -1 if form.qtd_piso != None else 0
            form.save()
            url='#'
            return HttpResponseRedirect(url)       
    else:
        form=QtdForm()
    context = {'object': obj,'form':form, 'qtdbm':qtdbm,'assinatura_binario': assinatura_binario,'total':total, 'assinatura':assinatura}
    return render(request, template_name, context)

@has_role_decorator('fiscal')
@login_required
def delete_assinatura(request,pk, id):
    ass = AssinaturaDigital.objects.get(pk=pk)
    obj = RDO.objects.get(pk=id)
    RDO.objects.filter(pk=id).update(aprovado=False)
    ass.delete()
    return HttpResponseRedirect(resolve_url('rdo:rdo_detail',obj.slug))

@has_role_decorator('rdo')
@login_required
def delete_item(request,id, ind):
    qtd = QtdBM.objects.get(pk=id)
    obj = RDO.objects.get(pk=ind)
    qtd.delete()
    return HttpResponseRedirect(resolve_url('rdo:rdo_detail',obj.slug))

from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class AssinaturaRDOView(LoginRequiredMixin, View):
    template_name = 'assinatura_rdo.html'

    def get(self, request, pk):
        rdo = get_object_or_404(RDO, pk=pk)
        form = AssinaturadigitalForm()
        context = {'rdo': rdo, 'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        rdo = get_object_or_404(RDO, pk=pk)
        form = AssinaturadigitalForm(request.POST, request.FILES)
        ass = request.POST.get('assinatura_digital')
        if form.is_valid():
            # Realize as verificações necessárias antes de aprovar o RDO
            # Por exemplo, verifique se o usuário atual é autorizado a assinar
            # ...

            
            # Registre quem assinou e quando
            assinatura = form.save(commit=False)
            assinatura.rdo = rdo
            assinatura.usuario_assinatura = request.user

            assinatura_base64 = ass.split(';base64,')[-1]

            # Decodifique a assinatura base64 e salve-a no campo BinaryField
            decoded_data = base64.b64decode(assinatura_base64)
            assinatura.assinatura_digital = decoded_data

            assinatura.data_hora_assinatura = timezone.now()
            assinatura.save()

            # Marque o RDO como aprovado
            rdo.aprovado = True
            rdo.save()

            # Redirecione para o sucesso ou para a mesma página de detalhes do RDO
            return HttpResponseRedirect(resolve_url('rdo:rdo_detail',rdo.slug))  # Substitua '#' pela URL desejada

        context = {'rdo': rdo, 'form': form}
        return render(request, self.template_name, context)


class BoletimCreate(CreateView):
    model = BoletimMedicao
    template_name = 'bm_form.html'
    form_class = BoletimForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.funcionario = self.request.user
        obj.save()  
        self.object = obj      
        return HttpResponseRedirect(self.get_success_url())
 
class BoletimUpdate(UpdateView):
    model = BoletimMedicao
    template_name = 'bm_form.html'
    form_class = BoletimForm

class BoletimList(ListView):
    model = BoletimMedicao
    template_name = 'bm_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'
    def get_queryset(self):
        queryset = super(BoletimList, self).get_queryset()
        search = self.request.GET.get('q')
        dms_null = self.request.GET.get('dms_null')
        if search:
            queryset = queryset.filter(
                Q(bm_n__icontains=search) |
                Q(d_aprovador__aprovador__icontains=search) |
                Q(unidade__area__icontains=search)|
                Q(d_numero__icontains=search)
            )
        if dms_null:
            queryset = queryset.filter(d_numero=None)
        return queryset

@login_required
@manager_required
def boletim_detail(request, pk):    
    template_name = 'bm_detail.html'
    obj = BoletimMedicao.objects.get(pk=pk)
    item = QtdBM.objects.filter(bmf__bm=pk,valor__isnull=False).values('valor__item_ref','valor__descricao','valor__und','valor__preco_item').annotate(Sum('total')).annotate(Sum('qtd'))
    

    if request.method == 'POST':
        vi = request.POST.get('valores')
        vi = str(vi)
        present = vi.split(",")
        present.pop()
        for i in present:
            if not i == "null":
                RDO.objects.filter(pk=i).update(bm=pk)
        bm_valor = QtdBM.objects.filter(bmf__bm=pk).aggregate(Sum('total'))['total__sum'] or 0
        BoletimMedicao.objects.filter(pk=pk).update(valor=bm_valor)
        url='#'
        return HttpResponseRedirect(url)

    context = {'object': obj,'item':item}
    return render(request, template_name, context)

@login_required
@manager_required
def bm_delete(request, pk, id):
    RDO.objects.filter(pk=id).update(bm=None)
    bm_valor = QtdBM.objects.filter(bmf__bm=pk).aggregate(Sum('total'))['total__sum'] or 0
    BoletimMedicao.objects.filter(pk=pk).update(valor=bm_valor)
    return HttpResponseRedirect(resolve_url('rdo:bm_detail',pk))

def export_csv_view(request,pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data_BM {}.csv"'.format(str(pk).zfill(5))

    writer = csv.writer(response, delimiter=';')
    #writer.writerow(['Número Antes', 'Número Depois', 'Quantidade'])
    #for _ in range(3):
        #writer.writerow(['0000', '0000', '0000'])
    # Agrupa os registros pelo campo 'valor' e calcula a soma da coluna 'qtd'
    writer.writerow(['0', '0000000000', '0','10','10','0,00'])
    qtd_bm_objects = QtdBM.objects.filter(bmf__bm=pk,valor__isnull=False).values('valor__item_ref', 'bmf__bm').annotate(total_qtd=Sum('qtd'))

    for qtd_bm in qtd_bm_objects:
        # Divida o campo 'item_ref' usando o caractere "-"
        numero_antes, numero_depois = qtd_bm['valor__item_ref'].split('-')

        total_qtd_formated = '{:.3f}'.format(qtd_bm['total_qtd']).replace('.',',')
        writer.writerow(['0', '0000000000',numero_antes, numero_depois, total_qtd_formated])

    return response

class FrsList(ListView):
    model = FRS
    template_name = 'frs_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'

class FRSCreate(CreateView):
    model = FRS
    template_name = 'frs_form.html'
    form_class = FrsForm
 
class FRSUpdate(UpdateView):
    model = FRS
    template_name = 'frs_form.html'
    form_class = FrsForm

@login_required
@manager_required
def frs_detail(request, pk):    
    template_name = 'frs_detail.html'
    obj = FRS.objects.get(pk=pk)
    itens = BoletimMedicao.objects.filter(frs=None)
    if request.method == 'POST':
        vi = request.POST.get('valores')
        vi = str(vi)
        present = vi.split(",")
        present.pop()
        for i in present:
            if not i == "null":
                BoletimMedicao.objects.filter(pk=i).update(frs=pk)
        bm_valor = BoletimMedicao.objects.filter(frs=pk).aggregate(Sum('valor'))['valor__sum'] or 0
        FRS.objects.filter(pk=pk).update(valor=bm_valor)
        url='#'
        return HttpResponseRedirect(url)
    context = {'object': obj, 'itens':itens}
    return render(request, template_name, context)

@login_required
@manager_required
def frsitem_delete(request, pk, id):
    BoletimMedicao.objects.filter(pk=pk).update(frs=None)
    
    valor_total = BoletimMedicao.objects.filter(frs=id).aggregate(Sum('valor'))['valor__sum'] or 0

    FRS.objects.filter(pk=id).update(valor=valor_total)
    return HttpResponseRedirect(resolve_url('rdo:frs_detail',id))

class ASCreate(CreateView):
    model = AS
    template_name = 'as_form.html'
    form_class = AsForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.funcionario = self.request.user
        obj.save()  
        self.object = obj      
        return HttpResponseRedirect(self.get_success_url())

@has_role_decorator('as')
@login_required
def as_edit(request, slug):
    template_name = 'as_form.html'
    if request.method == "GET":
        objeto = AS.objects.filter(slug=slug).first()
        if objeto is None:
            return redirect('rdo:as_list')
        form = AsForm(instance=objeto)
        context={'form':form}
        return render(request, template_name, context)
    if request.method == "POST":
        objeto = AS.objects.filter(slug=slug).first()
        if objeto is None:
            return redirect('rdo:as_list')
        form = AsForm(request.POST, request.FILES, instance=objeto)
        if form.is_valid():
            modelo = form.save()
            modelo.save()
            url='rdo:as_detail'
            return HttpResponseRedirect(resolve_url(url,modelo.slug))
        else:
            context={'form':form}
            return render(request, template_name, context)

class ASList(ListView):
    model = AS
    template_name = 'as_list.html'
    paginate_by = 15
    context_object_name = 'objects_list'
    def get_queryset(self):
        queryset = super(ASList, self).get_queryset()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(a_s__icontains=search) |
                Q(solicitante__solicitante__icontains=search)
            )
        return queryset

@has_role_decorator('as')   
@login_required
def as_detail(request, slug):
    template_name = 'as_detail.html'
    obj = AS.objects.get(slug=slug)
    total = QtdAS.objects.filter(a_s=obj.pk).aggregate(Sum("total"))['total__sum'] or 0
    if request.method == 'POST':
        form=QtdASForm(request.POST)
        itembm = request.POST.get('id_itembm')
        if form.is_valid():
            form=form.save(commit=False)
            form.a_s = obj
            item_bm = ItemBm.objects.get(pk=itembm)
            form.valor = item_bm
            form.save()
            url='#'
            return HttpResponseRedirect(url)       
    else:
        form=QtdASForm()
    context = {'object': obj,'form':form,'total':total}
    return render(request, template_name, context)

@has_role_decorator('as')
@login_required
def delete_item_as(request,id, ind):
    qtd = QtdAS.objects.get(pk=id)
    obj = AS.objects.get(pk=ind)
    qtd.delete()
    return HttpResponseRedirect(resolve_url('rdo:as_detail',obj.slug))

########### import csv ##############

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

@manager_required
def import_csv_itembm(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data(data)
        return HttpResponseRedirect(reverse('rdo:itembm_add'))

    template_name = 'model_import.html'
    return render(request, template_name)

def save_data_rdo(data):
    aux = []
    for item in data:
        funcionario = 2
        data_periodo = item.get('data_periodo')
        disciplina = item.get('disciplina')
        unidade = int(item.get('unidade'))
        solicitante = item.get('solicitante')
        contrato = item.get('contrato')
        tipo = item.get('tipo')
        escopo = item.get('escopo')
        local = item.get('local')
        projeto_cod = item.get('projeto_cod')
        clima = item.get('clima')
        inicio = item.get('inicio')
        termino = item.get('termino')
        inicio_pt = item.get('inicio_pt')
        termino_pt = item.get('termino_pt')
        #valor = float(item.get('valor'))
        #status = True if item.get('status') == 'True' else False
        obj = RDO(
                funcionario = User.objects.get(pk=funcionario),
                data_periodo = datetime.strptime(data_periodo, '%d/%m/%Y').date(),
                disciplina = disciplina,
                unidade = Area.objects.get(pk=unidade),
                solicitante = Solicitante.objects.get(pk=solicitante),
                contrato = Contrato.objects.get(pk=contrato),
                escopo = escopo,
                local = local,
                tipo = tipo,
                projeto_cod = ProjetoCodigo.objects.get(pk=projeto_cod),
                clima = clima,
                inicio = inicio,
                termino = termino,
                inicio_pt = inicio_pt,
                termino_pt = termino_pt,
        )
        aux.append(obj)
    RDO.objects.bulk_create(aux)

@manager_required
def import_csv_rdo(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data_rdo(data)
        return HttpResponseRedirect(reverse('rdo:rdo_list'))

    template_name = 'model_import.html'
    return render(request, template_name)

##############extras
def update_from_csv_itembm(request):
    if 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            item_ref = row['item_ref']
            preco_item = row['preco_item']

            try:
                item = ItemBm.objects.get(item_ref=item_ref)
                item.preco_item = preco_item
                item.save()
            except ItemBm.DoesNotExist:
                # Tratar o caso em que o item_ref não existe no banco de dados
                pass

        return HttpResponse("Atualização concluída com sucesso!")

    return HttpResponse("Falha na atualização. Certifique-se de fornecer um arquivo CSV.")


########## xls excel export ###################

def export_xlsx(model, filename, queryset, columns):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)

    row_num = 0

    header_style = xlwt.easyxf('pattern: pattern solid, fore_color dark_blue; font: color white, bold True;')

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], header_style)

    default_style = xlwt.XFStyle()

    # Definindo um estilo para data (DD/MM/YYYY)
    date_style = xlwt.easyxf(num_format_str='DD/MM/YYYY')

    rows = queryset
    for row, rowdata in enumerate(rows):
        row_num += 1
        for col, val in enumerate(rowdata):
            if 'data' in columns[col].lower():
                default_style = date_style
            else:
                default_style = xlwt.XFStyle()  # Reseta o estilo para não afetar outras colunas
            ws.write(row_num, col, val, default_style)

    wb.save(response)
    return response


@login_required
def export_xlsx_func_bmf(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'BoletimMedicao'
    filename = 'bmf_exportados.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = BoletimMedicao.objects.all().values_list('bm_n','funcionario__username','periodo_inicio','d_numero','b_numero','d_status',
                                             'd_data','d_aprovador','frs__frs','valor','follow_up','rev',
                                              'unidade__area')

    columns = ('bm_n','Planejador','data','DMS','BMS','status',
                                             'data DMS','aprovador','frs__frs','valor','OBS','rev','unidade')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response

@has_role_decorator('fiscal')
@login_required
def export_movimentacao(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'QtdBM'
    filename = 'movimentação.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = QtdBM.objects.filter(placa__isnull=False,bmf__solicitante__solicitante=request.user.first_name).values_list('placa','montagem','bmf__data_periodo','bmf__unidade__area'
                                                                     ,'bmf__solicitante__solicitante','qtd','qtd_t','qtd_e',
                                                                     'qtd_pranchao','qtd_piso')
                                             

    columns = ('placa','montagem','bmf__data_periodo','bmf__unidade','bmf__solicitante','qtd_módulo','qtd_tubo','qtd_encaixe','qtd_pranchao',
               'qtd_piso')
                                                                     
    response = export_xlsx(model, filename_final, queryset, columns)
    return response

@has_role_decorator('rdo')
@login_required
def export_movimentacao_completa(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'QtdBM'
    filename = 'movimentação.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = QtdBM.objects.filter(placa__isnull=False).values_list('placa','montagem','bmf__data_periodo','bmf__unidade__area'
                                                                     ,'bmf__solicitante__solicitante','qtd','qtd_t','qtd_e',
                                                                     'qtd_pranchao','qtd_piso')
                                             

    columns = ('placa','montagem','bmf__data_periodo','bmf__unidade','bmf__solicitante','qtd_módulo','qtd_tubo','qtd_encaixe','qtd_pranchao',
               'qtd_piso')
                                                                     
    response = export_xlsx(model, filename_final, queryset, columns)
    return response

##########pdf bm########
@login_required
def render_pdf_view(request, pk):
    object = get_object_or_404(BoletimMedicao, pk=pk)
    template_path = 'bm.html'
    item = QtdBM.objects.filter(bmf__bm=pk,valor__isnull=False).values('valor__item_ref','valor__descricao','valor__und','valor__preco_item').annotate(Sum('total')).annotate(Sum('qtd'))
    
    context = {'object': object,'item':item }
   
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    #if download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

