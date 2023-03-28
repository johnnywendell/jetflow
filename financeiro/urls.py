from django.urls import path
from financeiro import views as v
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required

app_name ='financeiro'

urlpatterns =[
    path('contrato/', v.contrato_add, name='contrato_add'),
    path('itembm/', v.itembm_add, name='itembm_add'),
    path('aprovador/', v.aprovador_add, name='aprovador_add'),
    path('bmf/', login_required(v.BmfList.as_view()), name='bmf_list'),
    path('dms/', login_required(v.DmsList.as_view()), name='dms_list'),
    path('bms/', login_required(v.BmsList.as_view()), name='bms_list'),
    path('frs/', login_required(v.FrsList.as_view()), name='frs_list'),
    path('bmf/<int:pk>/edit/', login_required(v.BmfUpdate.as_view()), name='bmf_update'),
    path('bmf/create/', login_required(v.BmfCreate.as_view()), name='bmf_create'),
    path('dms/<int:pk>/edit/', login_required(v.DMSUpdate.as_view()), name='dms_update'),
    path('dms/create/', login_required(v.DMSCreate.as_view()), name='dms_create'),
    path('bms/<int:pk>/edit/', login_required(v.BmsUpdate.as_view()), name='bms_update'),
    path('bms/create/', login_required(v.BmsCreate.as_view()), name='bms_create'),
    path('frs/<int:pk>/edit/', login_required(v.FRSUpdate.as_view()), name='frs_update'),
    path('frs/create/', login_required(v.FRSCreate.as_view()), name='frs_create'),
    path('bmf/<int:pk>/', v.bmf_detail, name='bmf_detail'),
    path('bmf/deleteitem/<int:pk>/<int:id>/<int:ind>/', v.delete_item, name='delete_item'),
    path('dms/<int:pk>/', v.dms_detail, name='dms_detail'),
    path('dms/deleteitem/<int:pk>/<int:id>/', v.dmsitem_delete, name='delete_itemdms'),
    path('bms/<int:pk>/', v.bms_detail, name='bms_detail'),
    path('bms/deleteitem/<int:pk>/<int:id>/', v.bmsitem_delete, name='delete_itembms'),
    path('frs/<int:pk>/', v.frs_detail, name='frs_detail'),
    path('frs/deleteitem/<int:pk>/<int:id>/', v.frsitem_delete, name='delete_itemfrs'),
    path('import/csvcontrato/', v.import_csv, name='import_csvcontrato'),
    path('itensbm/json/<str:ref>/', v.json_itens, name='json_itens'),
]