
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from menu.models import Dish
from .cart import Cart


def get_quantity(request):
    try:
        quantity = int(request.POST.get('quantity', 1))
        return quantity
    except (ValueError, TypeError):
        return None


def cart_detail(request):
    cart = Cart(request)

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
    })


@require_POST
def cart_add(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)

    quantity = get_quantity(request)

    if quantity is not None and quantity > 0:
        cart.add(dish=dish, quantity=quantity)

    return redirect('cart_detail')


@require_POST
def cart_remove(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)

    cart.remove(dish)

    return redirect('cart_detail')


@require_POST
def cart_update(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)

    quantity = get_quantity(request)

    if quantity is not None:
        if quantity > 0:
            cart.add(
                dish=dish,
                quantity=quantity,
                override_quantity=True,
            )
        else:
            cart.remove(dish)

    return redirect('cart_detail')
