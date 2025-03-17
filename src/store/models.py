from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files import File
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    ACTIVE = "active"
    DELETE = "delete"
    DRAFT = "draft"
    WAITING_FOR_APPROVAL = "waiting_approval"

    STATUS_CHOICES = [
        (ACTIVE, "active"),
        (DELETE, "delete"),
        (DRAFT, "draft"),
        (WAITING_FOR_APPROVAL, "waiting_approval"),

    ]
    vendor = models.ForeignKey(
        User, related_name="products", on_delete=models.CASCADE)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="catgory_products")

    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)

    image = models.ImageField(upload_to="uploads", blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="uploads/thumbnail/", blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default=ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_display_price(self):
        return self.price/100

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=85)

        name = image.name.replace('uploads/product_images/', '')
        thumbnail = File(thumb_io, name=name)

        return thumbnail

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url

        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)

                self.save()

                return self.thumbnail.url

            else:
                return "https://placehold.co/600x400?text=Image+Not+Available"


class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_intent = models.CharField(max_length=300)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="orders")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_display_price(self):
        return self.price/100

    def __str__(self):
        return self.first_name+" "+self.last_name


class OrderItems(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="items")
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orders")

    price = models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Order Items"
        
    def __str__(self):
        return self.product.name


class Puchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    product = models.ManyToManyField(Product)
    stripe_checkout_session_id=models.CharField(max_length=255,null=True,blank=True)
    completed = models.BooleanField(default=False)
    stripe_price = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
