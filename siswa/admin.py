from django.contrib import admin
from .models import Siswa, Nilai

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nisn', 'nis', 'gender', 'kelas')
    search_fields = ('nama', 'nisn', 'nis', 'gender', 'kelas')
    ordering = ('kelas', 'nama', 'gender')

@admin.register(Nilai)
class NilaiAdmin(admin.ModelAdmin):
    list_display = ('semester', 'siswa', 'matapelajaran', 'pengetahuan', 'keterampilan')
    search_fields = ('semester', 'siswa', 'matapelajaran', 'pengetahuan', 'keterampilan')
    ordering = ('semester', 'siswa', 'matapelajaran')