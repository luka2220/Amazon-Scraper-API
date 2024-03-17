from rest_framework import serializers
from .models import SearchProduct, Product


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchProduct
        fields = ['id', 'name', 'results', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'info', 'created_at']
