# Generated by Django 3.0.5 on 2021-03-12 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sekolah', '0013_auto_20210309_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sekolah',
            name='alamat',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='kecamatan',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='kelurahan',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='kepsek',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='is_kepsek', to=settings.AUTH_USER_MODEL, verbose_name='Kepala Sekolah'),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='kode_pos',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='kota',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Kota/Kabupaten'),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='nama',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='no_telepon',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Nomor Telepon'),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='npsn',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='provinsi',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='tingkat',
            field=models.CharField(blank=True, choices=[('SD', 'Sekolah Dasar'), ('SMP', 'Sekolah Menengah Pertama'), ('SMA', 'Sekolah Menengah Atas'), ('SMK', 'Sekolah Menengah Kejuruan')], max_length=3, null=True, verbose_name='Tingkat Sekolah'),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='website',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
