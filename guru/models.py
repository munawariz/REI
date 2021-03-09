from REI.settings import MEDIA_ROOT
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from helpers.choice import GENDER_CHOICE, TINGKAT_GELAR_CHOICE, JURUSAN_GELAR_CHOICE
from django.dispatch import receiver
from helpers.externalAPI import avatarAPI
import os

class UserManager(BaseUserManager):
    def create_user(self, nip, nama, password=None):
        if not nip or not nama:
            raise ValueError("Data is not complete")        

        user = self.model(nip = nip, nama = nama)
        if user.is_superuser:
            user.is_admin = True
            user.is_staff = True            
            user.is_walikelas = True
            user.is_staftu = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nip, nama, password):
        user = self.create_user(nip = nip, password = password, nama = nama)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_walikelas = True
        user.is_staftu = True
        user.save(using=self._db)
        return user

class Guru(AbstractBaseUser):
    nip = models.CharField(verbose_name='Nomor Induk', unique=True, max_length=18)    
    nama = models.CharField(max_length=255)
    nama_gelar = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True)
    gender = models.CharField(verbose_name='Jenis Kelamin', max_length=1, choices=GENDER_CHOICE, default=GENDER_CHOICE[0][0])
    tempat_lahir = models.CharField(max_length=255, null=True)
    tanggal_lahir = models.DateField(null=True)
    agama = models.CharField(max_length=255, null=True)
    alamat = models.CharField(max_length=255, null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_walikelas = models.BooleanField(default=True, verbose_name='Walikelas')
    is_staftu = models.BooleanField(default=True, verbose_name='Staf TU')
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatar/guru/', null=True, blank=True)

    USERNAME_FIELD = 'nip'
    REQUIRED_FIELDS = ['nama',]

    objects = UserManager()

    def __str__(self):
        return self.nama or ''

    def save(self, *args, **kwargs):
        try:
            self.nama_gelar = gelarize_nama_guru(self.nip)
        except Guru.DoesNotExist:
            pass
        return super(Guru, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

@receiver(models.signals.pre_save, sender=Guru)
def guru_pre_save(sender, instance, **kwargs):
    try:
        old_file = sender.objects.get(pk=instance.pk).avatar.path
        new_file = instance.avatar
        print('Deklarasi file')
        print(old_file)
        if (old_file and not new_file) or (old_file and new_file and not old_file == new_file):
            if os.path.isfile(old_file):
                print('pre_delete oldfile')
                os.remove(old_file)
                print('post_delete oldfile')
        if old_file and not os.path.isfile(old_file):
            print('pre_getapi')
            instance.avatar = avatarAPI(instance)
            print('post_getapi')
            
    except sender.DoesNotExist:
        return False
    except ValueError:
        return False
    except Exception as e:
        print(e)
        
@receiver(models.signals.post_save, sender=Guru)
def guru_post_save(sender, instance, created, **kwargs):
    if not instance.avatar:
        print('Post Save')
        instance.avatar = avatarAPI(instance)
        instance.save()

@receiver(models.signals.post_delete, sender=Guru)
def guru_post_delete(sender, instance, **kwargs):
    if instance.avatar.path:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


class Gelar(models.Model):
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE)
    tingkat_gelar = models.CharField(choices=TINGKAT_GELAR_CHOICE, max_length=5)
    verbose_tingkat = models.CharField(null=True, blank=True, max_length=255)
    jurusan = models.CharField(choices=JURUSAN_GELAR_CHOICE, max_length=255)
    verbose_jurusan = models.CharField(null=True, blank=True, max_length=255)
    universitas = models.CharField(max_length=255)
    gelar = models.CharField(null=True, blank=True, max_length=255)

    def save(self, *args, **kwargs):
        self.verbose_tingkat = self.get_tingkat_gelar_display()
        self.verbose_jurusan = self.get_jurusan_display()
        self.gelar = self.tingkat_gelar + self.jurusan
        return super(Gelar, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.guru.nama} {self.gelar} {self.universitas}'

@receiver(models.signals.pre_save, sender=Gelar)
def gelar_pre_save(sender, instance, **kwargs):
    try:
        gelar = Gelar.objects.filter(guru=instance.guru, tingkat_gelar=instance.tingkat_gelar, jurusan=instance.jurusan)
        if gelar and instance not in gelar:
            raise ValidationError("Gelar already exists")
    except Gelar.DoesNotExist:
        pass

@receiver(models.signals.post_save, sender=Gelar)
def gelar_post_save(sender, instance, **kwargs):
    Guru.objects.get(nip=instance.guru.nip).save()

@receiver(models.signals.post_delete, sender=Gelar)
def gelar_post_delete(sender, instance, **kwargs):
    Guru.objects.get(nip=instance.guru.nip).save()


def gelarize_nama_guru(nip):
    guru = Guru.objects.get(nip=nip)
    nama = guru.nama
    gelar = Gelar.objects.filter(guru=guru).order_by('verbose_tingkat', 'jurusan')
    order = ['Diploma 1', 'Diploma 2', 'Diploma 3', 'Diploma 4', 'Sarjana', 'Magister', 'Doktor']
    gelar = sorted(gelar, key=lambda x: order.index(x.verbose_tingkat))
    for gelar in gelar:
        vb_tingkat = gelar.verbose_tingkat
        if not 'Doktor' == vb_tingkat:
            nama = nama+', '+gelar.gelar    
        elif 'Doktor' == gelar.verbose_tingkat and not str(nama).startswith('Dr. '):
            nama = 'Dr. '+nama

    return nama