from django.urls import path
from .views import *

urlpatterns = [
	path('sign_up/',CustomerSignUp.as_view()),
]