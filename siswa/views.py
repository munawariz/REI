from REI import settings
from django.views.generic.edit import CreateView
from REI.decorators import staftu_required, walikelas_required, validkelas_required, activesemester_required
from django.http.response import FileResponse, Http404
from sekolah.models import Ekskul, MataPelajaran
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import Error, IntegrityError
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View, UpdateView
from .models import Absensi, NilaiEkskul, Siswa, Nilai
from .forms import SiswaForm, AbsenForm, NilaiEkskulForm, UploadExcelForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from helpers.nilai_helpers import zip_eksnilai, zip_pelnilai
from helpers import calculate_age, active_semester, get_initial, form_value, get_validkelas
from helpers.excel_handlers import extract_and_clean_siswa
from django.contrib import messages

@method_decorator(login_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class list_siswa(View):
    def get(self, request):
        request.session['page'] = 'Daftar Siswa'
        if 'search' in request.GET and request.GET['search'] != '':
            list_siswa = Siswa.objects.filter(
                (Q(nama__icontains=request.GET['search']) | Q(nis__istartswith=request.GET['search']) |
                Q(nisn__istartswith=request.GET['search']) | Q(email__icontains=request.GET['search']) |
                Q(tempat_lahir__icontains=request.GET['search']) | Q(tanggal_lahir__icontains=request.GET['search']) |
                Q(agama__icontains=request.GET['search']))
                ).order_by('nis')
        else:
            list_siswa = Siswa.objects.all().order_by('nis')

        paginator = Paginator(list_siswa, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        number_of_pages = [(number+1) for number in range(page_obj.paginator.num_pages)]
        context = {
            'list_siswa': page_obj,
            'page_obj': page_obj,
            'number_of_pages': number_of_pages,
            'siswa_form': SiswaForm(),
            'excel_form': UploadExcelForm(),
            'semester_aktif': active_semester(),
        }
        return render(request,  'pages/siswa/siswa.html', context)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class buat_siswa(CreateView):
    def post(self, request):
        siswa_form = SiswaForm(request.POST)
        try:
            if siswa_form.is_valid():
                siswa, created = Siswa.objects.get_or_create(**form_value(siswa_form))
                if created:
                    messages.success(request, f'Data siswa {siswa.nama} berhasil dibuat')
        except ValidationError:
            messages.error(request, 'Data gagal dibuat, periksa apakah NIS atau NISN sudah tersedia didata sebelumnya')
        finally:
            return redirect('list-siswa')

@method_decorator(login_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class detail_siswa(View):
    def get(self, request, nis):
        try:
            siswa = Siswa.objects.get(nis=nis)
        except ObjectDoesNotExist:
            raise Http404
        request.session['page'] = f'Detail {siswa.nama}'
        kelas = get_validkelas(siswa)
        if not kelas:
            messages.error(request, f'{siswa.nama} belum memiliki kelas di semester ini')

        context = {
            'siswa': siswa,
            'usia': calculate_age(siswa.tanggal_lahir),
            'siswa_form': SiswaForm(initial=get_initial(siswa)),
            'absensi': Absensi.objects.get_or_create(siswa=siswa, semester=active_semester())[0],
            'data_akademik': zip_pelnilai(siswa, active_semester()),
            'data_ekskul': zip_eksnilai(siswa, active_semester()),
            'kelas': kelas,
        }
        return render(request, 'pages/siswa/detail-siswa.html', context)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class profil_siswa(UpdateView):
    model = Siswa
    template_name = 'pages/siswa/profil-siswa.html'
    form_class = SiswaForm
    slug_field = 'nis'
    slug_url_kwarg = 'nis'    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['page'] = 'Profil Siswa'
        context['usia'] = calculate_age(context['object'].tanggal_lahir)
        return context

    def get_success_url(self, **kwargs):
        siswa = Siswa.objects.get(nis=self.kwargs['nis'])
        messages.success(self.request, f'Update profil {siswa.nama} berhasil')
        return reverse('detail-siswa', kwargs={'nis':siswa.nis})

@method_decorator(walikelas_required, name='dispatch')
@method_decorator(validkelas_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class nilai_siswa(View):
    def get(self, request, nis):
        request.session['page'] = 'Nilai Siswa'
        active_siswa = Siswa.objects.get(nis=nis)
        context = {
            'siswa': active_siswa,
            'usia': calculate_age(active_siswa.tanggal_lahir),
            'data': zip_pelnilai(active_siswa, active_semester()),
        }
        return render(request, 'pages/siswa/nilai-siswa.html', context)

    def post(self, request, nis):
        try:                
            active_siswa = Siswa.objects.get(nis=nis)
            data = zip_pelnilai(active_siswa, active_semester())
            for id_, matapelajaran, pengetahuan, keterampilan in data:
                matapelajaran = MataPelajaran.objects.get(id=id_)
                nilai_pengetahuan = int(request.POST[f'pengetahuan-{id_}'])
                nilai_keterampilan = int(request.POST[f'keterampilan-{id_}'])
                Nilai.objects.update_or_create(
                    siswa=active_siswa, matapelajaran=matapelajaran, semester=active_semester(),
                    defaults={'pengetahuan': nilai_pengetahuan, 'keterampilan': nilai_keterampilan}
                )
            messages.success(request, f'Update nilai {active_siswa.nama} berhasil')
            return redirect('nilai-siswa', nis=nis)
        except Siswa.DoesNotExist: 
            raise Http404

@method_decorator(walikelas_required, name='dispatch')
@method_decorator(validkelas_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class absen_siswa(View):
    def get(self, request, nis):
        request.session['page'] = 'Absensi Siswa'
        active_siswa = Siswa.objects.get(nis=nis)
        absen, created = Absensi.objects.get_or_create(
            siswa=active_siswa, semester=active_semester(),
            defaults={'izin': 0, 'sakit': 0, 'bolos': 0})
        absen_form = AbsenForm(initial=get_initial(absen))
        context = {
            'siswa': active_siswa,
            'absen_form': absen_form,
        }
        return render(request, 'pages/siswa/absen-siswa.html', context)

    def post(self, request, nis):
        active_siswa = Siswa.objects.get(nis=nis)
        absen_form = AbsenForm(request.POST)
        if absen_form.is_valid():
            Absensi.objects.filter(siswa=active_siswa, semester=active_semester()).update(**form_value(absen_form))
            messages.success(request, f'Update absensi {active_siswa.nama} berhasil')
            return redirect('absen-siswa', nis=nis)

@method_decorator(walikelas_required, name='dispatch')
@method_decorator(validkelas_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class ekskul_siswa(View):
    def get(self, request, nis):
        request.session['page'] = 'Ekskul Siswa'
        active_siswa = Siswa.objects.get(nis=nis)
        context = {
            'siswa': active_siswa,
            'data': zip_eksnilai(active_siswa, active_semester()),
            'tambah_absen_form': NilaiEkskulForm()
        }
        return render(request, 'pages/siswa/ekskul-siswa.html', context)

    def post(self, request, nis):
        active_siswa = Siswa.objects.get(nis=nis)
        data = zip_eksnilai(active_siswa, active_semester())
        for id_nil, id_eks, ekskul, nilai in data:
            nilai_form = request.POST[f'nilai-{id_eks}']
            if nilai != nilai_form:
                ekskul = Ekskul.objects.get(pk=id_eks)
                NilaiEkskul.objects.filter(siswa=active_siswa, ekskul=ekskul, semester=active_semester()).update(nilai=nilai_form)
                messages.success(request, f'Nilai {active_siswa.nama} untuk ekskul {ekskul.nama} berhasil diubah')
        return redirect('ekskul-siswa', nis=nis)

@method_decorator(walikelas_required, name='dispatch')
@method_decorator(validkelas_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class tambah_ekskul(View):
    def post(self, request, nis):
        absen_form = NilaiEkskulForm(request.POST)
        active_siswa = Siswa.objects.get(nis=nis)
        try:
            if absen_form.is_valid():
                NilaiEkskul.objects.create(**form_value(absen_form), siswa=active_siswa, semester=active_semester())
                messages.success(request, f'Ekskul {absen_form.cleaned_data["ekskul"]} berhasil ditambahkan untuk {active_siswa.nama}')
        except ValidationError:
            messages.error(request, f'{active_siswa.nama} sudah memiliki ekskul {absen_form.cleaned_data["ekskul"]}')
        finally:
            return redirect('ekskul-siswa', nis=nis)
    
@method_decorator(walikelas_required, name='dispatch')
@method_decorator(validkelas_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class hapus_ekskul_siswa(View):
    def get(self, request, nis, ekskul):
        active_siswa = Siswa.objects.get(nis=nis)
        ekskul = Ekskul.objects.get(pk=ekskul)
        NilaiEkskul.objects.get(ekskul=ekskul, siswa=active_siswa, semester=active_semester()).delete()
        messages.success(request, f'Ekskul {ekskul.nama} sudah dihapus dari data {active_siswa.nama}')
        return redirect('ekskul-siswa', nis=nis)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class hapus_siswa(View):
    def get(self, request, nis):
        Siswa.objects.get(nis=nis).delete()
        messages.success(request, 'Data siswa berhasil dihapus')
        return redirect('list-siswa')

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class import_excel_siswa(View):
    def post(self, request):
        excel_form = UploadExcelForm(request.POST, request.FILES)
        created_count = 0
        exists_count = 0
        error_count = 0
        if excel_form.is_valid():
            try:
                cleaned_json = extract_and_clean_siswa(request.FILES['file'])
                for siswa in cleaned_json:
                    try:
                        for key, value in siswa.items():
                            if key not in ['nama_wali', 'kelas']:
                                if not value: raise Error
                        obj, created = Siswa.objects.get_or_create(**siswa)
                        if created: created_count += 1
                    except IntegrityError:
                        exists_count += 1
                    except Error:
                        error_count += 1
                messages.success(request, 'Proses impor data dari berkas spreadsheet telah berhasil')
                messages.info(request, f'{created_count} data siswa baru, {exists_count} data siswa dengan NIS atau NISN yang sudah terdaftar sebelumnya, {error_count} data siswa yang gagal diinput')
            except ValueError:
                messages.error(request, 'File yang diunggah tidak didukung atau bukan sebuah file spreadsheet')
            finally:
                return redirect('list-siswa')

@method_decorator(staftu_required, name='dispatch')
class download_template_siswa(View):
    def get(self, request):
        file = open(f'{settings.MEDIA_ROOT}/excel_template/Siswa.xlsx', 'rb')
        response = FileResponse(file, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=Tabel Siswa.xlsx'
        return response