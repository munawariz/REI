from django.contrib import admin
from .models import Gelar, Guru
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Guru)
class UserAdmin(BaseUserAdmin): 
    list_display = ('nip', 'nama', 'nama_gelar', 'email', 'is_walikelas', 'is_staftu', 'gender', 'is_active')
    list_filter = ('is_walikelas', 'is_staftu', 'gender', 'is_active')
    fieldsets = (
        ('Account Profile', {'fields': ('nip', 'nama', 'email', 'gender', 'password', 'tempat_lahir', 'tanggal_lahir', 'agama', 'alamat', 'is_walikelas', 'is_staftu')}),
        ('Account Status', {'fields': ('is_active',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nip', 'nama', 'email', 'gender', 'tempat_lahir', 'tanggal_lahir', 'agama', 'alamat', 'password1', 'password2', 'is_walikelas', 'is_staftu'),
        }),
    )
    search_fields = ('nip', 'nama', 'email')
    ordering = ('is_walikelas', 'is_staftu', 'gender')
    filter_horizontal = ()

@admin.register(Gelar)
class GelarAdmin(admin.ModelAdmin):
    readonly_fields = ('verbose_tingkat', 'verbose_jurusan', 'gelar')
