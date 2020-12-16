from django.http import request
from django.shortcuts import redirect, render
from django.views.generic import View
from .models import Guru
from .forms import GuruEditForm, PasswordChangeForm
from django.contrib.auth import authenticate

def placeholder(request):
    return render(request, 'index.html')

class dashboard(View):
    def get(self, request):
        return render(request, 'pages/dashboard.html')

class edit_profil(View):
    def get(self, request):
        active_guru = Guru.objects.get(pk=request.user.pk)        
        initial = {
            'nama' : active_guru.nama,
            'gender' : active_guru.gender,
            'tempat_lahir' : active_guru.tempat_lahir, 
            'tanggal_lahir' : active_guru.tanggal_lahir, 
            'agama' : active_guru.agama,
            'alamat' : active_guru.alamat,
            'email' : active_guru.email,
        }

        context = {
            'profile_form': GuruEditForm(initial=initial),
            'password_form': PasswordChangeForm()
        }
        return render(request, 'pages/edit-profil.html', context)

    def post(self, request):
        active_guru = Guru.objects.get(pk=request.user.pk) 
        initial = {
            'nama' : active_guru.nama,
            'gender' : active_guru.gender,
            'tempat_lahir' : active_guru.tempat_lahir, 
            'tanggal_lahir' : active_guru.tanggal_lahir, 
            'agama' : active_guru.agama,
            'alamat' : active_guru.alamat,
            'email' : active_guru.email,
        }
        profile_form = GuruEditForm(request.POST, initial=initial)
        password_form = PasswordChangeForm(request.POST)
        context = {
            'profile_form': profile_form,
            'password_form': password_form,
        }
        
        if profile_form.is_valid() or password_form.is_valid():
            if profile_form.is_valid():
                guru = Guru.objects.get(pk=request.user.pk)
                guru.nama = profile_form.cleaned_data['nama']
                guru.email = profile_form.cleaned_data['email']
                guru.gender = profile_form.cleaned_data['gender']
                guru.tempat_lahir = profile_form.cleaned_data['tempat_lahir']
                guru.tanggal_lahir = profile_form.cleaned_data['tanggal_lahir']
                guru.agama = profile_form.cleaned_data['agama']
                guru.alamat = profile_form.cleaned_data['alamat']
                guru.save()

                return redirect('dashboard')

            if password_form.is_valid():
                newpassword=password_form.cleaned_data['new_password1']
                nip=request.user.nip
                password=password_form.cleaned_data['old_password']

                user = authenticate(nip=nip, password=password)
                if user is not None:
                    user.set_password(newpassword)
                    user.save()
                    return redirect('dashboard')

                else:
                    return render(request, 'pages/edit-profil.html', context)
        else:            
            return render(request, 'pages/edit-profil.html', context)
            
