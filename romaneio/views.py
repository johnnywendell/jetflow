from datetime import datetime
import csv
import io
import xlwt
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, resolve_url
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, ListView
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .models import Area, Solicitante, Romaneio
from .forms import RomaneioForm, AreaForm, SolicitanteForm
from material.models import Material
from material.forms import MaterialForm
from usuarios.decorators import manager_required, superuser_required
from django.contrib.auth.models import User
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import os

@login_required
def render_pdf_view_tag(request, pk):
    template_path = "qrcode.html"
    obj = Romaneio.objects.get(pk=pk)
    link = f"https://monsertec.singularcode.net/romaneios/{obj.pk}"
    context = {'object': obj, 'link':link}
   
    response = HttpResponse(content_type='application/pdf')

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
def render_pdf_view(request, pk):
    template_path = "romaneio.html"
    obj = Romaneio.objects.get(pk=pk)
    materiais = obj.romaneios.all()
    metro_quadrado = 0
    link = f"https://monsertec.singularcode.net/romaneios/{obj.pk}"
    for material in materiais:
        metro_quadrado += material.m2
    context = {'object': obj, 'metro':metro_quadrado, 'link':link}
   
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

class RomaneioList(ListView):
    model = Romaneio
    template_name = 'romaneio_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'
    def get_queryset(self):
        queryset = super(RomaneioList, self).get_queryset()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(romaneio__icontains=search) |
                Q(solicitante__solicitante__icontains=search) |
                Q(documento__icontains=search) 
            )
        return queryset


def romaneio_detail(request, pk):
    template_name = 'romaneio_detail.html'
    obj = Romaneio.objects.get(pk=pk)
    materiais = obj.romaneios.all()
    metro_quadrado = 0
    link = f"https://monsertec.singularcode.net/romaneios/{obj.pk}"
    for material in materiais:
        metro_quadrado += material.m2
    context = {'object': obj, 'metro':metro_quadrado, 'link':link}
    return render(request, template_name, context)

@login_required
@manager_required
def romaneio_add(request):
    template_name = 'romaneio_forms.html'
    romaneio_form=Romaneio()
    item_romaneio_formset = inlineformset_factory(
        Romaneio,
        Material,
        form=MaterialForm,
        extra=0,
        can_delete=False,
        min_num=1,
        validate_min=True
    )
    if request.method == 'POST':
        form=RomaneioForm(request.POST, instance=romaneio_form, prefix='main')
        formset=item_romaneio_formset(request.POST, instance=romaneio_form, prefix='romaneio' )
        if form.is_valid() and formset.is_valid():
            form=form.save(commit=False)
            form.funcionario = request.user
            form.save()
            formset.save()
            url='romaneio:romaneio_detail'
            return HttpResponseRedirect(resolve_url(url,form.pk))
    else:
        form=RomaneioForm(instance=romaneio_form, prefix='main')
        formset=item_romaneio_formset(instance=romaneio_form, prefix='romaneio' )
    context={'form':form, 'formset':formset}
    return render(request, template_name, context)


class RomaneioCreate(CreateView):
    model = Romaneio
    template_name = 'romaneio_form.html'
    form_class = RomaneioForm
 
class RomaneioUpdate(UpdateView):
    model = Romaneio
    template_name = 'romaneio_form.html'
    form_class = RomaneioForm

