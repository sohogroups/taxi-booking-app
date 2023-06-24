from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from .models import *
from app.models import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from app.utils import *
import random
from datetime import timedelta
# Create your views here.

class CustomerSignUp(APIView):
	permission_classes = (AllowAny,)
	def post(self,request,format=False):
		customer_serializers = CustomerSerializers(data=request.data)
		if customer_serializers.is_valid():
			customer = customer_serializers.save()
			email = request.data['email']
			name = request.data['name']
			phone_number = request.data['phone_number']
			fixed_digits = 5
			otp = random.randrange(11111, 99999, fixed_digits)
			expiry_date = datetime.datetime.now()+timedelta(minutes=10)
			user = UserMaster.objects.create(
				name = name,
				email = email,
				phone_number = phone_number,
				user_type = 'customer',
				otp = otp,
				otp_expiry_date = expiry_date
				)
			user_id = user.id
			customer.user_id = UserMaster.objects.get(id=user_id)
			customer.save()
			subject = 'Email Verfication'
			to_email = user.email
			email_body = str(otp)
			SendEmail(subject,email_body,to_email).start()
			return Response(customer_serializers.data,status=status.HTTP_200_OK)
		return Response(customer_serializers.errors,status=status.HTTP_400_BAD_REQUEST)

