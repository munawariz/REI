from guru.models import Guru
from siswa.models import Absensi, Siswa
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.query_utils import Q
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Ekskul, Jurusan, KKM, Kelas, MataPelajaran, Rapor, Sekolah, Semester
from .forms import EkskulForm, JurusanForm, KKMForm, KelasForm, MatapelajaranForm, SekolahForm, SemesterForm
from django.db.models.deletion import ProtectedError
from django.core.paginator import Paginator
from REI.decorators import staftu_required, validdirs_required, activesemester_required
from helpers import active_semester, generate_rapor_context, get_initial, form_value, get_validkelas, get_validwalikelas, get_validsiswabaru, get_validpelajaran
from helpers.nilai_helpers import zip_eksnilai, zip_pelkkm, zip_nilrapor
from django.contrib import messages
from REI import settings
import os, shutil

from helpers import generate_pdf
from django.http import HttpResponse, FileResponse

@method_decorator(login_required, name='dispatch')
class detail_sekolah(View):
    def get(self, request):
        request.session['page'] = 'Detail Sekolah'
        sekolah = Sekolah.objects.get()
        sekolah_form = SekolahForm(initial=get_initial(sekolah))
        context = {
            'sekolah_form': sekolah_form,
        }
        return render(request, 'pages/detail-sekolah.html', context)

    def post(self, request):
        sekolah_form = SekolahForm(request.POST)
        if sekolah_form.is_valid():
            Sekolah.objects.update(**form_value(sekolah_form))
            messages.success(request, 'Data Sekolah berhasil diubah')
            return redirect('detail-sekolah')
    
