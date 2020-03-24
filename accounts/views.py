from rest_framework import viewsets, exceptions
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_swagger.views import get_swagger_view
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from .models import User
from .permissions import StaffPermission
from .serializers import UserSerializer


class UserAPIViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (StaffPermission, )
    queryset = User.objects.none()

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)


class UserProfile(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ['get','put','delete','head']
    queryset = User.objects.none()

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)



class Register(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

class SwaggerRenderer(renderers.SwaggerUIRenderer):
    template = 'swagger_template.html'


class SwaggerView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    permission_classes = [StaffPermission,]
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        SwaggerRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator(
            title='BechneHo Documentation',
            url=None,
            patterns=None,
            urlconf=None
        )
        schema = generator.get_schema(request=request)

        if not schema:
            raise exceptions.ValidationError(
                'The schema generator did not return a schema Document'
            )

        return Response(schema, template_name='swagger_template2.html')