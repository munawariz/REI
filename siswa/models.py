from helpers.choice import GENDER_CHOICE
from django.db import models
from django.db.models.fields import CharField
from sekolah.models import Kelas, Tingkat

class Siswa(models.Model):
    nama = models.CharField(max_length=255, verbose_name='Nama Siswa')
    nisn = models.CharField(max_length=10, unique=True)
    nis = models.CharField(max_length=9, unique=True)
    tempat_lahir = models.CharField(max_length=255)
    tanggal_lahir = models.DateField()
    gender = models.CharField(verbose_name='Jenis Kelamin', max_length=1, choices=GENDER_CHOICE, default=GENDER_CHOICE[0][0])
    agama = models.CharField(max_length=255)
    anak_ke = models.SmallIntegerField()
    alamat = models.TextField()
    sekolah_asal = models.CharField(max_length=255)
    diterima_di_tingkat = models.ForeignKey(Tingkat, on_delete=models.SET_NULL, null=True)
    nama_ayah = models.CharField(max_length=255)
    nama_ibu = models.CharField(max_length=255)
    nama_wali = models.CharField(max_length=255, null=True, blank=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.nisn}/{self.nis}-{self.nama}'

    
