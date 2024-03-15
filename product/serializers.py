from rest_framework import serializers
from .models import SearchProduct


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchProduct
        fields = ['id', 'name', 'results', 'created_at']
