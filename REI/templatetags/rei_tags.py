from siswa.models import NilaiEkskul, Siswa
from django.forms.widgets import ClearableFileInput
from guru.models import Gelar
from sekolah.models import KKM, Kelas, MataPelajaran, Semester
from helpers import active_semester, active_tp
from django import template
import os
from django.core.exceptions import ObjectDoesNotExist
from django.forms import CheckboxInput, FileInput
register = template.Library()

@register.simple_tag(takes_context=True)
def active_kelas(context):
    if context['user'].is_walikelas:
        try:
            from guru.models import Guru
            from sekolah.models import Kelas
            guru = Guru.objects.get(nip=context['user'].nip)
            kelas = Kelas.objects.get(walikelas=guru, tahun_pelajaran=active_tp())
            return kelas
        except ObjectDoesNotExist:
            return None
    else:
        return None

@register.simple_tag
def semester_is_active():
    return active_semester()

@register.simple_tag(takes_context=False)
def semester_from_tp(tp):
    semester = Semester.objects.filter(tahun_pelajaran=tp).order_by('semester')
    return semester

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

@register.simple_tag(takes_context=False)
def get_gelar(guru, **kwargs):
    gelar = Gelar.objects.filter(guru=guru)
    order = ['Diploma 1', 'Diploma 2', 'Diploma 3', 'Diploma 4', 'Sarjana', 'Magister', 'Doktor']
    gelar = sorted(gelar, key=lambda x: order.index(x.verbose_tingkat))
    return gelar

@register.simple_tag(takes_context=False)
def get_basename(subjek):
    try:
        return os.path.basename(subjek.avatar.path)
    except:
        return os.path.basename(str(subjek))

@register.filter(takes_context=False, name='is_checkbox')
def is_checkbox(field):
  return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__

@register.filter(takes_context=False, name='is_file')
def is_file(field):
  return field.field.widget.__class__.__name__ == ClearableFileInput().__class__.__name__

@register.simple_tag(takes_context=False)
def count_member(kelas, gender=None):
    if gender:
        if gender == 'male':
            siswa = Siswa.objects.filter(kelas=kelas, kelas__tahun_pelajaran=active_tp(), gender='P')
        elif gender == 'female':
            siswa = Siswa.objects.filter(kelas=kelas, kelas__tahun_pelajaran=active_tp(), gender='W')
    else:
        siswa = Siswa.objects.filter(kelas=kelas, kelas__tahun_pelajaran=active_tp())
    return siswa.count()

@register.simple_tag(takes_context=False)
def count_mapel(kelas):
    return MataPelajaran.objects.filter(kelas=kelas, kelas__tahun_pelajaran=active_tp()).count()

@register.simple_tag(takes_context=False)
def get_active_kelas(siswa):
    try:
        return siswa.kelas.get(tahun_pelajaran=active_tp()).nama
    except ObjectDoesNotExist:
        return None

@register.simple_tag(takes_context=False)
def get_total_kelas(jurusan):
    try:
        return Kelas.objects.filter(jurusan=jurusan, tahun_pelajaran=active_tp()).count()
    except ObjectDoesNotExist:
        return 0

@register.simple_tag(takes_context=False)
def get_total_siswa_jurusan(jurusan):
    try:
        total = 0
        kelas = Kelas.objects.filter(jurusan=jurusan, tahun_pelajaran=active_tp())
        for kelas in kelas:
            total += kelas.siswa.count()
        return total
    except:
        return 0

@register.simple_tag(takes_context=False)
def get_total_siswa_ekskul(ekskul):
    try:
        return NilaiEkskul.objects.filter(ekskul=ekskul, semester=active_semester()).count()
    except ObjectDoesNotExist:
        return 0