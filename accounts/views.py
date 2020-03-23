from django.shortcuts import render
from .serializers import *
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from rest_framework import viewsets, exceptions
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework_swagger.views import get_swagger_view
import requests


class UserProfile(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class ValidatePhoneSendOTP(APIView):

    def post(self,reqeust,*args,**kwargs):
        phone_number = reqeust.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail':'Phone number already exists'
                })
            else:
                key=send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count >10:
                            return Response({
                                'status':False,
                                'detail':'Quota Exceeded for sending OTP'
                            })
                        old.count = count+1
                        old.save()
                        SENDSMS(phone,old.otp)
                        return Response({
                            'status': True,
                            'detail': 'OTP sent successfully'
                        })
                    else:
                        PhoneOTP.objects.create(
                            phone = phone,
                            otp = key,
                        )
                        SENDSMS(phone,key)
                        return Response({
                            'status': True,
                            'detail': 'OTP sent successfully'
                        })
                else:
                    return Response({
                        'status':False,
                        'detail':'Error while sending OTP'
                    })


        else:
            return Response({
                'status':False,
                'detail':"Please provide a phone number"
            })

def send_otp(phone):
    if phone:
        key=random.randint(999,9999)
        return key
    else:
        return False

def SENDSMS(phone,key):
    token = 'PvMofr71KjqsNyS810158AlqFwaCxdIOv0jw'
    to = phone
    sender = "Aashish"
    message = "Your One Time Password for GEMS registration is {}".format(key)
    url = 'http://beta.thesmscentral.com/api/v3/sms?token={}&sender={}&to={}&message={}'.format(token,sender,to,message)
    response = requests.get(url)
    if response.status_code !=200:
        print('Status:',response,'Problem With the request')

class ValidateOTP(APIView):

    def post(self,request,*args,**kwargs):
        phone = request.data.get('phone',False)
        otp_sent = request.data.get('otp',False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status':True,
                        'detail':'OTP Validated Successfully'
                    })
                else:
                    return Response({
                        'status':False,
                        'detail':'OTP Incorrect'
                    })

            else:
                return Response({
                    'status':False,
                    'detail':'Please generate OTP First'
                })

        else:
            return Response({
                'status':False,
                'detail':'Please enter both phonenumber and OTP'
            })

class Register(APIView):

    def post(self,request,*args,**kwargs):
        phone = request.data.get('phone',False)
        password = request.data.get('password',False)

        if phone and password:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                validated = old.validated

                if validated:
                    temp_data = {
                        'phone':phone,
                        'password':password
                    }
                    serializer = CreateUserSerializer(data=temp_data)
                    serializer.is_valid(raise_exception = True)
                    user = serializer.save()
                    old.delete()
                    return Response({
                        'status':True,
                        'detail':'Account Created'
                    })
                else:
                    return Response({
                        'status':False,
                        'detail':"OTP not verified.First Verify the OTP"
                    })
            else:
                return Response({
                    'status':False,
                    'detail':"Please verify phone first"
                })

class SwaggerRenderer(renderers.SwaggerUIRenderer):
    template = 'swagger_template.html'


class SwaggerView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        SwaggerRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator(
            title='Pastebin API',
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