from django.urls import path
from material import views as v


app_name ='material'

urlpatterns =[
    path('material/', v.material_list, name='material_list'),
    path('material/<int:pk>', v.material_detail, name='material_detail'),
    path('material/add/', v.RomaneioCreate.as_view(), name='material_add'),
    path('material/<int:pk>/edit/', v.MaterialUpdate.as_view(), name='material_edit'),
    path('tratamento/', v.tratamento_add, name='tratamento_add'),
    path('tintaf/', v.tintafundo_add, name='tintafundo_add'),
    path('tintai/', v.tintaintermediaria_add, name='tintaintermediaria_add'),
    path('tintaa/', v.tintaacabamento_add, name='tintaacabamento_add'),

]