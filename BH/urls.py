from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from marketplace.views import ImageCreate
from accounts.views import SwaggerView
from rest_framework.routers import DefaultRouter
from marketplace.views import *
from accounts.views import *


router = DefaultRouter()

router.register('api/accounts/userprofile',UserProfile)
router.register('api/market/updatedeletepost',AdvertisementViewset)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/',include('accounts.urls')),
    path('api/market/',include('marketplace.urls')),
    path('api/fileupload/',ImageCreate.as_view(),name="fileupload"),
    path('api/chat/',include('chat.urls')),
    path('docs/', SwaggerView.as_view()),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

urlpatterns += router.urls
