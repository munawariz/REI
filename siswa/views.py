import json

import pandas
from REI import settings
from django.views.generic.edit import CreateView
from REI.decorators import staftu_required, walikelas_required, validkelas_required, activesemester_required
from django.http.response import FileResponse, Http404, JsonResponse
from sekolah.models import Ekskul, Kelas, MataPelajaran
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import Error, IntegrityError
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.views.generic import View
from .models import Absensi, NilaiEkskul, Siswa, Nilai
from .forms import SiswaForm, AbsenForm, TambahEkskulSiswaForm, UploadExcelForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from helpers.nilai_helpers import has_ekskul, has_mapel, zip_eksnilai, zip_pelnilai
from helpers import active_tp, calculate_age, active_semester, get_initial, form_value, get_validekskul, get_validkelas, tambahmapel_choice
from helpers.excel_handlers import append_df_to_excel, extract_and_clean_siswa
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDictKeyError

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
        tp = active_tp()
        paginator = Paginator(list_siswa, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        number_of_pages = [(number+1) for number in range(page_obj.paginator.num_pages)]
        context = {
            'list_siswa': page_obj,
            'page_obj': page_obj,
            'number_of_pages': number_of_pages,
            'excel_form': UploadExcelForm(),
            'tp_aktif': tp,
        }
        return render(request,  'pages/siswa/siswa.html', context)

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class buat_siswa(View):
    def get(self, request):
        request.session['page'] = 'Buat Siswa'
        context = {
            'siswa_form': SiswaForm(),   
        }
        return render(request, 'pages/siswa/buat-siswa.html', context)

    def post(self, request):
        siswa_form = SiswaForm(request.POST)
        try:
            if siswa_form.is_valid():
                data = form_value(siswa_form)
                kelas = data['kelas']
                del data['kelas']
                siswa = Siswa.objects.create(**data)
                siswa.kelas.add(kelas)
                messages.success(request, 'Data siswa berhasil dicatat kedalam database')
            else:
                messages.error(request, 'Data gagal dibuat, periksa apakah NIS atau NISN sudah tersedia di basis data')    
        except IntegrityError:
            messages.error(request, 'Data gagal dibuat, periksa apakah NIS atau NISN sudah tersedia di basis data')
        finally:
            return redirect('list-siswa')

@method_decorator(login_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class detail_siswa(View):
    def get(self, request, nis):
        semester = active_semester()
        try:
            siswa = Siswa.objects.prefetch_related('kelas').get(nis=nis)
            kelas_aktif = siswa.kelas.get(tahun_pelajaran=semester.tahun_pelajaran)
        except Siswa.DoesNotExist: raise Http404
        except Kelas.DoesNotExist: kelas_aktif = None

        initial = get_initial(siswa)
        initial['kelas'] = kelas_aktif
        request.session['page'] = f'Detail {siswa.nama}'
        
        if not kelas_aktif: messages.info(request, f'{siswa.nama} belum memiliki kelas di semester ini')

        absen, created = Absensi.objects.get_or_create(
            siswa=siswa, semester=semester,
            defaults={'izin': 0, 'sakit': 0, 'bolos': 0})

        context = {
            'siswa': siswa,
            'kelas': kelas_aktif,
            'absensi': absen,
            'semester': semester,
            'siswa_form': SiswaForm(initial=initial),
            'absen_form': AbsenForm(initial=get_initial(absen)),
            'nilai_form': zip_pelnilai(siswa, semester),
            'data_ekskul': zip_eksnilai(siswa, semester),
            'ekskul_form': TambahEkskulSiswaForm(ekskul_list=tambahmapel_choice(get_validekskul(siswa))),
            'usia': calculate_age(siswa.tanggal_lahir),
        }
        return render(request, 'pages/siswa/detail-siswa.html', context)
        
    def post(self, request, nis):
        siswa_form = SiswaForm(request.POST)
        siswa = Siswa.objects.get(nis=nis)
        try: old_kelas = siswa.kelas.get(tahun_pelajaran=active_tp())
        except ObjectDoesNotExist: old_kelas = None

        if siswa_form.is_valid():
            data = form_value(siswa_form)
            kelas = data['kelas']
            del data['kelas']

            if old_kelas:
                siswa.kelas.remove(old_kelas)
            if kelas:
                siswa.kelas.add(kelas)
            siswa.save()
            Siswa.objects.filter(nis=nis).update(**data)
            messages.success(request, f'Profil {siswa.nama} berhasil diubah')
            return redirect('detail-siswa', nis=nis)
        else:
            context = {
                'siswa_form': siswa_form,
            }
            return render(request, 'pages/siswa/detail-siswa.html', context)

@method_decorator(walikelas_required, name='dispatch')
@method_decorator(validkelas_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class nilai_siswa(View):
     def post(self, request, nis):
        try:                
            active_siswa = Siswa.objects.get(nis=nis)
            semester = active_semester()
            data = zip_pelnilai(active_siswa, semester)
            for id_, matapelajaran, pengetahuan, keterampilan in data:
                matapelajaran = MataPelajaran.objects.get(id=id_)
                nilai_pengetahuan = int(request.POST[f'pengetahuan-{id_}'])
                nilai_keterampilan = int(request.POST[f'keterampilan-{id_}'])
                Nilai.objects.update_or_create(
                    siswa=active_siswa, matapelajaran=matapelajaran, semester=semester,
                    defaults={'pengetahuan': nilai_pengetahuan, 'keterampilan': nilai_keterampilan}
                )
            messages.success(request, f'Update nilai {active_siswa.nama} berhasil')
            return redirect('detail-siswa', nis=nis)
        except Siswa.DoesNotExist:
            raise Http404

@method_decorator(walikelas_required, name='dispatch')
@method_decorator(validkelas_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class absen_siswa(View):
    def post(self, request, nis):
        active_siswa = Siswa.objects.get(nis=nis)
        absen_form = AbsenForm(request.POST)
        if absen_form.is_valid():
            Absensi.objects.filter(siswa=active_siswa, semester=active_semester()).update(**form_value(absen_form))
            messages.success(request, f'Update absensi {active_siswa.nama} berhasil')
            return redirect('detail-siswa', nis=nis)

@method_decorator(walikelas_required, name='dispatch')
@method_decorator(validkelas_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class ekskul_siswa(View):
    def post(self, request, nis):
        active_siswa = Siswa.objects.get(nis=nis)
        semester = active_semester()
        data = zip_eksnilai(active_siswa, semester)
        try:
            for id_eks, id_nil, ekskul, nilai, jenis in data:
                nilai_form = request.POST[f'nilai-{id_eks}']
                
                if nilai_form and nilai != nilai_form:
                    ekskul = Ekskul.objects.get(pk=id_eks)
                    NilaiEkskul.objects.filter(siswa=active_siswa, ekskul=ekskul, semester=semester).update(nilai=nilai_form)
                    messages.success(request, f'Nilai {active_siswa.nama} untuk ekskul {ekskul.nama} berhasil diubah')
        except Exception as e:
            messages.error(request, e)
        return redirect('detail-siswa', nis=nis)

@method_decorator(walikelas_required, name='dispatch')
@method_decorator(validkelas_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class tambah_ekskul(View):
    def post(self, request, nis):
        ekskul_form = TambahEkskulSiswaForm(request.POST)
        siswa = Siswa.objects.get(nis=nis)
        ekskul = request.POST.getlist('ekskul')
        semester = active_semester()
        try:
            for ekskul in ekskul:
                NilaiEkskul.objects.create(ekskul=Ekskul.objects.get(id=ekskul), siswa=siswa, semester=semester)
            messages.success(request, f'Ekskul {ekskul_form.cleaned_data["ekskul"]} berhasil ditambahkan untuk {siswa.nama}')
        except ValidationError:
            messages.error(request, f'{siswa.nama} sudah memiliki ekskul {ekskul_form.cleaned_data["ekskul"]}')
        except Exception as e:
            request.error(request, e)
        finally:
            return redirect('detail-siswa', nis=nis)
    
@method_decorator(walikelas_required, name='dispatch')
@method_decorator(validkelas_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class hapus_ekskul_siswa(View):
    def get(self, request, nis, ekskul):
        active_siswa = Siswa.objects.get(nis=nis)
        ekskul = Ekskul.objects.get(pk=ekskul)
        NilaiEkskul.objects.get(ekskul=ekskul, siswa=active_siswa, semester=active_semester()).delete()
        messages.success(request, f'Ekskul {ekskul.nama} sudah dihapus dari data {active_siswa.nama}')
        return redirect('detail-siswa', nis=nis)

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
        tp = active_tp()
        if excel_form.is_valid():
            try:
                cleaned_json = extract_and_clean_siswa(request.FILES['file'])
                for siswa in cleaned_json:
                    kelas = siswa['kelas']
                    del siswa['kelas']
                    try:
                        for key, value in siswa.items():
                            if key not in ['nama_wali', 'kelas']:
                                if not value: raise Error
                        siswa, created = Siswa.objects.get_or_create(**siswa)
                        if kelas:
                            try:
                                old_kelas = siswa.kelas.get(tahun_pelajaran=tp)
                                siswa.kelas.remove(old_kelas)
                                kelas = Kelas.objects.get(nama=kelas, tahun_pelajaran=active_tp())
                                siswa.kelas.add(kelas)
                                siswa.save()
                            except Kelas.DoesNotExist:
                                pass
                        if created: created_count += 1
                    except IntegrityError:
                        exists_count += 1
                    except Error:
                        error_count += 1
                messages.success(request, 'Proses impor data dari berkas spreadsheet telah berhasil')
                messages.info(request, f'{created_count} data siswa baru, {exists_count} data siswa dengan NIS atau NISN yang sudah terdaftar sebelumnya, {error_count} data siswa yang gagal diinput')
            except ValueError:
                messages.error(request, 'File yang diunggah tidak didukung atau bukan sebuah file spreadsheet')
            except Exception as e:
                messages.error(request, e)
            finally:
                return redirect('list-siswa')

@method_decorator(staftu_required, name='dispatch')
class download_template_siswa(View):
    def get(self, request):
        file = open(f'{settings.MEDIA_ROOT}/excel/Siswa.xlsx', 'rb')
        response = FileResponse(file, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=Tabel Siswa.xlsx'
        return response

@method_decorator(staftu_required, name='dispatch')
@method_decorator(activesemester_required, name='dispatch')
class export_excel_siswa(View):
    def get(self, request):
        semester = active_semester()
        qs = list(Siswa.objects.select_related('kelas').all().values())
        if not qs:
            messages.error(request, 'Tidak ada data siswa yang dapat di ekspor')
            return redirect('list-siswa')
        cols = []

        for col in [field.name for field in Siswa._meta.fields]:
            if col in ['id']: continue
            if col in ['nis', 'nisn']:
                col = col.upper()
            else:
                col = col.title()
            col = col.replace('_', ' ')
            cols.append(col)
        cols.append('Kelas')
        
        for siswa in qs:
            try:
                siswa['kelas_id'] = Siswa.objects.get(nis=siswa['nis']).kelas.get(tahun_pelajaran=semester.tahun_pelajaran).nama.replace('-', ' ')
            except Kelas.DoesNotExist:
                siswa['kelas_id'] = None
            siswa['tanggal_lahir'] = siswa['tanggal_lahir'].strftime('%Y-%m-%d')
            if siswa['gender'] == 'P': siswa['gender'] = 'Pria'
            else: siswa['gender'] = 'Wanita'

        file = f'{settings.MEDIA_ROOT}/excel/Export Siswa.xlsx'
        json_string = json.dumps(qs)
        df = pandas.read_json(json_string, dtype={'nis':str, 'nisn':str})
        df = df.drop(columns='id')
        df.columns = cols

        append_df_to_excel(file, df)

        file = open(file, 'rb')
        response = FileResponse(file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename=Siswa {semester}.xlsx'
        return response