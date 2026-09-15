import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from books.models import Book, Category

# ── ساخت دسته‌بندی‌ها ──────────────────────────────────────────────

categories = {
    'رمان': 'roman',
    'شعر': 'sher',
    'روانشناسی و فلسفه': 'ravanshenasi',
    'ادبیات کودک': 'ketabe-koodak',
}

cat_objs = {}
for name, slug in categories.items():
    obj, created = Category.objects.get_or_create(
        slug=slug, defaults={'name': name}
    )
    cat_objs[slug] = obj
    print(f'{"[NEW]" if created else "[OK] "} دسته: {name}')

# ── نسبت دادن کتاب‌های موجود ────────────────────────────────────────

book_categories = {
    'roman': ['1984', 'برادران کارامازوف', 'صد سال تنهایی',
              'ملت عشق', 'کتابخانه نیمه شب', 'جزء از کل',
              'کیمیاگر', 'مغازه خودکشی'],
    'ravanshenasi': ['وقتی نیچه گریست'],
    'ketabe-koodak': ['شازده کوچولو'],
}

assigned = 0
for slug, titles in book_categories.items():
    for title in titles:
        try:
            book = Book.objects.get(title=title)
            book.category = cat_objs[slug]
            book.save(update_fields=['category'])
            assigned += 1
        except Book.DoesNotExist:
            print(f'  [!] "{title}" پیدا نشد — رد شد')

print(f'\n  کتاب‌های موجود وابسته شد: {assigned}')

# ── کتاب‌های جدید ─────────────────────────────────────────────────

new_books = [
    # ── شعر ──
    {
        'title': 'دیوان حافظ',
        'author': 'حافظ شیرازی',
        'description': 'غزلیات حافظ شیرازی، شاعر بزرگ قرن هشتم هجری، یکی از ماندگارترین آثار ادبیات فارسی است. حافظ با زبانی عاشقانه و رمزآلود، در قالب غزل از عشق، عرفان، سیاست و زندگی سخن گفته است.',
        'price': 120000,
        'category_slug': 'sher',
    },
    {
        'title': 'شعرهای سهراب سپهری',
        'author': 'سهراب سپهری',
        'description': 'مجموعه شعرهای سهراب سپهری، شاعر معاصر ایرانی، با تم‌های طبیعت، سکوت و جستجوی معنای زندگی. شعرهای ساده اما عمیق سپهری خواننده را به تأمل وامی‌دارد.',
        'price': 85000,
        'category_slug': 'sher',
    },
    {
        'title': 'تازیانه‌های سبز',
        'author': 'فروغ فرخزاد',
        'description': 'تازیانه‌های سبز سومین مجموعه شعر فروغ فرخزاد است که در آن صدای زن ایرانی با صراحت و شجاعت بی‌سابقه‌ای شنیده می‌شود. شعرهایی از عشق، تنهایی و بیداری.',
        'price': 78000,
        'category_slug': 'sher',
    },
    {
        'title': 'شمس تبریزی در کنار دیوان شمس',
        'author': 'مولانا جلال‌الدین رومی',
        'description': 'گزیده‌ای از اشعار شمس تبریزی مولانا با ترجمه و شرح معاصر. مولانا با الهام از شمس تبریزی، شاعر عارف، شعرهایی عاشقانه و عرفانی سرود که مرزهای زبانی را درنوردید.',
        'price': 95000,
        'category_slug': 'sher',
    },

    # ── روانشناسی و فلسفه ──
    {
        'title': 'انسان در جستجوی معنا',
        'author': 'اروین یالوم',
        'description': 'اروین یالوم در این کتاب تجربه زندگی در اردوگاه‌های کار اجباری نازی و تأثیر آن بر روح انسان را بررسی می‌کند. کتابی که به همه کسانی که به دنبال معنای زندگی هستند توصیه می‌شود.',
        'price': 92000,
        'category_slug': 'ravanshenasi',
    },
    {
        'title': 'هنر خوب زندگی کردن',
        'author': 'اروین یالوم',
        'description': 'یالوم در این اثر، داستان‌هایی واقعی از جلسات روان‌درمانی را روایت می‌کند و از درون آنها، درس‌های عمیقی درباره زندگی، مرگ، آزادی و مسئولیت ارائه می‌دهد.',
        'price': 105000,
        'category_slug': 'ravanshenasi',
    },
    {
        'title': 'اعداد حرف می‌زنند',
        'author': 'ناتانیل پاپ',
        'description': 'کتابی جذاب درباره آمار، احتمالات و نحوه تحلیل داده‌ها در زندگی روزمره. ناتانیل پاپ با زبانی ساده و طنزآمیز نشان می‌دهد چگونه اعداد می‌توانند حقیقت را پنهان یا آشکار کنند.',
        'price': 68000,
        'category_slug': 'ravanshenasi',
    },
    {
        'title': 'عادات اتمی',
        'author': 'جیمز کلیر',
        'description': 'جیمز کلیر در این کتاب سیستمی عملی برای شکستن عادت‌های بد و ایجاد عادت‌های خوب ارائه می‌دهد. با تکیه بر تحقیقات علمی، نشان می‌دهد چگونه تغییرات کوچک روزانه به نتایج بزرگ منجر می‌شوند.',
        'price': 72000,
        'category_slug': 'ravanshenasi',
    },

    # ── ادبیات کودک ──
    {
        'title': 'خاله سوسکه',
        'author': 'محمد هاشم اکبریانی',
        'description': 'خاله سوسکه یکی از محبوب‌ترین قصه‌های کودکان ایرانی است که توسط محمد هاشم اکبریانی نوشته شده و در مجموعه‌ی قصه‌های خوب برای بچه‌های خوب منتشر شده است.',
        'price': 45000,
        'category_slug': 'ketabe-koodak',
    },
    {
        'title': 'کلیله و دمنه',
        'author': 'عبدالله بن المقفع',
        'description': 'کلیله و دمنه مجموعه‌ای از افسانه‌های حیوانات است که در قرن دوم هجری به فارسی ترجمه شد. این اثر با زبانی ساده و داستان‌های آموزنده، درس‌های اخلاقی و اجتماعی را به کودکان می‌آموزد.',
        'price': 55000,
        'category_slug': 'ketabe-koodak',
    },
    {
        'title': 'مری پاپینز',
        'author': 'پی. ال. تراورس',
        'description': 'مری پاپینز داستان پرستاری جادویی است که با چترش از آسمان می‌آید و زندگی خانواده بانکس را در لندن دگرگون می‌کند. ماجراهای شگفت‌انگیز و طنزآمیزی که هم کودکان و هم بزرگسالان را مسحور می‌کند.',
        'price': 62000,
        'category_slug': 'ketabe-koodak',
    },
]

created_count = 0
for b in new_books:
    if Book.objects.filter(title=b['title']).exists():
        print(f'  [SKIP] "{b["title"]}" قبلاً وجود دارد')
        continue
    cat = cat_objs.get(b['category_slug']) if b['category_slug'] else None
    Book.objects.create(
        title=b['title'],
        author=b['author'],
        description=b['description'],
        price=b['price'],
        category=cat,
    )
    created_count += 1
    print(f'  [NEW]  {b["title"]}')

print(f'\n  کتاب‌های جدید ساخته شد: {created_count}')
print(f'  مجموع کل کتاب‌ها: {Book.objects.count()}')
print(f'  مجموع دسته‌ها: {Category.objects.count()}')
print('\n  تمام شد!')
