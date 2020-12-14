from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Sekolah, TanggalPendidikan, Jurusan, MataPelajaran

admin.site.register(Sekolah, SingletonModelAdmin)

@admin.register(TanggalPendidikan)
class TPAdmin(admin.ModelAdmin):
    list_display = ('tahun_mulai', 'tahun_akhir', 'semester', 'is_active')
    search_fields = ('tahun_mulai', 'tahun_akhir')
    ordering=('tahun_mulai', 'tahun_akhir', 'semester')

@admin.register(Jurusan)
class JurusanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'singkat')
    search_fields = ('nama', 'singkat')
    ordering=('nama',)

@admin.register(MataPelajaran)
class MataPelajaranAdmin(admin.ModelAdmin):
    list_display = ('nama', 'singkat', 'kelompok')
    search_fields = ('nama', 'singkat', 'kelompok')
    ordering=('nama', 'kelompok')