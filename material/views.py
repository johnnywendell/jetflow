import xlwt
import csv
import io
from django.urls import reverse
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Tratamento, TintaFundo, TintaIntermediaria, TintaAcabamento, Material
from .forms import MaterialForm, TratamentoForm, TintaFundoForm, TintaIntermediariaForm, TintaAcabamentoForm, MaterialForms
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import os
from django.conf import settings
from usuarios.decorators import manager_required
from romaneio.models import Romaneio
from django.db.models import Sum


@login_required
@manager_required
def tratamento_add(request):
    template_name = 'tratamento_add.html'
    tratamento_form = Tratamento()
    objects = Tratamento.objects.all()
    if request.method == 'POST':
        form=TratamentoForm(request.POST, instance=tratamento_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=TratamentoForm(instance=tratamento_form, prefix='main')
    context={'form':form,'objects_list': objects}
    return render(request, template_name, context)
@login_required
@manager_required
def tintafundo_add(request):
    template_name = 'tintafundo_add.html'
    tintaf_form = TintaFundo()
    objects = TintaFundo.objects.all()
    if request.method == 'POST':
        form=TintaFundoForm(request.POST, instance=tintaf_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=TintaFundoForm(instance=tintaf_form, prefix='main')
    context={'form':form,'objects_list': objects}
    return render(request, template_name, context)
@login_required
@manager_required
def tintaintermediaria_add(request):
    template_name = 'tintaintermediaria_add.html'
    tintai_form = TintaIntermediaria()
    objects = TintaIntermediaria.objects.all()
    if request.method == 'POST':
        form=TintaIntermediariaForm(request.POST, instance=tintai_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=TintaIntermediariaForm(instance=tintai_form, prefix='main')
    context={'form':form,'objects_list': objects}
    return render(request, template_name, context)
@login_required
@manager_required
def tintaacabamento_add(request):
    template_name = 'tintaacabamento_add.html'
    tintaa_form = TintaAcabamento()
    objects = TintaAcabamento.objects.all()
    if request.method == 'POST':
        form=TintaAcabamentoForm(request.POST, instance=tintaa_form, prefix='main')
        if form.is_valid():
            form=form.save()
            url='#'
            return HttpResponseRedirect(url)
    else:
        form=TintaAcabamentoForm(instance=tintaa_form, prefix='main')
    context={'form':form,'objects_list': objects}
    return render(request, template_name, context)



class MaterialList(ListView):
    model = Material
    template_name = 'material_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'
    def get_queryset(self):
        queryset = super(MaterialList, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(n_romaneio__romaneio__icontains=search) |
                Q(material__icontains=search)
            )
        return queryset
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            vi = request.POST.get('valores')
            vi = str(vi)
            present = vi.split(",")
            present.pop()
            for i in present:
                if not i == "False":
                    Material.objects.filter(pk=i).update(concluido=True)
            url='#'
            return HttpResponseRedirect(url)

def material_detail(request, pk):
    template_name = 'material_detail.html'
    obj = Material.objects.get(pk=pk)
    link = f"http://34.151.253.92/material/{obj.pk}"
    context = {'object': obj, 'link':link}
    return render(request, template_name, context)

################### pdf view

def render_pdf_view(request, pk):
    obj = get_object_or_404(Material, pk=pk)
    template_path = 'qrcode.html'
    link = f"http://34.151.253.92/material/{obj.pk}"
    context = {'material': obj, 'link':link}
   
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

class MaterialCreate(CreateView):
    model = Material
    template_name = 'material_form.html'
    form_class = MaterialForm

class MaterialUpdate(UpdateView):
    model = Material
    template_name = 'material_form.html'
    form_class = MaterialForms

################## gráficos
def json_material(request,begin,end):
    data_inicial = begin
    data__final = end
    data = list(Material.objects.filter(n_romaneio__entrada__range=[data_inicial, data__final]).values('n_romaneio__area__area').annotate(Sum('m2')))
    return JsonResponse({'data':data})

def json_status(request,begin,end):
    data_inicial = begin
    data__final = end
    data = list(Material.objects.filter(n_romaneio__entrada__range=[data_inicial, data__final]).values('concluido').annotate(Sum('m2')))
    return JsonResponse({'data':data})

def json_ti(request):
    data = list(TintaIntermediaria.objects.values())
    return JsonResponse({'data':data})

def json_ta(request):
    data = list(TintaAcabamento.objects.values())
    return JsonResponse({'data':data})

def json_tratamento(request):
    data = list(Tratamento.objects.values())
    return JsonResponse({'data':data})

################### exportações
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

@login_required
@manager_required
def export_xlsx_func_material(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'Material'
    filename = 'material_exportados.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = Material.objects.all().values_list('pk','concluido','n_romaneio__area','n_romaneio__solicitante', 'n_romaneio__romaneio', 'jato__tratamento', 
    'tf__tinta_fundo','ti__tinta_intermediaria', 'ta__tinta_acabamento', 'cor', 'material', 'descricao',
     'polegada', 'm_quantidade', 'm2', 'raio', 'largura', 'altura', 'comprimento','lados','relatorio')

    columns = ('id','concluido','area','solicitante', 'Nº romaneio', 'Tratamento', 'Primer','TI', 
    'TA', 'cor', 'material', 'descricao', 'polegada', 'M / Quant.', 'm2', 'Raio', 'Largura', 'Altura', 
    'Comprimento/lados','QTD_Equip','Nº Relatório')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response
def save_data(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:
        concluido = True if item.get('concluido') == 'True' else False
        n_romaneio = item.get('n_romaneio') # foreignkey
        jato = int(item.get('jato')) # foreignkey
        tf = int(item.get('tf')) # foreignkey
        ti = int(item.get('ti')) # foreignkey
        ta = int(item.get('ta')) # foreignkey
        cor = item.get('cor')
        material = item.get('material')
        descricao = item.get('descricao')
        polegada = item.get('polegada')
        m_quantidade =  0.00 if item.get('m_quantidade') == "" else float(item.get('m_quantidade'))
        m2 = float(item.get('m2'))
        raio = 0.00 if item.get('raio') == "" else float(item.get('raio'))
        largura = 0.00 if item.get('largura') == "" else float(item.get('largura'))
        altura = 0.00 if item.get('altura') == "" else float(item.get('altura'))
        lados = 0.00 if item.get('lados') == "" else float(item.get('lados'))
        relatorio = item.get('relatorio')

        obj = Material(
                concluido = concluido,
                n_romaneio = Romaneio.objects.get(pk=n_romaneio),
                jato = Tratamento.objects.get(pk=jato),
                tf = TintaFundo.objects.get(pk=tf),
                ti = TintaIntermediaria.objects.get(pk=ti),
                ta = TintaAcabamento.objects.get(pk=ta),
                cor = cor,
                material = material,
                descricao = descricao,
                polegada = polegada,
                m_quantidade = m_quantidade,
                m2 = m2,
                raio = raio,
                largura = largura,
                altura = altura,
                lados = lados,
                relatorio = relatorio,
        )
        aux.append(obj)
    Material.objects.bulk_create(aux)

@login_required
@manager_required
def import_csv(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data(data)
        return HttpResponseRedirect(reverse('material:material_list'))

    template_name = 'material_import.html'
    return render(request, template_name)
