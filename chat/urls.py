from django.urls import path
from .views import *

urlpatterns=[
    path('messagedetail/',MessageDetails.as_view()),
    path('createmessage/',CreateMessage.as_view()),
    path('listchatdialog/',ChatDialogView.as_view()),
]