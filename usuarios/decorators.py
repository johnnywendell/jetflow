# accounts/decorators.py
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def manager_required(function=None, login_url=settings.LOGIN_URL, redirect_field_name=REDIRECT_FIELD_NAME):
    '''
    Decorator que verifica se o usuário da sessão é ou não um gerente.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator