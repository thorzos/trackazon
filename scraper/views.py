from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer


@api_view(["GET", "POST"])
def products(request):
    if request.method == "GET":
        products_all = Product.objects.all()
        serializer = ProductSerializer(products_all, many=True)
        return JsonResponse(serializer.data, safe=False)  # try without.data

    elif request.method == "POST":
        return JsonResponse("created new Product!", safe=False)

    else:
        Response(status=405)  # Not allowed, because unsupported method.


@api_view(["GET", "POST"])
def get_product_by_id(request):
    product = Product.objects.filter()
    serializer = ProductSerializer(product, many=False)
    return JsonResponse(serializer.data, safe=False)


def detail(request, product_id):
    return HttpResponse("You're looking at product %s." % product_id)


def index(request):
    return HttpResponse("Hello, world. You're at the scraper index.")
