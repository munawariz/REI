from django import forms
from .models import Semester

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ('tahun_mulai', 'tahun_akhir', 'semester')
