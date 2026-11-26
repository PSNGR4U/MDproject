from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from menu.models import Category, Dish
from .cart import Cart


class CartTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Pizza')

        self.dish = Dish.objects.create(
            name='Margherita',
            description='Classic Italian pizza',
            price='12.50',
            category=self.category,
        )

    def test_add_dish_to_cart(self):
        response = self.client.post(
            reverse('cart_add', args=[self.dish.id]),
            {'quantity': 1}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.client.session['cart'][str(self.dish.id)]['quantity'],
            1
        )

    def test_cart_length(self):
        self.client.post(
            reverse('cart_add', args=[self.dish.id]),
            {'quantity': 3}
        )

        cart = Cart(self.client)
        self.assertEqual(len(cart), 3)

    def test_cart_total_price(self):
        self.client.post(
            reverse('cart_add', args=[self.dish.id]),
            {'quantity': 2}
        )

        cart = Cart(self.client)
        self.assertEqual(cart.get_total_price(), Decimal('25.00'))

    def test_adding_same_dish_increases_quantity(self):
        self.client.post(
            reverse('cart_add', args=[self.dish.id]),
            {'quantity': 1}
        )

        self.client.post(
            reverse('cart_add', args=[self.dish.id]),
            {'quantity': 1}
        )

        self.assertEqual(
            self.client.session['cart'][str(self.dish.id)]['quantity'],
            2
        )

    def test_update_dish_quantity(self):
        self.client.post(
            reverse('cart_add', args=[self.dish.id]),
            {'quantity': 1}
        )

        self.client.post(
            reverse('cart_update', args=[self.dish.id]),
            {'quantity': 5}
        )

        self.assertEqual(
            self.client.session['cart'][str(self.dish.id)]['quantity'],
            5
        )

    def test_remove_dish_from_cart(self):
        self.client.post(
            reverse('cart_add', args=[self.dish.id]),
            {'quantity': 1}
        )

        self.client.post(
            reverse('cart_remove', args=[self.dish.id])
        )

        self.assertEqual(
            self.client.session.get('cart', {}),
            {}
        )

    def test_invalid_quantity_does_not_add_dish(self):
        self.client.post(
            reverse('cart_add', args=[self.dish.id]),
            {'quantity': 'abc'}
        )

        self.assertEqual(
            self.client.session.get('cart', {}),
            {}
        )
