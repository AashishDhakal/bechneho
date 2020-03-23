from django.urls import path
from .views import *

urlpatterns=[
    path('messagedetail/',MessageDetails.as_view(),name='messagedetails'),
    path('createmessage/',CreateMessage.as_view(),name='createmessage'),
    path('userlist/',MessageUserlist.as_view(),name='messageuserlist'),
]