from django.contrib import admin
from .models import *
# Register your models here.

class AdvertisementModelAdmin(admin.ModelAdmin):
    list_editable = ('featured',)
    list_display = ('user','subcategory','ad_title','published_at','ads_validity','price','featured')
    list_filter = ('user','subcategory','ad_title','published_at','ads_validity','price','featured','ad_status')
    search_fields = ('user','subcategory','ad_title','published_at','ads_validity','price','featured')

class ImageModelAdmin(admin.ModelAdmin):
    list_display = ('image',)
    search_fields = ('image',)

class SubcategoryInline(admin.TabularInline):
    model = SubCategory

class CategoryAdmin(admin.ModelAdmin):
    inlines = (SubcategoryInline,)

class AdvertisementInline(admin.TabularInline):
    model = Advertisement

class SubCategoryAdmin(admin.ModelAdmin):
    inlines = (AdvertisementInline,)

admin.site.register(Advertisement,AdvertisementModelAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Image,ImageModelAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)