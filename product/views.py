from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Product
from .serializers import ProductSerializer
from .scripts import scraper


@api_view(['GET'])
def search_product(request, product_name):
    print(f'Requested product name for searching = {product_name}')
    return JsonResponse(data={"search": "result", "product": product_name}, status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
def product_data(request, product_id):
    try:
        # Check if the product has been search before and return the result if it exists
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)

        response_data = {
            'id': serializer.data['id'],
            'title': serializer.data['title'],
            'price': serializer.data['price'],
            'info': serializer.data['info']
        }

        return JsonResponse(data=response_data, status=status.HTTP_200_OK, safe=False)

    except Product.DoesNotExist:
        # If the product ID doesn't exist, scrape the site for the product data
        result = scraper.scrape_product(product_id)
        if result:
            serializer = ProductSerializer(data=result)
            if serializer.is_valid():
                serializer.save()
            else:
                print("Unable to store product data in db")

            return JsonResponse(data=result, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse(data={"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
