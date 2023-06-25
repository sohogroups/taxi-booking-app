from rest_framework import serializers
from .models import *

class CustomerSerializers(serializers.ModelSerializer):
	class Meta:
		model = Customers
		fields = ['name','email','phone_number','gender']
		
class CustomerProfileSerializers(serializers.ModelSerializer):
	class Meta:
		model = Customers
		fields = ['name','email','phone_number','gender','street','city','district']
