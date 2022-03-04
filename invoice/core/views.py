from invoice_engine.tasks import send_verification_email
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import generics
import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
# from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.sites.shortcuts import get_current_site
from .serializers import UserSerializer, AuthCustomTokenSerializer
from .models import User
from django.conf import settings


# from .utils import Util


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request)
        relativeLink = reverse('email_verify')
        absurl = 'http://'+str(current_site) + \
            str(relativeLink)+"?token="+str(token)
        email_body = 'Hi ' + user.email + \
            ', use link bellow to verify your email \n' + absurl
        data = {'email_body': email_body,
                'email_subject': 'Verify your email', 'to_email': user.email}
        # Util.send_email(data)
        send_verification_email.delay(data)

        return Response(f"You need to verify your email: {user_data['email']}")


class VerifyEmailAPIView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(pk=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'})
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation expired'})
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'})


class LoginAPIView(generics.GenericAPIView):
    serializer_class = AuthCustomTokenSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data.get('email')
        user = User.objects.get(email=user_email)
        if user.is_active:
            user_token, created = Token.objects.get_or_create(user=user)
            return Response({'token': user_token.key, })
        else:
            return Response({'error': 'Verify your email'})

# @api_view(['POST', ])
# def registration_view(request):

#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             user = serializer.save()
#             data['response'] = "Successfully registered a new user"
#             data['email'] = user.email
#             # token = Token.objects.get(user=user).key
#             # data['token'] = token
#         else:
#             data = {'serializer.errors': serializer.errors}
#         return Response(data)

# @api_view(['POST', ])
# def login_view(request):

#     if request.method == 'POST':
#         serializer = AuthCustomTokenSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             print(serializer.data)
#             user_email = serializer.data.get('email')
#             user = User.objects.get(email=user_email)
#             user_token, created = Token.objects.get_or_create(user=user)
#             print(user_token)

#             return Response({
#                 'token': user_token.key,
#                 'email': request.POST.get('email')
#             })
#         else:
#             data = {'serializer.errors': serializer.errors}
#         return Response(data)


# class CustomAuthToken(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })


# class CustomAuthToken(APIView):

#     class Meta:
#         model = User
#         serializer_class = AuthCustomTokenSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })
