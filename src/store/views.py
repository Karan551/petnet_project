from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import Product, Category
from django.db.models import Q
# Create your views here.


def product_search(request):
    query = request.GET.get("query", "")
    print("this is query:", query)
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))

        print("this is search result:", products)

        context = {
            "products": products,
            "query": query
        }
        return render(request, "store/search.html", context)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.catgory_products.all()
    # print("this is category:", category)
    # print("this is products:", products)

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
