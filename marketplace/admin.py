from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Advertisement)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Image)