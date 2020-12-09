from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class AccountsModelManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

class AccountsModel(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('Email Address', unique=True)
    time_created = models.DateTimeField('Time Created',auto_now_add=True)
    time_updated = models.DateTimeField('Time Updated',auto_now=True)
    is_staff = models.BooleanField('Staff',default=False)
    is_active = models.BooleanField('Active',default=False)
    is_superuser = models.BooleanField('Super User',default=False)

    objects = AccountsModelManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.email