from django.conf import settings
from store.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart
        self.qty = 0

    def __iter__(self):
        print('this is self.cart', self.cart)
        # To add product id and product information in cart
        for key in self.cart.keys():
            
            product = Product.objects.get(id=key)
            self.cart[key]["product"] = {
                'id': product.id,
                'name': product.name,
                'price': product.get_display_price(),
            }

        # print("here is session in cart: \n", self.session.__dict__)
        # print("this is cart ", self.cart)
        # print("here is session in cart------ \n", self.session.__dict__)
        # {'5': {'id': 5, 'quantity': 1, 'product': <Product: Apple Iphone>}}

        # To add product total price
        for item in self.cart.values():
            # print("this is item in cart:",item)
            # print('this is price',item["product"]["price"])
            item["total_price"] = int(
                item["product"]["price"] * item["quantity"])

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart

        # if we change in session then do this
        self.session.modified = True

    def add(self, product_id, quantity=1, update_quantity=False):
        quantity = int(quantity)
        # 'cart': {'5': {'id': 5, 'quantity': 1} }

        # first time when we add product in cart.
        if product_id not in self.cart:
            self.cart[product_id] = {"id": product_id, "quantity": quantity}

        if update_quantity:
            self.cart[product_id]["quantity"] += quantity

            if self.cart[product_id]["quantity"] == 0:
                self.remove(product_id)

        self.save()

    def remove(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):

        for p in self.cart.keys():
            self.cart[p]['product'] = Product.objects.get(pk=p)

        return sum(item['quantity'] * item['product'].price for item in self.cart.values())/100

    def get_total_quantity(self):
        for item in self.cart.keys():
            self.qty += self.cart[item]['quantity']
        return self.qty
