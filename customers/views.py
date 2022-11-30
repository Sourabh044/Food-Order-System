from django.shortcuts import redirect
from django.shortcuts import render
from accounts.forms import UserProfileForm, CustomerForm
from accounts.models import UserProfile

from django.contrib import messages
# Create your views here.


def CustomerProfile(request):
    customer = request.user
    userprofile = UserProfile.objects.get(user=customer)
    if request.method == 'POST':
        c_form = CustomerForm(request.POST, request.FILES, instance=customer)
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)
        if c_form.is_valid() and user_profile_form.is_valid():
            c_form.save()
            user_profile_form.save()
            messages.success(request, 'Successfully updated profile!')
            return redirect('Customer-Profile')
    c_form = CustomerForm(instance=customer)
    user_profile_form = UserProfileForm(instance=userprofile)
    context = {
        'customer': customer,
        'c_form': c_form,
        'user_profile_form': user_profile_form
    }
    return render(request, 'customers/customer-profile.html', context)
