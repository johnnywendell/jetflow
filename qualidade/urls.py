from django.urls import path
from qualidade import views as v
from django.contrib.auth.decorators import login_required

app_name ='qualidade'

urlpatterns =[
    path('qualidade/', v.RelatoriosList.as_view(), name='relatorios_list'),
    path('qualidade/edit/<int:pk>/', v.RelatorioUpdate.as_view(), name='relatorios_update'),
    path('qualidade/edit/etapa/<int:pk>/', v.EtapaUpdate.as_view(), name='etapas_update'),
    path('qualidade/<int:pk>/', v.relatorios_detail, name='relatorios_detail'),
    path('qualidade/add/', v.relatorios_add, name='relatorios_add'),
    path('photo/create/', v.photo_create, name='photo_create'),
    path('pdf/<int:pk>/', v.render_pdf_view, name='render_pdf_view'),
]
