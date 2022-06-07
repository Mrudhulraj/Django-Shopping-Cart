from django.shortcuts import render
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Product
from rest_framework.response import Response
# Create your views here.


class DemoView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        print(request.user)
        return Response({"success": "Authenticated successfully"})


class ProductView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        product_query = self.request.GET.get('category')
        queryset = Product.objects.all()
        if(product_query is not None):
            queryset = Product.objects.filter(
                category=product_query)
        return queryset
