import helpers
from django.db import models
from django.db.models import signals
from sekolah.models import Kelas, Tingkat, MataPelajaran, Semester
from helpers.choice import GENDER_CHOICE, NILAI_EKSKUL
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.dispatch import receiver
from sekolah.models import Ekskul

class Siswa(models.Model):
    nama = models.CharField(max_length=255, verbose_name='Nama Siswa')
    nisn = models.CharField(max_length=10, unique=True)
    nis = models.CharField(max_length=9, unique=True)
    email = models.EmailField(null=True)
    tempat_lahir = models.CharField(max_length=255)
    tanggal_lahir = models.DateField()
    gender = models.CharField(verbose_name='Jenis Kelamin', max_length=1, choices=GENDER_CHOICE, default=GENDER_CHOICE[0][0])
    agama = models.CharField(max_length=255)
    anak_ke = models.PositiveSmallIntegerField()
    alamat = models.CharField(max_length=255)
    sekolah_asal = models.CharField(max_length=255)
    diterima_di_tingkat = models.ForeignKey(Tingkat, on_delete=models.SET_NULL, null=True, related_name='siswa')
    nama_ayah = models.CharField(max_length=255)
    nama_ibu = models.CharField(max_length=255)
    nama_wali = models.CharField(max_length=255, null=True, blank=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.PROTECT, related_name='siswa')

    def __str__(self):
        return f'{self.nisn}/{self.nis}-{self.nama}'

@receiver(models.signals.post_save, sender=Siswa)
def nilai_post_save(sender, instance, created, **kwargs):
    if created:
        instance.semester = instance.siswa.kelas.semester
        instance.save()


class Nilai(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='nilai')
    matapelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE, related_name='nilai')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='nilai')
    pengetahuan = models.PositiveSmallIntegerField()
    keterampilan = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.siswa}/{self.matapelajaran}/{self.semester}'

    def save(self, *args, **kwargs):
        if self.pengetahuan < 0: self.pengetahuan = 0
        if self.pengetahuan > 100: self.pengetahuan = 100
        if self.keterampilan < 0: self.keterampilan = 0
        if self.keterampilan > 100: self.keterampilan = 100

        super(Nilai, self).save(*args, **kwargs)

@receiver(models.signals.pre_save, sender=Nilai)
def unique_together_tp_mapel(sender, instance, **kwargs):
    try:
        nilai = Nilai.objects.filter(siswa=instance.siswa, matapelajaran=instance.matapelajaran, semester=instance.semester)
        if nilai and instance not in nilai:
            raise ValidationError('Nilai for that Siswa with that Mata Pelajaran in that Semester already exists')
    except ObjectDoesNotExist:
        pass

@receiver(models.signals.post_save, sender=Nilai)
def nilai_post_save(sender, instance, created, **kwargs):
    if created:
        instance.semester = instance.siswa.kelas.semester
        instance.save()


class Absensi(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='absensi')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='absensi')
    izin = models.PositiveSmallIntegerField()
    sakit = models.PositiveSmallIntegerField()
    bolos = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.siswa}/{self.semester}'

@receiver(models.signals.pre_save, sender=Absensi)
def unique_together_siswa_semester(sender, instance, **kwargs):
    try:
        absen = Absensi.objects.filter(siswa=instance.siswa, semester=instance.semester)
        if absen and instance not in absen:
            raise ValidationError('Absen for that siswa in that semester already exists')
    except ObjectDoesNotExist:
        pass


class NilaiEkskul(models.Model):
    ekskul = models.ForeignKey(Ekskul, on_delete=models.CASCADE, related_name='nilai')
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='ekskul')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='nilai_ekskul')
    nilai = models.CharField(max_length=1, choices=NILAI_EKSKUL)

    def __str__(self):
        return f'{self.siswa} - {self.ekskul} - {self.nilai}'

@receiver(models.signals.pre_save, sender=NilaiEkskul)
def unique_together_siswa_ekskul_semester(sender, instance, **kwargs):
    try:
        nileks = NilaiEkskul.objects.filter(siswa=instance.siswa, semester=instance.semester, ekskul=instance.ekskul)
        if nileks and instance not in nileks:
            raise ValidationError('Nilai Ekskul for that siswa in that semester already exists')
    except ObjectDoesNotExist:
        pass

