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
    path('import/csv/', v.import_csv, name='import_csv'),
    path('romaneios/jsonromaneio/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77', v.json_romaneios, name='json_romaneio'),
    path('romaneios/jsonarea/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77', v.json_area, name='json_area'),
    path('romaneios/jsonsolicitante/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77', v.json_solicitante, name='json_solicitante'),
    path('romaneios/pdf/<int:pk>/', v.render_pdf_view, name='render_pdf_view'),
    path('romaneios/pdftag/<int:pk>/', v.render_pdf_view_tag, name='render_pdf_view_tag'),
]