@method_decorator(staftu_required, name='dispatch')
class list_semester(View):
    def get(self, request):
        request.session['page'] = 'Daftar Semester'
        if 'search' in request.GET and request.GET['search'] != '':
            list_semester = Semester.objects.filter(
                Q(nama__istartswith=request.GET['search']) |
                Q(tahun_mulai__icontains=request.GET['search']) |
                Q(tahun_akhir__icontains=request.GET['search']) |
                Q(semester__icontains=request.GET['search'])
            ).order_by('-tahun_mulai', '-tahun_akhir', '-semester')
        else:
            list_semester = Semester.objects.all().order_by('-tahun_mulai', '-tahun_akhir', '-semester')
        
        paginator = Paginator(list_semester, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        number_of_pages = [(number+1) for number in range(page_obj.paginator.num_pages)]
        context = {
            'list_semester': page_obj,
            'page_obj': page_obj,
            'create_form': SemesterForm(),
            'number_of_pages': number_of_pages,
        }
        return render(request, 'pages/semester/semester.html', context)

@method_decorator(staftu_required, name='dispatch')
class buat_semester(View):
    def post(self, request):
        semester_form = SemesterForm(request.POST)
        try:
            if semester_form.is_valid():
                semester = Semester.objects.create(**form_value(semester_form), is_active=False)
                messages.success(request, 'Semester berhasil dibuat')
        except ValidationError:
            messages.error(request, 'Semester dengan data persis seperti itu sudah ada')
        finally:
            return redirect('list-semester')

@method_decorator(staftu_required, name='dispatch')
class aktifkan_semester(View):
    def get(self, request, semester):
        semester = Semester.objects.get(pk=semester)
        semester.is_active = True
        semester.save()
        return redirect('list-semester')

@method_decorator(staftu_required, name='dispatch')
class hapus_semester(View):
    def get(self, request, semester):
        try:
            Semester.objects.get(pk=semester).delete()
            messages.success(request, 'Semester berhasil dihapus')
        except ProtectedError:
            messages.error(request, 'Semester masih memiliki kelas aktif, tidak dapat dihapus')
        finally:
            return redirect('list-semester')

@method_decorator(login_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class list_kelas(View):
    def get(self, request):
        request.session['page'] = 'Daftar Kelas'
        if 'search' in request.GET and request.GET['search'] != '':
            list_kelas = Kelas.objects.filter(
                Q(semester=active_semester()) & (
                Q(nama__icontains=request.GET['search']) |
                Q(walikelas__nama__icontains=request.GET['search']))
                ).order_by('jurusan', 'tingkat', 'kelas')
        else:
            list_kelas = Kelas.objects.filter(semester=active_semester()).order_by('jurusan', 'tingkat', 'kelas')
        
        paginator = Paginator(list_kelas, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        number_of_pages = [(number+1) for number in range(page_obj.paginator.num_pages)]
        context = {
            'page_obj': page_obj,
            'number_of_pages': number_of_pages,
            'list_kelas': list_kelas,
            'kelas_form': KelasForm(),
        }
        return render(request, 'pages/kelas/kelas.html', context)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class buat_kelas(View):
    def post(self, request):
        kelas_form = KelasForm(request.POST)
        try:
            if kelas_form.is_valid():
                kelas = Kelas.objects.create(**form_value(kelas_form), semester=active_semester())
                messages.success(request, 'Kelas berhasil dibuat, segera lengkapi data kelas tadi')
        except ValidationError:
            messages.error(request, 'Kelas itu sudah ada')
        finally:
            return redirect('list-kelas')

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class hapus_kelas(View):
    def get(self, request, kelas):
        try:
            Kelas.objects.get(nama=kelas, semester=active_semester()).delete()
            messages.success(request, f'Kelas {kelas} berhasil dihapus dari semester {active_semester()}')
        except ProtectedError:
            messages.error(request, 'Kelas masih memiliki siswa, tidak dapat dihapus')
        finally:
            return redirect('list-kelas')

@method_decorator(login_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class detail_kelas(View):
    def get(self, request, kelas):
        request.session['page'] = f'Detail {kelas}'
        try:
            kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        except ObjectDoesNotExist:
            raise Http404

        if kelas.walikelas == request.user or request.user.is_superuser: auth_walikelas = True
        else: auth_walikelas = False 

        context = {
            'kelas': kelas,
            'auth_walikelas': auth_walikelas,
            'list_siswa': Siswa.objects.filter(kelas=kelas).order_by('nama'),
            'list_matapelajaran': MataPelajaran.objects.filter(kelas=kelas).order_by('kelompok', 'nama'),
        }
        return render(request, 'pages/kelas/detail-kelas.html', context)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class walikelas_kelas(View):
    def get(self, request, kelas):
        request.session['page'] = f'Walikelas {kelas}'
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        try:
            active_walikelas = Guru.objects.get(kelas=kelas)
        except ObjectDoesNotExist:
            active_walikelas = None
        valid_walikelas = get_validwalikelas()
        context = {
            'kelas': kelas,
            'active_walikelas': active_walikelas,
            'valid_walikelas': valid_walikelas,
        }
        return render(request, 'pages/kelas/ubah-walikelas.html', context)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class ganti_walikelas(View):
    def post(self, request, kelas):
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        if request.POST['new_walikelas']:
            new_walikelas = Guru.objects.get(nip=request.POST['new_walikelas'])
            kelas.walikelas = new_walikelas
            kelas.save()
            messages.success(request, f'Walikelas untuk {kelas.nama} berhasil diubah')
        return redirect('walikelas-kelas', kelas=kelas.nama)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class anggota_kelas(View):
    def get(self, request, kelas):
        request.session['page'] = f'Anggota Kelas {kelas}'
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        context = {
            'kelas': kelas,
            'list_siswa': Siswa.objects.filter(kelas=kelas).order_by('nama'),
            'siswa_baru': get_validsiswabaru()
        }
        return render(request, 'pages/kelas/anggota-kelas.html', context)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class tambah_anggota(View):
    def get(self, request, kelas, siswa):
        siswa = Siswa.objects.get(nis=siswa)
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        siswa.kelas = kelas
        siswa.save()
        messages.success(request, f'{siswa.nama} berhasil menjadi anggota kelas {kelas.nama}')
        return redirect('anggota-kelas', kelas=kelas.nama)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class hapus_anggota(View):
    def get(self, request, kelas, siswa):
        siswa = Siswa.objects.get(nis=siswa)
        siswa.kelas = None
        siswa.save()
        messages.success(request, f'{siswa.nama} berhasil dihapus dari anggota kelas {kelas}')
        return redirect('anggota-kelas', kelas=kelas)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class pelajaran_kelas(View):
    def get(self, request, kelas):
        request.session['page'] = f'Matapelajaran {kelas}'
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        context = {
            'kelas': kelas,
            'list_matapelajaran': zip_pelkkm(MataPelajaran.objects.filter(kelas=kelas), active_semester()),
            'matapelajaran_baru': zip_pelkkm(get_validpelajaran(kelas.nama), active_semester()),
        }
        return render(request, 'pages/kelas/pelajaran-kelas.html', context)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class tambah_pelajaran(View):
    def get(self, request, kelas, pelajaran):
        matapelajaran = MataPelajaran.objects.get(pk=pelajaran)
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        kelas.matapelajaran.add(matapelajaran)
        messages.success(request, f'{matapelajaran.nama} berhasil ditambahkan ke kelas {kelas.nama}')
        return redirect('pelajaran-kelas', kelas=kelas.nama)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class hapus_pelajaran(View):
    def get(self, request, kelas, pelajaran):
        matapelajaran = MataPelajaran.objects.get(pk=pelajaran)
        kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
        kelas.matapelajaran.remove(matapelajaran)
        messages.success(request, f'{matapelajaran.nama} berhasil dihapus dari kelas {kelas.nama}')
        return redirect('pelajaran-kelas', kelas=kelas.nama)

@method_decorator(staftu_required, name='dispatch')
class list_jurusan(View):
    def get(self, request):
        request.session['page'] = 'Daftar Jurusan'
        context = {
            'list_jurusan': Jurusan.objects.all(),
            'jurusan_form': JurusanForm(),
        }
        return render(request, 'pages/jurusan/jurusan.html', context)

@method_decorator(staftu_required, name='dispatch')
class buat_jurusan(View):
    def post(self, request):
        jurusan_form = JurusanForm(request.POST)
        try:
            if jurusan_form.is_valid():
                jurusan = Jurusan.objects.create(**form_value(jurusan_form))
                messages.success(request, f'Jurusan {jurusan.nama} berhasil dibuat')
        except ValidationError:
            messages.error(request, f'Jurusan itu sudah tersedia')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat membuat jurusan')
        finally:
            return redirect('list-jurusan')

@method_decorator(staftu_required, name='dispatch')
class hapus_jurusan(View):
    def get(self, request, jurusan):
        try:
            jurusan = Jurusan.objects.get(pk=jurusan)
            nama_jurusan = jurusan.nama
            jurusan.delete()
            messages.success(request, f'{nama_jurusan} berhasil dihapus dari daftar jurusan sekolah')
        except ProtectedError:
            messages.error(request, f'{nama_jurusan} masih memiliki kelas aktif, tidak dapat dihapus')
        finally:
            return redirect('list-jurusan')


@method_decorator(staftu_required, name='dispatch')
class list_ekskul(View):
    def get(self, request):
        request.session['page'] = 'Daftar Ekskul'
        context = {
            'list_ekskul': Ekskul.objects.all().order_by('jenis'),
            'ekskul_form': EkskulForm(),
        }
        return render(request, 'pages/ekskul/ekskul.html', context)

@method_decorator(staftu_required, name='dispatch')
class buat_ekskul(View):
    def post(self, request):
        ekskul_form = EkskulForm(request.POST)
        try:
            if ekskul_form.is_valid():
                ekskul = Ekskul.objects.create(**form_value(ekskul_form))
                messages.success(request, f'Ekstrakulikuler {ekskul.nama} berhasil dibuat')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat membuat ekskul ')
        finally:
            return redirect('list-ekskul')

@method_decorator(staftu_required, name='dispatch')
class hapus_ekskul(View):
    def get(self, request, ekskul):
        try:
            ekskul = Ekskul.objects.get(pk=ekskul)
            nama_ekskul = ekskul.nama
            ekskul.delete()
            messages.success(request, f'{nama_ekskul} berhasil dihapus dari daftar ekstrakuliker sekolah')
        except Exception:
            messages.error(request, f'Terjadi kesalahan saat mencoba menghapus ekstrakulikuler')
        finally:
            return redirect('list-ekskul')

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class list_matapelajaran(View):
    def get(self, request):
        request.session['page'] = 'Daftar Matapelajaran'
        list_matapelajaran = MataPelajaran.objects.all().order_by('kelompok')
        context = {
            'data': zip_pelkkm(list_matapelajaran, active_semester()),
            'list_matapelajaran': list_matapelajaran,
            'matapelajaran_form': MatapelajaranForm(),
        }
        return render(request, 'pages/matapelajaran/matapelajaran.html', context)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class buat_matapelajaran(View):
    def post(self, request):
        matapelajaran_form = MatapelajaranForm(request.POST)
        try:
            if matapelajaran_form.is_valid():
                mapel = MataPelajaran.objects.create(**form_value(matapelajaran_form))
                messages.success(request, f'{mapel.nama} berhasil dibuat')
        except Exception as e:
            messages.error(request, 'Terjadi kesalahan saat mencoba membuat Matapelajaran')
        finally:
            return redirect('list-matapelajaran')

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class detail_matapelajaran(View):
    def get(self, request, matapelajaran):
        try:
            matapelajaran = MataPelajaran.objects.get(pk=matapelajaran)
        except ObjectDoesNotExist:
            raise Http404
        request.session['page'] = f'Detail {matapelajaran.nama}'
        kkm, created = KKM.objects.get_or_create(matapelajaran=matapelajaran, semester=active_semester())
        context = {
            'matapelajaran': matapelajaran,
            'kkm': kkm,
            'matapelajaran_form': MatapelajaranForm(initial=get_initial(matapelajaran)),
            'kkm_form': KKMForm(initial=get_initial(kkm)),
        }
        return render(request, 'pages/matapelajaran/detail-matapelajaran.html', context)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class ubah_matapelajaran(View):
    def post(self, request, matapelajaran):
        matapelajaran_form = MatapelajaranForm(request.POST)
        try:
            if matapelajaran_form.is_valid():
                MataPelajaran.objects.filter(pk=matapelajaran).update(**form_value(matapelajaran_form))
                nama_mapel = MataPelajaran.objects.get(pk=matapelajaran).nama
                messages.success(request, f'Data Matapelajaran {nama_mapel} berhasil diubah')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat mencoba mengubah data Matapelajaran')
        finally:
            return redirect('detail-matapelajaran', matapelajaran=matapelajaran)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class ubah_kkm(View):
    def post(self, request, matapelajaran):
        kkm_form = KKMForm(request.POST)
        mapel = MataPelajaran.objects.get(pk=matapelajaran)
        try:
            if kkm_form.is_valid():
                kkm = KKM.objects.filter(matapelajaran=mapel, semester=active_semester())
                kkm.update(**form_value(kkm_form))
                messages.success(request, f'Data KKM untuk Matapelajaran {mapel.nama} berhasil diubah')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat mencoba mengubah data KKM untuk Matapelajaran {mapel.nama}')
        finally:
            return redirect('detail-matapelajaran', matapelajaran=matapelajaran)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class hapus_matapelajaran(View):
    def get(self, request, matapelajaran):
        try:
            mapel = MataPelajaran.objects.get(pk=matapelajaran)
            nama_mapel = mapel.nama
            mapel.delete()
            messages.success(request, f'{nama_mapel} telah berhasil dihapus')
        except Exception as e:
            messages.error(request, 'Terjadi kesalahan saat mencoba menghapus Matapelajaran')
        finally:
            return redirect('list-matapelajaran')

@method_decorator(login_required, name='dispatch')
@method_decorator(validdirs_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class rapor_view(View):
    def get(self, request, nis, action, **kwargs):
        try:
            siswa = Siswa.objects.get(nis=nis)
        except ObjectDoesNotExist:
            raise Http404
        sekolah = Sekolah.objects.get()
        semester = active_semester()
        context = generate_rapor_context(sekolah, semester, siswa)
        generate_pdf(siswa, kwargs['pdf_dir'], context)
        rapor = Rapor.objects.get(siswa=siswa, semester=semester)
        with open(rapor.rapor, 'rb') as result:            
            response = HttpResponse(result, content_type='application/pdf;')
            if action == 'unduh':
                response['Content-Disposition'] = f'attachment; filename={siswa.nama}.pdf'
                response['Content-Transfer-Encoding'] = 'binary'
            elif action == 'pratinjau':
                response['Content-Disposition'] = f'inline; filename={siswa.nama}.pdf'
                response['Content-Transfer-Encoding'] = 'binary'
            else:
                return redirect('dashboard')

            return response

@method_decorator(login_required, name='dispatch')
@method_decorator(validdirs_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class bundle_rapor_view(View):
    def get(self, request, kelas, **kwargs):
        try:
            sekolah = Sekolah.objects.get()
            semester = active_semester()
            kelas = Kelas.objects.get(nama=kelas, semester=semester)
            siswa = Siswa.objects.filter(kelas=kelas)
        except ObjectDoesNotExist:
            raise Http404

        for siswa in siswa:
            context = generate_rapor_context(sekolah, semester, siswa)
            generate_pdf(siswa, kwargs['pdf_dir'], context)

        bundle_dir = f'{settings.MEDIA_ROOT}/rapor/{kelas.semester.tahun_mulai} - {kelas.semester.tahun_akhir} {kelas.semester.semester}/bundel/{kelas.jurusan}'
        if not os.path.isdir(bundle_dir):
            os.makedirs(bundle_dir)
        
        shutil.make_archive(f'{bundle_dir}/Rapor-{kelas.nama}', 'zip', kwargs['pdf_dir'])
        zip_file = open(f'{bundle_dir}/Rapor-{kelas.nama}.zip', 'rb')
        response = FileResponse(zip_file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename=Rapor-{kelas.nama}.zip'

        return response