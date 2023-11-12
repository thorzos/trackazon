from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    products = models.ManyToManyField("scraper.Product", related_name="user_products")

    def __str__(self):
        return self.username

    def tracked_urls(self):
        return self.products.all()


class Product(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    image_url = models.URLField()
    users = models.ManyToManyField("scraper.CustomUser", related_name="price_history")

    def __str__(self):
        return self.name

    def get_product_url(self):
        return self.url


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_history")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.price)

    def get_timestamp(self):
        return self.timestamp
