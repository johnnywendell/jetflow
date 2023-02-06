from django.urls import path
from romaneio import views as v


app_name ='romaneio'

urlpatterns =[
    path('romaneios/', v.romaneio_list, name='romaneio_list'),
    path('romaneios/<int:pk>/', v.romaneio_detail, name='romaneio_detail'),
    path('romaneios/add/', v.romaneio_add, name='romaneios_add'),
    path('add/', v.RomaneioCreate.as_view(), name='romaneio_add'),
    path('romaneios/<int:pk>/edit/', v.RomaneioUpdate.as_view(), name='romaneio_edit'),
]