from django.contrib import admin
from .models import RelatorioInspecao, EtapaPintura, Photo

class EtapalInline(admin.TabularInline):
    model = EtapaPintura
    extra = 0


# Register your models here.
@admin.register(RelatorioInspecao)
class RelatoriosAdmin(admin.ModelAdmin):
    inlines = (EtapalInline,)
    list_display = (
        '__str__',
        'cliente',
        'fiscal',
        'data',
        'unidade',
    )

admin.site.register(Photo)
