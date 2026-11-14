from django.shortcuts import render
from .models import Dish, Category


def menu_page(request):
    dishes = Dish.objects.select_related('category').all()
    categories = Category.objects.all()

    context = {
        'dishes': dishes,
        'categories': categories,
    }

    return render(request, 'menu/menu.html', context)