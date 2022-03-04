from django.urls import path, include
from .views import *
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('register/', registration_view, name='register'),
    # path('login/', login_view, name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email_verify/', VerifyEmailAPIView.as_view(), name='email_verify'),



]
