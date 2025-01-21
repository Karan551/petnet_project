from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import Product, Category
# Create your views here.


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.catgory_products.all()
    print("this is category:", category)
    print("this is products:", products)
    
    context = {
        "category": category,
        "products": products,
    }
    return render(request, "store/category_detail.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    context = {
        "product": product
    }
    return render(request, "store/product_detail.html", context)
