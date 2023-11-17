from django.urls import path
from rdo import views as v
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required
from rolepermissions.decorators import has_role_decorator

app_name ='financeiro'

urlpatterns =[
    path('rdo/create/', has_role_decorator('coordenador')(v.RdoCreate.as_view()), name='rdo_create'),

 ]