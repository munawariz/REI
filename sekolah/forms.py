from django import forms
from .models import Ekskul, Jurusan, Kelas, Semester, Sekolah

class SekolahForm(forms.ModelForm):
    class Meta:
        model = Sekolah
        fields = '__all__'

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ('tahun_mulai', 'tahun_akhir', 'semester')

class KelasForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = ('tingkat', 'jurusan', 'kelas')

class JurusanForm(forms.ModelForm):
    class Meta:
        model = Jurusan
        fields = '__all__'

class EkskulForm(forms.ModelForm):
    class Meta:
        model = Ekskul
        fields = '__all__'