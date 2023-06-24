from django.db import models
from django.utils import timezone
import datetime
import os
from app.models import UserMaster
# Create your models here.

class Driver(models.Model):
	def upload_path(instance,filename):
	    d = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S_')
	    file = os.path.splitext(filename)
	    td = datetime.datetime.now().strftime('%Y/%m/%d')
	    return f'driver/{td}/{instance.name}/{str(d)+str(file)}'

	name = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	phone_number = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	user_id = models.ForeignKey(UserMaster,on_delete=models.SET_NULL,null=True)
	is_active = models.BooleanField(default=True)
	photo = models.ImageField(null=True,upload_to=upload_path)
	created_on = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return self.name

class Car(models.Model):

	def upload_path(instance,filename):
	    d = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S_')
	    file = os.path.splitext(filename)
	    td = datetime.datetime.now().strftime('%Y/%m/%d')
	    return f'car/{td}/{instance.name}/{str(d)+str(file)}'

	name = models.CharField(max_length=255)
	driver_id = models.ForeignKey(Driver,on_delete=models.SET_NULL,null=True)
	car_modal = models.CharField(max_length=255)
	license_plate_no = models.CharField(max_length=255)
	base_rate = models.IntegerField()
	is_active = models.BooleanField(default=True)
	car_make = models.CharField(max_length=255)
	car_year = models.IntegerField()
	photo = models.ImageField(null=True,upload_to=upload_path)
	created_on = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return self.name

class Documents(models.Model):
	def upload_path(instance,filename):
	    d = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S_')
	    file = os.path.splitext(filename)
	    td = datetime.datetime.now().strftime('%Y/%m/%d')
	    return f'documents/{td}/{instance.name}/{str(d)+str(file)}'

	name = models.CharField(max_length=255)
	driver_id = models.ForeignKey(Driver,on_delete=models.SET_NULL,null=True)
	driver_category = models.CharField(max_length=255)
	document_code = models.CharField(max_length=255)
	expiry_date = models.DateTimeField()
	photo = models.ImageField(null=True,upload_to=upload_path)
	created_on = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return self.name