###########json modelos
def json_fatores(request):
    data = {
            'perfil_I':{'3':0.41,'4':0.50,'5':0.59,'6':0.68,'8':0.84,'10':1.03,'12':1.18,'14':1.35,'18':1.53,'20':1.76,'22':1.94,'24':2.13,'26':2.32},
            'perfil_H':{'4':0.61,'5':0.77,'6':0.92,'7':1.08,'8':1.23,'9':1.39,'10':1.54,'11':1.70,'12':1.85,'13':2.01,'14':2.16,'15':2.32,'16':2.47,'17':2.63,'18':2.78,'19':2.94,'20':3.09},
            'perfil_U':{'3':0.32,'4':0.38,'6':0.56,'8':0.68,'10':0.84,'12':0.96,'14':1.15,'16':1.29,'18':1.45,'20':1.60,'22':1.76,'24':1.91,'26':2.07},
            'perfil_L':{'1':0.10,'2':0.20,'2,5':0.26,'3':0.31,'4':0.41,'5':0.51,'6':0.61,'8':0.82,'10':1.03,'12':1.24},
            'barra_chata':{'0,5':0.03,'1':0.05,'2':0.10,'2,5':0.13,'3':0.15,'4':0.20,'5':0.25,'6':0.30,'8':0.41,'10':0.51,'12':0.61},
            'tubulacao':{'0,5':0.08,'0,75':0.1,'1':0.13,'1,5':0.16,'2':0.21,'2,5':0.25,'3':0.31,'4':0.39,'6':0.57,'8':0.73,'10':0.9,'12':1.07,'14':1.18,'16':1.36,'18':1.52,'20':1.68,'22':1.84,'24':2,'26':2.18,
            '28':2.35,'30':2.51,'32':2.68,'34':2.85,'36':3.01,'38':3.18,'40':3.35,'44':4.00,'50':4.21,'52':4.42,'54':4.63,'56':4.84,'58':5.05,'60':5.26},
            'acess_T':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.01,'2':0.02,'2,5':0.02,'3':0.03,'4':0.05,'6':0.11,'8':0.18,'10':0.26,'12':0.37,'14':0.45,'16':0.62,'18':0.78,'20':0.96,'22':1.12,'24':1.38,
            '26':1.62,'28':1.89,'30':2.15,'32':2.37,'34':2.61,'36':2.86,'38':3.10,'40':3.34,'44':3.58,'50':3.83,'52':4.07,'54':4.31,'56':4.56,'58':4.80,'60':5.04},
            'acess_FLG':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.01,'2':0.02,'2,5':0.02,'3':0.03,'4':0.05,'6':0.11,'8':0.18,'10':0.26,'12':0.37,'14':0.45,'16':0.62,'18':0.78,'20':0.96,'22':1.12,'24':1.38,
            '26':1.62,'28':1.89,'30':2.15,'32':2.37,'34':2.61,'36':2.86,'38':3.10,'40':3.34,'44':3.58,'50':3.83,'52':4.07,'54':4.31,'56':4.56,'58':4.80,'60':5.04},
            'acess_RED':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.01,'2':0.02,'2,5':0.02,'3':0.03,'4':0.05,'6':0.11,'8':0.18,'10':0.26,'12':0.37,'14':0.45,'16':0.62,'18':0.78,'20':0.96,'22':1.12,'24':1.38,
            '26':1.62,'28':1.89,'30':2.15,'32':2.37,'34':2.61,'36':2.86,'38':3.10,'40':3.34,'44':3.58,'50':3.83,'52':4.07,'54':4.31,'56':4.56,'58':4.80,'60':5.04},
            'acess_CV90':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.02,'2':0.03,'2,5':0.04,'3':0.06,'4':0.1,'6':0.21,'8':0.36,'10':0.52,'12':0.74,'14':0.94,'16':1.23,'18':1.55,'20':1.92,'22':2.34,'24':2.75,
            '26':3.23,'28':3.77,'30':4.3,'32':4.76,'34':5.25,'36':5.75,'38':6.24,'40':6.74,'44':7.23,'50':7.72,'52':8.22,'54':8.71,'56':9.21,'58':9.70,'60':10.19},
            'acess_CV45':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.01,'2':0.02,'2,5':0.02,'3':0.03,'4':0.05,'6':0.11,'8':0.18,'10':0.26,'12':0.37,'14':0.45,'16':0.62,'18':0.78,'20':0.96,'22':1.12,'24':1.38,
            '26':1.62,'28':1.89,'30':2.15,'32':2.37,'34':2.61,'36':2.86,'38':3.10,'40':3.34,'44':3.58,'50':3.83,'52':4.07,'54':4.31,'56':4.56,'58':4.80,'60':5.04},
            'acess_VV':{'0,5':0.06,'0,75':0.1,'1':0.14,'1,5':0.28,'2':0.34,'2,5':0.38,'3':0.45,'4':0.59,'6':0.88,'8':1.17,'10':1.54,'12':1.94,'14':2.38,'16':2.82,'18':3.25,'20':3.69,'22':4.14,'24':4.57,'26':5,
            '28':5.55,'30':5.89,'32':6.47,'34':7.22,'36':7.86,'38':8.22,'40':8.85,'44':9.64,'50':10.38,'52':11.12,'54':11.86,'56':12.60,'58':13.34,'60':14.08},
            'acess_VVC':{'0,5':0.09,'0,75':0.15,'1':0.21,'1,5':0.33,'2':0.45,'2,5':0.57,'3':0.68,'4':0.77,'6':1.14,'8':1.52,'10':1.95,'12':2.33,'14':2.84,'16':3.38,'18':3.9,'20':4.43,'22':4.89,'24':5.48,
            '26':6.01,'28':6.52,'30':7.06,'32':7.69,'34':8.22,'36':8.96,'38':9.77,'40':10.65,'44':11.61,'50':12.72,'52':13.83,'54':14.94,'56':16.05,'58':17.16,'60':18.27},
            'acess_CAP':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.01,'2':0.02,'2,5':0.02,'3':0.03,'4':0.05,'6':0.11,'8':0.18,'10':0.26,'12':0.37,'14':0.45,'16':0.62,'18':0.78,'20':0.96,'22':1.12,'24':1.38,
            '26':1.62,'28':1.89,'30':2.15,'32':2.37,'34':2.61,'36':2.86,'38':3.10,'40':3.34,'44':3.58,'50':3.83,'52':4.07,'54':4.31,'56':4.56,'58':4.80,'60':5.04}
            }
    return JsonResponse({'data':data})


