from django.contrib import admin
from .models import Area, Solicitante, Romaneio
from material.admin import MaterialInline

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )
@admin.register(Solicitante)
class SolicitanteAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )
    
@admin.register(Romaneio)
class RomaneioAdmin(admin.ModelAdmin):
    inlines = (MaterialInline,)
    list_display = (
        '__str__',
        'entrada',
        'documento',
        'area',
        'solicitante',
    )

# Register your models here.
