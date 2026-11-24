
from decimal import Decimal, InvalidOperation
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Dish, Category
from .forms import DishForm, CategoryForm


def menu_manager_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (
            request.user.is_superuser
            or request.user.is_staff
            or request.user.role == 'manager'
        ):
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


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

    can_manage_menu = request.user.is_authenticated and (
        request.user.is_superuser
        or request.user.is_staff
        or request.user.role == 'manager'
    )

    context = {
        'dishes': dishes,
        'categories': categories,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'can_manage_menu': can_manage_menu,
    }

    return render(request, 'menu/menu.html', context)


@menu_manager_required
def add_dish(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = DishForm()

    return render(request, 'menu/dish_form.html', {'form': form})


@menu_manager_required
def edit_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)

    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish)

        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = DishForm(instance=dish)

    return render(
        request,
        'menu/dish_form.html',
        {'form': form, 'dish': dish}
    )


@menu_manager_required
def delete_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)

    if request.method == 'POST':
        dish.delete()
        return redirect('menu')

    return render(
        request,
        'menu/confirm_delete.html',
        {'dish': dish}
    )


@menu_manager_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = CategoryForm()

    return render(request, 'menu/category_form.html', {'form': form})


@menu_manager_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        'menu/category_form.html',
        {'form': form, 'category': category}
    )


@menu_manager_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        if category.dishes.exists():
            return render(
                request,
                'menu/confirm_category_delete.html',
                {
                    'category': category,
                    'error': 'Cannot delete a category that contains dishes.'
                }
            )

        category.delete()
        return redirect('menu')

    return render(
        request,
        'menu/confirm_category_delete.html',
        {'category': category}
    )
