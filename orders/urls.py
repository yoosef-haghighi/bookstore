from django.urls import path

from .views import (
    CartDetailView,
    CartAddView,
    CartRemoveView,
    CartUpdateView,
    CouponApplyView,
    CouponRemoveView,
    OrderCreateView,
    OrderPayView,
    OrderPayConfirmView,
    OrderSkipPayView,
    OrderSuccessView,
    OrderListView,
    OrderDetailView,
    OrderTrackView,
)


urlpatterns = [
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:pk>/', CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:pk>/', CartRemoveView.as_view(), name='cart_remove'),
    path('cart/update/<int:pk>/', CartUpdateView.as_view(), name='cart_update'),
    path('coupon/apply/', CouponApplyView.as_view(), name='coupon_apply'),
    path('coupon/remove/', CouponRemoveView.as_view(), name='coupon_remove'),
    path('checkout/', OrderCreateView.as_view(), name='checkout'),
    path('track/', OrderTrackView.as_view(), name='order_track'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/pay/', OrderPayView.as_view(), name='order_pay'),
    path('orders/<int:pk>/pay/confirm/', OrderPayConfirmView.as_view(), name='order_pay_confirm'),
    path('orders/<int:pk>/pay/skip/', OrderSkipPayView.as_view(), name='order_pay_skip'),
    path('orders/<int:pk>/success/', OrderSuccessView.as_view(), name='order_success'),
]