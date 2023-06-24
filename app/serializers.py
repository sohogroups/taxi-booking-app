from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from app.models import *

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = UserMaster
    fields = ['email', 'password']

class SetPasswordSerializers(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password','confirm_password']

class ChangePasswordSerializers(serializers.Serializer):
  old_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['old_password','password','confirm_password']

class ForgotPasswordSerializers(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

class ResetPasswordSerializers(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  otp = serializers.IntegerField()
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['email','otp','password','confirm_password']

class EmailOtpVerificationSerializers(serializers.Serializer):
  otp = serializers.IntegerField()
  class Meta:
    fields = ['email','otp']