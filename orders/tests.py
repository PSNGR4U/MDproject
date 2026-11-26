
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from menu.models import Category, Dish
from .models import Order, OrderItem


User = get_user_model()


class CheckoutTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testclient',
            password='testpassword123'
        )

        self.category = Category.objects.create(
            name='Pizza'
        )

        self.dish = Dish.objects.create(
            name='Margherita',
            description='Classic pizza',
            price=Decimal('35.00'),
            category=self.category
        )

        self.client.force_login(self.user)

        session = self.client.session
        session['cart'] = {
            str(self.dish.id): {'quantity': 2}
        }
        session.save()

    def test_checkout_page_loads(self):
        response = self.client.get(reverse('checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Checkout')

    def test_checkout_creates_order_and_items(self):
        response = self.client.post(
            reverse('checkout'),
            {
                'customer_name': 'Test Client',
                'phone': '+48 123 456 789'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        order = Order.objects.first()

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.customer_name, 'Test Client')
        self.assertEqual(order.phone, '+48 123 456 789')
        self.assertEqual(order.status, Order.Status.PENDING)

        item = order.items.first()

        self.assertEqual(item.dish, self.dish)
        self.assertEqual(item.dish_name, 'Margherita')
        self.assertEqual(item.unit_price, Decimal('35.00'))
        self.assertEqual(item.quantity, 2)

        self.assertEqual(order.total_price, Decimal('70.00'))

    def test_checkout_clears_cart_after_success(self):
        self.client.post(
            reverse('checkout'),
            {
                'customer_name': 'Test Client',
                'phone': '+48 123 456 789'
            }
        )

        session = self.client.session

        self.assertNotIn('cart', session)

    def test_invalid_phone_does_not_create_order(self):
        response = self.client.post(
            reverse('checkout'),
            {
                'customer_name': 'Test Client',
                'phone': 'abc'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)

    def test_unauthenticated_user_cannot_checkout(self):
        self.client.logout()

        response = self.client.get(reverse('checkout'))

        self.assertRedirects(
            response,
            '/login/?next=/orders/checkout/'
        )
