from django.contrib import admin
from .models import NilaiEkskul, Siswa, Nilai, Absensi

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

@admin.register(Absensi)
class AbsensiAdmin(admin.ModelAdmin):
    list_display = ('semester', 'siswa', 'izin', 'sakit', 'bolos')
    search_fields = ('semester', 'siswa', 'izin', 'sakit', 'bolos')
    ordering = ('semester', 'siswa', 'izin', 'sakit', 'bolos')

@admin.register(NilaiEkskul)
class NilaiEkskulAdmin(admin.ModelAdmin):
    list_display = ('semester', 'siswa', 'ekskul')
    search_fields = ('semester', 'siswa', 'ekskul')
    ordering = ('semester', 'siswa', 'ekskul', 'nilai')