from cgi import print_arguments
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from accounts.models import User
from .forms import UserRegisterForm
from django.contrib.auth.hashers import make_password

# Create your views here.
def Register_User(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            # user.password = user.set_password(request.POST.get('password'))
            user.password = make_password(request.POST.get("password"))
            user.save()
            messages.success(request, "Your Account has been created.")
            return redirect("Home")
        else:
            print("invalid form") 
            print(form.errors)
            messages.error(request, "An Error Occured.")
            return render(request, "accounts/register-user.html", {"form": form})
            # return HttpResponse(form.errors.as_ul())
    else: 
        form = UserRegisterForm()
        return render(request, "accounts/register-user.html", {"form": form})


def Register_Vendor(request):
    form = UserRegisterForm()
    return render(request,"accounts/register-vendor.html",{'form':form,})

def Login_User(request):
    return HttpResponse('LoginPage')