from django.urls import path
from core import views as v


app_name ='core'

urlpatterns =[
    path('', v.index, name='index'),
    path('dashjato/', v.dashboard_jato, name='dash_jato'),
    path('dashfinanceiro/', v.dashboard_financeiro, name='dash_financeiro'),
]
