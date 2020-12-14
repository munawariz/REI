from django.db import models
from django.db.models.fields.related import ForeignKey
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
    nama = models.CharField(verbose_name='Nama Lengkap', max_length=255)
    singkat = models.CharField(verbose_name='Nama Singkat', max_length=10)

    def __str__(self):
        return self.singkat

class MataPelajaran(models.Model):
    MATAPELAJARAN_CHOICE = [
        ('NA', 'Normatif Adaptif'),
        ('WS', 'Kejuruan'),
        ('MULOK', 'Muatan Lokal')
    ]

    nama = models.CharField(verbose_name='Nama Mata Pelajaran', max_length=255)
    singkat = models.CharField(verbose_name='Nama Singkat Mata Pelajaran', max_length=20)
    kelompok = models.CharField(verbose_name='Kelompok Mata Pelajaran', max_length=5, choices=MATAPELAJARAN_CHOICE)

    def __str__(self):
        return f'{self.singkat}/{self.kelompok}'

    def save(self, *args, **kwargs):
        self.singkat = str(self.singkat).upper()
        super(MataPelajaran, self).save(*args, **kwargs)

class KKM(models.Model):
    matapelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE)
    tgl_pendidikan = models.ForeignKey(TanggalPendidikan, on_delete=models.CASCADE)
    pengetahuan = models.SmallIntegerField(verbose_name='KKM Pengetahuan')
    keterampilan = models.SmallIntegerField(verbose_name='KKM Keterampilan')

    def __str__(self):
        return f'{self.matapelajaran}({self.tgl_pendidikan})'

    def save(self, *args, **kwargs):
        if self.pengetahuan < 0: self.pengetahuan = 0
        if self.pengetahuan > 100: self.pengetahuan = 100
        if self.keterampilan < 0: self.keterampilan = 0
        if self.keterampilan > 100: self.keterampilan = 100
        super(KKM, self).save(*args, **kwargs)

@receiver(models.signals.pre_save, sender=KKM)
def only_one_instance_with_same_tp_and_mapel(sender, instance, **kwargs):
    kkm = KKM.objects.filter(matapelajaran=instance.matapelajaran, tgl_pendidikan=instance.tgl_pendidikan)
    if kkm:
        for kkm in kkm:                                        
            kkm.delete()            