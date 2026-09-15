from django.contrib import admin
from .models import Book, Comment, Category, Rating, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'stock', 'created_by')
    list_filter = ('category', 'created_by', 'publisher')
    search_fields = ('title', 'author', 'isbn')
    list_editable = ('stock', 'price')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'body', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('body',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'value', 'created_at')
    list_filter = ('value',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'created_at')