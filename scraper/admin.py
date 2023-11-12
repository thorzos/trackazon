from django.contrib import admin
from .models import CustomUser, Product, PriceHistory

admin.site.register(Product)
admin.site.register(CustomUser)
admin.site.register(PriceHistory)

