from django.contrib import admin
from .models import Book, Comment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'created_by')
    list_filter = ('created_by',)
    search_fields = ('title', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'body', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('body',)
