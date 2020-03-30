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
from fcm_django.models import FCMDevice

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
        receiverid = request.POST.get('receiver')
        message = request.POST.get('message',False)
        attachment = request.POST.get('attachment',False)
        sender = self.request.user
        serializer = CreateMessageSerializer(data=self.request.data)
        if serializer.is_valid():
            try:
                receiver = User.objects.get(id=receiverid)
                chatdialog = ChatDialog.objects.get(Q(receiver=receiver,sender=sender) or Q(sender=receiver,receiver=sender))
                chatdialog.modified = datetime.now()
                chatdialog.save()
                serializer.save(chatdialog=chatdialog,sender=sender)
                user = User.objects.get(id=receiverid)
                sender = User.objects.get(id=self.request.user.id)
                title = f'{sender.first_name} {sender.last_name}'
                try:
                    device = FCMDevice.objects.get(device_id=user.firebase_id)
                    if message:
                        body = message
                    else:
                        body = "New Attachment Received"
                    device.send_message(title=title,body=body)
                except FCMDevice.DoesNotExist:
                    pass
                return Response(serializer.data)
            except ChatDialog.DoesNotExist:
                    receiver = User.objects.get(id=receiverid)
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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ChatDialogSerializer(queryset,many=True)
        serialized_data = serializer.data
        try:
            for data in range(len(serialized_data)):
                print(data)
                if serialized_data[data]['sender']['pk'] == self.request.user.id:
                    serialized_data[data]['user'] = serialized_data[data]['receiver']
                    chatdialogid=serialized_data[data]['id']
                    serialized_data[data]['latest_message']=Message.objects.filter(chatdialog=chatdialogid).order_by('-timestamp')[0].message
                else:
                    serialized_data[data]['user'] = serialized_data[0]['sender']
                    chatdialogid=serialized_data[data]['id']
                    serialized_data[data]['latest_message']=Message.objects.filter(chatdialog=chatdialogid).order_by('-timestamp')[0].message
            return Response(serialized_data)
        except IndexError:
            return Response('You have no conversations.')
