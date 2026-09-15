from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    WishlistView,
    WishlistToggleView,
    RateBookView,
)


urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/toggle/<int:pk>/', WishlistToggleView.as_view(), name='wishlist_toggle'),
    path('book/rate/<int:pk>/', RateBookView.as_view(), name='book_rate'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('new/', BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/edit', BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete', BookDeleteView.as_view(), name='book_delete'),
]