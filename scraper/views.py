from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Product, PriceHistory, CustomUser
from .serializers import ProductSerializer, PriceHistorySerializer, CustomUserSerializer


@api_view(["GET"])
def get_all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def get_product_by_id(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        serializer = ProductSerializer(product, many=False)
        return JsonResponse(serializer.data, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def create_product(request):
    product_data = request.data
    serializer = ProductSerializer(data=product_data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)  # 201 Created
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 400 Bad Request


"""
@api_view(["PUT"])
def update_product(request, product_id):
    product = get_product_by_id(request, product_id)
    if product:
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
"""


@api_view(["DELETE"])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)

        product.delete()
        return JsonResponse({"message": "Product has been deleted"}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_price_history(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        price_history = PriceHistory.objects.filter(product=product)
        serializer = PriceHistorySerializer(price_history, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "PUT", "DELETE"])
def user_detail(request, user_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CustomUserSerializer(user, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    else:
        return JsonResponse({"error": "Only GET, PUT, or DELETE methods are accepted"},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def register_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


def detail(request, product_id):
    return HttpResponse("You're looking at product %s." % product_id)
