from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Book, Comment


class CommentTests(TestCase):
    def setUp(self):
        self.user_a = get_user_model().objects.create_user(
            username='alice', email='alice@example.com', password='testpass123'
        )
        self.user_b = get_user_model().objects.create_user(
            username='bob', email='bob@example.com', password='testpass123'
        )
        self.book = Book.objects.create(
            title='Book A',
            author='Some Author',
            description='A test book',
            price=1000,
            created_by=self.user_a,
        )
        self.old_comment = Comment.objects.create(
            book=self.book,
            user=self.user_b,
            body='An existing comment from a viewer.',
        )

    # Scenario 1: Logged-out user views a book and can see comments
    def test_logged_out_user_can_view_comments(self):
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'An existing comment from a viewer.')
        self.assertContains(response, self.user_b.username)

    # Scenario 2: Logged-out user tries to comment -> blocked and asked to log in
    def test_logged_out_user_cannot_comment(self):
        response = self.client.post(
            reverse('book_detail', args=[self.book.id]),
            {'body': 'I want to comment'},
        )
        # Blocked: comment must NOT be created; page shows login prompt
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.filter(body='I want to comment').count(), 0)
        self.assertContains(response, 'ورود به حساب کاربری')
        self.assertContains(response, 'برای ارسال نظر ابتدا باید وارد')

    def test_logged_out_user_ajax_comment_rejected(self):
        response = self.client.post(
            reverse('book_detail', args=[self.book.id]),
            {'body': 'I want to comment'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Comment.objects.filter(body='I want to comment').count(), 0)

    # Scenario 3: Logged-in user submits a valid comment -> created successfully
    def test_logged_in_user_can_comment(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.post(
            reverse('book_detail', args=[self.book.id]),
            {'body': 'This is a valid comment.'},
        )
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.filter(book=self.book, body='This is a valid comment.')
        self.assertEqual(comment.count(), 1)
        self.assertEqual(comment.first().user, self.user_b)

    def test_logged_in_user_comment_ajax_success(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.post(
            reverse('book_detail', args=[self.book.id]),
            {'body': 'AJAX comment'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['comment']['username'], 'bob')
        self.assertEqual(Comment.objects.filter(body='AJAX comment').count(), 1)

    # Scenario 4: Logged-in user submits an empty comment -> rejected
    def test_empty_comment_rejected(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.post(
            reverse('book_detail', args=[self.book.id]),
            {'body': '   '},
        )
        self.assertIn(response.status_code, [200, 400])
        self.assertEqual(Comment.objects.all().count(), 1)  # only the setUp comment
        self.assertEqual(Comment.objects.filter(body='   ').count(), 0)

    def test_empty_comment_ajax_rejected(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.post(
            reverse('book_detail', args=[self.book.id]),
            {'body': ''},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(Comment.objects.all().count(), 1)

    # Prevents user impersonation: comment author must come from the session
    def test_cannot_impersonate_another_user_in_comment(self):
        self.client.login(username='bob', password='testpass123')
        # Attempt to inject a user_id field through the request body
        response = self.client.post(
            reverse('book_detail', args=[self.book.id]),
            {'body': 'Trying to fake the author', 'user': self.user_a.id, 'user_id': self.user_a.id},
        )
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.get(book=self.book, body='Trying to fake the author')
        # Author must be bob (the authenticated session user), NOT alice
        self.assertEqual(comment.user, self.user_b)

    def test_comment_persisted_in_database(self):
        self.client.login(username='bob', password='testpass123')
        self.client.post(
            reverse('book_detail', args=[self.book.id]),
            {'body': 'Persisted in the DB'},
        )
        comment = Comment.objects.get(body='Persisted in the DB')
        self.assertEqual(comment.book, self.book)
        self.assertEqual(comment.user, self.user_b)
        self.assertIsNotNone(comment.created_at)

    # Scenario 9: Existing comments continue to work correctly
    def test_existing_comments_still_visible(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertContains(response, 'An existing comment from a viewer.')


class BookOwnershipTests(TestCase):
    def setUp(self):
        self.user_a = get_user_model().objects.create_user(
            username='alice', email='alice@example.com', password='testpass123'
        )
        self.user_b = get_user_model().objects.create_user(
            username='bob', email='bob@example.com', password='testpass123'
        )
        self.book = Book.objects.create(
            title='Book A',
            author='Some Author',
            description='Alice authored this book entry',
            price=1000,
            created_by=self.user_a,
        )

    # Scenario 5: Owner can edit their own book
    def test_owner_can_edit_own_book(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('book_update', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse('book_update', args=[self.book.id]),
            {'title': 'Updated Title', 'author': 'Some Author',
             'description': 'Updated desc', 'price': '2000', 'cover': ''},
        )
        self.assertIn(response.status_code, [302, 200])
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    # Scenario 6: Another authenticated user cannot edit
    def test_other_user_cannot_edit(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.get(reverse('book_update', args=[self.book.id]))
        self.assertEqual(response.status_code, 403)

    def test_other_user_cannot_edit_direct_post(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.post(
            reverse('book_update', args=[self.book.id]),
            {'title': 'Hacked', 'author': 'Bad',
             'description': 'Changed by bob', 'price': '9999', 'cover': ''},
        )
        self.assertEqual(response.status_code, 403)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Book A')  # unchanged

    # Scenario 7: Logged-out user cannot edit
    def test_logged_out_user_cannot_edit(self):
        response = self.client.get(reverse('book_update', args=[self.book.id]))
        # Either redirect to login or 403 - both are rejections
        self.assertIn(response.status_code, [302, 403])

    def test_logged_out_user_cannot_edit_direct_post(self):
        response = self.client.post(
            reverse('book_update', args=[self.book.id]),
            {'title': 'Hacked', 'author': 'Bad',
             'description': 'Changed by anonymous', 'price': '9999', 'cover': ''},
        )
        self.assertIn(response.status_code, [302, 403])
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Book A')  # unchanged

    # Scenario 8: Direct API bypass attempt by another user -> rejected
    def test_api_bypass_rejected(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.post(
            reverse('book_update', args=[self.book.id]),
            {'title': 'Hacked via API', 'author': 'Bad',
             'description': 'Changed by bob via direct API', 'price': '9999', 'cover': ''},
        )
        self.assertEqual(response.status_code, 403)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Book A')

    # Never trust user-provided owner/creator ID in the request body
    def test_cannot_transfer_ownership_via_request_body(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(
            reverse('book_update', args=[self.book.id]),
            {'title': 'Still Alices Book', 'author': 'Some Author',
             'description': 'Ownership must stay with alice', 'price': '1000', 'cover': '',
             'created_by': self.user_b.id},
        )
        self.assertIn(response.status_code, [302, 200])
        self.book.refresh_from_db()
        self.assertEqual(self.book.created_by, self.user_a)

    # Owner determined from authenticated user + book creator ID
    def test_owner_is_created_by_authenticated_user(self):
        self.assertEqual(self.book.created_by, self.user_a)

    # Scenario 9: Existing books continue to work correctly
    def test_existing_books_still_viewable(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book A')


class BookCreateTests(TestCase):
    def setUp(self):
        self.user_a = get_user_model().objects.create_user(
            username='alice', email='alice@example.com', password='testpass123'
        )

    def test_logged_out_user_cannot_create_book(self):
        response = self.client.get(reverse('book_create'))
        self.assertIn(response.status_code, [302, 403])
        self.assertEqual(Book.objects.count(), 0)

    def test_logged_in_user_create_book_sets_owner(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(
            reverse('book_create'),
            {'title': 'New Book', 'author': 'Author X',
             'description': 'Created by alice', 'price': '5000', 'cover': ''},
        )
        self.assertIn(response.status_code, [302, 200])
        book = Book.objects.get(title='New Book')
        self.assertEqual(book.created_by, self.user_a)

    def test_cannot_impersonate_owner_on_create(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(
            reverse('book_create'),
            {'title': 'Fake Owner Book', 'author': 'Author X',
             'description': 'Creator must be alice', 'price': '5000', 'cover': '',
             'created_by': 99999},
        )
        self.assertIn(response.status_code, [302, 200])
        book = Book.objects.get(title='Fake Owner Book')
        self.assertEqual(book.created_by, self.user_a)


class BookDeleteTests(TestCase):
    def setUp(self):
        self.user_a = get_user_model().objects.create_user(
            username='alice', email='alice@example.com', password='testpass123'
        )
        self.user_b = get_user_model().objects.create_user(
            username='bob', email='bob@example.com', password='testpass123'
        )
        self.book = Book.objects.create(
            title='Book A',
            author='Some Author',
            description='Alice authored this',
            price=1000,
            created_by=self.user_a,
        )

    def test_owner_can_delete(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('book_delete', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_delete(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.get(reverse('book_delete', args=[self.book.id]))
        self.assertEqual(response.status_code, 403)
        self.client.post(reverse('book_delete', args=[self.book.id]))
        self.assertEqual(Book.objects.filter(id=self.book.id).count(), 1)

    def test_logged_out_user_cannot_delete(self):
        response = self.client.get(reverse('book_delete', args=[self.book.id]))
        self.assertIn(response.status_code, [302, 403])
        self.assertEqual(Book.objects.filter(id=self.book.id).count(), 1)