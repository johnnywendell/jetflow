from django.urls import path
from qualidade import views as v
from django.contrib.auth.decorators import login_required

app_name ='qualidade'

urlpatterns =[
    path('qualidade/', v.RelatoriosList.as_view(), name='relatorios_list'),
    path('qualidade/<int:pk>/', v.relatorios_detail, name='relatorios_detail'),
]