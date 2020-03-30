from rest_framework import viewsets, exceptions
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from fcm_django.models import FCMDevice
from .serializers import CreateFCMDeviceSerializer
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import Token

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
    """
    Return a user profile on get request,updates user profile on put request and deletes user profile on delete request
    You dont need to pass user id to get profile,but need to pass authentication token header.For updating and deleting
    a user profile,you need to pass authentication token header and the corresponding user id as well.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ['get','put','delete','head']
    queryset = User.objects.none()

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)



class Register(CreateAPIView):
    '''
    This endpoint is used to register a new user.You need to create a post request with all the data in body.
    '''
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        user = User.objects.get(id=instance.id)
        current_site = get_current_site(self.request)
        token = account_activation_token.make_token(user)
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'token':token,
        })
        tokenobject=Token.objects.create(user=user,token=token)
        tokenobject.save()
        user.email_user('Activate Your BechneHo Account',message=message)

class ResendVerificationEmail(APIView):
    '''
    Send a post request with user email requesting a verification email again.
    parameter for posting user email is
    :parameter
    useremail
    '''
    def post(self, request, *args, **kwargs):
        useremail=self.request.POST.get('useremail')
        try:
            user = User.objects.get(email=useremail)
        except User.DoesNotExist:
            user = None
        if user is not None:
            current_site = get_current_site(self.request)
            savedtoken = Token.objects.get(user=user)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'token': savedtoken.token,
            })
            user.email_user('Activate Your BechneHo Account',message=message)
            return Response("Resend Successful.Please check your email.")
        else:
            return Response("User with provided email doesnot exist.")

class ActivateUserView(APIView):

    def get(self,request,*args,**kwargs):
        token = self.request.query_params.get('token')
        savedtoken = None
        try:
            savedtoken = Token.objects.get(token=token)
            user = savedtoken.user
        except(TypeError, ValueError, OverflowError, Token.DoesNotExist):
            user = None
        if user is not None and token==savedtoken.token:
            user.is_active = True
            user.save()
            savedtoken.delete()
            return Response('Thank you for your email confirmation. Now you can login your account.')
        else:
            return Response('Activation link is invalid!')

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

def privacy(request):
    return render(request,'privacy.html', {})

class FCMDeviceCreateView(APIView):

    def post(self, request,*args,**kwargs):
        device_id = request.data.get('device_id')
        print(request.data)
        try:
            fcmobject = FCMDevice.objects.get(device_id=device_id)
            data = request.data
            data = data.copy()
            serializer = CreateFCMDeviceSerializer(fcmobject,data=data)
        except FCMDevice.DoesNotExist:
            data = request.data
            serializer = CreateFCMDeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
