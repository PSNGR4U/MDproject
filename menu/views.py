from decimal import Decimal, InvalidOperation

from django.shortcuts import render
from .models import Dish, Category


def menu_page(request):
    dishes = Dish.objects.select_related('category').all()
    categories = Category.objects.all()

    category_id = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if category_id:
        try:
            dishes = dishes.filter(category_id=int(category_id))
        except ValueError:
            pass

    if min_price:
        try:
            price = Decimal(min_price)
            if price.is_finite() and price >= 0:
                dishes = dishes.filter(price__gte=price)
        except InvalidOperation:
            pass

    if max_price:
        try:
            price = Decimal(max_price)
            if price.is_finite() and price >= 0:
                dishes = dishes.filter(price__lte=price)
        except InvalidOperation:
            pass

    context = {
        'dishes': dishes,
        'categories': categories,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'menu/menu.html', context)