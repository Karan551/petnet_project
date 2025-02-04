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
