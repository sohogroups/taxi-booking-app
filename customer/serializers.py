from rest_framework import serializers
from .models import *

class CustomerSerializers(serializers.ModelSerializer):
	class Meta:
		model = Customers
		fields = ['name','email','phone_number','gender']