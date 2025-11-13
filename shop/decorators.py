from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps

def admin_required(function):
    """
    Decorador para requerir que el usuario sea staff/admin
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return redirect('accounts:login')
    return wrap
