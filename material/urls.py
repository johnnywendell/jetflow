from django.urls import path
from material import views as v


app_name ='material'

urlpatterns =[
    path('material/', v.material_list, name='material_list'),
    path('material/<int:pk>', v.material_detail, name='material_detail'),
]