from .models import *
from rest_framework import serializers

class ClienterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =('id', 'username', 'email', 'first_name', 'last_name','phone_number','user_role')

class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =('id', 'username', 'email', 'first_name', 'last_name','phone_number','user_role')

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =('id', 'username', 'email', 'first_name', 'last_name','phone_number','user_role')

class SellerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =('id', 'username', 'email', 'first_name', 'last_name','phone_number','user_role')

class SellerDetailSerializer(serializers.ModelSerializer):
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

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','sku','name_product','cost_price','opt','retail','descriptions')

class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id','user','created_at')

class CartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id','user','created_at')


class CartItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id','cart','quantity','product_id')

class CartItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id','cart','quantity','product_id')



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','total_price')

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','total_price')



class OrderItemSerializer(serializers.ModelSerializer):
     class Meta:
         model = OrderItem
         fields = ('id','product','quantity','price','created_at')


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('id', 'name', 'expense_type', 'amount', 'date', 'note', 'created_at')


class DailySalesSerializer(serializers.Serializer):
    """Күнүмдүк сатуу"""
    date = serializers.DateField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    cost = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    orders_count = serializers.IntegerField()


class CategoryProfitSerializer(serializers.Serializer):
    """Категория боюнча прибыль (Product SKU префикси же аталышы)"""
    category = serializers.CharField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    cost = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    qty_sold = serializers.IntegerField()


class AnalyticsSummarySerializer(serializers.Serializer):
    """Жалпы жыйынтык"""
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


