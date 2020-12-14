from django.db import models
from solo.models import SingletonModel

class Sekolah(SingletonModel):
    TINGKAT_SEKOLAH = [
        ('SD', 'Sekolah Dasar'),
        ('SMP', 'Sekolah Menengah Pertama'),
        ('SMA', 'Sekolah Menengah Atas'),
        ('SMK', 'Sekolah Kejuruan'),
    ]
    nama = models.CharField(max_length=255)
    tingkat = models.CharField(verbose_name='Tingkat Sekolah', max_length=3, choices=TINGKAT_SEKOLAH)
    npsn = models.CharField(max_length=8)
    alamat = models.TextField()
    kode_pos = models.CharField(max_length=5)
    no_telepon = models.CharField(verbose_name='Nomor Telepon', max_length=20)
    kelurahan = models.CharField(max_length=50)
    kecamatan = models.CharField(max_length=50)
    kota = models.CharField(verbose_name='Kota/Kabupaten', max_length=50)
    provinsi = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return "Informasi Sekolah"

    class Meta:
        verbose_name = "Informasi Sekolah"