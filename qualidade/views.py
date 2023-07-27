from django.views.generic import CreateView, UpdateView, ListView
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.shortcuts import render, resolve_url, redirect, get_object_or_404
from django.db.models import Q
from .models import RelatorioInspecao, EtapaPintura, Photo, Assinatura
from .forms import EtapasForm, RelatoriosForm, PhotoForm
from material.models import Material
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import os
from django.conf import settings
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required
from rolepermissions.decorators import has_role_decorator



@login_required
def render_pdf_view(request, pk):
    relatorio = get_object_or_404(RelatorioInspecao, pk=pk)
    template_path = 'rip.html'
    obj = relatorio.rip
    teste = relatorio.relatorio.all()
    materiais= Material.objects.filter(relatorio=obj)
    ass = Assinatura.objects.filter(rip_numero=pk).first()
    links = []
    for item in teste:
        if item.photo:
            link = item.photo.url
            link = link[1:]
            links.append(link)
    context = {'relatorio': relatorio, 'materiais':materiais, 'links':links, 'ass':ass}
   
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

class RelatoriosList(ListView):
    model = RelatorioInspecao
    template_name = 'relatorios_list.html'
    paginate_by = 20
    context_object_name = 'objects_list'
    def get_queryset(self):
        queryset = super(RelatoriosList, self).get_queryset()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(rip__icontains=search) |
                Q(cliente__icontains=search)
            )
        return queryset

@login_required
@manager_required
def relatorios_detail(request, pk):
    ass = Assinatura.objects.filter(rip_numero=pk).first()
    template_name = 'relatorios_detail.html'
    obj = RelatorioInspecao.objects.get(pk=pk)
    relatorio = obj.rip
    material = Material.objects.select_related('n_romaneio').filter(concluido=True, relatorio=None)
    material_relatorio = Material.objects.select_related('n_romaneio').filter(relatorio=relatorio)
    metro = 0
    for item in material_relatorio:
        metro += item.m2
    context = {'object': obj, 'material_list': material, 'material_relatorio':material_relatorio, 'metro':metro,'ass':ass}
    if request.method == 'POST':
        vi = request.POST.get('valores')
        vi = str(vi)
        present = vi.split(",")
        present.pop()
        for i in present:
            Material.objects.filter(pk=i).update(relatorio=relatorio)
        url='qualidade:relatorios_detail'
        return HttpResponseRedirect(resolve_url(url,pk))
    return render(request, template_name, context)

@login_required
@manager_required
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
            form.funcionario=request.user
            form.save()
            formset.save()
            url='qualidade:relatorios_detail'
            return HttpResponseRedirect(resolve_url(url,form.pk))
    else:
        form=RelatoriosForm(instance=relatorios_form, prefix='main')
        formset=item_relatorios_formset(instance=relatorios_form, prefix='relatorio' )
    context={'form':form, 'formset':formset}
    return render(request, template_name, context)

class RelatorioUpdate(UpdateView):
    model = RelatorioInspecao
    template_name = 'relatorio_form.html'
    form_class = RelatoriosForm

class EtapaUpdate(UpdateView):
    model = EtapaPintura
    template_name = 'relatorio_form.html'
    form_class = EtapasForm

@login_required
@manager_required
def photo_create(request):
    template_name = 'photo_form.html'
    form = PhotoForm(request.POST or None)
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        if form.is_valid():
            rip = form.save(commit=False)
            Photo.objects.create(rip_numero=rip.rip_numero, photo=photo)
            return redirect('qualidade:relatorios_list')
    context ={'form':form}
    return render(request, template_name, context)

@login_required
@manager_required
def delete_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    photo.delete()
    return redirect('qualidade:relatorios_list')

######################## assinaturas

@has_role_decorator('inspetor')
def assign_insp(request,pk):
    user = str(request.user)
    ass = "media/" + user + "_ass.png"
    rip = RelatorioInspecao.objects.get(pk=pk)
    Assinatura.objects.create(rip_numero=rip, ass_insp=ass)
    url='qualidade:relatorios_detail'
    return HttpResponseRedirect(resolve_url(url,pk))

@has_role_decorator('coordenador')
def assign_coord(request,pk):
    user = str(request.user)
    ass = "media/" + user + "_ass.png"
    Assinatura.objects.filter(rip_numero=pk).update(ass_coord=ass)
    url='qualidade:relatorios_detail'
    return HttpResponseRedirect(resolve_url(url,pk))

@has_role_decorator('fiscal')
def assign_fiscal(request,pk):
    user = str(request.user)
    ass = "media/" + user + "_ass.png"
    Assinatura.objects.filter(rip_numero=pk).update(ass_fiscal=ass)
    url='qualidade:relatorios_detail'
    return HttpResponseRedirect(resolve_url(url,pk))
