import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY



base_end_point = "http://127.0.0.1:8000"
success_url = f"{base_end_point}/store/product/success/"
cancel_url = f"{base_end_point}/store/cart-view/"


"""_summary_
1. Create Product object and get product id
2. Create Price Object and pass product_id
3. Create session Object and pass price id
"""


def product_sales(products: list):

    line_items=[]
    for product in products:
        stripe_product_obj = stripe.Product.create(
            name=product["product_name"])

        stripe_product_obj_id = stripe_product_obj.id

        stripe_price_object = stripe.Price.create(
            currency="usd",
            unit_amount=product["price"],
            product=stripe_product_obj_id,
        )

        stripe_price_id = stripe_price_object.id

        line_items.append({
            "price":stripe_price_id,
            "quantity":product["quantity"]
        })
    
    
    
    checkout_session = stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        line_items=line_items,
        mode="payment",
    )

    print("this is checkout::", checkout_session)
    print("this is success url::", checkout_session.url)
    return checkout_session
    return checkout_session.url, checkout_session.payment_intent



