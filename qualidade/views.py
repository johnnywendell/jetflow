from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from .models import RelatorioInspecao, EtapaPintura
from .forms import EtapasForm, RelatoriosForm
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
    relatorio = obj.rip
    material = Material.objects.filter(concluido=True, relatorio=None)
    context = {'object': obj, 'material_list': material}
    if request.method == 'POST':
        vi = request.POST.get('valores')
        vi = str(vi)
        present = vi.split(",")
        present.pop()
        for i in present:
            Material.objects.filter(pk=i).update(relatorio=relatorio)
        return HttpResponseRedirect('/')
    return render(request, template_name, context)

def relatorios_add(request):
    template_name = 'relatorios_add.html'
    relatorios_form=RelatorioInspecao()
    item_relatorios_formset = inlineformset_factory(
        RelatorioInspecao,
        EtapaPintura,
        form=EtapasForm,
        extra=0,
        can_delete=False,
        min_num=1,
        validate_min=True
    )
    if request.method == 'POST':
        form=RelatoriosForm(request.POST, instance=relatorios_form, prefix='main')
        formset=item_relatorios_formset(request.POST, instance=relatorios_form, prefix='relatorio' )
        if form.is_valid() and formset.is_valid():
            form=form.save(commit=False)
            form.save()
            formset.save()
            url='qualidade:relatorios_detail'
            return HttpResponseRedirect(resolve_url(url,form.pk))
    else:
        form=RelatoriosForm(instance=relatorios_form, prefix='main')
        formset=item_relatorios_formset(instance=relatorios_form, prefix='relatorio' )
    context={'form':form, 'formset':formset}
    return render(request, template_name, context)
