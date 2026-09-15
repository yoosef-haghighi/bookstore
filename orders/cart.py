from django.db.models import Sum

from .models import CartItem


class Cart:
    def __init__(self, request):
        self.request = request
        user = getattr(request, 'user', None)
        self.is_authenticated = bool(user and user.is_authenticated)
        self.user = user if self.is_authenticated else None
        self.session = getattr(request, 'session', None)
        self.session_key = (
            self.session.session_key if self.session else None
        )

    def _ensure_key(self):
        if self.is_authenticated:
            return f'user:{self.user.id}'
        if self.session is not None:
            if not self.session_key:
                self.session.save()
                self.session_key = self.session.session_key
            return self.session_key
        return None

    def _base_queryset(self):
        qs = CartItem.objects.all()
        if self.is_authenticated:
            return qs.filter(user=self.user)
        if self.session_key:
            return qs.filter(session_key=self.session_key, user__isnull=True)
        return qs.none()

    def add(self, book, quantity=1, update_quantity=False):
        if self.is_authenticated:
            item, _ = CartItem.objects.get_or_create(user=self.user, book=book)
        else:
            key = self._ensure_key()
            item, _ = CartItem.objects.get_or_create(
                session_key=key, book=book, user__isnull=True
            )
        if update_quantity:
            item.quantity = max(quantity, 1)
        else:
            item.quantity = item.quantity + max(quantity, 1)
        item.quantity = min(item.quantity, max(book.stock, 1))
        item.price = book.price
        item.save()

    def remove(self, book):
        self._base_queryset().filter(book=book).delete()

    def clear(self):
        self._base_queryset().delete()

    def __iter__(self):
        items = self._base_queryset().select_related('book')
        for item in items:
            yield {
                'book': item.book,
                'quantity': item.quantity,
                'price': item.price,
                'total_price': item.price * item.quantity,
                'id': item.id,
            }

    def __len__(self):
        return sum(item['quantity'] for item in self)

    def has_items(self):
        return bool(self._base_queryset().exists())

    def get_total_price(self):
        return sum(item['total_price'] for item in self)

    # --- Coupon support --------------------------------
    def _get_coupon(self):
        if self.session is None:
            return None
        coupon_id = self.session.get('coupon_id')
        if not coupon_id:
            return None
        from .models import Coupon
        try:
            coupon = Coupon.objects.get(pk=coupon_id)
        except Coupon.DoesNotExist:
            return None
        if not coupon.is_valid():
            return None
        return coupon

    def set_coupon(self, coupon):
        if self.session is not None:
            self.session['coupon_id'] = coupon.id
            self.session.save()

    def remove_coupon(self):
        if self.session is not None and 'coupon_id' in self.session:
            del self.session['coupon_id']
            self.session.save()

    def get_discount(self):
        coupon = self._get_coupon()
        if not coupon:
            return 0
        return min(coupon.discount_amount, self.get_total_price())

    def get_final_total_price(self):
        return self.get_total_price() - self.get_discount()