from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from marketplace.context_processors import get_cart_count
from vendor.models import Vendor
from menu.models import FoodItem, Category
from django.db.models import Prefetch
from .models import Cart

# Create your views here.


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    context = {"vendors": vendors, "vendors_count": vendors.count()}
    return render(request, "marketplace/listings.html", context)


def VendorDetail(request, vendor_slug):
    if vendor_slug:
        vendor = Vendor.objects.get(vendor_slug=vendor_slug)
        categories = Category.objects.filter(vendor=vendor).prefetch_related(
            Prefetch("fooditems", queryset=FoodItem.objects.filter(is_available=True))
        )

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
            print(cart)
        else:
            cart = None

        context = {
            "vendor": vendor,
            "categories": categories,
            "cart": cart,
        }
    return render(request, "marketplace/vendor-details.html", context)


def AddToCart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    chkcart.quantity += 1
                    chkcart.save()
                    return JsonResponse(
                        {"success": True, "message": "Increased the cart", 'cart_count':get_cart_count(request), 'qty':chkcart.quantity}
                    )
                except:
                    cart = Cart.objects.create(
                        user=request.user, fooditem=fooditem, quantity=1
                    )
                    return JsonResponse({"success": True, "message": "Added to cart", 'cart_count':get_cart_count(request), 'qty':chkcart.quantity})
            except:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Food item does not exist",
                    }
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Invalid Request",
                }
            )
    else:
        return JsonResponse(
            {
                "success": False,
                "message": "User is not authenticated",
            }
        )


# def DecreaseCart(request,pk=None):
#     if request.user.is_authenticated:
#         if request.headers.get('x-requested-with')=='XMLHttpRequest':
#             try:
#                 fooditem = FoodItem.objects.get(id=pk)
#                 chkcart = Cart.objects.get(user=request.user)
#             except:

#     else:
#         return JsonResponse({
#         'success': False,
#         'message': 'User is not authenticated',
#     })
