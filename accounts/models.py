from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models import Q
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import random
import os
import requests

class UserManager(BaseUserManager):
    def create_user(self,phone,password=None,is_staff=False,is_active=True,is_admin=False):
        if not phone:
            raise ValueError("User must have a phone number")
        if not password:
            raise ValueError("User must have a password")

        user_obj = self.model(phone=phone)
        user_obj.set_password(password)
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,phone,password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self,phone,password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message="Phone number must be entered with the area code format like +977980000000000")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    name = models.CharField(max_length=20,null=True,blank=True)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.name:
            return self.name
        else:
            return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active




class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex= r'^\+?1?\d{9,14}$',message="Phone number must be entered with the area code format like +977980000000000")
    phone = models.CharField(validators=[phone_regex],max_length=17,unique=True)
    otp = models.CharField(max_length=9,blank=True,null=True)
    count = models.IntegerField(default=0,help_text="Number of times otp is sent")
    validated = models.BooleanField(default=False,help_text="If it is true user hava validated OTP successfully")

    def __str__(self):
        return str(self.phone) + 'is sent' + str(self.otp)
