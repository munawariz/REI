# Generated by Django 3.1.4 on 2020-12-15 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siswa', '0003_auto_20201216_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siswa',
            name='alamat',
            field=models.CharField(max_length=255),
        ),
    ]