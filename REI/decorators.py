from helpers import active_semester, active_tp, get_validkelas
from sekolah.models import Kelas
from siswa.models import Siswa
from django.core.exceptions import ObjectDoesNotExist
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
import os

def login_redirect(request):
    path = request.build_absolute_uri()
    resolved_login_url = resolve_url(settings.LOGIN_URL)
    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    current_scheme, current_netloc = urlparse(path)[:2]
    if ((not login_scheme or login_scheme == current_scheme) and (not login_netloc or login_netloc == current_netloc)):
        path = request.get_full_path()

    messages.error(request, 'Silahkan login terlebih dahulu')
    return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)

def login_required(function=None):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_active:
            return login_redirect(request)
        if request.user.first_login: return redirect('first-login')

        return function(request, *args, **kwargs)

    return wrapper

def staftu_required(function=None):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_active:
            return login_redirect(request)
        
        if request.user.first_login: return redirect('first-login')
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
        if not request.user.is_authenticated or not request.user.is_active:
            return login_redirect(request)
        if request.user.first_login: return redirect('first-login')
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

def validkelas_required(function=None):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        siswa = Siswa.objects.get(nis=kwargs['nis'])
        if get_validkelas(siswa):
            return function(request, *args, **kwargs)
        else:
            return redirect('detail-siswa', nis=siswa.nis)

    return wrapper

def validdirs_required(function=None):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        try:
            if kwargs['nis']:
                siswa = Siswa.objects.get(nis=kwargs['nis'])
                kelas = get_validkelas(siswa)
        except KeyError:
            try:
                if kwargs['kelas']:
                    kelas = Kelas.objects.get(nama=kwargs['kelas'], tahun_pelajaran=active_tp())
            except KeyError:
                kelas = None
                return redirect('dashboard')
        semester = active_semester()
        dirs = f'{settings.MEDIA_ROOT}/rapor/{kelas.tahun_pelajaran.mulai} - {kelas.tahun_pelajaran.akhir} {semester.semester}/{kelas.jurusan}/{kelas.nama}'
        if not os.path.isdir(dirs): 
            os.makedirs(dirs)
        kwargs['pdf_dir'] = dirs

        return function(request, *args, **kwargs)

    return wrapper

def activesemester_required(function=None):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if active_semester():
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Halaman itu tidak bisa diakses sebelum ada semester yang diaktifkan')
            return redirect('dashboard')

    return wrapper

def staforself_required(function=None):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated: return login_redirect(request)
        user = Guru.objects.filter(Q(pk=request.user.pk) & (Q(is_staftu=True) | Q(is_superuser=True)))
        if user or request.user.nip == kwargs['guru']:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Hanya Staf TU atau Admin atau Akun yang bersangkutan yang diperbolehkan mengakses halaman tadi')
            if request.META.get('HTTP_REFERER'):
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect('dashboard')

    return wrapper