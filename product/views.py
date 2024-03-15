from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .models import SearchProduct
from .serializers import SearchSerializer
from .scripts import scraper


@api_view(['GET'])
def search_product(request, product_name):
    print(f'Requested product name for searching = {product_name}')
    return JsonResponse(data={"search": "result", "product": product_name}, status=status.HTTP_200_OK)


@api_view(['GET'])
def product_data(request, product_id):
    result = scraper.scrape_product(product_id)
    return JsonResponse(data=result, status=status.HTTP_200_OK)
