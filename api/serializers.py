from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs["price"] < 0:
            raise serializers.ValidationError("Price can't be less than 0.")    
        return attrs
    
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock", "image"]
