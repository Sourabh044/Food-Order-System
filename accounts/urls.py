from django.urls import include, path
from .views import *
urlpatterns = [
    path('register-user',Register_User,name='Register-User'),
    path('register-vendor',Register_Vendor,name='Register-Vendor'),
    path('login-user',Login_User,name='Login-User'),
]
