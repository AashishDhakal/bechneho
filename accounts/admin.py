from __future__ import unicode_literals
from .models import *
from django.contrib.auth import get_user_model
from django.contrib import admin
User = get_user_model()

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm,UserAdminChangeForm

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('first_name','last_name','email',)
    list_filter = ('is_staff','is_active','is_superuser')
    fieldsets = (
        (None,{'fields':('email','password')}),
        ('Personal Info',{'fields':('first_name','last_name','mobile')}),
        ('Permissions',{'fields':('is_staff','is_active','is_superuser')}),
    )

    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2')
        }),
    )

    search_fields = ('email','first_name','last_name')
    ordering = ('email','first_name','last_name')
    filter_horizontal = ()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request,obj)

admin.site.register(User,UserAdmin)

