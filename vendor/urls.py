from django.urls import include, path
from .views import *
from accounts.views import VendorDashboard
urlpatterns = [
    path('',VendorDashboard,name='vendor'),
    path('profile/',VendorProfile,name='Vendor-Profile') # Also We can say Restaurant Profile Page.
]
