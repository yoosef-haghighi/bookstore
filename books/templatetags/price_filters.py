from django import template

register = template.Library()

FA_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
ARABIC_DIGITS = str.maketrans('٠١٢٣٤٥٦٧٨٩', '۰۱۲۳۴۵۶۷۸۹')


@register.filter(name='fa_num')
def fa_num(value):
    try:
        return format(int(value), ',').translate(FA_DIGITS)
    except (TypeError, ValueError):
        return value


@register.filter(name='fa_digits')
def fa_digits(value):
    return str(value).translate(FA_DIGITS).translate(ARABIC_DIGITS)