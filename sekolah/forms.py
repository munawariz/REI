from helpers import active_semester, get_sekolah
from helpers.choice import tingkat_choice
from django import forms
from .models import Ekskul, Jurusan, KKM, Kelas, MataPelajaran, Semester, Sekolah
class SekolahForm(forms.ModelForm):
    class Meta:
        model = Sekolah
        fields = '__all__'

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ('tahun_mulai', 'tahun_akhir', 'semester')

class KelasForm(forms.ModelForm):
    tingkat = forms.ChoiceField(choices=tingkat_choice(get_sekolah()))
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