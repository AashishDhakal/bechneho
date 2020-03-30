from rest_framework import serializers
from chat.models import Message,ChatDialog
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk','first_name', 'last_name','profile_pic')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','chatdialog','sender', 'message', 'timestamp']

class CreateMessageSerializer(serializers.ModelSerializer):
    receiver = serializers.CharField(read_only=True)
    attachment = serializers.CharField(required=False)

    class Meta:
        model = Message
        fields = ['receiver', 'message', 'timestamp','attachment']

class ChatDialogSerializer(serializers.ModelSerializer):
    receiver = UserSerializer()
    sender = UserSerializer()
    user = serializers.JSONField()

    class Meta:
        model = ChatDialog
        fields = ['sender','receiver','modified','id','user']
