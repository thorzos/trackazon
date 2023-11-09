from django.contrib.auth.models import AbstractUser
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    image_url = models.URLField()

    def __str__(self):
        return self.name

    def get_product_url(self):
        return self.url


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.price

    def get_timestamp(self):
        return self.timestamp


class User(models.Model):
    email = models.EmailField(unique=True)
    user_name = models.CharField(unique=True, max_length=30)
    products = models.ManyToManyField(Product, related_name="users")

    def __str__(self):
        return self.user_name

    def tracked_urls(self):
        return self.products
