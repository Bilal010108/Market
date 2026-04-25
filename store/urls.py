from .models import *
from rest_framework import routers
from .views import *
from django.urls import path, include


routers = routers.SimpleRouter()

urlpatterns = [
    path('', include(routers.urls)),

    path('clients/', CartAPIView.as_view(), name='clients'),
    path('clients/<int:pk>/', ClientDetailAPIView.as_view(), name='clients-detail'),

    path('seller/', SellerAPIView.as_view(), name='seller'),
    path('seller/<int:pk>/', SellerDetailAPIView.as_view(), name='seller-detail'),

    path('administrator/', AdministratorAPIView.as_view(), name='administrator'),

    path('product/', ProductAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),


    path('cart/', CartAPIView.as_view(), name='cart-detail'),
    path('cart/<int:pk>/', CartDetailAPIView.as_view(), name='cart-detail'),

    path('cart_item/', CartItemAPIView.as_view(), name='cart_item'),
    path('cart_item/<int:pk>/', CartItemDetailAPIView.as_view(), name='cart_item-detail'),

    path('orders/', OrderAPIView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),


    path('orders_item/', OrderAPIView.as_view(), name='order-create'),
    path('orders_item/<int:pk>/', OrderItemDetailAPIView.as_view(), name='order_item-detail'),

    # Чыгыш CRUD
    path('expenses/', ExpenseListCreateAPIView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', ExpenseRetrieveUpdateDestroyAPIView.as_view(), name='expense-detail'),

    # Аналитика
    path('analytics/summary/', AnalyticsSummaryAPIView.as_view(), name='analytics-summary'),
]


