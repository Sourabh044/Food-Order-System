from django.shortcuts import get_object_or_404, render, redirect
from .forms import VendorRegisterForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages


# Create your views here.


def VendorProfile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == "POST":
        vendor_form = VendorRegisterForm(request.POST, request.FILES, instance=vendor)
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile
        )
        if user_profile_form.is_valid() and vendor_form.is_valid():
            user_profile_form.save()
            vendor_form.save()
            messages.success(request, "Your Profile Has been updated.")
            return redirect("Vendor-Profile")
        else:
            print(user_profile_form.errors)
            print(vendor_form.errors)
    else:
        vendor_form = VendorRegisterForm(instance=vendor)
        user_profile_form = UserProfileForm(instance=user_profile)
    context = {"vendor_form": vendor_form, "user_profile_form": user_profile_form}
    return render(request, "vendor/vendor-profile.html", context)
