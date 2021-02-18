from django import forms
from django.db.utils import OperationalError
from .models import Ekskul, Jurusan, KKM, Kelas, MataPelajaran, Semester, Sekolah, TahunPelajaran
from helpers.choice import tingkat_choice
from helpers import get_sekolah, get_validwalikelas, walikelas_choice
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
        walikelas = forms.ChoiceField(choices=walikelas_choice(get_validwalikelas()), required=False)
    except Exception:
        pass

    def __init__(self, tingkat_list, walikelas_list, *args, **kwargs):
        super(KelasForm, self).__init__(*args, **kwargs)
        self.fields["tingkat"] = forms.ChoiceField(choices=tingkat_list)
        self.fields["walikelas"] = forms.ChoiceField(choices=walikelas_list, required=False)
    class Meta:
        model = Kelas
        fields = ('tingkat', 'jurusan', 'kelas')

class DisabledKelasForm(forms.ModelForm):
    try:
        tingkat = forms.CharField()
        walikelas = forms.CharField()
        jurusan = forms.CharField()
        kelas = forms.CharField()
    except Exception:
        pass
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