
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PREPARING = "preparing", "Preparing"
        READY = "ready", "Ready"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    @property
    def total_price(self):
        return sum(
            (item.unit_price * item.quantity for item in self.items.all()),
            Decimal("0.00")
        )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    dish = models.ForeignKey(
        "menu.Dish",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items"
    )

    dish_name = models.CharField(max_length=150)

    unit_price = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f"{self.dish_name} x {self.quantity}"
