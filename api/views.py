from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer

class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"products": serializer.data}, status=HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"product": serializer.data, "message": "Product created successfully!"}, status=HTTP_201_CREATED)
        return Response({"product": serializer.data, "errors": serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response({"product": serializer.data}, status=HTTP_200_OK)
    
    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"product": serializer.data, "message": "Product updated successfuly!"}, status=HTTP_200_OK)
        return Response({"product": serializer.data, "errors": serializer.errors}, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"message": "Product deleted successfully!"}, status=HTTP_204_NO_CONTENT)