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

    path("marketplace/", include("marketplace.urls")),


    path('cart/', CartView,name='CartView'),

] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
