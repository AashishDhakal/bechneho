from django.shortcuts import render,get_object_or_404
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser

class ImageCreate(APIView):
    parser_class = (FileUploadParser,)
    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=self.request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.all()

class SubCategoryListView(ListAPIView):
    serializer_class = SubCategorySerializer
    def get_queryset(self):
        return SubCategory.objects.filter(category__slug=self.request.query_params.get('slug'))

class AllSubCategoryListView(ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.all()

class CreateAdvertisementView(CreateAPIView):
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdvertisementListView(ListAPIView):
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        subcategory = self.request.query_params.get('subcategory_slug')
        return Advertisement.objects.filter(subcategory__slug=subcategory)

class AdvertisementDetailView(ListAPIView):
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
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Advertisement.objects.filter(user=self.request.user)

class FeaturedAdvertisementsView(ListAPIView):
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.filter(featured='y')

class RecentAdvertisementsView(ListAPIView):
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.order_by('-published_at')

class PopularAdvertisementsView(ListAPIView):
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.order_by('-views')

class AllAdvertisementsView(ListAPIView):
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.all()

class ListUserAdvertisementView(ListAPIView):
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        userid = self.request.query_params.get('id')
        return Advertisement.objects.filter(user_id=userid)