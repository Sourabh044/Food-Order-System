from django.urls import include, path
from .views import *

urlpatterns = [
    path("register-user", Register_User, name="Register-User"),
    path("register-vendor", Register_Vendor, name="Register-Vendor"),
    path("login-user", Login_User, name="Login"),
    path("logout-user", Logout_User, name="Logout"),
    path("my-account", Myaccount, name="My-Account"),
    path("vendordashboard", VendorDashboard, name="Vendor-Dashboard"),
    path("custdashboard", CustomerDashboard, name="Customer-Dashboard"),
    path("activate/<uidb64>/<token>/", Activate, name="Activate-User"),
    path("forgot-password", Forgot_Password, name="Forgot-Password"),
    path(
        "reset-password-validate/<uidb64>/<token>/",
        Reset_Password_Validate,
        name="Reset-Password-Validate",
    ),
    path("reset-password/", Reset_Password, name="Reset-Password"),
    path("vendor/", include("vendor.urls")),
    path('customer/', include("customers.urls")),
]
