from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    vendor = models.ForeignKey(
        User, related_name="products", on_delete=models.CASCADE)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="catgory_products")

    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)

    image = models.ImageField(upload_to="uploads", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_display_price(self):
        return self.price/100
