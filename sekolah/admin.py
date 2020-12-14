from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Sekolah, TanggalPendidikan, Jurusan

admin.site.register(Sekolah, SingletonModelAdmin)

@admin.register(TanggalPendidikan)
class TPAdmin(admin.ModelAdmin):
    list_display = ('tahun_mulai', 'tahun_akhir', 'semester', 'is_active')
    search_fields = ('tahun_mulai', 'tahun_akhir')
    ordering=('tahun_mulai', 'tahun_akhir', 'semester')

@admin.register(Jurusan)
class JurusanAdmin(admin.ModelAdmin):
    list_display = ('lengkap', 'singkat')
    search_fields = ('lengkap', 'singkat')
    ordering=('lengkap',)