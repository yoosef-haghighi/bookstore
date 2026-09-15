from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'description', 'price', 'old_price',
            'stock', 'publisher', 'isbn', 'publication_year',
            'category', 'cover',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'publication_year': forms.NumberInput(attrs={'placeholder': 'مثلاً 1402'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'مثلاً 978-964-311-000-0'}),
        }

    def clean(self):
        cleaned = super().clean()
        price = cleaned.get('price')
        old_price = cleaned.get('old_price')
        if price and old_price and old_price <= price:
            raise forms.ValidationError(
                'قیمت اصلی باید از قیمت فروش بیشتر باشد تا تخفیف معتبر باشد.'
            )
        return cleaned