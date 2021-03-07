from sekolah.models import Semester
from helpers import active_semester, active_tp
from django import template
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.simple_tag(takes_context=True)
def active_kelas(context):
    if context['user'].is_walikelas:
        try:
            from guru.models import Guru
            from sekolah.models import Kelas
            from helpers import active_semester
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