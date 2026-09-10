from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .models import Book, Comment


class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    template_name = 'books/book_list.html'
    context_object_name = 'books'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('user')
        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()

        if not request.user.is_authenticated:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'برای ارسال نظر ابتدا وارد شوید.'}, status=403)
            from django.contrib import messages
            messages.error(request, 'برای ارسال نظر ابتدا وارد شوید.')
            return self.get(request, *args, **kwargs)

        body = request.POST.get('body', '').strip()
        if not body:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'متن نظر نمی‌تواند خالی باشد.'}, status=400)
            from django.contrib import messages
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
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover']
    template_name = 'books/book_create.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover']
    template_name = 'books/book_update.html'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        book = self.get_object()
        if book.created_by != request.user:
            from django.contrib import messages
            from django.http import HttpResponseForbidden
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
            from django.contrib import messages
            from django.http import HttpResponseForbidden
            messages.error(request, 'شما اجازه حذف این کتاب را ندارید.')
            return HttpResponseForbidden('شما اجازه حذف این کتاب را ندارید.')
        return super().dispatch(request, *args, **kwargs)
