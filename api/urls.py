from rest_framework.authtoken import views
from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'User', UserViewset, basename='User')
router.register(r'UserProfile', UserProfileViewset, basename='UserProfile')


urlpatterns = [
    path('token/', views.obtain_auth_token),
]

urlpatterns += router.urls
