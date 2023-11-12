from django.urls import path

from . import views

urlpatterns = [
    # ex: /scraper/

    # ex: /scraper/5/

    path("<int:product_id>/", views.detail, name="detail"),
    # ex: /scraper/5/pricehistory/
    # path("<int:product_id>/pricehistory/", views.pricehistory, name="results"),

    # REST-API #
    # 1. products

    # Retrieve all products
    path("api/products/", views.get_all_products),

    # Retrieve product by id
    path("api/products/<int:product_id>/", views.get_product_by_id),

    # Create a new product
    path("api/products/create/", views.create_product),

    # Update a product
    #path("api/products/<int:product_id>/update/", views.update_product),

    # Delete a product
    path("api/products/<int:product_id>/delete/", views.delete_product),


    # 2. price history

    # Retrieve the price history of a product
    path("api/products/<int:product_id>/price_history/", views.get_price_history),


    # 3. users

    # Retrieve, update and delete user details
    path("api/users/<int:user_id>/", views.user_detail),

    # Register a new user
    path("api/users/register/", views.register_user),

    # Log in a user
    path("api/users/login/", views.login_user),

]