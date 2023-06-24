from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
import os
from app.models import *

# Create your models here.

class Customers(models.Model):

	def upload_path(instance,filename):
	    d = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S_')
	    file = os.path.splitext(filename)
	    td = datetime.datetime.now().strftime('%Y/%m/%d')
	    return f'customer/{td}/{instance.name}/{str(d)+str(file)}'

	name = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	phone_number = models.CharField(max_length=255)
	street = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	district = models.CharField(max_length=255)
	user_id = models.ForeignKey(UserMaster,on_delete=models.SET_NULL,null=True)
	is_active = models.BooleanField(default=True)
	photo = models.ImageField(null=True,upload_to=upload_path)
	created_on = models.DateTimeField(default=timezone.now)
	gender = models.CharField(max_length=255,null=True)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return self.name
