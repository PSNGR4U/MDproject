
from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'phone',
        'user',
        'status',
        'created_at',
    )

    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone', 'user__username')

    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'dish_name',
        'order',
        'unit_price',
        'quantity',
    )

    search_fields = ('dish_name',)
