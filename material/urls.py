from django.urls import path
from material import views as v


app_name ='material'

urlpatterns =[
    path('material/', v.MaterialList.as_view(), name='material_list'),
    path('material/<int:pk>', v.material_detail, name='material_detail'),
    path('material/add/', v.MaterialCreate.as_view(), name='material_add'),
    path('material/<int:pk>/edit/', v.MaterialUpdate.as_view(), name='material_edit'),
    path('tratamento/', v.tratamento_add, name='tratamento_add'),
    path('tintaf/', v.tintafundo_add, name='tintafundo_add'),
    path('tintai/', v.tintaintermediaria_add, name='tintaintermediaria_add'),
    path('tintaa/', v.tintaacabamento_add, name='tintaacabamento_add'),
    path('material/export/xlsx/', v.export_xlsx_func_material, name='export_xlsx_func_material'),
    path('equipamento/', v.EquipamentoList.as_view(), name='equipamento_list'),
    path('equipamento/<int:pk>', v.equipamento_detail, name='equipamento_detail'),
    path('equipamento/add/', v.EquipamentoCreate.as_view(), name='equipamento_add'),
    path('equipamento/<int:pk>/edit/', v.EquipamentoUpdate.as_view(), name='equipamento_edit'),
]