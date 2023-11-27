from datetime import datetime
import csv
import io
import xlwt
from django.db.models import Sum
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, resolve_url, redirect,get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import CreateView, UpdateView, ListView
from django.db.models import Q, F
from rdo.models import Contrato, RDO, ItemBm, QtdBM,Aprovador,BoletimMedicao,FRS, AssinaturaDigital, ProjetoCodigo, Area, Solicitante
from .forms import ContratoForm, RdoForm, ItemForm, QtdForm,AprovadorForm, BoletimForm, AssinaturadigitalForm, ProjetoForm, AreaForm, SolicitanteForm
from django.db.models import Sum, Count, Case, When
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required, superuser_required
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import View
import base64
from django.core.files.base import ContentFile

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

@has_role_decorator('rdo')   
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
        if form.is_valid():
            form=form.save(commit=False)
            form.bmf = obj
            item_bm = ItemBm.objects.get(pk=itembm)
            form.valor = item_bm
            form.save()
            url='#'
            return HttpResponseRedirect(url)       
    else:
        form=QtdForm()
    context = {'object': obj,'form':form, 'qtdbm':qtdbm,'assinatura_binario': assinatura_binario,'total':total}
    return render(request, template_name, context)

@has_role_decorator('rdo')
@login_required
def delete_item(request,id, ind):
    qtd = QtdBM.objects.get(pk=id)
    obj = RDO.objects.get(pk=ind)
    qtd.delete()
    return HttpResponseRedirect(resolve_url('rdo:rdo_detail',obj.slug))

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
    template_name = 'form.html'
    form_class = BoletimForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.funcionario = self.request.user
        obj.save()  
        self.object = obj      
        return HttpResponseRedirect(self.get_success_url())
 
class BoletimUpdate(UpdateView):
    model = BoletimMedicao
    template_name = 'form.html'
    form_class = BoletimForm

class BoletimList(ListView):
    model = BoletimMedicao
    template_name = 'bm_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'

@login_required
@manager_required
def boletim_detail(request, pk):    
    template_name = 'bm_detail.html'
    obj = BoletimMedicao.objects.get(pk=pk)
    itens = RDO.objects.filter(bm=None)
    item = QtdBM.objects.filter(bmf__bm=pk).values('valor__item_ref','valor__descricao','valor__und','valor__preco_item').annotate(Sum('total')).annotate(Sum('qtd'))
    bm_valor = QtdBM.objects.filter(bmf__bm=pk).aggregate(Sum('total'))['total__sum'] or 0

    if request.method == 'POST':
        vi = request.POST.get('valores')
        vi = str(vi)
        present = vi.split(",")
        present.pop()
        for i in present:
            if not i == "null":
                RDO.objects.filter(pk=i).update(bm=pk)
        url='#'
        return HttpResponseRedirect(url)

    context = {'object': obj, 'itens':itens,'item':item,'bm_valor':bm_valor}
    return render(request, template_name, context)

def export_csv_view(request,pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data_BM {}.csv"'.format(str(pk).zfill(5))

    writer = csv.writer(response, delimiter=';')
    #writer.writerow(['Número Antes', 'Número Depois', 'Quantidade'])
    #for _ in range(3):
        #writer.writerow(['0000', '0000', '0000'])
    # Agrupa os registros pelo campo 'valor' e calcula a soma da coluna 'qtd'
    writer.writerow(['0', '0000000000', '0','10','10','0,00'])
    qtd_bm_objects = QtdBM.objects.filter(bmf__bm=pk).values('valor__item_ref', 'bmf__bm').annotate(total_qtd=Sum('qtd'))

    for qtd_bm in qtd_bm_objects:
        # Divida o campo 'item_ref' usando o caractere "-"
        numero_antes, numero_depois = qtd_bm['valor__item_ref'].split('-')

        total_qtd_formated = '{:.3f}'.format(qtd_bm['total_qtd']).replace('.',',')
        writer.writerow(['0', '0000000000',numero_antes, numero_depois, total_qtd_formated])

    return response

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