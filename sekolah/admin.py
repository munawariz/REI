from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Sekolah, Semester, Jurusan, MataPelajaran, KKM, Kelas, Ekskul, Rapor, TahunPelajaran
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(Sekolah)
class SekolahAdmin(SingletonModelAdmin):
    readonly_fields = ('tingkat_verbose',)

@admin.register(TahunPelajaran)
class TPAdmin(admin.ModelAdmin):
    list_display = ('mulai', 'akhir', 'is_active')
    search_fields = ('mulai', 'akhir')
    ordering = ('-mulai', '-akhir')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('tahun_pelajaran', 'semester', 'is_active')
    ordering = ('-tahun_pelajaran', '-semester')

@admin.register(Jurusan)
class JurusanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'singkat')
    search_fields = ('nama', 'singkat')
    ordering = ('nama',)

@admin.register(MataPelajaran)
class MataPelajaranAdmin(admin.ModelAdmin):
    list_display = ('nama', 'singkat', 'kelompok')
    search_fields = ('nama', 'singkat', 'kelompok')
    ordering = ('nama', 'kelompok')

@admin.register(KKM)
class KKMAdmin(admin.ModelAdmin):
    list_display = ('matapelajaran', 'tahun_pelajaran', 'pengetahuan', 'keterampilan')
    search_fields = ('matapelajaran', 'tahun_pelajaran', 'pengetahuan', 'keterampilan')
    ordering = ('matapelajaran', 'tahun_pelajaran')

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('nama', 'tingkat', 'jurusan', 'kelas', 'walikelas', 'tahun_pelajaran')
    search_fields = ('tingkat', 'jurusan', 'kelas', 'walikelas', 'tahun_pelajaran')
    ordering = ('tingkat', 'jurusan', 'kelas')

@admin.register(Ekskul)
class EkskulAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jenis')
    search_fields = ('nama', 'jenis')
    ordering = ('nama', 'jenis')
    list_filter = ('jenis',)

@admin.register(Rapor)
class RaporAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'semester')
    list_filter = ('semester',)
    search_fields = ('siswa',)
    ordering = ('-semester', 'siswa')