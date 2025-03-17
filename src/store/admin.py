from django.contrib import admin
from .models import Category, Product, Order, OrderItems, Puchase


# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Puchase)
