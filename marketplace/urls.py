from django.urls import include, path
from .views import *
urlpatterns = [
    path('',marketplace,name='marketplace'),
    path('<slug:vendor_slug>/',VendorDetail,name='Vendor-Detail'),

    path('add-to-cart/<int:food_id>',AddToCart,name='Add-To-Cart')
]