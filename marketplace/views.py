from django.shortcuts import render,get_object_or_404
from rest_framework.generics import CreateAPIView,ListAPIView,DestroyAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from accounts.permissions import IsUpdateProfile,IsOwnerOrReadOnly

class ImageCreate(APIView):
    '''
    This endpoint is used to create a fileupload.You will post a file to this endpoint's body and in response you will
    get the url to the file/image.This link will be now passed to those fields in database where image or files are required.
    '''
    parser_class = (FileUploadParser,)
    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=self.request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(ListAPIView):
    '''
    This enpoint list all the categories.
    '''
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.all()

class SubCategoryListView(ListAPIView):
    '''
    This endpoint lists subcategories under a category.
    You should pass category slug as query parameter.
    :parameter
    -slug
    '''
    serializer_class = SubCategorySerializer
    def get_queryset(self):
        return SubCategory.objects.filter(category__slug=self.request.query_params.get('slug'))

class AllSubCategoryListView(ListAPIView):
    '''
    This endpoint lists all the subcategories
    '''
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.all()

class CreateAdvertisementView(CreateAPIView):
    '''
    This endpoint is for creating a post/product or advertisement.A user needs to be logged in to create a post.So,its
    mandatory to pass in Authentication header while posting data.
    '''
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdvertisementListView(ListAPIView):
    '''
    This lists all the advertisements on a particular subcategory.
    You need to pass subcategory slug as query parameter.
    :parameter
    -subcategory_slug
    '''
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        subcategory = self.request.query_params.get('subcategory_slug')
        return Advertisement.objects.filter(subcategory__slug=subcategory)

class AdvertisementDetailView(ListAPIView):
    '''
    This is for detail listing a post/advertisement.Pass in post slug as a query parameter.
    :parameter
    -slug
    '''
    serializer_class = AdvertisementSerializer

    def get_serializer_context(self):
        session_key = 'viewed_topic_{}'.format(self.ad.slug)
        if not self.request.session.get(session_key, False):
            self.ad.views += 1
            self.ad.save()
            self.request.session[session_key] = True
        return super().get_serializer_context()

    def get_queryset(self):
        slug = self.request.query_params.get('slug')
        self.ad = get_object_or_404(Advertisement,slug=slug)
        queryset = Advertisement.objects.filter(slug=slug)
        return queryset

class MyAdvertisementsView(ListAPIView):
    '''
    This lists advertisements posted by logged in user.You need to pass authentication header.
    '''
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Advertisement.objects.filter(user=self.request.user)

class FeaturedAdvertisementsView(ListAPIView):
    '''
    Lists featured advertisements
    '''
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.filter(featured='Yes')

class RecentAdvertisementsView(ListAPIView):
    '''
    Lists recent advertisements
    '''
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.order_by('-published_at')

class PopularAdvertisementsView(ListAPIView):
    '''
    List popular advertisements
    '''
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.order_by('-views')

class AllAdvertisementsView(ListAPIView):
    '''
    List all the advertisements
    '''
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.all()

class ListUserAdvertisementView(ListAPIView):
    '''
    Lists advertisements posted by a particular user.You need to pass user id to get his/her posted ads.
    :parameter
    -id
    '''
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        userid = self.request.query_params.get('id')
        return Advertisement.objects.filter(user_id=userid)


class AdvertisementViewset(ModelViewSet):
    """
    Updates advertisement on put request and deletes advertisement on delete request
    You dont need to pass user id to get advertisement,but need to pass authentication token header.For updating and deleting
    a advertisement,you need to pass authentication token header and the corresponding advertisement id as well.
    """

    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ['put','delete','head']
    queryset = Advertisement.objects.none()

    def get_queryset(self):
        if self.request.user.is_staff:
            return Advertisement.objects.all()
        return Advertisement.objects.filter(user_id=self.request.user.pk)

    def get_permissions(self):
        if self.request.method =='put' or self.request.method =='delete':
            self.permission_classes =[IsAuthenticated,IsOwnerOrReadOnly]
        else:
            self.permission_classes=[IsAuthenticated,]

