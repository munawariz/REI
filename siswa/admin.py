from django.contrib import admin
from .models import Siswa

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nisn', 'nis', 'gender', 'kelas')
    search_fields = ('nama', 'nisn', 'nis', 'gender', 'kelas')
    ordering = ('kelas', 'nama', 'gender')