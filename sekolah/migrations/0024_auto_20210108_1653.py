# Generated by Django 3.1.4 on 2021-01-08 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siswa', '0013_auto_20210108_1653'),
        ('sekolah', '0023_auto_20210108_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kelas',
            name='tingkat',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='matapelajaran',
            name='singkat',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Nama Singkat Mata Pelajaran'),
        ),
        migrations.DeleteModel(
            name='Tingkat',
        ),
    ]