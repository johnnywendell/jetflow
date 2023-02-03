from django.shortcuts import render
from .models import Tratamento, TintaFundo, TintaIntermediaria, TintaAcabamento, Material

def material_list(request):
    template_name = 'material_list.html'
    objects = Material.objects.all()
    context = {'objects_list': objects}
    return render(request, template_name, context)

def material_detail(request, pk):
    template_name = 'material_detail.html'
    obj = Material.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)
