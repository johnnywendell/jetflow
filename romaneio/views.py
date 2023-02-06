from django.shortcuts import render, resolve_url
from django.views.generic import CreateView, UpdateView
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from .models import Area, Solicitante, Romaneio
from .forms import RomaneioForm
from material.models import Material
from material.forms import MaterialForm


def romaneio_list(request):
    template_name = 'romaneio_list.html'
    objects = Romaneio.objects.all()
    context = {'objects_list': objects}
    return render(request, template_name, context)


def romaneio_detail(request, pk):
    template_name = 'romaneio_detail.html'
    obj = Romaneio.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)

def romaneio_add(request):
    template_name = 'romaneio_forms.html'
    romaneio_form=Romaneio()
    item_romaneio_formset = inlineformset_factory(
        Romaneio,
        Material,
        form=MaterialForm,
        extra=0,
        min_num=1,
        validate_min=True
    )
    if request.method == 'POST':
        form=RomaneioForm(request.POST, instance=romaneio_form, prefix='main')
        formset=item_romaneio_formset(request.POST, instance=romaneio_form, prefix='romaneio' )
        if form.is_valid() and formset.is_valid():
            form=form.save()
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




