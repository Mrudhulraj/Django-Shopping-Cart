from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Cart, CartItems
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated
from products.serializers import ProductSerializer
from products.models import Product
from rest_framework.response import Response
# Create your views here.


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItems
        fields = '__all__'


class CartSerializer(ModelSerializer):
    cart = CartItemSerializer()
    products = ProductSerializer()

    class Meta:
        model = Cart
        fields = '__all__'


class CartView(ModelViewSet):
    queryset = CartItems.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.GET.get('user')
        queryset = CartItems.objects.all()
        if(user is not None):
            cart = Cart.objects.filter(user=user, ordered=False).first()
            queryset = CartItems.objects.filter(cart=cart)
        return queryset

    def create(self, request):
        data = request.data
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, ordered=False)
        product = Product.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity')
        cart_items = CartItems(user=user, product=product, cart=cart,
                               price=price, quantity=quantity)
        cart_items.save()

        total_price = 0.0
        cart_items = CartItems.objects.filter(user=user, cart=cart.id)

        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({"success": "Added to cart"})
