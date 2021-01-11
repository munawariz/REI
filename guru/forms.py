from django import forms
from .models import Guru
from helpers import input_type as type

class GuruCreateForm(forms.ModelForm):
    password = forms.CharField(max_length=18)
    class Meta:
        model = Guru
        fields = ('nip', 'password', 'nama', 'email', 'gender', 'tempat_lahir', 'tanggal_lahir', 'agama', 'alamat')
        widgets = {
            'tanggal_lahir': type.DateInput(),
            'email': type.EmailInput(),
            'password': type.PasswordInput(),
        }

class GuruEditForm(forms.ModelForm):    
    class Meta:
        model = Guru
        fields = ('nama', 'email', 'gender', 'tempat_lahir', 'tanggal_lahir', 'agama', 'alamat')
        widgets = {
            'tanggal_lahir': type.DateInput(),
            'email': type.EmailInput(),
        }

    def clean_password(self):
        return self.initial["password"]

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Password Lama Anda', max_length = 20, widget=forms.TextInput(attrs={'type':'password'}))
    new_password1 = forms.CharField(label='Password Baru', max_length = 20, widget=forms.TextInput(attrs={'type':'password'}))
    new_password2 = forms.CharField(label='Konfirmasi Password Baru', max_length = 20, widget=forms.TextInput(attrs={'type':'password'}))

    def clean(self):
        if 'new_password1' in self.cleaned_data and 'new_password2' in self.cleaned_data:
            if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
                raise forms.ValidationError("Pastikan Password baru dan Konfirmasi Password baru sama")
        return self.cleaned_data