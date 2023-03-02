from django.urls import path
from material import views as v
from django.contrib.auth.decorators import login_required

app_name ='material'

urlpatterns =[
    path('material/', v.MaterialList.as_view(), name='material_list'),
    path('material/<int:pk>', v.material_detail, name='material_detail'),
    path('material/add/', login_required(v.MaterialCreate.as_view()), name='material_add'),
    path('material/<int:pk>/edit/', login_required(v.MaterialUpdate.as_view()), name='material_edit'),
    path('tratamento/', v.tratamento_add, name='tratamento_add'),
    path('tintaf/', v.tintafundo_add, name='tintafundo_add'),
    path('tintai/', v.tintaintermediaria_add, name='tintaintermediaria_add'),
    path('tintaa/', v.tintaacabamento_add, name='tintaacabamento_add'),
    path('material/export/xlsx/', v.export_xlsx_func_material, name='export_xlsx_func_material'),
    path('material/pdf/<int:pk>/', v.render_pdf_view, name='render_pdf_view'),
    path('material/import_csv/', v.import_csv, name='import_csv_material'),
]