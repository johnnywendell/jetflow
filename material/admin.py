from django.contrib import admin
from .models import Tratamento, TintaFundo, TintaAcabamento, TintaIntermediaria, Material

admin.site.register(Tratamento)
admin.site.register(TintaFundo)
admin.site.register(TintaAcabamento)
admin.site.register(TintaIntermediaria)



class MaterialInline(admin.TabularInline):
    model = Material
    extra = 0

