from django.contrib import admin
from .models import *
# Register your models here.

class ChatDialogModelAdmin(admin.ModelAdmin):
    list_filter = ('sender','receiver','modified')
    list_display = ('sender','receiver','modified')
    search_fields = ('modified','sender','receiver')

class MessageModelAdmin(admin.ModelAdmin):
    list_filter = ('timestamp','chatdialog','sender')
    list_display = ('timestamp','chatdialog','sender','is_read')
    search_fields = ('timestamp','chatdialog','sender')
    list_editable = ('is_read',)

admin.site.register(Message,MessageModelAdmin)
admin.site.register(ChatDialog,ChatDialogModelAdmin)