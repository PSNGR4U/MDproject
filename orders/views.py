
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem


@login_required(login_url='login')
def checkout(request):
    cart = Cart(request)
    cart_items = list(cart)

    if not cart_items:
        return redirect('cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)

                order.user = request.user
                order.save()

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        dish=item['dish'],
                        dish_name=item['dish'].name,
                        unit_price=item['dish'].price,
                        quantity=item['quantity'],
                    )

            cart.session.pop('cart', None)
            cart.session.modified = True

            return render(
                request,
                'orders/order_created.html',
                {'order': order}
            )

    else:
        form = OrderCreateForm()

    return render(
        request,
        'orders/checkout.html',
        {
            'form': form,
            'cart_items': cart_items,
            'cart': cart,
        }
    )
