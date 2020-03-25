from rest_framework import serializers
from chat.models import Message,ChatDialog
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','chatdialog','sender', 'message', 'timestamp']

class CreateMessageSerializer(serializers.ModelSerializer):
    receiver = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = ['receiver', 'message', 'timestamp']

class ChatDialogSerializer(serializers.ModelSerializer):
    receiver = serializers.StringRelatedField()
    sender = serializers.StringRelatedField()

    class Meta:
        model = ChatDialog
        fields = '__all__'
