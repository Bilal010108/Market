from django.shortcuts import render
from rest_framework import viewsets,generics, permissions, status, response
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count,F,DecimalField,ExpressionWrapper
from django.db.models.functions import TruncDate

from django.utils import timezone
from datetime import date, timedelta
from .serializers import *


class SellerAPIView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = SellerSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class SellerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = SellerDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class ClientDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = SellerDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class ClientAPIView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = SellerSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)




class OwnerAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = OwnerSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class AdministratorAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = AdminstratorSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)



class ProductAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

class CartAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer

class CartDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartDetailSerializer

class CartItemAPIView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer

class CartItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemDetailSerializer


class OrderAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

class OrderItemAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /expenses/        — чыгыштар тизмеси
    POST /expenses/        — жаңы чыгыш кошуу
    """
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Expense.objects.all().order_by('-date')
        expense_type = self.request.query_params.get('type')
        if expense_type:
            qs = qs.filter(expense_type=expense_type)
        return qs


class ExpenseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /expenses/<id>/  — бир чыгыш
    PUT    /expenses/<id>/  — өзгөртүү
    DELETE /expenses/<id>/  — өчүрүү
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]


class AnalyticsSummaryAPIView(APIView):
    """
    GET /analytics/summary/?period=week|month|all

    Жооп:
    {
        period_start, period_end,
        total_revenue, total_cost_goods, gross_profit,
        total_expenses, net_profit, margin_percent,
        orders_count, items_sold,
        daily_sales: [ {date, revenue, cost, profit, orders_count}, ... ],
        category_profit: [ {category, revenue, cost, profit, qty_sold}, ... ],
        top_products: [ {name, qty_sold, revenue, profit}, ... ],
        expense_breakdown: [ {type, amount}, ... ]
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        period = request.query_params.get('period', 'month')

        today = date.today()
        if period == 'week':
            start = today - timedelta(days=7)
        elif period == 'month':
            start = today - timedelta(days=30)
        else:
            start = date(2000, 1, 1)

        # ── Сатуулар (OrderItem) ─────────────────────────────
        order_items = OrderItem.objects.filter(
            order__created_at__date__gte=start
        ).select_related('product', 'order')

        total_revenue = order_items.aggregate(
            s=Sum(ExpressionWrapper(F('price') * F('quantity'),
                                    output_field=DecimalField()))
        )['s'] or Decimal('0.00')

        total_cost_goods = order_items.aggregate(
            s=Sum(ExpressionWrapper(F('product__cost_price') * F('quantity'),
                                    output_field=DecimalField()))
        )['s'] or Decimal('0.00')

        gross_profit = total_revenue - total_cost_goods

        # ── Чыгыштар ────────────────────────────────────────
        total_expenses = Expense.objects.filter(
            date__gte=start
        ).aggregate(s=Sum('amount'))['s'] or Decimal('0.00')

        net_profit = gross_profit - total_expenses
        margin_pct = float(round(net_profit / total_revenue * 100, 1)) if total_revenue else 0.0

        orders_count = Order.objects.filter(created_at__date__gte=start).count()
        items_sold = order_items.aggregate(s=Sum('quantity'))['s'] or 0

        # ── Күнүмдүк сатуу ──────────────────────────────────
        daily_raw = (
            order_items
            .annotate(day=TruncDate('order__created_at'))
            .values('day')
            .annotate(
                revenue=Sum(ExpressionWrapper(F('price') * F('quantity'),
                                              output_field=DecimalField())),
                cost=Sum(ExpressionWrapper(F('product__cost_price') * F('quantity'),
                                           output_field=DecimalField())),
                orders_count=Count('order', distinct=True),
            )
            .order_by('day')
        )
        daily_sales = [
            {
                'date': r['day'],
                'revenue': r['revenue'] or Decimal('0'),
                'cost': r['cost'] or Decimal('0'),
                'profit': (r['revenue'] or Decimal('0')) - (r['cost'] or Decimal('0')),
                'orders_count': r['orders_count'],
            }
            for r in daily_raw
        ]

        # ── Категория боюнча прибыль (SKU 3 символ = категория) ──
        cat_raw = (
            order_items
            .values('product__sku')
            .annotate(
                revenue=Sum(ExpressionWrapper(F('price') * F('quantity'),
                                              output_field=DecimalField())),
                cost=Sum(ExpressionWrapper(F('product__cost_price') * F('quantity'),
                                           output_field=DecimalField())),
                qty_sold=Sum('quantity'),
            )
        )
        category_profit = [
            {
                'category': r['product__sku'][:3] if r['product__sku'] else '—',
                'revenue': r['revenue'] or Decimal('0'),
                'cost': r['cost'] or Decimal('0'),
                'profit': (r['revenue'] or Decimal('0')) - (r['cost'] or Decimal('0')),
                'qty_sold': r['qty_sold'] or 0,
            }
            for r in cat_raw
        ]

        # ── Топ 5 товар ──────────────────────────────────────
        top_raw = (
            order_items
            .values('product__name_product')
            .annotate(
                qty_sold=Sum('quantity'),
                revenue=Sum(ExpressionWrapper(F('price') * F('quantity'),
                                              output_field=DecimalField())),
                cost=Sum(ExpressionWrapper(F('product__cost_price') * F('quantity'),
                                           output_field=DecimalField())),
            )
            .order_by('-qty_sold')[:5]
        )
        top_products = [
            {
                'name': r['product__name_product'],
                'qty_sold': r['qty_sold'],
                'revenue': str(r['revenue'] or 0),
                'profit': str((r['revenue'] or Decimal('0')) - (r['cost'] or Decimal('0'))),
            }
            for r in top_raw
        ]

        # ── Чыгыш түрлөрү боюнча ────────────────────────────
        exp_break = (
            Expense.objects.filter(date__gte=start)
            .values('expense_type')
            .annotate(amount=Sum('amount'))
            .order_by('-amount')
        )
        expense_breakdown = [
            {'type': r['expense_type'], 'amount': str(r['amount'] or 0)}
            for r in exp_break
        ]

        data = {
            'period_start': start,
            'period_end': today,
            'total_revenue': total_revenue,
            'total_cost_goods': total_cost_goods,
            'gross_profit': gross_profit,
            'total_expenses': total_expenses,
            'net_profit': net_profit,
            'margin_percent': margin_pct,
            'orders_count': orders_count,
            'items_sold': items_sold,
            'daily_sales': daily_sales,
            'category_profit': category_profit,
            'top_products': top_products,
            'expense_breakdown': expense_breakdown,
        }

        serializer = AnalyticsSummarySerializer(data)
        return Response(serializer.data)





