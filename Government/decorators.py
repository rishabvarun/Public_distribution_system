from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def user_required(function=None, redirect_field_name='', login_url='http://127.0.0.1:8000/User/'):
   
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.first_name=='ration',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def distributor_required(function=None, redirect_field_name='', login_url='http://127.0.0.1:8000/accounts/login/'):
   
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.first_name=='distributor',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_required(function=None, redirect_field_name='', login_url='http://127.0.0.1:8000/accounts/login/'):
   
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.first_name=='ADMIN',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


