from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk','email', 'mobile', 'first_name', 'last_name','firebase_id')

