
from decimal import Decimal, InvalidOperation
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q

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
    dishes = Dish.objects.select_related("category").all()
    all_categories = Category.objects.all()

    search_query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    if search_query:
        dishes = dishes.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    if selected_category:
        dishes = dishes.filter(category__pk=selected_category)

    if min_price:
        dishes = dishes.filter(price__gte=min_price)

    if max_price:
        dishes = dishes.filter(price__lte=max_price)

    can_manage_menu = request.user.is_authenticated and (
        request.user.is_staff or request.user.is_superuser
    )

    context = {
        "dishes": dishes,
        "categories": all_categories,
        "all_categories": all_categories,
        "search_query": search_query,
        "selected_category": selected_category,
        "min_price": min_price,
        "max_price": max_price,
        "can_manage_menu": can_manage_menu,
    }
    return render(request, "menu/menu.html", context)


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

def dish_detail(request, pk):
    dish = get_object_or_404(Dish.objects.select_related("category"), pk=pk)
    context = {
        "dish": dish,
        "can_manage_menu": request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser),
    }
    return render(request, "menu/dish_detail.html", context)
