
from decimal import Decimal

from menu.models import Dish


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get('cart', {})

    def add(self, dish, quantity=1, override_quantity=False):
        dish_id = str(dish.id)

        if dish_id not in self.cart:
            self.cart[dish_id] = {'quantity': 0}

        if override_quantity:
            self.cart[dish_id]['quantity'] = quantity
        else:
            self.cart[dish_id]['quantity'] += quantity

        self.save()

    def remove(self, dish):
        dish_id = str(dish.id)

        if dish_id in self.cart:
            del self.cart[dish_id]
            self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __iter__(self):
        dish_ids = self.cart.keys()

        dishes = Dish.objects.filter(
            id__in=dish_ids
        ).select_related('category')

        dishes_dict = {dish.id: dish for dish in dishes}

        for dish_id, item in self.cart.items():
            dish = dishes_dict.get(int(dish_id))

            if dish:
                quantity = item['quantity']

                yield {
                    'dish': dish,
                    'quantity': quantity,
                    'total_price': dish.price * quantity,
                }

    def __len__(self):
        return sum(
            item['quantity'] for item in self.cart.values()
        )

    def get_total_price(self):
        return sum(
            (item['total_price'] for item in self),
            Decimal('0.00')
        )
