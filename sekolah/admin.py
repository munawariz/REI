from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Sekolah, TanggalPendidikan

admin.site.register(Sekolah, SingletonModelAdmin)

@admin.register(TanggalPendidikan)
class TPAdmin(admin.ModelAdmin):
    list_display = ('tahun_mulai', 'tahun_akhir', 'semester', 'is_active')
    search_fields = ('tahun_mulai', 'tahun_akhir')
    ordering=('tahun_mulai', 'tahun_akhir', 'semester')