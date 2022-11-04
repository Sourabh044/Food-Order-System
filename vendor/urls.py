from django.urls import include, path
from .views import *
from accounts.views import VendorDashboard
urlpatterns = [
    path('',VendorDashboard,name='vendor'),
    path('profile/',VendorProfile,name='Vendor-Profile'), # Also We can say Restaurant Profile Page.
    path("menu-builder/", MenuBuilder, name="Menu-Builder"),
    path("menu-builder/category/<int:pk>", FoodItemByCategory, name="FoodItems-Categories"),
]
