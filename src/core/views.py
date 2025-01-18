from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home_page_view(request):
    return render(request, "core/index.html")


def about_page_view(request):
    return render(request, "core/about.html")
