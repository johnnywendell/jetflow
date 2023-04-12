from django.urls import path
from financeiro import views as v
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required

app_name ='financeiro'

urlpatterns =[
    path('gerencia/', v.administracao, name='gerencia'),
    path('contrato/', v.contrato_add, name='contrato_add'),
    path('itembm/', v.itembm_add, name='itembm_add'),
    path('aprovador/', v.aprovador_add, name='aprovador_add'),
    path('bmf/', manager_required(v.BmfList.as_view()), name='bmf_list'),
    path('bmf/planejador/', v.bmf_list_planejador, name='bmf_list_planejador'),
    path('dms/', manager_required(v.DmsList.as_view()), name='dms_list'),
    path('bms/', manager_required(v.BmsList.as_view()), name='bms_list'),
    path('frs/', manager_required(v.FrsList.as_view()), name='frs_list'),
    path('bmf/<int:pk>/edit/', login_required(v.BmfUpdate.as_view()), name='bmf_update'),
    path('bmf/create/', login_required(v.BmfCreate.as_view()), name='bmf_create'),
    path('dms/<int:pk>/edit/', manager_required(v.DMSUpdate.as_view()), name='dms_update'),
    path('dms/create/', manager_required(v.DMSCreate.as_view()), name='dms_create'),
    path('bms/<int:pk>/edit/', manager_required(v.BmsUpdate.as_view()), name='bms_update'),
    path('bms/create/', manager_required(v.BmsCreate.as_view()), name='bms_create'),
    path('frs/<int:pk>/edit/', manager_required(v.FRSUpdate.as_view()), name='frs_update'),
    path('frs/create/', manager_required(v.FRSCreate.as_view()), name='frs_create'),
    path('bmf/<slug:slug>/', v.bmf_detail, name='bmf_detail'),
    path('bmf/deleteitem/<int:pk>/<int:id>/<int:ind>/', v.delete_item, name='delete_item'),
    path('dms/<int:pk>/', v.dms_detail, name='dms_detail'),
    path('dms/deleteitem/<int:pk>/<int:id>/', v.dmsitem_delete, name='delete_itemdms'),
    path('bms/<int:pk>/', v.bms_detail, name='bms_detail'),
    path('bms/deleteitem/<int:pk>/<int:id>/', v.bmsitem_delete, name='delete_itembms'),
    path('frs/<int:pk>/', v.frs_detail, name='frs_detail'),
    path('frs/deleteitem/<int:pk>/<int:id>/', v.frsitem_delete, name='delete_itemfrs'),
    path('import/csvcontrato/', v.import_csv, name='import_csvcontrato'),
    path('import/csvbmf/', v.import_csv_bmf, name='import_csv_bmf'),
    path('import/csvdms/', v.import_csv_dms, name='import_csv_dms'),
    path('import/csvaprovador/', v.import_csv_aprovador, name='import_csv_aprovador'),
    path('import/csvsolicitante/', v.import_csv_solicitante, name='import_csv_solicitante'),
    path('itensbm/json/<str:ref>/<int:pk>/', v.json_itens, name='json_itens'),
    path('bmf/export/xlsx/', v.export_xlsx_func_bmf, name='export_xlsx_func_bmf'),
    path('bmf/json_fat_uni/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77/<str:begin>/<str:end>/', v.json_fat_uni, name='json_fat_uni'),
    path('bmf/json_fat_sol/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77/<str:begin>/<str:end>/', v.json_fat_sol, name='json_fat_sol'),
    path('bmf/json_fat_tipo/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77/<str:begin>/<str:end>/', v.json_fat_tipo, name='json_fat_tipo'),
    path('bmf/json_fat_dms/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77/<str:begin>/<str:end>/<str:status>/', v.json_fat_dms, name='json_fat_dms'),
]