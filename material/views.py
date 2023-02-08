from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView
from django.http import HttpResponseRedirect
from .models import Tratamento, TintaFundo, TintaIntermediaria, TintaAcabamento, Material
from .forms import MaterialForm, TratamentoForm, TintaFundoForm, TintaIntermediariaForm, TintaAcabamentoForm

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
            queryset = queryset.filter(material__icontains=search)
        return queryset

def material_detail(request, pk):
    template_name = 'material_detail.html'
    obj = Material.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)

class MaterialCreate(CreateView):
    model = Material
    template_name = 'material_form.html'
    form_class = MaterialForm

class MaterialUpdate(UpdateView):
    model = Material
    template_name = 'material_form.html'
    form_class = MaterialForm
