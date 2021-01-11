from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from guru import views as guru_view
from siswa import views as siswa_view
from sekolah import views as sekolah_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='pages/guru/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='pages/guru/login.html'), name='logout'),
    path('admin/', admin.site.urls),
    path('', guru_view.index),
    # URL for both Walikelas and Staf TU
    path('dashboard/', guru_view.dashboard.as_view(), name='dashboard'),
    path('guru/', include([
        path('', guru_view.list_guru.as_view(), name='list-guru'),
        path('buat/', guru_view.buat_guru.as_view(), name='buat-guru'),
        path('hapus/<guru>/', guru_view.hapus_guru.as_view(), name='hapus-guru'),
        path('profil/', guru_view.profil.as_view(), name='profil'),
        path('profil/<guru>/', guru_view.profil_lain.as_view(), name='profil-guru-lain'),
        path('password/ganti/', guru_view.ganti_password.as_view(), name='ganti-password'),
    ])),
    path('siswa/', include([
        path('', siswa_view.list_siswa.as_view(), name='list-siswa'),
        path('buat/', siswa_view.buat_siswa.as_view(), name='buat-siswa'),
        path('<nis>/', siswa_view.detail_siswa.as_view(), name='detail-siswa'),
        path('<nis>/profil/', siswa_view.profil_siswa.as_view(), name='profil-siswa'),
        path('<nis>/nilai/', siswa_view.nilai_siswa.as_view(), name='nilai-siswa'),
        path('<nis>/absen/', siswa_view.absen_siswa.as_view(), name='absen-siswa'),
        path('<nis>/ekskul/', siswa_view.ekskul_siswa.as_view(), name='ekskul-siswa'),
        path('<nis>/ekskul/tambah/', siswa_view.tambah_ekskul.as_view(), name='tambah-ekskul'),
        path('<nis>/ekskul/hapus/<ekskul>', siswa_view.hapus_ekskul_siswa.as_view(), name='hapus-ekskul-siswa'),
        path('<nis>/rapor/', sekolah_view.rapor_view.as_view(), name='rapor'),
        path('<nis>/hapus/', siswa_view.hapus_siswa.as_view(), name='hapus-siswa'),
    ])),
    path('sekolah/', sekolah_view.detail_sekolah.as_view(), name='detail-sekolah'),
    path('semester/', include([
        path('', sekolah_view.list_semester.as_view(), name='list-semester'),
        path('buat/', sekolah_view.buat_semester.as_view(), name='buat-semester'),
        path('<semester>/aktifkan/', sekolah_view.aktifkan_semester.as_view(), name='aktifkan-semester'),
        path('<semester>/hapus/', sekolah_view.hapus_semester.as_view(), name='hapus-semester')
    ])),
    path('jurusan/', include([
        path('', sekolah_view.list_jurusan.as_view(), name='list-jurusan'),
        path('buat/', sekolah_view.buat_jurusan.as_view(), name='buat-jurusan'),
        # path('<jurusan>/', guru_view.placeholder, name='detail-jurusan'),
        path('<jurusan>/hapus/', sekolah_view.hapus_jurusan.as_view(), name='hapus-jurusan')
    ])),
    path('ekskul/', include([
        path('', sekolah_view.list_ekskul.as_view(), name='list-ekskul'),
        path('buat/', sekolah_view.buat_ekskul.as_view(), name='buat-ekskul'),
        path('<ekskul>/hapus/', sekolah_view.hapus_ekskul.as_view(), name='hapus-ekskul')
    ])),
    path('ekskul/', include([
        path('', sekolah_view.list_ekskul.as_view(), name='list-ekskul'),
        path('buat/', sekolah_view.buat_ekskul.as_view(), name='buat-ekskul'),
        path('<ekskul>/hapus/', sekolah_view.hapus_ekskul.as_view(), name='hapus-ekskul')
    ])),
    path('matapelajaran/', include([
        path('', sekolah_view.list_matapelajaran.as_view(), name='list-matapelajaran'),
        path('buat/', sekolah_view.buat_matapelajaran.as_view(), name='buat-matapelajaran'),
        path('<matapelajaran>/', sekolah_view.detail_matapelajaran.as_view(), name='detail-matapelajaran'),
        path('<matapelajaran>/ubah/matapelajaran/', sekolah_view.ubah_matapelajaran.as_view(), name='ubah-matapelajaran'),
        path('<matapelajaran>/ubah/kkm/', sekolah_view.ubah_kkm.as_view(), name='ubah-kkm'),
        path('<matapelajaran>/hapus/', sekolah_view.hapus_matapelajaran.as_view(), name='hapus-matapelajaran')
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
