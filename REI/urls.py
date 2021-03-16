from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from guru import views as guru_view
from siswa import views as siswa_view
from sekolah import views as sekolah_view
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500
import debug_toolbar
from . import views as rei_views

urlpatterns = [
    path('login/', guru_view.CustomLoginView.as_view(template_name='pages/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='pages/auth/login.html'), name='logout'),
    path('admin/', admin.site.urls),
    path('about-dev/', rei_views.about_dev, name='about-dev'),
    path('', sekolah_view.index),
    path('first-login/', guru_view.first_login.as_view(), name='first-login'),
    path('dashboard/', sekolah_view.dashboard.as_view(), name='dashboard'),
    path('guru/', include([
        path('', guru_view.list_guru.as_view(), name='list-guru'),
        path('buat/', guru_view.buat_guru.as_view(), name='buat-guru'),
        path('hapus/<guru>/', guru_view.hapus_guru.as_view(), name='hapus-guru'),
        path('profil/<guru>/', guru_view.profil_lain.as_view(), name='detail-guru'),
        path('ubah/<guru>/', guru_view.ubah_profil_guru.as_view(), name='ubah-profil-guru'),
        path('password/ganti/', guru_view.ganti_password.as_view(), name='ganti-password'),
        path('gelar/tambah/<guru>/', guru_view.tambah_gelar.as_view(), name='tambah-gelar'),
        path('gelar/hapus/<guru>/<gelar>/', guru_view.hapus_gelar.as_view(), name='hapus-gelar')
    ])),
    path('siswa/', include([
        path('', siswa_view.list_siswa.as_view(), name='list-siswa'),
        path('buat/', siswa_view.buat_siswa.as_view(), name='buat-siswa'),
        path('download-template-excel/', siswa_view.download_template_siswa.as_view(), name='download-template-siswa'),
        path('import-from-excel/', siswa_view.import_excel_siswa.as_view(), name='import-excel-siswa'),
        path('export-to-excel/', siswa_view.export_excel_siswa.as_view(), name='export-excel-siswa'),
        path('<nis>/', siswa_view.detail_siswa.as_view(), name='detail-siswa'),
        path('<nis>/profil/', siswa_view.detail_siswa.as_view(), name='profil-siswa'),
        path('<nis>/nilai/', siswa_view.nilai_siswa.as_view(), name='nilai-siswa'),
        path('<nis>/absen/', siswa_view.absen_siswa.as_view(), name='absen-siswa'),
        path('<nis>/ekskul/', siswa_view.ekskul_siswa.as_view(), name='ekskul-siswa'),
        path('<nis>/ekskul/tambah/', siswa_view.tambah_ekskul.as_view(), name='tambah-ekskul'),
        path('<nis>/ekskul/hapus/<ekskul>', siswa_view.hapus_ekskul_siswa.as_view(), name='hapus-ekskul-siswa'),        
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
    path('matapelajaran/', include([
        path('', sekolah_view.list_matapelajaran.as_view(), name='list-matapelajaran'),
        path('buat/', sekolah_view.buat_matapelajaran.as_view(), name='buat-matapelajaran'),
        path('<matapelajaran>/', sekolah_view.detail_matapelajaran.as_view(), name='detail-matapelajaran'),
        path('<matapelajaran>/hapus/', sekolah_view.hapus_matapelajaran.as_view(), name='hapus-matapelajaran')
    ])),
    path('kelas/', include([
        path('', sekolah_view.list_kelas.as_view(), name='list-kelas'),
        path('buat/', sekolah_view.buat_kelas.as_view(), name='buat-kelas'),
        path('<kelas>/', sekolah_view.detail_kelas.as_view(), name='detail-kelas'),
        path('<kelas>/walikelas/ganti/', sekolah_view.ganti_walikelas.as_view(), name='ganti-walikelas'),
        path('<kelas>/anggota/tambah/', sekolah_view.tambah_anggota.as_view(), name='tambah-anggota'),
        path('<kelas>/anggota/hapus/<siswa>/', sekolah_view.hapus_anggota.as_view(), name='hapus-anggota'),
        path('<kelas>/pelajaran/tambah/', sekolah_view.tambah_pelajaran.as_view(), name='tambah-pelajaran'),
        path('<kelas>/pelajaran/hapus/<pelajaran>/', sekolah_view.hapus_pelajaran.as_view(), name='hapus-pelajaran'),
        path('<kelas>/hapus/', sekolah_view.hapus_kelas.as_view(), name='hapus-kelas'),
    ])),
    path('rapor/', include([
        path('bundle/<kelas>/', sekolah_view.bundle_rapor_view.as_view(), name='rapor-bundle'),
        path('<nis>/<action>/', sekolah_view.rapor_view.as_view(), name='rapor'),
    ])),
    path('debug/', include(debug_toolbar.urls)),
    path('select2/', include('django_select2.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'REI.views.error_404'
handler500 = 'REI.views.error_500'