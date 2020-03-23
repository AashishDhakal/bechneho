from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Message
from .serializers import MessageSerializer,MessageUserSerializer,CreateMessageSerializer
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from accounts.serializers import UserSerializer
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings

class MessageDetails(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        receiver_id = self.request.query_params.get("receiver_id")
        sender_id = self.request.user.id
        return Message.objects.filter(sender_id=sender_id,receiver_id=receiver_id) | Message.objects.filter(sender_id=receiver_id,receiver_id=sender_id)

class CreateMessage(CreateAPIView):
    serializer_class = CreateMessageSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
        receiver = self.request.POST['receiver']
        user = User.objects.get(username=receiver)
        send_mail("Bechneho:New Message Received",receiver,from_email=settings.EMAIL_HOST_USER,recipient_list=[user.email,])
        print("Mail Delivered")




class MessageUserlist(ListAPIView):
    serializer_class = MessageUserSerializer
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        user = self.request.user.id
        messages= Message.objects.filter(sender_id=user) | Message.objects.filter(receiver_id=user)
        try:
            return messages['sender']
        except TypeError:
            print(messages.values_list('sender','receiver'))
        return None
