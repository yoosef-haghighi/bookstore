from django.contrib import admin

from .models import Order, OrderItem, Coupon, CartItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('book', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'tracking_code', 'user', 'status', 'payment_method', 'total_price', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'first_name', 'last_name', 'phone', 'tracking_code')
    inlines = [OrderItemInline]
    readonly_fields = ('total_price', 'discount_amount', 'created_at', 'updated_at')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_amount', 'active', 'used_count', 'max_usage', 'valid_to')
    list_filter = ('active',)
    search_fields = ('code',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity', 'price', 'user', 'session_key', 'added_at')
    search_fields = ('book__title', 'session_key')