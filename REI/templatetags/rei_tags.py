from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def active_kelas(context):
    if context['user'].is_walikelas:
        from guru.models import Guru
        from sekolah.models import Kelas
        from helpers import active_semester
        guru = Guru.objects.get(nip=context['user'].nip)
        kelas = Kelas.objects.get(walikelas=guru, semester=active_semester())
        return kelas
    else:
        return None