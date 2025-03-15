from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from store.models import Product, Category, OrderItems, Order
from django.db.models import Q
from .forms import ProductForm, OrderForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .cart import Cart
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
import stripe
import json
from .utils import product_sales
# Create your views here.


def product_search(request):
    query = request.GET.get("query", "")
    if query:
        products = Product.objects.filter(status=Product.ACTIVE).filter(
            Q(name__icontains=query) | Q(description__icontains=query))

        context = {
            "products": products,
            "query": query
        }
        return render(request, "store/search.html", context)

# TODO: show product items number in templates


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.catgory_products.filter(status=Product.ACTIVE)
    count = category.catgory_products.filter(status=Product.ACTIVE).count()

    print(f"this is total products in {category} :", category.catgory_products.filter(
        status=Product.ACTIVE).count())
    # print("this is products:", products)

    context = {
        "category": category,
        "products": products,
    }
    return render(request, "store/category_detail.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, status=Product.ACTIVE)

    context = {
        "product": product
    }
    return render(request, "store/product_detail.html", context)


@login_required
def add_product(request):
    if request.method == "POST":
        title = request.POST.get("name", "")

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.slug = slugify(title)

            product.save()

            messages.success(request, "Product Added Successfully.")
            # redirect here

            return redirect("userprofile:my_store")

    form = ProductForm()
    context = {
        "form": form,
        "title": "Add Product"
    }
    return render(request, "store/product_form.html", context)


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, vendor=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():

            form.save()
            messages.success(request, "Product Changed Successfully.")
            # redirect here

            return redirect("userprofile:my_store")

    form = ProductForm(instance=product)
    context = {
        "form": form,
        "title": "Edit Product"
    }
    return render(request, "store/product_form.html", context)


@login_required
def delete_product(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(
            Product, id=product_id, vendor=request.user)

        product.status = Product.DELETE
        product.save()

        messages.success(request, "Product Deleted Successfully.")
        return redirect("userprofile:my_store")


def add_to_cart(request, product_id):
    cart = Cart(request)

    cart.add(product_id)

    return redirect("store:cart_view")


def cart_view(request):
    cart = Cart(request)
    print('this is cart length::', len(cart))
    context = {
        "cart": cart
    }
    return render(request, "store/cart_view.html", context)


def remove_to_cart(request, product_id):
    print("this is product id", product_id)
    cart = Cart(request)
    cart.remove(product_id)
    messages.success(request, "Item removed from cart")

    return redirect("store:cart_view")


def change_quantity(request, product_id):
    quantity = request.GET.get("quantity", "")
    cart = Cart(request)
    if quantity:
        cart.add(product_id, quantity, update_quantity=True)
    return redirect("store:cart_view")


@login_required
def checkout(request):

    cart = Cart(request)
    print('this is cart length::', len(cart))

    if len(cart) == 0:
        return redirect("store:cart_view")

    if request.method == "POST":
        form = OrderForm(request.POST)

        # TODO: fix payment intent issue
        if form.is_valid():

            items = {}
            products = []
            for item in cart:
                product = item["product"]

                products.append({
                    "product_name": product.name,
                    "price": item["quantity"]*product.price,
                    "quantity": item["quantity"]
                })

            checkout_session = product_sales(products)

            items["checkout_url"] = checkout_session.url
            items["payment_intent"] = checkout_session.payment_intent

            # TODO: come again
            print()
            # request.session["purchase_id"] = json.dumps(checkout_session.id)
            
            request.session["purchase_id"] = checkout_session.id
            print('this is session::',request.session.__dict__)
            print('this is sesssion:',request.session)
            if request.session["purchase_id"]:
                order = form.save(commit=False)
                order.created_by = request.user
                order.paid_amount = cart.get_total_cost()
                # order.is_paid = True
                order.payment_intent = items["payment_intent"] or checkout_session.id
                
                order.save()

         
                # del request.session["purchase_id"]
                for item in cart:
                    product = item["product"]
                    quantity = item["quantity"]
                    total_price = quantity * product.price

                    item = OrderItems.objects.create(
                        product=product, order=order, price=total_price, quantity=quantity)

                    # cart.clear()

                    # messages.success(request, "Order Placed Successfully.")
        # return redirect("userprofile:my_account")
        # return JsonResponse({"msg": "hello"})
        # session, payment_intent = items
        # url = items["checkout_url"]
            return HttpResponseRedirect(checkout_session.url)
        # return JsonResponse({"session": session, "order": payment_intent})

    form = OrderForm()
    context = {
        "form": form,
        "pub_key": settings.STRIPE_PUB_KEY
    }
    return render(request, "store/checkout.html", context)

@login_required
def success(request):
    cart=Cart(request)
    purchase_id = request.session.get("purchase_id")
    print('this is id ',request.session['purchase_id'])
    print('this is request.session',request.session.__dict__)
    print("this is purchase id::",purchase_id)
    order = Order.objects.get(payment_intent=purchase_id)
    if purchase_id:
        order.is_paid = True
        order.save()
        messages.success(request, "Order Placed Successfully.")
        del request.session["purchase_id"]
        # cart.clear()
        return render(request, "store/success.html")
    else:
        return redirect("store:cart_view")