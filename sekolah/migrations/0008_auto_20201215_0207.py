# Generated by Django 3.1.4 on 2020-12-14 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sekolah', '0007_auto_20201215_0201'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tingkat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tingkat', models.SmallIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='kelas',
            name='tingkat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sekolah.tingkat'),
        ),
    ]
