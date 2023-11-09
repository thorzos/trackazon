from django.urls import path

from . import views

urlpatterns = [
    # ex: /scraper/
    path("", views.index, name="index"),
    # ex: /scraper/5/

    path("<int:product_id>/", views.detail, name="detail"),
    # ex: /scraper/5/pricehistory/
    # path("<int:product_id>/pricehistory/", views.pricehistory, name="results"),

    #REST API
    path("api/products", views.products),
]