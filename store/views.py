from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets, generics, permissions, status, response


class SellerAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = SellerSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class OwnerAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = OwnerSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class AdminstratorAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = AdminstratorSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)



class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartAPIView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemAPIView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemAPIView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer





