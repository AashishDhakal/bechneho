from django.urls import path
from .views import *

urlpatterns=[
    path('createpost/',CreateAdvertisementView.as_view(),name='createad'),
    path('postlist/',AdvertisementListView.as_view(),name='listpost'),
    path('postview/',AdvertisementDetailView.as_view(),name='viewpost'),
    path('myads/',MyAdvertisementsView.as_view(),name='myads'),
    path('featured/',FeaturedAdvertisementsView.as_view(),name='featured'),
    path('recent/',RecentAdvertisementsView.as_view(),name='recent'),
    path('popular/',PopularAdvertisementsView.as_view(),name='popular'),
    path('advertisements/',AllAdvertisementsView.as_view(),name='advertisements'),
    path('allsubcategories/',AllSubCategoryListView.as_view(),name='allsubcategories'),
    path('listuserads/',ListUserAdvertisementView.as_view(),name='listuserads'),
]