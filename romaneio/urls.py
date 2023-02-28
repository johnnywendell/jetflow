from django.urls import path
from romaneio import views as v
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required

app_name ='romaneio'

urlpatterns =[
    path('romaneios/', login_required(v.RomaneioList.as_view()), name='romaneio_list'),
    path('romaneios/<int:pk>/', v.romaneio_detail, name='romaneio_detail'),
    path('romaneios/add/', v.romaneio_add, name='romaneios_add'),
    path('romaneios/<int:pk>/edit/', manager_required(v.RomaneioUpdate.as_view()), name='romaneio_edit'),
    path('romaneios/json/', v.json_fatores, name='json_fatores'),
    path('area/', v.area_add, name='area_add'),
    path('solicitante/', v.solicitante_add, name='solicitante_add'),
    path('export/xlsx/', v.export_xlsx_func, name='export_xlsx_func'),
]
