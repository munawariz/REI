from sekolah.models import Kelas
from django import forms
from django.forms import fields
from .models import Siswa, Nilai, Absensi, NilaiEkskul
from helpers import active_semester, input_type as type

class KelasSelect(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.tingkat} {obj.jurusan} {obj.kelas}'

class SiswaForm(forms.ModelForm):
    kelas = KelasSelect(queryset=Kelas.objects.filter(semester=active_semester()), required=False)
    class Meta:
        model = Siswa
        fields = '__all__'
        widgets = {
            'tanggal_lahir': type.DateInput(),
            'email': type.EmailInput(),
        }

class NilaiForm(forms.ModelForm):
    class Meta:
        model = Nilai
        fields = ('pengetahuan', 'keterampilan')

class AbsenForm(forms.ModelForm):
    class Meta:
        model = Absensi
        fields = ('izin', 'sakit', 'bolos')

class NilaiEkskulForm(forms.ModelForm):
    class Meta:
        model = NilaiEkskul
        fields = ('ekskul', 'nilai')
