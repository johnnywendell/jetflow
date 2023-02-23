from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView
from .models import RelatorioInspecao, EtapaPintura
from material.models import Material


class RelatoriosList(ListView):
    model = RelatorioInspecao
    template_name = 'relatorios_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'
    def get_queryset(self):
        queryset = super(RelatoriosList, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(rip__icontains=search) |
                Q(cliente__icontains=search)
            )
        return queryset


def relatorios_detail(request, pk):
    template_name = 'relatorios_detail.html'
    obj = RelatorioInspecao.objects.get(pk=pk)
    material = Material.objects.filter(concluido=True)
    context = {'object': obj, 'material_list': material}
    return render(request, template_name, context)