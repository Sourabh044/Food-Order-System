from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from marketplace.context_processors import get_cart_amount, get_cart_count
from vendor.models import Vendor
from menu.models import FoodItem, Category
from django.db.models import Prefetch, Q
from .models import Cart
from django.contrib.auth.decorators import login_required

from django.contrib.gis.geos import GEOSGeometry
# ``D`` is a shortcut for ``Distance``
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

# Create your views here.


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    context = {"vendors": vendors, "vendors_count": vendors.count()}
    return render(request, "marketplace/listings.html", context)


def VendorDetail(request, vendor_slug):
    if vendor_slug:
        vendor = Vendor.objects.get(vendor_slug=vendor_slug)
        categories = Category.objects.filter(vendor=vendor).prefetch_related(
            Prefetch("fooditems", queryset=FoodItem.objects.filter(
                is_available=True))
        )

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
            # print(cart)
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
                    chkcart = Cart.objects.get(
                        user=request.user, fooditem=fooditem)
                    chkcart.quantity += 1
                    chkcart.save()
                    return JsonResponse(
                        {
                            "status": True,
                            "message": "Increased the cart",
                            "cart_count": get_cart_count(request),
                            "qty": chkcart.quantity,
                            "cart_amount": get_cart_amount(request),
                        }
                    )
                except:
                    cart = Cart.objects.create(
                        user=request.user, fooditem=fooditem, quantity=1
                    )
                    return JsonResponse(
                        {
                            "status": True,
                            "message": "Added to cart",
                            "cart_count": get_cart_count(request),
                            "qty": cart.quantity,
                            "cart_amount": get_cart_amount(request),
                        }
                    )
            except:
                return JsonResponse(
                    {
                        "status": False,
                        "message": "Food item does not exist",
                    }
                )
        else:
            return JsonResponse(
                {
                    "status": False,
                    "message": "Invalid Request",
                }
            )
    else:
        return JsonResponse(
            {
                "status": "login_required",
                "message": "Please Login To Continue",
            }
        )


def DecreaseCart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkcart = Cart.objects.get(
                        user=request.user, fooditem=fooditem)
                    if chkcart.quantity > 1:
                        chkcart.quantity -= 1
                        chkcart.save()
                    else:
                        chkcart.delete()
                        chkcart.quantity = 0
                    return JsonResponse(
                        {
                            "status": "Success",
                            "message": "Decreased the cart",
                            "cart_count": get_cart_count(request),
                            "qty": chkcart.quantity,
                            "cart_amount": get_cart_amount(request),
                        }
                    )
                except:
                    return JsonResponse(
                        {
                            "status": "Failed",
                            "message": "You Dont have this item in cart",
                        }
                    )
            except:
                return JsonResponse(
                    {
                        "status": "Failed",
                        "message": "Food item does not exist",
                    }
                )
        else:
            return JsonResponse(
                {
                    "status": "Failed",
                    "message": "Invalid Request",
                }
            )
    else:
        return JsonResponse(
            {
                "status": "login_required",
                "message": "User is not authenticated",
            }
        )


def DeleteCart(request, cart_id=None):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            try:
                cart = Cart.objects.get(id=cart_id)
                if cart:
                    cart.delete()
                    return JsonResponse({"status": True, "message": "Cart Deleted.", "cart_amount": get_cart_amount(request), })
            except:
                return JsonResponse(
                    {"status": False, "message": "item not in the cart."}
                )

        else:
            return JsonResponse({"status": False, "message": "Invalid request"})
    else:
        return JsonResponse({"status": "login_required", "message": "Unauthorized"})


@login_required(login_url="Login")
def CartView(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).order_by("created_at")
        context = {
            "cart": cart,
            "cart_amount": get_cart_amount(request),
        }
        return render(request, "marketplace/cart.html", context)


def Search(request):
    '''The lng and lat will be the the cooridinates recieved from the google map api from the front end
    and these coordinates will be of the address(second field in teh home search) given in the fields'''

    if not 'lat' in request.GET:
        return redirect('marketplace')
    else:
        lat = request.GET['lat']
        lng = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['keyword']
        
        fetch_vendors_by_food_or_byCategory = FoodItem.objects.filter(
            Q(food_title__icontains=keyword, is_available=True) | Q(category__category_name__icontains=keyword, is_available=True)).values_list('vendor', flat=True)
        print(fetch_vendors_by_food_or_byCategory)
        vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_food_or_byCategory) | Q(
            vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
        if lat and lng and radius:
            print(lat, lng, radius)
            pnt = GEOSGeometry('POINT(%s %s)' % (lng, lat))
            vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_food_or_byCategory) | Q(
                vendor_name__icontains=keyword, is_approved=True, user__is_active=True),
                user_profile__latlng__distance_lte=(pnt, D(km=radius))
            ).annotate(distance=Distance('user_profile__latlng', pnt)).order_by('distance')

            print(vendors)

            for v in vendors:
                v.kms = round(v.distance.km, 1)

            vendor_count = vendors.count()
            context = {
                'vendors': vendors,
                'vendors_count': vendor_count,
            }
            return render(request, 'marketplace/listings.html', context)
