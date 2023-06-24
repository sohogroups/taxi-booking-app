from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
import os

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class UserMaster(AbstractBaseUser,PermissionsMixin):
	def validate_contact_email(value):
	    if "@" and "." in value:
	        return value
	    else:
	        raise ValidationError("Enter valid email")

	name = models.CharField(max_length=100,blank=True)
	password = models.CharField(max_length=250,blank=True)
	email = models.EmailField(blank=True,unique=True,validators =[validate_contact_email])
	phone_number = models.CharField(max_length=255,null=True)
	user_type = models.CharField(max_length=250,blank=True)
	is_staff = models.BooleanField(default=False,blank=True)
	is_superuser = models.BooleanField(default=False,blank=True)
	is_active = models.BooleanField(default=True,blank=True)
	date_joined = models.DateTimeField(default=timezone.now,blank=True)
	last_login = models.DateTimeField(default=timezone.now,blank=True)
	otp = models.IntegerField(blank=True,null=True)
	otp_expiry_date = models.DateTimeField(blank=True,null=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = UserManager()

	class Meta:
		ordering = ['id']

	def __str__(self):
		return self.name

