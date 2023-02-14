from django.contrib import admin
from .models import Tratamento, TintaFundo, TintaAcabamento, TintaIntermediaria, Material, Equipamento

admin.site.register(Tratamento)
admin.site.register(TintaFundo)
admin.site.register(TintaAcabamento)
admin.site.register(TintaIntermediaria)
admin.site.register(Equipamento)


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 0

