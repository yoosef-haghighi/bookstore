from django.conf import settings
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    old_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name='قیمت اصلی (برای تخفیف)')
    stock = models.PositiveIntegerField(default=5, verbose_name='موجودی')
    publisher = models.CharField(max_length=200, blank=True, verbose_name='ناشر')
    isbn = models.CharField(max_length=20, null=True, blank=True, unique=True, verbose_name='شابک (ISBN)')
    publication_year = models.PositiveIntegerField(null=True, blank=True, verbose_name='سال انتشار')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
    )
    cover = models.ImageField(upload_to='covers/', blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id])

    @property
    def has_discount(self):
        return bool(self.old_price and self.old_price > self.price)

    @property
    def discount_percent(self):
        if self.has_discount:
            return int((self.old_price - self.price) / self.old_price * 100)
        return 0

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def rating_count(self):
        return self.ratings.count()

    @property
    def average_rating(self):
        total = sum(r.value for r in self.ratings.all())
        count = self.ratings.count()
        return round(total / count, 1) if count else 0


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} on {self.book.title}'

    def clean(self):
        if not self.body or not self.body.strip():
            raise ValidationError({'body': 'Comment body cannot be empty.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    value = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('book', 'user')]

    def __str__(self):
        return f'{self.user.username} rated {self.book.title} -> {self.value}'


class Wishlist(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='wishlists')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlist',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [('user', 'book')]

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'
