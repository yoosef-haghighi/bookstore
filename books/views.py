from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .forms import BookForm
from .models import Book, Comment, Category, Rating, Wishlist


class BookListView(generic.ListView):
    model = Book
    paginate_by = 6
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        qs = super().get_queryset().select_related('category').prefetch_related('ratings')
        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        user = self.request.user
        if user.is_authenticated:
            context['wishlist_books'] = Book.objects.filter(wishlists__user=user)
        else:
            context['wishlist_books'] = Book.objects.none()
        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('user')
        user = self.request.user
        context['user_rating'] = None
        if user.is_authenticated:
            context['user_rating'] = Rating.objects.filter(
                book=self.object, user=user
            ).first()
            context['wishlist_books'] = Book.objects.filter(wishlists__user=user)
        else:
            context['wishlist_books'] = Book.objects.none()
        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()

        if not request.user.is_authenticated:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'برای ارسال نظر ابتدا وارد شوید.'}, status=403)
            messages.error(request, 'برای ارسال نظر ابتدا وارد شوید.')
            return self.get(request, *args, **kwargs)

        body = request.POST.get('body', '').strip()
        if not body:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'متن نظر نمی‌تواند خالی باشد.'}, status=400)
            messages.error(request, 'متن نظر نمی‌تواند خالی باشد.')
            return self.get(request, *args, **kwargs)

        comment = Comment(book=book, user=request.user, body=body)
        comment.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'body': comment.body,
                    'username': comment.user.username,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                }
            })

        return self.get(request, *args, **kwargs)


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = BookForm
    template_name = 'books/book_create.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = BookForm
    template_name = 'books/book_update.html'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        book = self.get_object()
        if book.created_by != request.user:
            messages.error(request, 'شما اجازه ویرایش این کتاب را ندارید.')
            return HttpResponseForbidden('شما اجازه ویرایش این کتاب را ندارید.')
        return super().dispatch(request, *args, **kwargs)


class BookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('book_list')
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        book = self.get_object()
        if book.created_by != request.user:
            messages.error(request, 'شما اجازه حذف این کتاب را ندارید.')
            return HttpResponseForbidden('شما اجازه حذف این کتاب را ندارید.')
        return super().dispatch(request, *args, **kwargs)


class WishlistView(LoginRequiredMixin, generic.ListView):
    model = Wishlist
    template_name = 'books/wishlist.html'
    context_object_name = 'wishlist_items'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Wishlist.objects.filter(
            user=self.request.user
        ).select_related('book')


class WishlistToggleView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        wish = Wishlist.objects.filter(user=request.user, book=book)
        if wish.exists():
            wish.delete()
            added = False
        else:
            Wishlist.objects.create(user=request.user, book=book)
            added = True

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'added': added})

        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
        if next_url:
            return redirect(next_url)
        return redirect(reverse('book_detail', args=[pk]))


class RateBookView(generic.View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'برای امتیازدهی ابتدا وارد شوید.'}, status=403)

        book = get_object_or_404(Book, pk=pk)
        try:
            value = int(request.POST.get('value', 0))
        except (TypeError, ValueError):
            value = 0
        if value not in range(1, 6):
            return JsonResponse({'success': False, 'error': 'امتیاز باید بین ۱ تا ۵ باشد.'}, status=400)

        Rating.objects.update_or_create(
            book=book, user=request.user, defaults={'value': value}
        )
        return JsonResponse({
            'success': True,
            'average': book.average_rating,
            'count': book.rating_count,
        })