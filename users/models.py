from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def create_user(self, email=None, password=None, **extra_fields):
        return super(CustomUserManager, self).create_user(email, email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        return super(CustomUserManager, self).create_superuser(email, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        max_length=100,
        help_text="Email",
    )
    is_active = models.BooleanField(default=True)
    username = models.CharField(unique=True, max_length=30)
    firstname = models.CharField(max_length=30, verbose_name='Имя')
    lastname = models.CharField(max_length=30, verbose_name='Фамилия')
    is_staff = models.BooleanField(default=False)
    organization = models.ForeignKey('organizations.Organization', null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='users')

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.username = self.email
        return super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def __str__(self):
        return str(self.email)
