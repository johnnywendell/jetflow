from django.urls import path
from material import views as v
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required

app_name ='material'

urlpatterns =[
    path('material/', login_required(v.MaterialList.as_view()), name='material_list'),
    path('material/<int:pk>', v.material_detail, name='material_detail'),
    path('material/add/', manager_required(v.MaterialCreate.as_view()), name='material_add'),
    path('material/<int:pk>/edit/', manager_required(v.MaterialUpdate.as_view()), name='material_edit'),
    path('tratamento/', v.tratamento_add, name='tratamento_add'),
    path('tintaf/', v.tintafundo_add, name='tintafundo_add'),
    path('tintai/', v.tintaintermediaria_add, name='tintaintermediaria_add'),
    path('tintaa/', v.tintaacabamento_add, name='tintaacabamento_add'),
    path('material/export/xlsx/', v.export_xlsx_func_material, name='export_xlsx_func_material'),
    path('material/pdf/<int:pk>/', v.render_pdf_view, name='render_pdf_view'),
    path('material/import_csv/', v.import_csv, name='import_csv_material'),
    path('material/jsonmaterial/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77/<str:begin>/<str:end>/', v.json_material, name='json_material'),
    path('material/jsontratamento/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77', v.json_tratamento, name='json_tratamento'),
    path('material/jsonstatus/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77/<str:begin>/<str:end>/', v.json_status, name='json_status'),
    path('material/jsonti/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77', v.json_ti, name='json_ti'),
    path('material/jsonta/2b76e8ce5dfae938c4974bc08d48ed4e97e49d77', v.json_ta, name='json_ta'),
]
