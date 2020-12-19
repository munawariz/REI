from django import forms
from django.forms import fields
from .models import Siswa, Nilai
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