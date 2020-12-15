from django.db import models
from sekolah.models import Kelas, Tingkat, MataPelajaran, Semester
from helpers.choice import GENDER_CHOICE
from django.core.exceptions import ValidationError
from django.dispatch import receiver

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
    diterima_di_tingkat = models.ForeignKey(Tingkat, on_delete=models.SET_NULL, null=True, related_name='siswa')
    nama_ayah = models.CharField(max_length=255)
    nama_ibu = models.CharField(max_length=255)
    nama_wali = models.CharField(max_length=255, null=True, blank=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.PROTECT, related_name='siswa')

    def __str__(self):
        return f'{self.nisn}/{self.nis}-{self.nama}'

class Nilai(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='nilai')
    matapelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE, related_name='nilai')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='nilai', editable=False)
    pengetahuan = models.SmallIntegerField()
    keterampilan = models.SmallIntegerField()

    def __str__(self):
        return f'{self.siswa}/{self.matapelajaran}/{self.semester}'

    def save(self, *args, **kwargs):
        if self.pengetahuan < 0: self.pengetahuan = 0
        if self.pengetahuan > 100: self.pengetahuan = 100
        if self.keterampilan < 0: self.keterampilan = 0
        if self.keterampilan > 100: self.keterampilan = 100

        self.semester = self.siswa.kelas.semester
        super(Nilai, self).save(*args, **kwargs)

@receiver(models.signals.pre_save, sender=Nilai)
def unique_together_tp_mapel(sender, instance, **kwargs):
    nilai = Nilai.objects.filter(siswa=instance.siswa, matapelajaran=instance.matapelajaran, semester=instance.semester)
    if nilai and instance not in nilai:
        raise ValidationError('Nilai for that Siswa with that Mata Pelajaran in that Semester already exists')

    
