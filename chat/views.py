from .models import Message,ChatDialog
from .serializers import MessageSerializer,CreateMessageSerializer,ChatDialogSerializer
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from datetime import datetime
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()

class MessageDetails(ListAPIView):
    '''
    This endpoint lists all the messages ordered by time,you need to pass chatdialog id to list down all the messages and requesting user must be
    authenticated as well.So,pass authentication token as header and chatdialog id as query parameter.
    :parameter
    chatdialog_id
    '''
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        chatdialog = self.request.query_params.get("chatdialog_id")
        return Message.objects.filter(chatdialog_id=chatdialog)

class CreateMessage(APIView):
    '''
    This endpoint creates messages.Pass authentication token as authorization header.
    '''
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        receiver = request.POST.get('receiver')
        sender = self.request.user
        serializer = CreateMessageSerializer(data=self.request.data)
        if serializer.is_valid():
            try:
                chatdialog = ChatDialog.objects.get(Q(receiver=receiver) | Q(receiver=sender) | Q(sender=sender) | Q(sender=receiver))
                chatdialog.modified = datetime.now()
                chatdialog.save()
                serializer.save(chatdialog=chatdialog,sender=sender)
                return Response(serializer.data)
            except ChatDialog.DoesNotExist:
                    receiver = User.objects.get(id=receiver)
                    chatdialog=ChatDialog.objects.create(sender=sender,receiver=receiver,modified=datetime.now())
                    serializer.save(chatdialog=chatdialog,sender=sender)
                    return Response(serializer.data)
        else:
            return Response({
                'status': False,
                'Detail': 'Invalid Data',
            })

class ChatDialogView(ListAPIView):
    '''
    This endpoint list all the chat history or heads of a user.User requesting chat dialogs must be authenticated.So,pass in authentication token as authorization
    header.
    '''
    serializer_class = ChatDialogSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        return ChatDialog.objects.filter(Q(sender=user)|Q(receiver=user))

