from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django import forms
from django.forms.models import model_to_dict
from django.contrib import messages
from weasyprint import HTML
from django.template.loader import render_to_string
  
def calculate_age(birthDate):
    days_in_year = 365    
    age = int((date.today() - birthDate).days / days_in_year) 
    return age 

def active_semester():    
    try:
        from sekolah.models import Semester
        return Semester.objects.get(is_active=True)        
    except ObjectDoesNotExist:
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
    all_walikelas = Guru.objects.filter(is_walikelas=True, is_superuser=False, is_staftu=False, is_active=True)
    for walikelas in all_walikelas:
        if walikelas.kelas:
            list_kelas = [kelas.semester for kelas in Kelas.objects.filter(walikelas=walikelas)]
            if not active_semester() in list_kelas:
                valid_walikelas.append(walikelas)
        else:
            valid_walikelas.append(walikelas)

    return valid_walikelas

def get_validsiswabaru():
    from siswa.models import Siswa
    from sekolah.models import Kelas
    valid_siswa = []
    all_siswa = Siswa.objects.all()
    for siswa in all_siswa:
        if siswa.kelas:
            list_kelas = [kelas.semester for kelas in Kelas.objects.filter(siswa=siswa)]
            if not active_semester() in list_kelas:
                valid_siswa.append(siswa)
        else:
            valid_siswa.append(siswa)

    return valid_siswa

def get_validpelajaran(kelas):
    from sekolah.models import MataPelajaran
    from sekolah.models import Kelas
    valid_pelajaran = []
    all_pelajaran = MataPelajaran.objects.all()
    kelas = Kelas.objects.get(nama=kelas, semester=active_semester())
    for pelajaran in all_pelajaran:
        if pelajaran.kelas.all():
            list_kelas = [kelas for kelas in pelajaran.kelas.all()]
            if not kelas in list_kelas:
                valid_pelajaran.append(pelajaran)
        else:
            valid_pelajaran.append(pelajaran)
            
    return valid_pelajaran

def realkelas(siswa):
    from sekolah.models import Kelas
    from siswa.models import Siswa
    siswa = Siswa.objects.get(nis=siswa.nis)
    try:
        if siswa.kelas:
            kelas = Kelas.objects.get(nama=siswa.kelas.nama, semester=active_semester())
            anggota_kelas = [siswa for siswa in Siswa.objects.filter(kelas=kelas)]
            if siswa in anggota_kelas:
                return kelas
            else:
                raise ObjectDoesNotExist
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return None

def get_validkelas(siswa):
    from sekolah.models import Kelas
    try:
        if not siswa.kelas: raise ObjectDoesNotExist
        kelas = Kelas.objects.get(nama=siswa.kelas.nama, semester=active_semester())
        if kelas == realkelas(siswa):
            return kelas
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return None

def generate_pdf(siswa, pdf_dir, context):
    from sekolah.models import Rapor
    html_string = render_to_string('pages/rapor/rapor.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target=f'{pdf_dir}/{siswa.nama}.pdf', stylesheets=['static/css/rapor.css'])
    rapor, created = Rapor.objects.update_or_create(siswa=siswa, semester=active_semester(), defaults={'rapor': f'{pdf_dir}/{siswa.nama}.pdf'})