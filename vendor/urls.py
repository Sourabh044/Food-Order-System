from django.urls import include, path
from .views import *
from accounts.views import VendorDashboard
urlpatterns = [
    path('',VendorDashboard,name='vendor'),
    path('profile/',VendorProfile,name='Vendor-Profile'), # Also We can say Restaurant Profile Page.
    path("menu-builder/", MenuBuilder, name="Menu-Builder"),
    path("menu-builder/category/<int:pk>", FoodItemByCategory, name="FoodItems-Categories"),


    # Categories CRUD

    path("menu-builder/category/add", AddCategory, name="Add-Category"),
    path("menu-builder/category/update/<int:pk>", UpdateCategory, name="Update-Category"),
    path("menu-builder/category/delete/<int:pk>", DeleteCategory, name="Delete-Category"),


]
