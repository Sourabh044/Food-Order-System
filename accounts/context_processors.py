from vendor.models import Vendor, UserProfile
from django.conf import settings as s

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)


def get_google_api_key(request):
    return {'GOOGLE_API_KEY':s.GOOGLE_API_KEY}