from django.urls import path
from .views import *

urlpatterns = [
	path('sign_up/',CustomerSignUp.as_view()),
	path('customer_profile/<int:user_id>/',CustomerProfile.as_view()),
]
