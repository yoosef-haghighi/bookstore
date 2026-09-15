from decimal import Decimal
import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy

from books.models import Book

from .cart import Cart
from .forms import OrderCreateForm
from .models import Order, Coupon, CartItem


class CartDetailView(generic.TemplateView):
    template_name = 'orders/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        context['coupon'] = cart._get_coupon()
        return context


class CartAddView(generic.View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        cart = Cart(request)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1

        quantity = max(quantity, 1)

        if not book.is_in_stock:
            msg = f'«{book.title}» در حال حاضر ناموجود است.'
            if is_ajax:
                return JsonResponse({'success': False, 'error': msg})
            messages.warning(request, msg)
            return redirect('cart_detail')

        if quantity > book.stock:
            msg = f'موجودی «{book.title}» فقط {book.stock} عدد است.'
            if is_ajax:
                return JsonResponse({'success': False, 'error': msg})
            messages.warning(request, msg)
            return redirect('cart_detail')

        cart.add(book, quantity=quantity)
        msg = f'«{book.title}» به سبد خرید اضافه شد.'
        if is_ajax:
            return JsonResponse({'success': True, 'message': msg, 'cart_count': len(cart)})
        messages.success(request, msg)
        return redirect('cart_detail')


class CartRemoveView(generic.View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        cart = Cart(request)
        cart.remove(book)
        messages.success(request, f'«{book.title}» از سبد خرید حذف شد.')
        return redirect('cart_detail')


class CartUpdateView(generic.View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        cart = Cart(request)
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1
        if quantity <= 0:
            cart.remove(book)
        elif quantity > book.stock:
            messages.warning(request, f'موجودی «{book.title}» فقط {book.stock} عدد است.')
            return redirect('cart_detail')
        else:
            cart.add(book, quantity=quantity, update_quantity=True)
        return redirect('cart_detail')


class CouponApplyView(generic.View):
    def post(self, request):
        code = request.POST.get('code', '').strip()
        cart = Cart(request)
        now = None
        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            coupon = None
        if not coupon or not coupon.is_valid():
            messages.error(request, 'کد تخفیف نامعتبر است.')
            return redirect('cart_detail')
        cart.set_coupon(coupon)
        messages.success(request, f'کد تخفیف {coupon.code} با موفقیت اعمال شد.')
        return redirect('cart_detail')


class CouponRemoveView(generic.View):
    def post(self, request):
        cart = Cart(request)
        cart.remove_coupon()
        messages.success(request, 'کد تخفیف حذف شد.')
        return redirect('cart_detail')


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = OrderCreateForm
    template_name = 'orders/checkout.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart.has_items():
            messages.warning(request, 'سبد خرید شما خالی است.')
            return redirect('book_list')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        context['coupon'] = cart._get_coupon()
        return context

    def _generate_tracking_code(self):
        for _ in range(50):
            code = 'BS-' + secrets.token_hex(4).upper()
            if not Order.objects.filter(tracking_code=code).exists():
                return code
        return 'BS-' + str(secrets.randbelow(10**10)).zfill(10)

    def form_valid(self, form):
        cart = Cart(self.request)
        if not cart.has_items():
            messages.warning(self.request, 'سبد خرید شما خالی است.')
            return redirect('book_list')

        for item in cart:
            if item['quantity'] > item['book'].stock:
                messages.error(
                    self.request,
                    f'موجودی «{item["book"].title}» برای این تعداد کافی نیست.',
                )
                return redirect('cart_detail')

        coupon = cart._get_coupon()
        order = form.save(commit=False)
        order.user = self.request.user
        order.coupon = coupon
        order.discount_amount = cart.get_discount()
        order.total_price = cart.get_final_total_price()
        order.tracking_code = self._generate_tracking_code()
        order.save()

        for item in cart:
            order.items.create(
                book=item['book'],
                quantity=item['quantity'],
                price=item['price'],
            )
            item['book'].stock -= item['quantity']
            item['book'].save(update_fields=['stock'])

        if coupon:
            coupon.used_count += 1
            coupon.save(update_fields=['used_count'])

        cart.clear()
        cart.remove_coupon()
        messages.success(self.request, 'سفارش شما با موفقیت ثبت شد.')

        if order.payment_method == 'cod':
            return redirect(reverse('order_success', args=[order.pk]))
        return redirect(reverse('order_pay', args=[order.pk]))


class OrderPayView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'orders/order_pay.html'
    context_object_name = 'order'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        order = self.object
        if order.status == 'paid':
            return redirect('order_success', pk=order.pk)
        return response


class OrderPayConfirmView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['pk'])
        if order.user != request.user and not request.user.is_superuser:
            messages.error(request, 'شما اجازه پرداخت این سفارش را ندارید.')
            return redirect('order_list')
        self.order = order
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.order.status = 'paid'
        self.order.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'پرداخت با موفقیت انجام شد.')
        return redirect('order_success', pk=self.order.pk)


class OrderSkipPayView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['pk'])
        if order.user != request.user and not request.user.is_superuser:
            return redirect('order_list')
        return redirect('order_success', pk=order.pk)


class OrderSuccessView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'orders/order_success.html'
    login_url = reverse_lazy('login')
    context_object_name = 'order'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all().prefetch_related('items__book')
        return Order.objects.filter(user=self.request.user).prefetch_related('items__book')


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__book')


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all().prefetch_related('items__book')
        return Order.objects.filter(user=self.request.user).prefetch_related('items__book')


class OrderTrackView(generic.TemplateView):
    template_name = 'orders/order_track.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tracking_code = self.request.GET.get('tracking_code', '').strip()
        phone = self.request.GET.get('phone', '').strip()
        context['query'] = {'tracking_code': tracking_code, 'phone': phone}
        context['order'] = None
        if tracking_code and phone:
            try:
                order = Order.objects.filter(
                    tracking_code__iexact=tracking_code, phone=phone
                ).first()
            except Order.DoesNotExist:
                order = None
            context['order'] = order
        return context