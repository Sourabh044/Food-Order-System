from .models import Cart
from menu.models import FoodItem


def get_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(user=request.user)
            if cart:
                for cart_item in cart:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
        return dict(cart_count=cart_count)
    else:
        pass


def get_cart_amount(request):
    subtotal = 0
    tax = 0
    total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for items in cart_items:
            fooditem = items.fooditem
            subtotal += fooditem.price * items.quantity
        total = subtotal + tax
        print(subtotal)
        print(total)

        return dict(subtotal=subtotal, tax=tax, total=total)
    else:
        pass
