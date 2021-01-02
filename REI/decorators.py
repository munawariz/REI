from django.db.models.query_utils import Q
from django.shortcuts import redirect
from guru.models import Guru
from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url
from django.contrib.auth import REDIRECT_FIELD_NAME
from urllib.parse import urlparse
from . import settings
from django.contrib import messages

def login_redirect(request):
    path = request.build_absolute_uri()
    resolved_login_url = resolve_url(settings.LOGIN_URL)
    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    current_scheme, current_netloc = urlparse(path)[:2]
    if ((not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)):
        path = request.get_full_path()

    messages.error(request, 'Silahkan login terlebih dahulu')
    return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)

def staftu_required(function=None):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated: return login_redirect(request)
        user = Guru.objects.filter(Q(pk=request.user.pk) & (Q(is_staftu=True) | Q(is_superuser=True)))
        if user:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Hanya Staf TU atau Admin yang diperbolehkan mengakses halaman tadi')
            if request.META.get('HTTP_REFERER'):
                return redirect(request.META.get('HTTP_REFERER'))
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
            messages.error(request, 'Hanya Walikelas atau Admin yang diperbolehkan mengakses halaman tadi')
            if request.META.get('HTTP_REFERER'):
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect('dashboard')

    return wrapper