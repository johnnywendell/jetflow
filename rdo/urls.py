from django.urls import path
from rdo import views as v
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required
from rolepermissions.decorators import has_role_decorator

app_name ='rdo'

urlpatterns =[
    path('rdo/create/', has_role_decorator('coordenador')(v.RdoCreate.as_view()), name='rdo_create'),
    path('rdo/<slug:slug>/', v.rdo_detail, name='rdo_detail'),
    path('rdo/', manager_required(v.RdoList.as_view()), name='rdo_list'),
    path('rdo/edit/<slug:slug>/', v.rdo_edit, name='rdo_edit'),
    path('itembm/', v.itembm_add, name='itembm_add'),
    path('import/csvitembm/', v.import_csv_itembm, name='import_csv_itembm'),
    path('rdo/deleteitem/<int:id>/<int:ind>/', v.delete_item, name='delete_item'),
    path('bm/', manager_required(v.BoletimList.as_view()), name='bm_list'),
    path('bm/<int:pk>/edit/', manager_required(v.BoletimUpdate.as_view()), name='bm_update'),
    path('bm/create/', manager_required(v.BoletimCreate.as_view()), name='bm_create'),
    path('bm/<int:pk>/', v.boletim_detail, name='bm_detail'),
    path('aprovador/', v.aprovador_add, name='aprovador_add'),
 ]