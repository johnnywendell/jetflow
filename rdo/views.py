from datetime import datetime
import csv
import io
import xlwt
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render, resolve_url, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import CreateView, UpdateView, ListView
from django.db.models import Q, F
from rdo.models import Contrato, RDO, ItemBm, QtdBM,Aprovador,BoletimMedicao,FRS
from .forms import ContratoForm, RdoForm, ItemForm, QtdForm,AprovadorForm
from django.db.models import Sum, Count, Case, When
from django.db import models
from django.contrib.auth.models import User
from romaneio.models import Area, Solicitante
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required, superuser_required
from rolepermissions.decorators import has_role_decorator

# Create your views here.
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

@login_required
@manager_required
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
        form = RdoForm(request.POST, instance=objeto)
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
    paginate_by = 20
    context_object_name = 'objects_list'
    def get_queryset(self):
        queryset = super(RdoList, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(bmf__icontains=search) |
                Q(solicitante__solicitante__icontains=search) |
                Q(unidade__area__icontains=search)|
                Q(status__icontains=search)
            )
        return queryset
    
@login_required
def rdo_detail(request, slug):
    template_name = 'rdo_detail.html'
    obj = RDO.objects.get(slug=slug)
    qtdbm = QtdBM.objects.filter(bmf=obj.pk)
    if request.method == 'POST':
        form=QtdForm(request.POST)
        itembm = request.POST.get('id_itembm')
        if form.is_valid():
            obj.item_bm.add(itembm)
            form=form.save(commit=False)
            form.bmf = obj
            item_bm = ItemBm.objects.get(pk=itembm)
            form.valor = item_bm
            form.save()
            url='#'
            return HttpResponseRedirect(url)       
    else:
        form=QtdForm()

    context = {'object': obj,'form':form, 'qtdbm':qtdbm}
    return render(request, template_name, context)


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

@superuser_required
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