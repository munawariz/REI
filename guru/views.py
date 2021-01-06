from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.query_utils import Q
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.views.generic import View
from helpers import active_semester, get_initial, form_value
from .models import Guru
from siswa.models import Siswa
from sekolah.models import Kelas, Sekolah
from .forms import GuruEditForm, PasswordChangeForm
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages

def placeholder(request):
    return render(request, 'base.html')

def index(request):
    return redirect('dashboard')

@method_decorator(login_required, name='dispatch')
class dashboard(View):
    def get(self, request):
        request.session['page'] = 'Dashboard'
        context = {
            'sekolah': Sekolah.objects.get(),
            'semester': active_semester(),
        }
        return render(request, 'pages/dashboard.html', context)

@method_decorator(login_required, name='dispatch')
class profil(View):
    def get(self, request):
        request.session['page'] = 'Profil Anda'
        guru = Guru.objects.get(pk=request.user.pk)
        context = {
            'profile_form': GuruEditForm(initial=get_initial(guru)),
            'password_form': PasswordChangeForm(),
            'guru': guru,
        }
        return render(request, 'pages/guru/profil.html', context)

    def post(self, request):
        profile_form = GuruEditForm(request.POST)
        if profile_form.is_valid():
            Guru.objects.filter(pk=request.user.pk).update(**form_value(profile_form))
            messages.success(request, 'Update profil berhasil!')
            return redirect('profil')

@method_decorator(login_required, name='dispatch')
class ganti_password(View):
    def post(self, request):
        password_form = PasswordChangeForm(request.POST)
        if password_form.is_valid():
            newpassword=password_form.cleaned_data['new_password1']
            password=password_form.cleaned_data['old_password']
            user = authenticate(nip=request.user.nip, password=password)
            if user is not None:
                user.set_password(newpassword)
                user.save()
                messages.success(request, 'Password anda berhasil diganti')
            else:
                messages.error(request, 'Password lama anda salah, silahkan coba lagi')
        else:
            if ValidationError: messages.error(request, 'Konfirmasi password baru anda salah')
        
        return redirect('profil')

@method_decorator(login_required, name='dispatch')
class profil_lain(View):
    def get(self, request, guru):
        try:
            guru = Guru.objects.get(nip=guru)
            kelas = Kelas.objects.get(walikelas=guru, semester=active_semester())
        except Guru.DoesNotExist:
            raise Http404
        except Kelas.DoesNotExist:
            kelas=None
        request.session['page'] = f'Profil {guru.nama}'
        if guru == request.user: return redirect('profil')
        
        context = {
            'profile_form': GuruEditForm(initial=get_initial(guru)),
            'guru': guru,
            'kelas': kelas,
        }
        return render(request, 'pages/guru/profil.html', context)