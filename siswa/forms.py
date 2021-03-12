from sekolah.models import Kelas
from django import forms
from django_select2 import forms as s2forms
from .models import Siswa, Nilai, Absensi, NilaiEkskul
from helpers import active_tp, input_type as type, get_sekolah
from helpers.choice import tingkat_choice

class KelasSelect(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.tingkat} {obj.jurusan} {obj.kelas}'

class SiswaForm(forms.ModelForm):
    kelas = KelasSelect(queryset=Kelas.objects.filter(tahun_pelajaran=active_tp()), required=False)
    try:
        diterima_di_tingkat = forms.ChoiceField(choices = tingkat_choice(get_sekolah()))
    except Exception as e:
        print(e)
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

class MultiEkskul(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "nama__icontains",
    ]
class TambahEkskulSiswaForm(forms.ModelForm):
    def __init__(self, ekskul_list, *args, **kwargs):
        super(TambahEkskulSiswaForm, self).__init__(*args, **kwargs)
        self.fields["ekskul"] = forms.MultipleChoiceField(choices=ekskul_list)
    class Meta:
        model = NilaiEkskul
        fields = ('ekskul',)
        widgets = {
            'ekskul': MultiEkskul
        }

class UploadExcelForm(forms.Form):
    file = forms.FileField()
