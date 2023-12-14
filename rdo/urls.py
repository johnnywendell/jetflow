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
    path('rdo_fiscal/', has_role_decorator('fiscal')(v.RdoListFiscal.as_view()), name='rdo_list_fiscal'),
    path('rdo/edit/<slug:slug>/', v.rdo_edit, name='rdo_edit'),
    path('itembm/', v.itembm_add, name='itembm_add'),
    path('import/csvitembm/', v.import_csv_itembm, name='import_csv_itembm'),
    path('rdo/deleteitem/<int:id>/<int:ind>/', v.delete_item, name='delete_item'),
    path('bm/', has_role_decorator('bms')(v.BoletimList.as_view()), name='bm_list'),
    path('bm/<int:pk>/edit/', has_role_decorator('bms')(v.BoletimUpdate.as_view()), name='bm_update'),
    path('bm/create/', has_role_decorator('bms')(v.BoletimCreate.as_view()), name='bm_create'),
    path('bm/<int:pk>/', v.boletim_detail, name='bm_detail'),
    path('bm/<int:pk>/<int:id>/', v.bm_delete, name='bm_delete'),
    path('aprovador/', v.aprovador_add, name='aprovador_add'),
    path('contrato/', v.contrato_add, name='contrato_add'),
    path('projeto_cod/', v.projeto_add, name='projeto_add'),
    path('rdo/<int:pk>/assinatura/', has_role_decorator('fiscal')(v.AssinaturaRDOView.as_view()), name='assinatura_rdo'),
    path('export_csv/<int:pk>/', v.export_csv_view, name='export_csv'),
    path('area_rdo/', v.area_add, name='area_add'),
    path('solicitante_rdo/', v.solicitante_add, name='solicitante_add'),
    path('frs/', manager_required(v.FrsList.as_view()), name='frs_list'),
    path('frs/<int:pk>/edit/', manager_required(v.FRSUpdate.as_view()), name='frs_update'),
    path('frs/create/', manager_required(v.FRSCreate.as_view()), name='frs_create'),
    path('frs/<int:pk>/', v.frs_detail, name='frs_detail'),
    path('frs/deleteitem/<int:pk>/<int:id>/', v.frsitem_delete, name='delete_itemfrs'),
    path('bmf/export/xlsx/', v.export_xlsx_func_bmf, name='export_xlsx_func_bmf'),
    path('bmf/exportmov/xlsx/', v.export_movimentacao, name='export_movimentacao'),
    path('pdfbms/<int:pk>/', v.render_pdf_view, name='render_pdf_view'),
    path('rdo/deleteass/<int:pk>/<int:id>/', v.delete_assinatura, name='delete_assinatura'),
############

 ]