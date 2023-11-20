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

@admin.register(Aprovador)
class ContratoBmAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )
# Register your models here.
