# Generated by Django 3.1.4 on 2020-12-15 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sekolah', '0013_remove_kelas_angkatan'),
        ('siswa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nilai',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pengetahuan', models.SmallIntegerField()),
                ('keterampilan', models.SmallIntegerField()),
                ('matapelajaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sekolah.matapelajaran')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sekolah.semester')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siswa.siswa')),
            ],
        ),
    ]
