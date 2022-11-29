from django.contrib import admin
from django.urls import include, path
from FoodOnline.views import HomeView
from django.conf import settings
from django.conf.urls.static import static
from marketplace.views import CartView
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView, name="Home"),
    path("", include("accounts.urls")),

<<<<<<< HEAD
    # Marketplace
    path("marketplace/", include("marketplace.urls")),

    # Cart
    path('cart/', CartView, name='CartView'),

    # Search

=======
    path("marketplace/", include("marketplace.urls")),


    path('cart/', CartView,name='CartView'),
>>>>>>> c64ac00cf1bee929791284b6fa6d91e088e004ab

] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
