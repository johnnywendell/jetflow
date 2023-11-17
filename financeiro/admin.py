from django.contrib import admin
from .models import Contrato, RDO, ItemBm, QtdBM,Aprovador,BoletimMedicao,FRS


@admin.register(RDO)
class BMFAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )
    #prepopulated_fields = {"slug": ("escopo", "local")}

@admin.register(ItemBm)
class ItemBmAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )

@admin.register(Contrato)
class ContratoBmAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )


#class EtapalInline(admin.TabularInline):
#    model = EtapaPintura
#    extra = 0
#
#
## Register your models here.
#@admin.register(RelatorioInspecao)
#class RelatoriosAdmin(admin.ModelAdmin):
#    inlines = (EtapalInline,)
#    list_display = (
#        '__str__',
#        'cliente',
#        'fiscal',
#        'data',
#        'unidade',
#    )
#

