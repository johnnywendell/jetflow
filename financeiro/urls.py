from django.urls import path
from financeiro import views as v
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required

app_name ='financeiro'

urlpatterns =[
    path('contrato/', v.contrato_add, name='contrato_add'),
    path('itembm/', v.itembm_add, name='itembm_add'),
    path('bmf/', login_required(v.BmfList.as_view()), name='bmf_list'),
    path('bmf/<int:pk>/edit/', login_required(v.BmfUpdate.as_view()), name='bmf_update'),
    path('bmf/create/', login_required(v.BmfCreate.as_view()), name='bmf_create'),
    path('bmf/<int:pk>/', v.bmf_detail, name='bmf_detail'),
]