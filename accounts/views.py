from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages, auth

from accounts.models import User, UserProfile
from accounts.utils import detectUser, send_verification_email
from vendor.forms import VendorRegisterForm
from vendor.models import Vendor
from .forms import UserRegisterForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator

# Restrict Customer from acessing the Vendor Dashboard
def check_role_vendor(user):
    try:
        if user.role == 1:
            return True
        else:
            raise PermissionDenied
    except:
        raise PermissionDenied

# Restrict the Vendor from accessing the Customer
def check_role_customer(user):
    try:
        if user.role == 2:
            return True
        else:
            raise PermissionDenied
    except:
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
            mail_subject = "Confirm Your Registration"
            template_name = "accounts/emails/account_verification_email.html"
            send_verification_email(request, user, mail_subject, template_name)
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
            mail_subject = "Confirm Your Registration"
            template_name = "accounts/emails/account_verification_email.html"
            send_verification_email(request, user, mail_subject, template_name)
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
    if request.user.is_anonymous:
        messages.warning(request, "You Need To login!!")
        return redirect("Login")
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)


@user_passes_test(check_role_customer)
def CustomerDashboard(request):
    if request.user.is_anonymous:
        messages.warning(request, "You Need To login!!")
        return redirect("Login")
    return render(
        request,
        "accounts/userdashboard.html",
    )

@login_required(login_url="Login")
@user_passes_test(check_role_vendor)
def VendorDashboard(request):
    # if request.is_anonymous:
    #     messages.warning(request, "You Need To login!!")
    #     return redirect("Login")
    vendor = Vendor.objects.get(user=request.user)
    context = {"vendor": vendor}
    return render(request, "accounts/vendordashboard.html", context)


def Activate(request, uidb64, token):
    try:
        print(type(uidb64), type(token))
        from django.utils.encoding import force_bytes, force_str
        from django.utils.http import urlsafe_base64_decode

        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(id=uid)
    except (OverflowError, User.DoesNotExist, TypeError, ValueError) as e:
        print(e)
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your Account has been Verified")
        return redirect("My-Account")
    else:
        messages.error(request, "Invalid Token Address")
        return redirect("My-Account")


def Forgot_Password(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already Logged in.!")
        return redirect("Home")
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # sending the password resetting maiil
            mail_subject = "Reset Password"
            template_name = "accounts/emails/account_password_reset_email.html"
            send_verification_email(request, user, mail_subject, template_name)
            messages.success(request, "Reset link has been sent")
            return redirect("Login")
        else:
            messages.error(request, "User with email does not exist!")
            return redirect("Forgot-Password")

    return render(request, "accounts/forgot-password.html")


def Reset_Password_Validate(request, uidb64, token):
    try:
        print(type(uidb64), type(token))
        from django.utils.encoding import force_bytes, force_str
        from django.utils.http import urlsafe_base64_decode

        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        user = User._default_manager.get(id=uid)
        print(user)
    except (OverflowError, User.DoesNotExist, TypeError, ValueError) as e:
        print(e)
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please Enter Your New Password")
        return redirect("Reset-Password")
    else:
        messages.error(request, "expired token")
        return redirect("Login")


def Reset_Password(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already Logged in.!")
        return redirect("Home")
    if request.method == "POST":
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        if password == confirmpassword:
            pk = request.session["uid"]
            user = User.objects.get(id=pk)
            user.set_password(password)
            user.save()
            messages.success(request, "Your password is changed!")
            return redirect("Login")
        else:
            messages.error(request, "Password does not match!!")
            return redirect("Reset-password")
    return render(request, "accounts/reset-password.html")
