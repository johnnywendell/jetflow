from django.shortcuts import render, render, resolve_url
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import CreateView, UpdateView, ListView
from django.db.models import Q
from .models import Contrato, BMF, ItemBm, QtdBM
from .forms import ContratoForm, BmfForm, ItemForm, QtdForm


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

def itembm_add(request):
    template_name = 'itembm.html'
    item_form = ItemBm()
    objects = ItemBm.objects.all()
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
    context={'form':form,'objects_list': objects}
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

class BmfCreate(CreateView):
    model = BMF
    template_name = 'bmf_form.html'
    form_class = BmfForm
 
class BmfUpdate(UpdateView):
    model = BMF
    template_name = 'bmf_form.html'
    form_class = BmfForm


def bmf_detail(request, pk):
    template_name = 'bmf_detail.html'
    obj = BMF.objects.get(pk=pk)
    itens_bm = ItemBm.objects.filter(~Q(bmf__pk=pk))
    qtdbm = QtdBM.objects.filter(bmf=pk)
    item_form = QtdBM()
    if request.method == 'POST':
        form=QtdForm(request.POST, instance=item_form, prefix='main')
        itembm = request.POST.get('main-valor')
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
 
    context = {'object': obj, 'itens_bm':itens_bm, 'form':form, 'qtdbm':qtdbm}
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