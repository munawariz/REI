from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Sekolah, Semester, Jurusan, MataPelajaran, KKM, Tingkat, Kelas

admin.site.register(Sekolah, SingletonModelAdmin)

@admin.register(Semester)
class TPAdmin(admin.ModelAdmin):
    list_display = ('tahun_mulai', 'tahun_akhir', 'semester', 'is_active')
    search_fields = ('tahun_mulai', 'tahun_akhir')
    ordering = ('tahun_mulai', 'tahun_akhir', 'semester')

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
    list_display = ('matapelajaran', 'semester', 'pengetahuan', 'keterampilan')
    search_fields = ('matapelajaran', 'semester', 'pengetahuan', 'keterampilan')
    ordering = ('matapelajaran', 'semester')

@admin.register(Tingkat)
class TingkatAdmin(admin.ModelAdmin):
    list_display = ('tingkat',)    
    ordering = ('tingkat',)

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('tingkat', 'jurusan', 'kelas', 'walikelas', 'semester')
    search_fields = ('tingkat', 'jurusan', 'kelas', 'walikelas', 'semester')
    ordering = ('tingkat', 'jurusan', 'kelas')