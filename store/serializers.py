from .models import *
from rest_framework import serializers


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =('id', 'username', 'email', 'first_name', 'last_name','phone_number','user_role')

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =('id', 'username', 'email', 'first_name', 'last_name','phone_number','user_role')


class AdminstratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =('id', 'username', 'email', 'first_name', 'last_name','phone_number','user_role')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','sku','name_product','cost_price','opt','retail','descriptions')

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id','user','created_at')

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id','cart','quantity','product_id')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','total_price','created_at',)


class OrderItemSerializer(serializers.ModelSerializer):
     class Meta:
         model = OrderItem
         fields = ('id','product','quantity','price','created_at')



