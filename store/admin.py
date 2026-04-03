from django.contrib import admin
from .models import UserProfile, OrderItem, Product, Cart, CartItem, Order



admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
