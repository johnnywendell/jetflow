from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from material.models import Material, Romaneio
from django.shortcuts import render
from django.core import serializers

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def dashboard_jato(request):
    romaneios = Romaneio.objects.all().order_by('-romaneio')[:5]
    begin = "2023-01-01"
    end = "2023-12-30"
    materiais = Material.objects.filter(n_romaneio__entrada__range=[begin, end]).order_by('-modified')
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
    
    if request.method == 'POST':
        begin = request.POST.get('begin')
        end = request.POST.get('end')
        tratamento = 0
        tintaf = 0
        tintai = 0
        tintaa = 0
        materiais = Material.objects.filter(n_romaneio__entrada__range=[begin, end])
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
    
    context={'tratamento':tratamento, 'tintaf':tintaf,'tintai':tintai,'tintaa':tintaa, 'begin':begin, 
             'end':end, 'romaneios':romaneios, 'materiais':materiais}      
    return render(request, 'dash_jato.html', context)
