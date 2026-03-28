from .models import *
from rest_framework import routers
from .views import *
from django.urls import path, include


routers = routers.SimpleRouter()

urlpatterns = [
    path('', include(routers.urls)),

    path('clients/', CartAPIView.as_view(), name='clients'),
    path('seller/', SellerAPIView.as_view(), name='seller'),
    path('administrator/', AdminstratorAPIView.as_view(), name='adminstrator'),

    path('product/', ProductAPIView.as_view(), name='product_list'),

    path('cart/', CartAPIView.as_view(), name='cart-detail'),
    path('cart_item/', CartItemAPIView.as_view(), name='cart_item'),

    path('orders/', OrderAPIView.as_view(), name='order_list'),
    path('orders_item/', OrderAPIView.as_view(), name='order-create'),

]
