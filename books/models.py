from django.conf import settings
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
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
