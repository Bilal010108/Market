from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'user_role')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'sku', 'name_product', 'cost_price', 'opt', 'retail', 'descriptions')


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'sku', 'name_product', 'cost_price', 'opt', 'retail', 'descriptions')


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # ИСПРАВЛЕНО: вместо product_id — вложенный объект
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'quantity', 'product', 'product_id', 'total_price')


class CartItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'quantity', 'product', 'total_price')


class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'created_at', 'total_price', 'total_positions', 'total_items')


class CartDetailSerializer(serializers.ModelSerializer):
    items = CartItemListSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'created_at', 'total_price', 'total_positions', 'total_items', 'items')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'price')


class OrderItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'price')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'total_price', 'created_at')  # ИСПРАВЛЕНО: добавлены user и created_at


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total_price', 'created_at', 'items')


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('id', 'name', 'expense_type', 'amount', 'date', 'note', 'created_at')


class DailySalesSerializer(serializers.Serializer):
    date = serializers.DateField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    cost = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    orders_count = serializers.IntegerField()


class CategoryProfitSerializer(serializers.Serializer):
    category = serializers.CharField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    cost = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    qty_sold = serializers.IntegerField()


class AnalyticsSummarySerializer(serializers.Serializer):
    period_start = serializers.DateField()
    period_end = serializers.DateField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_cost_goods = serializers.DecimalField(max_digits=12, decimal_places=2)
    gross_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    margin_percent = serializers.FloatField()
    orders_count = serializers.IntegerField()
    items_sold = serializers.IntegerField()
    daily_sales = DailySalesSerializer(many=True)
    category_profit = CategoryProfitSerializer(many=True)
    top_products = serializers.ListField()
    expense_breakdown = serializers.ListField()