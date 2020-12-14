from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Sekolah

admin.site.register(Sekolah, SingletonModelAdmin)
