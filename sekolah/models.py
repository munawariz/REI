from django.db import models
from solo.models import SingletonModel
from django.dispatch import receiver

class Sekolah(SingletonModel):
    TINGKAT_SEKOLAH = [
        ('SD', 'Sekolah Dasar'),
        ('SMP', 'Sekolah Menengah Pertama'),
        ('SMA', 'Sekolah Menengah Atas'),
        ('SMK', 'Sekolah Menengah Kejuruan'),
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

class TanggalPendidikan(models.Model):
    SEMESTER_CHOICE = [
        ('1', 'Ganjil'),
        ('2', 'Genap')
    ]
    tahun_mulai = models.CharField(verbose_name='Tahun Mulai', max_length=4)
    tahun_akhir = models.CharField(verbose_name='Tahun Berakhir', max_length=4)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.tahun_mulai}/{self.tahun_akhir} {self.semester}'

@receiver(models.signals.pre_save, sender=TanggalPendidikan)
def only_one_is_active_instance(sender, instance, **kwargs):
    tp = TanggalPendidikan.objects.filter(is_active=True)
    if tp and instance.is_active:
        for tp in tp:                                        
            tp.is_active = False
            tp.save()

class Jurusan(models.Model):
    lengkap = models.CharField(verbose_name='Nama Lengkap', max_length=255)
    singkat = models.CharField(verbose_name='Nama Singkat', max_length=10)
