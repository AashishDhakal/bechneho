from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


urlpatterns = [
    path('api-get-token-auth/',obtain_auth_token, name='api_token_auth'),
    path('register/', Register.as_view()),
]