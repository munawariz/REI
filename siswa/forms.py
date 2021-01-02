from django import forms
from django.forms import fields
from .models import Siswa, Nilai, Absensi, NilaiEkskul
from helpers import input_type as type

class SiswaForm(forms.ModelForm):    
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
