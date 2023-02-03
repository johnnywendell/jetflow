from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from .models import Area, Solicitante, Romaneio
from .forms import RomaneioForm


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
    template_name = 'romaneio_form.html'
    return render(request, template_name)

class RomaneioCreate(CreateView):
    model = Romaneio
    template_name = 'romaneio_form.html'
    form_class = RomaneioForm
    
class RomaneioUpdate(UpdateView):
    model = Romaneio
    template_name = 'romaneio_form.html'
    form_class = RomaneioForm




