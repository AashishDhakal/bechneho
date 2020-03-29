from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

User = get_user_model()
# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.category)
        super(Category,self).save(*args,**kwargs)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='adcategory')
    Sub_Category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images',blank=True)
    slug = models.SlugField(blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.Sub_Category)
        super(SubCategory,self).save(*args,**kwargs)

    def __str__(self):
        return self.Sub_Category

    class Meta:
        verbose_name_plural = "Sub Categories"

class Advertisement(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='aduser')
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='addsubcategory')
    published_at = models.DateTimeField(auto_now_add=True)
    ad_title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    ads_validity = models.DateField()
    price = models.CharField(max_length=30)
    image1 = models.TextField(blank=True)
    image2 = models.TextField(blank=True)
    image3 = models.TextField(blank=True)
    image4 = models.TextField(blank=True)
    image5 = models.TextField(blank=True)
    image6 = models.TextField(blank=True)
    image7 = models.TextField(blank=True)
    image8 = models.TextField(blank=True)
    image9 = models.TextField(blank=True)
    image10 = models.TextField(blank=True)
    negotiable = models.CharField(max_length=10,choices=(
        ('Yes','Yes'),
        ('No','No')),blank=True)
    condition = models.CharField(max_length=30,choices=(
        ('Brand New','Brand New'),
        ('Like New(Used Few Times)','Like New(Used Few Times)'),
        ('Excellent','Excellent'),
        ('Good','Good'),
        ('Not Working','Not Working')),blank=True)
    used_for = models.CharField(max_length=100,blank=True)
    home_delivery = models.CharField(max_length=30,choices=(
        ('Available','Available'),
        ('Not Available','Not Available')),blank=True)
    delivery_areas = models.CharField(max_length=100,choices=(
        ('Within My Area','Within my area'),
        ('Within My City','Within my city'),
        ('All over Nepal','All over Nepal')),blank=True)
    delivery_charges = models.CharField(max_length=30,blank=True)
    warranty_type = models.CharField(max_length=30,choices=(
        ('Seller/Shop','Seller/Shop'),
        ('Manufacuturer/Importer','Manufacturer/Importer'),
        ('No Warranty','No Warranty')),blank=True)
    warranty_period = models.CharField(max_length=100,blank=True)
    warranty_includes = models.CharField(max_length=300,blank=True)
    featured = models.CharField(max_length=30,choices=(
        ('Yes','Yes'),
        ('No','No')),blank=True,default='n')
    ad_status = models.CharField(max_length=30,choices=(
        ('Available','Available'),
        ('Sold Out','Sold Out')),blank=True,default='a')
    views = models.BigIntegerField(default=0)
    location = JSONField(default=None)

    def save(self,*args,**kwargs):
        super(Advertisement, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = "bh" + str(self.id) + "-" + slugify(self.ad_title)
            self.save()


    def __str__(self):
        return self.ad_title

class Image(models.Model):
    image = models.ImageField(upload_to="images")
    def __str__(self):
        return self.image.url

