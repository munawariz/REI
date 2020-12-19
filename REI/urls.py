from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from guru import views as guru_view
from siswa import views as siswa_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # URL for both Walikelas and Staf TU
    path('dashboard/', guru_view.dashboard.as_view(), name='dashboard'),
    path('profil/', guru_view.profil.as_view(), name='profil'),
    path('siswa/', include([
        path('', siswa_view.list_siswa.as_view(), name='list-siswa'),
        path('<nis>/', siswa_view.detail_siswa.as_view(), name='detail-siswa'),
    ])),
    

    #URL for Walikelas    
    path('insert-nilai/', guru_view.placeholder, name='insert-nilai'),
    path('insert-absensi/', guru_view.placeholder, name='insert-absensi'),
    path('insert-ekskul/', guru_view.placeholder, name='insert-ekskul'),    
    path('export-rapor/', guru_view.placeholder, name='export-rapor'),
    
    #URL for Staf TU
    path('create-siswa/', guru_view.placeholder, name='create-siswa'),
    path('edit-siswa/<nis>/', guru_view.placeholder, name='edit-siswa'),
    path('delete-siswa/<nis>/', guru_view.placeholder, name='delete-siswa'),
    path('create-guru/', guru_view.placeholder, name='create-guru'),
    path('edit-guru/<nip>/', guru_view.placeholder, name='edit-guru'),
    path('delete-guru/<nip>/', guru_view.placeholder, name='delete-guru'),
    path('create-matapelajaran/', guru_view.placeholder, name='create-matapelajaran'),
    path('edit-matapelajaran/<id>', guru_view.placeholder, name='edit-matapelajaran'),
    path('delete-matapelajaran/<id>', guru_view.placeholder, name='delete-matapelajaran'),
    path('create-kelas/', guru_view.placeholder, name='create-kelas'),
    path('edit-kelas/<id>', guru_view.placeholder, name='edit-kelas'),
    path('delete-kelas/<id>', guru_view.placeholder, name='delete-kelas'),
    path('create-jurusan/', guru_view.placeholder, name='create-jurusan'),
    path('edit-jurusan/<id>', guru_view.placeholder, name='edit-jurusan'),
    path('delete-jurusan/<id>', guru_view.placeholder, name='delete-jurusan'),
    path('create-ekskul/', guru_view.placeholder, name='create-ekskul'),
    path('edit-ekskul/<id>', guru_view.placeholder, name='edit-ekskul'),
    path('delete-ekskul/<id>', guru_view.placeholder, name='delete-ekskul'),
    path('create-ekskul/', guru_view.placeholder, name='create-ekskul'),
    path('edit-ekskul/<id>', guru_view.placeholder, name='edit-ekskul'),
    path('delete-ekskul/<id>', guru_view.placeholder, name='delete-ekskul'),
    path('set-walikelas/', guru_view.placeholder, name='set-walikelas'),
    path('set-semester/', guru_view.placeholder, name='set-semester'),
    path('insert-informasi-sekolah/', guru_view.placeholder, name='insert-informasi-sekolah'),
    path('dump-excel', guru_view.placeholder, name='dump-excel'),
    path('', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
