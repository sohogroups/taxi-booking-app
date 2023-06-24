from django.urls import path
from .views import *

urlpatterns = [
	path('login/',UserLoginView.as_view()),
	path('set_password/',SetPasswordView.as_view()),
	path('change_password/',ChangePasswordView.as_view()),
	path('forgot_password/',ForgotPasswordView.as_view()),
	path('reset_password/',ResetPasswordView.as_view()),
	path('email_otp_verification/',EmailOtpVerificationView.as_view())
]