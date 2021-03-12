# Generated by Django 3.0.5 on 2021-03-12 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sekolah', '0014_auto_20210312_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sekolah',
            name='kepsek',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='is_kepsek', to=settings.AUTH_USER_MODEL, verbose_name='Kepala Sekolah'),
        ),
    ]
