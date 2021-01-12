from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from helpers.choice import GENDER_CHOICE

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

    USERNAME_FIELD = 'nip'
    REQUIRED_FIELDS = ['nama',]

    objects = UserManager()

    def __str__(self):
        return self.nama or ''

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True