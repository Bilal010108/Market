from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal


class Expense(models.Model):
    EXPENSE_TYPES = (
        ('salary', 'Жалакы'),
        ('rent', 'Ижара'),
        ('purchase', 'Товар закупка'),
        ('other', 'Башка'),
    )
    name = models.CharField(max_length=200)
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.amount}"


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    ROLE_CHOICES = (
        ('administrator', 'administrator'),
        ('owner', 'owner'),
        ('seller', 'seller'),
    )
    user_role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='seller')
    profile_image = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username or self.user_role


class Product(models.Model):
    sku = models.CharField(max_length=27)
    name_product = models.CharField(max_length=67)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    opt = models.DecimalField(max_digits=10, decimal_places=2)
    retail = models.DecimalField(max_digits=10, decimal_places=2)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name_product


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all()) or Decimal('0.00')

    @property
    def total_positions(self):
        return self.items.count()

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.retail * self.quantity

    def __str__(self):
        return self.cart.user.username


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.order.user.username