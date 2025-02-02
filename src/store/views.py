from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from store.models import Product, Category
from django.db.models import Q
from .forms import ProductForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .cart import Cart
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
    
    context = {
        "cart": cart
    }
    return render(request, "store/cart_view.html", context)


def remove_to_cart(request, product_id):
    print("this is product id",product_id)
    cart = Cart(request)
    cart.remove(product_id)
    messages.success(request,"Item removed from cart")
    
    return redirect("store:cart_view")
   
