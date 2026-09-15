from django.conf import settings
from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name='کد تخفیف')
    discount_amount = models.PositiveIntegerField(verbose_name='مبلغ تخفیف (تومان)')
    active = models.BooleanField(default=True, verbose_name='فعال')
    valid_from = models.DateTimeField(null=True, blank=True, verbose_name='از تاریخ')
    valid_to = models.DateTimeField(null=True, blank=True, verbose_name='تا تاریخ')
    max_usage = models.PositiveIntegerField(default=100, verbose_name='حداکثر استفاده')
    used_count = models.PositiveIntegerField(default=0, verbose_name='تعداد استفاده')

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        if not self.active:
            return False
        if self.used_count >= self.max_usage:
            return False
        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_to and now > self.valid_to:
            return False
        return True


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart_items',
    )
    session_key = models.CharField(max_length=64, null=True, blank=True)
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='cart_items',
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.book}'

    def get_cost(self):
        return self.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('cancelled', 'لغو شده'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('online', 'پرداخت آنلاین'),
        ('cod', 'پرداخت در محل'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default='online'
    )
    tracking_code = models.CharField(
        max_length=30, unique=True, null=True, blank=True, verbose_name='کد پیگیری'
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='کد تخفیف',
    )
    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=0, default=0, verbose_name='مبلغ تخفیف'
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} - {self.user.username}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=0)

    def __str__(self):
        return f'{self.quantity} x {self.book}'

    def get_cost(self):
        return self.price * self.quantity