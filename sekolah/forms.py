from django import forms
from .models import Semester, Sekolah

class SekolahForm(forms.ModelForm):
    class Meta:
        model = Sekolah
        fields = '__all__'

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ('tahun_mulai', 'tahun_akhir', 'semester')
