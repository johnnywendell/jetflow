import xlwt
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView
from django.http import HttpResponseRedirect, HttpResponse
from .models import Tratamento, TintaFundo, TintaIntermediaria, TintaAcabamento, Material
from .forms import MaterialForm, TratamentoForm, TintaFundoForm, TintaIntermediariaForm, TintaAcabamentoForm
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import os
from django.conf import settings

@login_required
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

    
def material_list(request):
    template_name = 'material_list.html'
    objects = Material.objects.all()
    search =request.GET.get('search')
    if search:
        objects = objects.filter(material__icontains=search)
    context = {'objects_list': objects}
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

def material_detail(request, pk):
    template_name = 'material_detail.html'
    obj = Material.objects.get(pk=pk)
    link = f"www.google.com/{obj.pk}"
    context = {'object': obj, 'link':link}
    return render(request, template_name, context)

def render_pdf_view(request, pk):
    obj = get_object_or_404(Material, pk=pk)
    template_path = 'qrcode.html'
    link = f"www.google.com/{obj.pk}"
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
    form_class = MaterialForm


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

def export_xlsx_func_material(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'Material'
    filename = 'material_exportados.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = Material.objects.all().values_list('concluido', 'n_romaneio__romaneio', 'jato__tratamento', 
    'tf__tinta_fundo','ti__tinta_intermediaria', 'ta__tinta_acabamento', 'cor', 'material', 'descricao',
     'polegada', 'm_quantidade', 'm2', 'raio', 'largura', 'altura', 'comprimento','lados','relatorio')

    columns = ('concluido', 'Nº romaneio', 'Tratamento', 'Primer','TI', 
    'TA', 'cor', 'material', 'descricao', 'polegada', 'M / Quant.', 'm2', 'Raio', 'Largura', 'Altura', 
    'Comprimento/lados','QTD_Equip','Nº Relatório')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response
