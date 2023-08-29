from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from material.models import Material, Romaneio
from financeiro.models import BMF,DMS,BMS
from django.shortcuts import render
from django.core import serializers
from django.db.models import Sum



@login_required
def navbar(request):
    return render(request, 'navbar.html')

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def dashboard_jato(request):
    # mat = Material.objects.filter(~F('modified') == F('created')).order_by('-romaneio')[:10]
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


@login_required
def dashboard_financeiro(request):
    #romaneios = Romaneio.objects.all().order_by('-romaneio')[:5]
    begin = "2023-01-01"
    end = "2023-12-30"
    status_dms = "APROVADO"
    bmf = BMF.objects.filter(data_periodo__range=[begin, end]).order_by('-modified')
    pendencias = BMF.objects.filter(data_periodo__range=[begin, end],status=False).values('funcionario__username').annotate(Sum('valor'))
    fat_total = 0
    fat_pen = 0
    fat_aprov = 0
    for item in bmf:
        if item.status == True and item.valor != None:
            fat_aprov += item.valor
    for item in bmf:
        if item.status == False and item.valor != None:
            fat_pen += item.valor
    for item in bmf:
        if item.valor != None:
            fat_total += item.valor
    if request.method == 'POST':
        begin = request.POST.get('begin')
        end = request.POST.get('end')
        status_dms = request.POST.get('status_dms')
        bmf = BMF.objects.filter(data_periodo__range=[begin, end])
        pendencias = BMF.objects.filter(data_periodo__range=[begin, end],status=False).values('funcionario__username').annotate(Sum('valor'))
        fat_total = 0
        fat_pen = 0
        fat_aprov = 0
        for item in bmf:
            if item.status == True and item.valor != None:
                fat_aprov += item.valor
        for item in bmf:
            if item.status == False and item.valor != None:
                fat_pen += item.valor
        for item in bmf:
            if item.valor != None:
                fat_total += item.valor
    
    context={'fat_aprov':fat_aprov, 'fat_pen':fat_pen,'fat_total':fat_total,'begin':begin, 
             'end':end, 'pendencias':pendencias, 'status_dms':status_dms}      
    return render(request, 'dash_financeiro.html', context)
