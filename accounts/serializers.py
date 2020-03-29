from rest_framework import serializers

from .models import User
from fcm_django.models import FCMDevice


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk','email', 'mobile', 'first_name', 'last_name','firebase_id','password','profile_pic')

class CreateFCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ('user','registration_id','device_id')