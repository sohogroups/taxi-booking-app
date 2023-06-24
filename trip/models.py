from django.db import models
from customer.models import *
from driver.models import *
from django.utils import timezone
import datetime
import os

# Create your models here.

class Trip(models.Model):
	customer_id = models.ForeignKey(Customers,on_delete=models.SET_NULL,null=True)
	driver_id = models.ForeignKey(Driver,on_delete=models.SET_NULL,null=True)
	car_id = models.ForeignKey(Car,on_delete=models.SET_NULL,null=True)
	start_location_id = models.CharField(max_length=255)
	end_location_id = models.CharField(max_length=255)
	start_time = models.DateTimeField(null=True)
	end_time = models.DateTimeField(null=True)
	wait_time = models.IntegerField(null=True)
	trip_status = models.CharField(max_length=255)
	created_on = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ['id']

	def __int__(self):
		return self.id

class FeedBack(models.Model):
	trip_id = models.ForeignKey(Trip,on_delete=models.SET_NULL,null=True)
	message = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ['id']

	def __int__(self):
		return self.id

class Rating(models.Model):
	trip_id = models.ForeignKey(Trip,on_delete=models.SET_NULL,null=True)
	rating  = models.IntegerField(null=True)

	class Meta:
		ordering = ['id']

	def __int__(self):
		return self.id