from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
# Create your views here.


def home_page_view(request):
    products = Product.objects.filter(status=Product.ACTIVE)[:6]

    context = {
        "products": products
    }
    return render(request, "core/index.html", context)


def about_page_view(request):
    return render(request, "core/about.html")
