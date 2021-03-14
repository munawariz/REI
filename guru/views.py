from django.db.utils import IntegrityError
from REI.decorators import staforself_required, staftu_required, activesemester_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.query_utils import Q
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.views.generic import View, CreateView
from helpers import active_semester, active_tp, get_initial, form_value, get_sekolah
from .models import Gelar, Guru
from siswa.models import Siswa
from sekolah.models import Ekskul, Jurusan, Kelas, MataPelajaran, Sekolah
from .forms import GelarForm, GuruEditForm, PasswordChangeForm, GuruCreateForm, LoginForm
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.utils.datastructures import MultiValueDictKeyError
from REI.settings import MEDIA_ROOT
from helpers.externalAPI import avatarAPI


class CustomLoginView(LoginView):
    authentication_form = LoginForm

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
                messages.success(request, 'Password anda berhasil diganti. Silahkan login menggunakan password baru')
            else:
                messages.error(request, 'Password lama anda salah, silahkan coba lagi')
        else:
            if ValidationError: messages.error(request, 'Konfirmasi password baru anda salah')
        
        return redirect('detail-guru', guru=user.nip)

@method_decorator(staftu_required, name='dispatch')
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

        paginator = Paginator(list_guru, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        number_of_pages = [(number+1) for number in range(page_obj.paginator.num_pages)]
        context = {
            'list_guru': page_obj,
            'page_obj': page_obj,
            'number_of_pages': number_of_pages,
        }
        return render(request, 'pages/guru/guru.html', context)

@method_decorator(staftu_required, name='dispatch')
class buat_guru(View):
    def get(self, request):
        request.session['page'] = 'Buat Guru'
        context = {
            'guru_form': GuruCreateForm()
        }
        return render(request, 'pages/guru/buat-guru.html', context)

    def post(self, request):
        guru_form = GuruCreateForm(request.POST)
        try:
            if guru_form.is_valid():
                guru = Guru.objects.create(**form_value(guru_form), is_active=True)
                guru.set_password(guru_form.cleaned_data['password'])
                guru.save()
                messages.success(request, 'Akun berhasil dibuat')
        except IntegrityError:
            registered_nip = Guru.objects.get(nip=guru_form.cleaned_data['nip'])
            if not registered_nip.is_active:
                messages.error(request, 'Akun dengan NIP itu sudah ada tetapi statusnya nonaktif, silahkan minta admin untuk mengaktifkan akun tadi')
            else:
                messages.error(request, 'Akun dengan NIP itu sudah ada')
        finally:
            return redirect('list-guru')

@method_decorator(login_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class profil_lain(View):
    def get(self, request, guru):
        try:
            guru = Guru.objects.get(nip=guru)
            kelas = Kelas.objects.get(walikelas=guru, tahun_pelajaran=active_tp())
        except Guru.DoesNotExist:
            raise Http404
        except Kelas.DoesNotExist:
            kelas=None
        request.session['page'] = f'Profil {guru.nama}'
        
        context = {
            'profile_form': GuruEditForm(initial=get_initial(guru)),
            'password_form': PasswordChangeForm(),
            'gelar_form': GelarForm(),
            'guru': guru,
            'kelas': kelas,
        }
        return render(request, 'pages/guru/detail-guru.html', context)

@method_decorator(staftu_required, name='dispatch')
class hapus_guru(View):
    def get(self, request, guru):
        guru = Guru.objects.get(nip=guru)
        if not request.user.is_superuser and guru.is_superuser:
            messages.error(request, 'Akun Staf TU tidak bisa menghapus akun admin')
        else:
            guru.is_active = False
            guru.save()
            messages.success(request, f'Akun {guru.nama} berhasil dihapus')
        return redirect('list-guru')

@method_decorator(staforself_required, name='dispatch')
class ubah_profil_guru(View):
    def post(self, request, guru):
        profile_form = GuruEditForm(request.POST, request.FILES)
        try:
            if profile_form.is_valid():
                Guru.objects.filter(nip=guru).update(**form_value(profile_form))
                subjek = Guru.objects.get(nip=guru)
                try:
                    new_ava = request.FILES['avatar']
                    if '.' in str(new_ava)[-4:]: ext = str(new_ava)[-3:]
                    else: ext = str(new_ava)[-4:]
                    ava_dir = f'{MEDIA_ROOT}/avatar/guru/{subjek.nip}.{ext}'
                    with open(ava_dir, 'wb+') as destination:
                        for chunk in new_ava.chunks():
                            destination.write(chunk)
                    destination.close()
                    subjek.avatar = ava_dir
                    subjek.save()
                except MultiValueDictKeyError:
                    try:
                        clearbox = request.POST['avatar-clear']
                        if clearbox == 'on':
                            subjek.avatar = avatarAPI(subjek)
                            subjek.save()
                    except:
                        pass
                except Exception as e:
                    messages.error(request, e)
                    
                messages.success(request, 'Update profil berhasil!')
            else:
                messages.error(request, 'Silahkan pilih salah satu antara melakukan clear avatar atau mengupload avatar baru')
        except Exception as e:
            messages.error(request, e)
        finally:
            return redirect('detail-guru', guru=guru)

@method_decorator(staforself_required, name='dispatch')
class tambah_gelar(View):
    def post(self, request, guru):
        gelar_form = GelarForm(request.POST)
        try:
            subjek = Guru.objects.get(nip=guru)
        except Guru.DoesNotExist:
            raise Http404
        if gelar_form.is_valid():
            Gelar.objects.create(**form_value(gelar_form), guru=subjek)
            messages.success(request, 'Gelar berhasil ditambahkan')
        return redirect('detail-guru', guru=guru)

@method_decorator(staforself_required, name='dispatch')
class hapus_gelar(View):
    def get(self, request, guru, gelar):
        try:
            gelar = Gelar.objects.get(id=gelar)
        except Gelar.DoesNotExist:
            raise Http404
        gelar.delete()
        messages.success(request, 'Gelar berhasil dihapus')
        return redirect('detail-guru', guru=guru)