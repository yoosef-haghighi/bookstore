from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'address', 'payment_method']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}),
            'phone': forms.TextInput(attrs={'placeholder': 'مثلاً 09121234567'}),
            'address': forms.Textarea(attrs={'placeholder': 'آدرس کامل پستی', 'rows': 3}),
            'payment_method': forms.RadioSelect(),
        }