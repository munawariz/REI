from REI.decorators import staftu_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.query_utils import Q
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.views.generic import View
from helpers import active_semester, get_initial, form_value, get_sekolah
from .models import Guru
from siswa.models import Siswa
from sekolah.models import Kelas, Sekolah
from .forms import GuruEditForm, PasswordChangeForm, GuruCreateForm
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

def index(request):
    return redirect('dashboard')

@method_decorator(login_required, name='dispatch')
class dashboard(View):
    def get(self, request):
        request.session['page'] = 'Dashboard'
        context = {
            'sekolah': get_sekolah(),
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
        return render(request, 'pages/guru/detail-guru.html', context)

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
class list_guru(View):
    def get(self, request):
        request.session['page'] = 'Daftar Guru'
        if 'search' in request.GET and request.GET['search'] != '':
            list_guru = Guru.objects.filter(Q(is_active=True) &
                (Q(nama__icontains=request.GET['search']) | Q(nip__istartswith=request.GET['search']) |
                Q(email__icontains=request.GET['search']) | Q(tempat_lahir__icontains=request.GET['search']) |
                Q(tanggal_lahir__icontains=request.GET['search']) | Q(agama__icontains=request.GET['search']))
                ).order_by('is_superuser', 'is_staftu', 'is_walikelas', 'nama')
        else:
            list_guru = Guru.objects.filter(is_active=True).order_by('is_superuser', 'is_staftu', 'is_walikelas', 'nama')

        paginator = Paginator(list_guru, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        number_of_pages = [(number+1) for number in range(page_obj.paginator.num_pages)]
        context = {
            'list_guru': page_obj,
            'page_obj': page_obj,
            'number_of_pages': number_of_pages,
            'guru_form': GuruCreateForm()
        }
        return render(request, 'pages/guru/guru.html', context)

@method_decorator(staftu_required, name='dispatch')
class buat_guru(View):
    def post(self, request):
        guru_form = GuruCreateForm(request.POST)
        try:
            if guru_form.is_valid():
                if request.GET['level'] == 'staftu': 
                    is_staftu = True
                    is_walikelas = False
                if request.GET['level'] == 'walikelas': 
                    is_walikelas = True
                    is_walikelas = False

                guru = Guru.objects.create(**form_value(guru_form), is_staftu=is_staftu, is_walikelas=is_walikelas, is_active=True)
                guru.set_password(guru_form.cleaned_data['password'])
                guru.save()
                messages.success(request, 'Akun berhasil dibuat')
        except ValueError:
            messages.error(request, f'Akun dengan NIP itu sudah ada')
        finally:
            return redirect('list-guru')

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
        return render(request, 'pages/guru/detail-guru.html', context)

@method_decorator(staftu_required, name='dispatch')
class hapus_guru(View):
    def get(self, request, guru):
        guru = Guru.objects.get(nip=guru)
        guru.is_active = False
        guru.save()
        messages.success(request, f'Akun {guru.nama} berhasil dihapus')
        return redirect('list-guru')