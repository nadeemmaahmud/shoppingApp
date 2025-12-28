from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer

User = get_user_model()

class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"success": True, "products": serializer.data}, status=HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "product": serializer.data, "message": "Product created successfully!"}, status=HTTP_201_CREATED)
        return Response({"success": False, "product": serializer.data, "errors": serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response({"success": True, "product": serializer.data}, status=HTTP_200_OK)
    
    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "product": serializer.data, "message": "Product updated successfuly!"}, status=HTTP_200_OK)
        return Response({"success": False, "product": serializer.data, "errors": serializer.errors}, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"success": True, "message": "Product deleted successfully!"}, status=HTTP_204_NO_CONTENT)
    
class OrderListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        orders = Order.objects.all()
        serializers = OrderSerializer(orders, many=True)
        return Response({"success": True, "orders": serializers.data}, status=HTTP_200_OK)
    
    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"success": True, "orders": serializer.data, "message": "Order created successfully!"}, status=HTTP_201_CREATED)
        return Response({"success": False, "orders": serializer.data, "errors": serializer.errors}, status=HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        order = get_object_or_404(Order, order_id=id)
        serializer=OrderSerializer(order)
        return Response({"success": True, 'order': serializer.data}, status=HTTP_200_OK)
    
    def patch(self, request, id):
        order = get_object_or_404(Order, order_id=id)
        serializer = OrderSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "order": serializer.data, "message": "Order updated successfully!"}, status=HTTP_200_OK)
        return Response({"success": False, "order": serializer.data}, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        order = get_object_or_404(Order, order_id=id)
        order.delete()
        return Response({"success": True, "message": "Order deleted successfully!"}, status=HTTP_204_NO_CONTENT)