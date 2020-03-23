from django.urls import path
from .views import *

urlpatterns=[
    path('myads/',MyAdvertisementsView.as_view(),name='myads'),
    path('featured/',FeaturedAdvertisementsView.as_view(),name='featured'),
    path('recent/',RecentAdvertisementsView.as_view(),name='recent'),
    path('popular/',PopularAdvertisementsView.as_view(),name='popular'),
    path('allsubcategories/',AllSubCategoryListView.as_view(),name='allsubcategories'),
    path('listuserads/',ListUserAdvertisementView.as_view(),name='listuserads'),
]