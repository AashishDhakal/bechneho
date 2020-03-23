from __future__ import unicode_literals
from .models import *
from django.contrib.auth import get_user_model
from django.contrib import admin
User = get_user_model()

from django.contrib import admin
from .models import User

# Register your models here.
admin.site.register(User)