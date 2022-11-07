from django.shortcuts import get_object_or_404, render, redirect
from .forms import VendorRegisterForm
from accounts.forms import UserProfileForm
from menu.forms import CategoryForm, FoodItemForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from menu.models import FoodItem, Category
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from django.template.defaultfilters import slugify

# Create your views here.


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url="Login")
@user_passes_test(check_role_vendor)
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


@login_required(login_url="Login")
@user_passes_test(check_role_vendor)
def MenuBuilder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        "vendor": vendor,
        "categories": categories,
    }
    return render(request, "vendor/menu-builder.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_vendor)
def FoodItemByCategory(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    food_items = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        "food_items": food_items,
        "category": category,
    }
    
    return render(request, "vendor/fooditems_by_categories.html", context)


#  ------------------------- CRUD OF THE FOOOD ITEMS -----------------------------------


def AddCategory(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            category = form.save(commit=False)
            vendor = get_vendor(request)
            category.vendor = vendor
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category added successfully")
            return redirect("Menu-Builder")
    context = {"form": form}
    return render(request, "vendor/add-category.html", context)


def UpdateCategory(request, pk=None):
    if pk:
        category = get_object_or_404(Category, pk=pk)
        if request.method == "POST":
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                category_name = form.cleaned_data["category_name"]
                category = form.save(commit=False)
                vendor = get_vendor(request)
                category.vendor = vendor
                category.slug = slugify(category_name)
                form.save()
                messages.success(request, "Category updated successfully")
                return redirect("Menu-Builder")
            else:
                print(form.errors)
        else:
            form = CategoryForm(instance=category)
        context = {
            "form": form,
            "category": category,
        }
        return render(request, "vendor/update-category.html", context)
    else:
        return redirect("403.html")


def DeleteCategory(request, pk=None):
    if pk:
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, "Category removed.")
        return redirect("Menu-Builder")
    else:
        return redirect("403.html")


#  ------------------------- CRUD OF THE FOOOD ITEMS ------------------------------------#


def AddFood(request):

    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data["food_title"]
            fooditem = form.save(commit=False)
            fooditem.vendor = get_vendor(request)
            fooditem.slug = slugify(food_title)
            form.save()
            messages.success(request, "Food added successfully")
            return redirect("Menu-Builder")
        else:
            print(form.errors)
            return render(request, "vendor/add-food.html", context={"form": form})
    form = FoodItemForm()
    form.fields["category"].queryset = Category.objects.filter(
        vendor=get_vendor(request)
    )
    context = {"form": form}
    return render(request, "vendor/add-food.html", context)


def UpdateFood(request, pk=None):
    if pk:
        food = get_object_or_404(FoodItem, pk=pk)
        form = FoodItemForm(instance=food)
        if request.method == "POST":
            form = FoodItemForm(request.POST, instance=food)
            if form.is_valid():
                form.save()
                messages.success(request, f"{food.food_title} Updated successfully")
                return redirect("Menu-Builder")
            else:
                print(form.errors)

        form.fields["category"].queryset = Category.objects.filter(
            vendor=get_vendor(request)
        )
        context = {
            "form": form,
            "food": food,
        }
        # messages.success(request,'Food item deleted successfully')
        return render(request, "vendor/update-food.html", context)
    else:
        messages.error(request, "Food does not exist.")


def DeleteFood(request, pk=None):
    if pk:
        food = FoodItem.objects.get(id=pk)
        food.delete()
        messages.success(request, "Food item deleted successfully")
        return redirect("Menu-Builder")
    else:
        messages.error(request, "Food does not exist.")
        return redirect("Menu-Builder")
        return redirect("Menu-Builder")
