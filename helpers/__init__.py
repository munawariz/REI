from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django import forms
from django.forms.models import model_to_dict
from weasyprint import HTML
from django.template.loader import render_to_string
from django.db.utils import OperationalError, ProgrammingError
  
def calculate_age(birthDate):
    age = int((date.today() - birthDate).days / 365) 
    return age 

def active_tp():
    try:
        from sekolah.models import TahunPelajaran
        return TahunPelajaran.objects.get(is_active=True)
    except ObjectDoesNotExist:
        return None
    except OperationalError:
        return None
    except ProgrammingError:
        return None

def active_semester():    
    try:
        from sekolah.models import Semester
        return Semester.objects.get(is_active=True)
    except ObjectDoesNotExist:
        return None
    except OperationalError:
        return None

def semiactive_semester():
    try:
        from sekolah.models import Semester
        curr_active = active_semester()
        for i in ['Ganjil', 'Genap']:
            if not curr_active.semester == i:
                semester = i

        semiactive = Semester.objects.get(
            tahun_pelajaran__mulai=curr_active.tahun_pelajaran.mulai,
            tahun_pelajaran__akhir=curr_active.tahun_pelajaran.akhir,
            semester=semester)
        return semiactive
    except ObjectDoesNotExist:
        return None
    except OperationalError:
        return None


def get_initial(object):
    object_dict = model_to_dict(object)
    initial = {}
    for key, value in object_dict.items():
        initial[key] = value
    
    return initial

def form_value(valid_form: forms):
    field_value = {}
    for key, value in valid_form.cleaned_data.items():
        field_value[key] = value

    return field_value

def get_validwalikelas():
    from guru.models import Guru
    from sekolah.models import Kelas
    valid_walikelas = []
    all_walikelas = Guru.objects.filter(is_walikelas=True, is_active=True)
    tp = active_tp()
    for walikelas in all_walikelas:
        try:
            list_kelas = [kelas.tahun_pelajaran for kelas in Kelas.objects.select_related('tahun_pelajaran').filter(walikelas=walikelas)]
            if not tp in list_kelas:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            valid_walikelas.append(walikelas)

    return valid_walikelas

def walikelas_choice(validwalikelas):
    vw = {}
    vw[None] = '---------'
    for walikelas in validwalikelas:
        vw[walikelas.nip] = walikelas.nama

    return [(nip, walikelas) for nip, walikelas in vw.items()]

def tambahmapel_choice(list_mapel):
    vw = {}
    for mapel in list_mapel:
        vw[mapel.id] = mapel.nama

    return [(_id, nama) for _id, nama in vw.items()]

def tambahanggota_choice(list_siswa):
    vw = {}
    for siswa in list_siswa:
        vw[siswa.nis] = siswa.nama

    return [(nis, nama) for nis, nama in vw.items()]

def get_validsiswabaru():
    from siswa.models import Siswa
    from sekolah.models import Kelas
    valid_siswa = []
    all_siswa = Siswa.objects.all()
    tp = active_tp()
    for siswa in all_siswa:
        try:
            list_kelas = [kelas.tahun_pelajaran for kelas in Kelas.objects.select_related('tahun_pelajaran').filter(siswa=siswa)]
            if not tp in list_kelas:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            valid_siswa.append(siswa)

    return valid_siswa

def get_validpelajaran(kelas):
    from sekolah.models import MataPelajaran
    from sekolah.models import Kelas
    valid_pelajaran = []
    all_pelajaran = MataPelajaran.objects.prefetch_related('kelas')
    kelas = Kelas.objects.get(nama=kelas, tahun_pelajaran=active_tp())
    for pelajaran in all_pelajaran:
        try:
            list_kelas = [kelas for kelas in pelajaran.kelas.all()]
            if not kelas in list_kelas:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            valid_pelajaran.append(pelajaran)
            
    return valid_pelajaran

def get_validkelas(siswa):
    try:
        if not siswa.kelas: raise ObjectDoesNotExist
        kelas = siswa.kelas.get(tahun_pelajaran=active_tp())
        return kelas
    except ObjectDoesNotExist:
        return None

def get_validekskul(siswa):
    from siswa.models import NilaiEkskul
    from sekolah.models import Ekskul
    list_ekskul = Ekskul.objects.all()
    valid_ekskul = []
    list_nilai = [ekskul.ekskul.id for ekskul in NilaiEkskul.objects.filter(siswa=siswa, semester=active_semester())]
    for ekskul in list_ekskul:
        if not ekskul.id in list_nilai:
            valid_ekskul.append(ekskul)
    return valid_ekskul


def generate_rapor_context(sekolah, semester, siswa):
    from siswa.models import Absensi
    from helpers.nilai_helpers import zip_eksnilai, zip_nilrapor
        
    if siswa.gender == 'P': jenkel_siswa = 'Pria'
    else: jenkel_siswa = 'Wanita'
    return {
            'siswa': siswa,
            'jenkel_siswa': jenkel_siswa,
            'kelas': get_validkelas(siswa),
            'matapelajaran': zip_nilrapor(siswa, semester),
            'ekskul': zip_eksnilai(siswa, semester),
            'absensi': Absensi.objects.get_or_create(siswa=siswa, semester=semester)[0],
            'sekolah': sekolah,
            'semester': semester,
        }

def generate_pdf(siswa, pdf_dir, context):
    from sekolah.models import Rapor
    html_string = render_to_string('pages/rapor/rapor.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target=f'{pdf_dir}/{siswa.nama}.pdf', stylesheets=['static/css/rapor.css'])
    Rapor.objects.update_or_create(siswa=siswa, semester=context['semester'], defaults={'rapor': f'{pdf_dir}/{siswa.nama}.pdf'})

def get_sekolah():
    from sekolah.models import Sekolah
    try:
        return Sekolah.objects.get_or_create()[0]
    except ObjectDoesNotExist:
        return None
    except OperationalError:
        return None