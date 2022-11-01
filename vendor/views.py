from django.shortcuts import render

# Create your views here.
def VendorProfile(request):
    return render(request,'vendor/vendor-profile.html')
