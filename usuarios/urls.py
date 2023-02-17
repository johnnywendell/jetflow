from django.urls import path
from usuarios import views as v

urlpatterns = [
    path('cadastro/', v.cadastro, name='cadastro'),
    path('login/', v.login, name='login'),
]