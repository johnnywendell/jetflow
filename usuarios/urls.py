from django.urls import path
from usuarios import views as v

urlpatterns = [
    path('update/', v.login_update, name='update'),
    path('login/', v.login, name='login'),
]