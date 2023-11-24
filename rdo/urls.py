from django.urls import path
from rdo import views as v
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required
from rolepermissions.decorators import has_role_decorator

app_name ='rdo'

urlpatterns =[
    path('rdo/create/', has_role_decorator('rdo')(v.RdoCreate.as_view()), name='rdo_create'),
    path('rdo/<slug:slug>/', v.rdo_detail, name='rdo_detail'),
    path('rdo/', has_role_decorator('rdo')(v.RdoList.as_view()), name='rdo_list'),
    path('rdo/edit/<slug:slug>/', v.rdo_edit, name='rdo_edit'),
    path('itembm/', v.itembm_add, name='itembm_add'),
    path('import/csvitembm/', v.import_csv_itembm, name='import_csv_itembm'),
    path('rdo/deleteitem/<int:id>/<int:ind>/', v.delete_item, name='delete_item'),
    path('bm/', has_role_decorator('bms')(v.BoletimList.as_view()), name='bm_list'),
    path('bm/<int:pk>/edit/', has_role_decorator('bms')(v.BoletimUpdate.as_view()), name='bm_update'),
    path('bm/create/', has_role_decorator('bms')(v.BoletimCreate.as_view()), name='bm_create'),
    path('bm/<int:pk>/', v.boletim_detail, name='bm_detail'),
    path('aprovador/', v.aprovador_add, name='aprovador_add'),
    path('contrato/', v.contrato_add, name='contrato_add'),
    path('projeto_cod/', v.projeto_add, name='projeto_add'),
    path('rdo/<int:pk>/assinatura/', has_role_decorator('fiscal')(v.AssinaturaRDOView.as_view()), name='assinatura_rdo'),
 ]