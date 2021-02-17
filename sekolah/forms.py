from django import forms
from django.db.utils import OperationalError
from .models import Ekskul, Jurusan, KKM, Kelas, MataPelajaran, Semester, Sekolah, TahunPelajaran
from helpers.choice import tingkat_choice
from helpers import get_sekolah
class SekolahForm(forms.ModelForm):
    class Meta:
        model = Sekolah
        exclude = ('tingkat_verbose',)

class SemesterForm(forms.ModelForm):
    class Meta:
        model = TahunPelajaran
        fields = ('mulai', 'akhir')

class KelasForm(forms.ModelForm):
    try:
        tingkat = forms.ChoiceField(choices=tingkat_choice(get_sekolah()))
    except Exception as e:
        print(e)
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

class MatapelajaranForm(forms.ModelForm):
    class Meta:
        model = MataPelajaran
        fields = '__all__'

class KKMForm(forms.ModelForm):
    class Meta:
        model = KKM
        fields = ('pengetahuan', 'keterampilan')