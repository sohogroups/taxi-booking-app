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
from rest_framework import renderers
from django.contrib.auth import authenticate,logout
from rest_framework_simplejwt.tokens import RefreshToken
import json
from app.utils import *
import random
from datetime import timedelta
# Create your views here.
class UserRenderer(renderers.JSONRenderer):
	charset='utf-8'
	def render(self, data, accepted_media_type=None, renderer_context=None):
		response = ''
		if 'ErrorDetail' in str(data):
			response = json.dumps({'errors':data})
		else:
			response = json.dumps(data)

		return response

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserLoginView(APIView):
	renderer_classes = [UserRenderer]
	permission_classes = (AllowAny,)
	def post(self, request, format=None):
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = serializer.data.get('email')
		password = serializer.data.get('password')
		user = authenticate(email=email, password=password)
		if user is not None:
			token = get_tokens_for_user(user)
			user_id = user.id
			return Response({'token':token, "id":user_id ,"email":email ,'msg':'Login Success'}, status=status.HTTP_200_OK)
		else:
			return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class SetPasswordView(APIView):
	permission_classes = [IsAuthenticated]
	def post(self,request,format=None):
		serializer = SetPasswordSerializers(data=request.data)
		if serializer.is_valid():
			password = request.data['password']
			confirm_password = request.data['confirm_password']
			if password != confirm_password:
				return Response({'errors':{'non_field_errors':['Password not match']}}, status=status.HTTP_404_NOT_FOUND)
			else:
				user_id = request.user.id
				user = UserMaster.objects.get(id=user_id)
				user.set_password(password)
				user.save()
		return Response({'msg':'Password set successfully'}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
	permission_classes = [IsAuthenticated]
	def post(self,request,format=None):
		serializer = ChangePasswordSerializers(data=request.data)
		if serializer.is_valid():
			old_password = request.data['old_password']
			password = request.data['password']
			confirm_password = request.data['confirm_password']
			user_id = request.user.id
			user = UserMaster.objects.get(id=user_id)
			if not user.check_password(old_password):
				return Response({'errors':{'old_password':['Your old password was entered incorrectly. Please enter it again.']}}, status=status.HTTP_404_NOT_FOUND)
			elif password != confirm_password:
				return Response({'errors':{'non_field_errors':['Password not match']}}, status=status.HTTP_404_NOT_FOUND)
			user.set_password(password)
			user.save()
		return Response({'msg':'Password Changed successfully'}, status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
	permission_classes = [AllowAny]
	def post(self,request,format=None):
		serializer = ForgotPasswordSerializers(data=request.data)
		if serializer.is_valid():
			email = request.data['email']
			if UserMaster.objects.filter(email=email).exists():
				user = UserMaster.objects.get(email = email)
				fixed_digits = 5
				otp = random.randrange(11111, 99999, fixed_digits)
				user.otp = otp
				expiry_date = datetime.datetime.now()+timedelta(minutes=10)
				user.otp_expiry_date = expiry_date
				user.save()
				subject = 'Reset Your Password'
				to_email = user.email
				email_body = str(otp)
				SendEmail(subject,email_body,to_email).start()
				return Response({'msg':'OTP send. Please check your Email'}, status=status.HTTP_200_OK)
		return Response({'errors':{'email':['You are not a Registered User']}}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
	permission_classes = [AllowAny]
	def post(self,request,format=None):
		serializer = ResetPasswordSerializers(data=request.data)
		if serializer.is_valid():
			email = request.data['email']
			otp = request.data['otp']
			password = request.data['password']
			confirm_password = request.data['confirm_password']
			if UserMaster.objects.filter(email=email,otp=otp).exists():
				user = UserMaster.objects.get(email=email,otp=otp)
				user_mail = user.email
				user_otp = user.otp
				user_expiry_date = user.otp_expiry_date
				expiry_date = user_expiry_date.strftime('%Y-%m-%d %H:%M:%S')
				expiry_date1 = datetime.datetime.strptime(str(expiry_date), "%Y-%m-%d %H:%M:%S")
				today_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				today_date1 = datetime.datetime.strptime(today_date,'%Y-%m-%d %H:%M:%S')
				active_otp = user.is_active
				if expiry_date1 >= today_date1:
					user.set_password(password)
					user.save()
					return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
				return Response({'errors':{'otp':['Your OTP is expired']}}, status=status.HTTP_404_NOT_FOUND)
		return Response({'errors':{'msg':['mail or OTP is invalid']}}, status=status.HTTP_404_NOT_FOUND)

class EmailOtpVerificationView(APIView):
	permission_classes = [AllowAny]
	def post(self,request,format=None):
		serializer = EmailOtpVerificationSerializers(data=request.data)
		if serializer.is_valid():
			otp = request.data['otp']
			email = request.data['email']
			try:
				user = UserMaster.objects.get(email=email,otp=otp)
				user_mail = user.email
				user_otp = user.otp
				user_expiry_date = user.otp_expiry_date
				expiry_date = user_expiry_date.strftime('%Y-%m-%d %H:%M:%S')
				expiry_date1 = datetime.datetime.strptime(str(expiry_date), "%Y-%m-%d %H:%M:%S")
				today_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				today_date1 = datetime.datetime.strptime(today_date,'%Y-%m-%d %H:%M:%S')
				if expiry_date1 >= today_date1:
					return Response({'msg':'Email Verified Successfully'}, status=status.HTTP_200_OK)
				else:
					return Response({'errors':{'otp':['Your OTP is expired']}}, status=status.HTTP_404_NOT_FOUND)
			except UserMaster.DoesNotExist:
				return Response({'errors':{'msg':['OTP is invalid']}}, status=status.HTTP_404_NOT_FOUND)
		return Response({'errors':{'msg':['OTP is invalid']}}, status=status.HTTP_404_NOT_FOUND)