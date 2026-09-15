from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from books.models import Book
from .cart import Cart
from .models import Order, OrderItem


class _StubRequest:
    def __init__(self, session):
        self.session = session


def _cart_from_client(client):
    return Cart(_StubRequest(client.session))


class CartTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='alice', email='alice@example.com', password='testpass123'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Some Author',
            description='A cart test book',
            price=1000,
        )
        self.book2 = Book.objects.create(
            title='Second Book',
            author='Another Author',
            description='Another book',
            price=2000,
        )

    def test_add_to_cart(self):
        response = self.client.post(reverse('cart_add', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        cart = _cart_from_client(self.client)
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart.get_total_price(), 1000)

    def test_cart_detail_page_shows_items(self):
        self.client.post(reverse('cart_add', args=[self.book.id]))
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    def test_anonymous_user_can_use_cart(self):
        self.client.post(reverse('cart_add', args=[self.book.id]))
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    def test_add_multiple_books_and_total(self):
        self.client.post(reverse('cart_add', args=[self.book.id]))
        self.client.post(reverse('cart_add', args=[self.book2.id]))
        cart = _cart_from_client(self.client)
        self.assertEqual(len(cart), 2)
        self.assertEqual(cart.get_total_price(), 3000)

    def test_update_quantity(self):
        self.client.post(reverse('cart_add', args=[self.book.id]))
        self.client.post(
            reverse('cart_update', args=[self.book.id]), {'quantity': '3'}
        )
        cart = _cart_from_client(self.client)
        self.assertEqual(len(cart), 3)
        self.assertEqual(cart.get_total_price(), 3000)

    def test_remove_from_cart(self):
        self.client.post(reverse('cart_add', args=[self.book.id]))
        self.client.post(reverse('cart_remove', args=[self.book.id]))
        cart = _cart_from_client(self.client)
        self.assertEqual(len(cart), 0)

    def test_empty_cart_page(self):
        response = self.client.get(reverse('cart_detail'))
        self.assertContains(response, 'سبد خرید شما خالی است')


class OrderTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='alice', email='alice@example.com', password='testpass123'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Some Author',
            description='An order test book',
            price=1000,
        )
        self.book2 = Book.objects.create(
            title='Second Book',
            author='Another Author',
            description='Another book',
            price=2000,
        )

    def test_checkout_requires_login(self):
        response = self.client.get(reverse('checkout'))
        self.assertIn(response.status_code, [302, 403])

    def test_checkout_with_empty_cart_redirects(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)

    def test_place_order_creates_order_and_items(self):
        self.client.login(username='alice', password='testpass123')
        self.client.post(reverse('cart_add', args=[self.book.id]))
        self.client.post(
            reverse('cart_add', args=[self.book2.id]),
            {'quantity': '2'},
        )
        response = self.client.post(
            reverse('checkout'),
            {
                'first_name': 'علی',
                'last_name': 'محمدی',
                'phone': '09120000000',
                'address': 'تهران، خیابان انقلاب',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_price, 1000 + 2000 * 2)
        self.assertEqual(order.items.count(), 2)
        self.assertEqual(order.status, 'pending')

    def test_order_created_with_correct_snapshot_prices(self):
        self.client.login(username='alice', password='testpass123')
        self.client.post(reverse('cart_add', args=[self.book.id]))
        self.client.post(reverse('checkout'), {
            'first_name': 'علی',
            'last_name': 'محمدی',
            'phone': '09120000000',
            'address': 'تهران',
        })
        items = OrderItem.objects.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items.first().book, self.book)
        self.assertEqual(items.first().price, 1000)

    def test_cart_cleared_after_order(self):
        self.client.login(username='alice', password='testpass123')
        self.client.post(reverse('cart_add', args=[self.book.id]))
        self.client.post(reverse('checkout'), {
            'first_name': 'علی',
            'last_name': 'محمدی',
            'phone': '09120000000',
            'address': 'تهران',
        })
        cart = _cart_from_client(self.client)
        self.assertEqual(len(cart), 0)

    def test_order_list_shows_only_own_orders(self):
        other_user = get_user_model().objects.create_user(
            username='bob', email='bob@example.com', password='testpass123'
        )
        order = Order.objects.create(
            user=self.user, first_name='علی', last_name='محمدی',
            phone='09120000000', address='تهران', total_price=1000,
        )
        Order.objects.create(
            user=other_user, first_name='رضا', last_name='احمدی',
            phone='09130000000', address='شیراز', total_price=500,
        )
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('order_list'))
        self.assertContains(response, f'سفارش #{order.id}')
        self.assertNotContains(response, 'رضا')

    def test_order_success_page_requires_order_owner(self):
        self.client.login(username='alice', password='testpass123')
        order = Order.objects.create(
            user=self.user, first_name='علی', last_name='محمدی',
            phone='09120000000', address='تهران', total_price=1000,
        )
        response = self.client.get(reverse('order_success', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'سفارش شما با موفقیت ثبت شد')