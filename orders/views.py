from django.shortcuts import redirect, render
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amount
from orders.forms import OrderForm
from .models import Order
# Create your views here.


def PlaceOrder(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    subtotal = get_cart_amount(request)['subtotal']
    tax = get_cart_amount(request)['tax']
    total = get_cart_amount(request)['total']
    print(subtotal, total, tax)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.city = form.cleaned_data['city']
            order.country = form.cleaned_data['country']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = total
            order.total_tax = tax
            order.total_tax = tax
            order.payment_method = request.POST['options-outlined']
            order.order_number = '123'
            order.tax_data = ''
            order.save()
            return redirect('Place-Order')
        else:
            print(form.errors)

    return render(request, 'orders/place-order.html')
