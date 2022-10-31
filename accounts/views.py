from cgi import print_arguments
from re import L
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages, auth

from accounts.models import User, UserProfile
from accounts.utils import detectUser
from vendor.forms import VendorRegisterForm
from vendor.models import Vendor
from .forms import UserRegisterForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

# Restrict Customer from acessing the Vendor Dashboard
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the Vendor from accessing the Customer
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# Create your views here.
def Register_User(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already Logged in.!")
        return redirect("Dashboard")

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
    if request.user.is_authenticated:
        messages.warning(request, "You are already Logged in.!")
        return redirect("Dashboard")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        v_form = VendorRegisterForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            user = form.save(commit=False)
            user.role = User.RESTAURANT
            # user.password = user.set_password(request.POST.get('password'))
            user.password = make_password(request.POST.get("password"))
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get(user=user)
            vendor.save()
            messages.success(
                request, "Your Account has been created. Please Wait For the Approval."
            )
            return redirect("Home")
        else:
            print("invalid form")
            print(form.errors)
            print(v_form.errors)
            messages.error(request, "An Error Occured.")
            return render(
                request,
                "accounts/register-vendor.html",
                {"form": form, "v_form": v_form},
            )
            # return HttpResponse(form.errors.as_ul())
    else:
        form = UserRegisterForm()
        v_form = VendorRegisterForm()
        return render(
            request, "accounts/register-vendor.html", {"form": form, "v_form": v_form}
        )


def Login_User(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already Logged in.!")
        return redirect("Home")

    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
        if not user is None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("My-Account")
        else:
            messages.error(request, "Invalid Login Credenatials")
            return redirect("Login")
    return render(request, "accounts/login.html")


def Logout_User(request):
    auth.logout(request)
    return redirect("Login")


@login_required(login_url="Login")
def Myaccount(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You Need To login!!")
        return redirect("Login")
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)

@user_passes_test(check_role_customer)
def CustomerDashboard(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You Need To login!!")
        return redirect("Login")
    return render(
        request,
        "accounts/userdashboard.html",
    )

@user_passes_test(check_role_vendor)
def VendorDashboard(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You Need To login!!")
        return redirect("Login")
    return render(
        request,
        "accounts/vendordashboard.html",
    )
