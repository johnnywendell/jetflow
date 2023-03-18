from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from material.models import Material

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def dashboard_jato(request):
    materiais = Material.objects.all()
    tratamento = 0
    tintaf = 0
    tintai = 0
    tintaa = 0
    for material in materiais:
        if material.jato != None:
            tratamento += material.m2
    for material in materiais:
        if material.tf != None:
            tintaf += material.m2
    for material in materiais:
        if material.ti != None:
            tintai += material.m2
    for material in materiais:
        if material.ta != None:
            tintaa += material.m2
    context={'tratamento':tratamento, 'tintaf':tintaf,'tintai':tintai,'tintaa':tintaa}
    return render(request, 'dash_jato.html', context)

