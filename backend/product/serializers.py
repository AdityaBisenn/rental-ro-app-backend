# serializers.py
from rest_framework import serializers
from .models import FashionProduct

class FashionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FashionProduct
        fields = ['id', 'name', 'price', 'url', 'images', 'description', 'brand', 'colour', 'sizes', 'rating', 'num_reviews', 'gender', 'category_details', 'created_at', 'updated_at']

class SwipePageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FashionProduct
        fields = ['id', 'name', 'price', 'url', 'images', 'description', 'brand', 'colour', 'sizes', 'created_at', 'updated_at']
