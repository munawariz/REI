from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from guru import views as guru_view
from siswa import views as siswa_view
from sekolah import views as sekolah_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', guru_view.index),
    # URL for both Walikelas and Staf TU
    path('dashboard/', guru_view.dashboard.as_view(), name='dashboard'),
    path('profil/', guru_view.profil.as_view(), name='profil'),
    path('profil/password/ganti/', guru_view.ganti_password.as_view(), name='ganti-password'),
    path('siswa/', include([
        path('', siswa_view.list_siswa.as_view(), name='list-siswa'),
        path('<nis>/', siswa_view.detail_siswa.as_view(), name='detail-siswa'),
        path('<nis>/profil/', siswa_view.profil_siswa.as_view(), name='profil-siswa'),
        path('<nis>/nilai/', siswa_view.nilai_siswa.as_view(), name='nilai-siswa'),
        path('<nis>/absen/', siswa_view.absen_siswa.as_view(), name='absen-siswa'),
        path('<nis>/ekskul/', siswa_view.ekskul_siswa.as_view(), name='ekskul-siswa'),
        path('<nis>/ekskul/tambah/', siswa_view.tambah_ekskul.as_view(), name='tambah-ekskul'),
        path('<nis>/ekskul/hapus/<ekskul>', siswa_view.hapus_ekskul_siswa.as_view(), name='hapus-ekskul-siswa'),
    ])),
    path('sekolah/', sekolah_view.detail_sekolah.as_view(), name='detail-sekolah'),
    path('semester/', include([
        path('', sekolah_view.list_semester.as_view(), name='list-semester'),
        path('buat/', sekolah_view.buat_semester.as_view(), name='buat-semester'),
        path('<semester>/aktifkan/', sekolah_view.aktifkan_semester.as_view(), name='aktifkan-semester'),
        path('<semester>/hapus/', sekolah_view.hapus_semester.as_view(), name='hapus-semester')
    ])),
    path('kelas/', include([
        path('', sekolah_view.list_kelas.as_view(), name='list-kelas'),
        path('buat/', sekolah_view.buat_kelas.as_view(), name='buat-kelas'),
        path('<kelas>/', sekolah_view.detail_kelas.as_view(), name='detail-kelas'),
        path('<kelas>/walikelas/', sekolah_view.walikelas_kelas.as_view(), name='walikelas-kelas'),
        path('<kelas>/walikelas/ganti/', sekolah_view.ganti_walikelas.as_view(), name='ganti-walikelas'),
        path('<kelas>/anggota/', sekolah_view.anggota_kelas.as_view(), name='anggota-kelas'),
        path('<kelas>/anggota/tambah/<siswa>/', sekolah_view.tambah_anggota.as_view(), name='tambah-anggota'),
        path('<kelas>/anggota/hapus/<siswa>/', sekolah_view.hapus_anggota.as_view(), name='hapus-anggota'),
        path('<kelas>/pelajaran/', sekolah_view.pelajaran_kelas.as_view(), name='pelajaran-kelas'),
        path('<kelas>/pelajaran/tambah/<pelajaran>/', sekolah_view.tambah_pelajaran.as_view(), name='tambah-pelajaran'),
        path('<kelas>/pelajaran/hapus/<pelajaran>/', sekolah_view.hapus_pelajaran.as_view(), name='hapus-pelajaran'),
        path('<kelas>/hapus/', sekolah_view.hapus_kelas.as_view(), name='hapus-kelas'),
    ])),
    path('guru/', include([
        path('<nip>/', guru_view.placeholder),
    ])),
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
    path('insert-informasi-sekolah/', guru_view.placeholder, name='insert-informasi-sekolah'),
    path('dump-excel', guru_view.placeholder, name='dump-excel'),
    path('', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
