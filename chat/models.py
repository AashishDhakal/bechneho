from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()# Create your models here.

class ChatDialog(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    modified = models.DateTimeField()

    def __str__(self):
        return f'{self.sender.name} & {self.receiver.name}'

class Message(models.Model):
    chatdialog = models.ForeignKey(ChatDialog, on_delete=models.CASCADE, related_name='chatdialog')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)