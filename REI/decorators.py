from django.db.models.query_utils import Q
from django.shortcuts import redirect
from guru.models import Guru
from functools import wraps

def staftu_required(function=None):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        user = Guru.objects.filter(Q(pk=request.user.pk) & (Q(is_staftu=True) | Q(is_superuser=True)))
        if user:
            return function(request, *args, **kwargs)
        else:
            return redirect('dashboard')

    return wrapper

def walikelas_required(function=None):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        user = Guru.objects.filter(Q(pk=request.user.pk) & (Q(is_walikelas=True) | Q(is_superuser=True)))
        if user:
            return function(request, *args, **kwargs)
        else:
            return redirect('dashboard')

    return wrapper