from django.urls import include, path
from .views import *
urlpatterns = [
    path('register-user',Register_User,name='Register-User')
]