def json_romaneios(request):
    data = list(Romaneio.objects.values())
    return JsonResponse({'data':data})

def json_area(request):
    data = list(Area.objects.values())
    return JsonResponse({'data':data})

def json_solicitante(request):
    data = list(Solicitante.objects.values())
    return JsonResponse({'data':data})
###############################################

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

################## excel 

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
@superuser_required
def export_xlsx_func(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'Romaneio'
    filename = 'romaneio_exportados.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = Romaneio.objects.all().values_list('funcionario', 'nf', 'romaneio', 
    'documento','obs', 'area__area', 'solicitante__solicitante')
    columns = ('funcionario', 'nf', 'romaneio', 
    'documento','obs', 'area', 'solicitante')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response

def save_data(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:
        funcionario = int(item.get('funcionario')) #foreignkey
        entrada = item.get('entrada')
        nf = str(item.get('nf'))
        romaneio = item.get('romaneio')
        documento = str(item.get('documento'))
        obs = item.get('obs')
        area = int(item.get('area')) #foreignkey
        solicitante = int(item.get('solicitante')) #foreignkey
        obj = Romaneio(
                funcionario = User.objects.get(pk=funcionario),
                entrada = datetime.strptime(entrada, '%d/%m/%Y').date(),
                nf = nf,
                romaneio = romaneio,
                documento = documento,
                obs = obs,
                area = Area.objects.get(pk=area),
                solicitante = Solicitante.objects.get(pk=solicitante),
        )
        aux.append(obj)
    Romaneio.objects.bulk_create(aux)

@login_required
@superuser_required
def import_csv(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data(data)
        return HttpResponseRedirect(reverse('romaneio:romaneio_list'))

    template_name = 'romaneio_import.html'
    return render(request, template_name)


