from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


urlpatterns = [
    path('api-get-token-auth/',obtain_auth_token, name='api_token_auth'),
    path('userprofile/',UserProfile.as_view(),name='profile'),
    path('validatephone/', ValidatePhoneSendOTP.as_view()),
    path('validateotp/', ValidateOTP.as_view()),
    path('register/', Register.as_view()),
]