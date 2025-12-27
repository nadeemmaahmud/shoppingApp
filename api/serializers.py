from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs["price"] < 0:
            raise serializers.ValidationError("Price can't be less than 0.")    
        return attrs
    
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "image"]

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.CharField(source='product.price', read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.item_subtotal

    class Meta:
        model = OrderItem
        fields = ["product_name", "product_price", "quantity", "total_price"]

class OrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    def get_total_amount(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta:
        model = Order
        fields = ["order_id", "user_name", "created_at", "status", "items", "total_amount"]