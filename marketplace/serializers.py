from rest_framework import serializers
from .models import *
from accounts.serializers import UserSerializer

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class AdvertisementSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    slug = serializers.SlugField(required=False)
    image1 = serializers.CharField(required=False)
    image2 = serializers.CharField(required=False)
    image3 = serializers.CharField(required=False)
    image4 = serializers.CharField(required=False)
    image5 = serializers.CharField(required=False)
    image6 = serializers.CharField(required=False)
    image7 = serializers.CharField(required=False)
    image8 = serializers.CharField(required=False)
    image9 = serializers.CharField(required=False)
    image10 = serializers.CharField(required=False)
    featured = serializers.CharField(required=False,initial='n')
    ad_status = serializers.CharField(required=False,initial='a')
    views = serializers.IntegerField(required=False)
    subcategory=serializers.SlugRelatedField(slug_field='Sub_Category',queryset=SubCategory.objects.all())

    class Meta:
        model = Advertisement
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = '__all__'



