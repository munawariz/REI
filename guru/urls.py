from os import name
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # URL for both Walikelas and Staf TU
    path('dashboard/', views.dashboard.as_view(), name='dashboard'),
    path('profil/', views.profil.as_view(), name='profil'),
    path('siswa/', include([
        path('', views.list_siswa.as_view(), name='list-siswa'),
        path('<nis>/', views.placeholder, name='detail-siswa'),
    ])),
    

    #URL for Walikelas    
    path('insert-nilai/', views.placeholder, name='insert-nilai'),
    path('insert-absensi/', views.placeholder, name='insert-absensi'),
    path('insert-ekskul/', views.placeholder, name='insert-ekskul'),    
    path('export-rapor/', views.placeholder, name='export-rapor'),
    
    #URL for Staf TU
    path('create-siswa/', views.placeholder, name='create-siswa'),
    path('edit-siswa/<nis>/', views.placeholder, name='edit-siswa'),
    path('delete-siswa/<nis>/', views.placeholder, name='delete-siswa'),
    path('create-guru/', views.placeholder, name='create-guru'),
    path('edit-guru/<nip>/', views.placeholder, name='edit-guru'),
    path('delete-guru/<nip>/', views.placeholder, name='delete-guru'),
    path('create-matapelajaran/', views.placeholder, name='create-matapelajaran'),
    path('edit-matapelajaran/<id>', views.placeholder, name='edit-matapelajaran'),
    path('delete-matapelajaran/<id>', views.placeholder, name='delete-matapelajaran'),
    path('create-kelas/', views.placeholder, name='create-kelas'),
    path('edit-kelas/<id>', views.placeholder, name='edit-kelas'),
    path('delete-kelas/<id>', views.placeholder, name='delete-kelas'),
    path('create-jurusan/', views.placeholder, name='create-jurusan'),
    path('edit-jurusan/<id>', views.placeholder, name='edit-jurusan'),
    path('delete-jurusan/<id>', views.placeholder, name='delete-jurusan'),
    path('create-ekskul/', views.placeholder, name='create-ekskul'),
    path('edit-ekskul/<id>', views.placeholder, name='edit-ekskul'),
    path('delete-ekskul/<id>', views.placeholder, name='delete-ekskul'),
    path('create-ekskul/', views.placeholder, name='create-ekskul'),
    path('edit-ekskul/<id>', views.placeholder, name='edit-ekskul'),
    path('delete-ekskul/<id>', views.placeholder, name='delete-ekskul'),
    path('set-walikelas/', views.placeholder, name='set-walikelas'),
    path('set-semester/', views.placeholder, name='set-semester'),
    path('insert-informasi-sekolah/', views.placeholder, name='insert-informasi-sekolah'),
    path('dump-excel', views.placeholder, name='dump-excel'),
]