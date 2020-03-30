from rest_framework import serializers
from chat.models import Message,ChatDialog
from django.contrib.auth import get_user_model
from django.utils.timesince import timesince

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk','first_name', 'last_name','profile_pic')

class MessageSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(MessageSerializer, self).to_representation(instance)
        data.update(timestamp=timesince(instance.timestamp))
        return data

    class Meta:
        model = Message
        fields = ['id','chatdialog','sender', 'message', 'timestamp']

class CreateMessageSerializer(serializers.ModelSerializer):
    receiver = serializers.CharField(read_only=True)
    attachment = serializers.CharField(required=False)
    message = serializers.CharField(required=False)

    class Meta:
        model = Message
        fields = ['receiver', 'message', 'timestamp','attachment']

class ChatDialogSerializer(serializers.ModelSerializer):
    receiver = UserSerializer()
    sender = UserSerializer()
    user = serializers.JSONField()
    latest_message = serializers.JSONField()

    def to_representation(self, instance):
        data = super(ChatDialogSerializer, self).to_representation(instance)
        data.update(modified=timesince(instance.modified))
        return data

    class Meta:
        model = ChatDialog
        fields = ['sender','receiver','modified','id','user','latest_message']
