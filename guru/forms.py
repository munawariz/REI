from django import forms
from django.core.exceptions import ValidationError
from .models import Gelar, Guru
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                _("Akun ini terdaftar tetapi memiliki status nonaktif, silahkan minta admin untuk mengaktifkan akun anda"),
                code='inactive',
            )

    error_messages = {
        'invalid_login': _(
            "Nomor Induk atau Password salah silahkan coba lagi"
        ),
        'inactive': _("Akun ini nonaktif, silahkan minta admin untuk mengaktifkan akun anda"),
    }


class GuruCreateForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'type':'password'}))
    class Meta:
        model = Guru
        fields = ('nip', 'password', 'nama', 'email', 'gender', 'tempat_lahir', 'tanggal_lahir', 'agama', 'alamat', 'is_walikelas', 'is_staftu')
        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        if 'nip' in self.cleaned_data:
            if self.cleaned_data['nip'] in Guru.objects.all().values('nip'):
                raise forms.ValidationError('Guru dengan NIP itu sudah terdaftar')

class GuruEditForm(forms.ModelForm):
    tanggal_lahir = forms.DateField()
    class Meta:
        model = Guru
        fields = ('avatar', 'nama', 'email', 'gender', 'tempat_lahir', 'tanggal_lahir', 'agama', 'alamat')
        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date'})
        }


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Password Lama Anda', max_length = 20, widget=forms.TextInput(attrs={'type':'password'}))
    new_password1 = forms.CharField(label='Password Baru', max_length = 20, widget=forms.TextInput(attrs={'type':'password'}))
    new_password2 = forms.CharField(label='Konfirmasi Password Baru', max_length = 20, widget=forms.TextInput(attrs={'type':'password'}))

    def clean(self):
        if 'new_password1' in self.cleaned_data and 'new_password2' in self.cleaned_data:
            if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
                raise forms.ValidationError("Pastikan Password baru dan Konfirmasi Password baru sama")
        return self.cleaned_data

class GelarForm(forms.ModelForm):
    class Meta:
        model = Gelar
        fields = ('tingkat_gelar', 'jurusan', 'universitas')