import json
import os
import re
import urllib.parse
import urllib.request

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from PIL import Image
from django.core.files.base import ContentFile

from books.models import Book

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36'

WIKI_EN = 'https://en.wikipedia.org/api/rest_v1/page'
WIKI_FA = 'https://fa.wikipedia.org/api/rest_v1/page'
FIDIBO = 'https://fidibo.com'


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=timeout)


def get_json(url):
    return json.loads(get(url).read().decode('utf-8'))


def get_html(url):
    return get(url).read().decode('utf-8', 'ignore')


def wiki_cover(summary_url):
    try:
        j = get_json(summary_url)
        img = j.get('originalimage', {}).get('source') or j.get('thumbnail', {}).get('source')
        if img and 'svg' not in img.lower():
            return img
    except Exception:
        pass
    return None


def wiki_media_list(page_title):
    try:
        url = f'https://en.wikipedia.org/api/rest_v1/page/media-list/{urllib.parse.quote(page_title)}'
        j = get_json(url)
        for item in j.get('items', []):
            if item.get('type') == 'image' and item.get('srcset'):
                for s in item['srcset']:
                    if s.get('scale', '') == '1x':
                        src = s.get('src', '')
                        if 'svg' not in src.lower() and 'icon' not in src.lower():
                            return 'https:' + src if src.startswith('//') else src
    except Exception:
        pass
    return None


def download_cover(url):
    try:
        data = get(url, timeout=40).read()
        if len(data) < 1500:
            return None
        img = Image.open(__import__('io').BytesIO(data))
        img.load()
        w, h = img.size
        if w < 150 or h < 200:
            return None
        buf = __import__('io').BytesIO()
        img.convert('RGB').save(buf, 'JPEG', quality=88)
        return buf.getvalue()
    except Exception:
        return None


BOOK_SOURCES = [
    {
        'id': 24, 'title': 'دیوان حافظ',
        'wiki_en': 'Divan_of_Hafez',
        'wiki_fa': 'دیوان_حافظ',
        'fidibo_cats': ['/ebooks/literature-poetry-persian'],
        'bing_query': 'دیوان حافظ book cover حافظ شیرازی',
    },
    {
        'id': 25, 'title': 'شعرهای سهراب سپهری',
        'wiki_en': 'Sohrab_Sepehri',
        'wiki_fa': 'شعرهای_سهراب_سپهری',
        'fidibo_cats': ['/ebooks/literature-poetry-persian'],
        'bing_query': 'شعرهای سهراب سپهری جلد کتاب',
    },
    {
        'id': 26, 'title': 'تازیانه‌های سبز',
        'wiki_en': 'Forough_Farrokhzad',
        'wiki_fa': 'تازیانه‌های_سبز',
        'fidibo_cats': ['/ebooks/literature-poetry-persian'],
        'bing_query': 'تازیانه های سبز فروغ فرخزاد جلد کتاب',
    },
    {
        'id': 27, 'title': 'شمس تبریزی در کنار دیوان شمس',
        'wiki_en': 'Shams_Tabrizi',
        'wiki_fa': None,
        'fidibo_cats': ['/ebooks/literature-poetry-persian', '/ebooks/philosophy'],
        'bing_query': 'شمس تبریزی در کنار دیوان شمس مولانا',
    },
    {
        'id': 28, 'title': 'انسان در جستجوی معنا',
        'wiki_en': 'Man%27s_Search_for_Meaning',
        'wiki_fa': 'انسان_در_جستجوی_معنا',
        'fidibo_cats': ['/ebooks/psychology'],
        'bing_query': 'انسان در جستجوی معنا ویکتور فرانکل',
    },
    {
        'id': 29, 'title': 'هنر خوب زندگی کردن',
        'wiki_en': None,
        'wiki_fa': None,
        'fidibo_cats': ['/ebooks/psychology'],
        'bing_query': 'هنر خوب زندگی کردن جلد کتاب',
    },
    {
        'id': 30, 'title': 'اعداد حرف می‌زنند',
        'wiki_en': None,
        'wiki_fa': None,
        'fidibo_cats': ['/ebooks/psychology'],
        'bing_query': 'اعداد حرف می زنند کتاب',
    },
    {
        'id': 31, 'title': 'عادات اتمی',
        'wiki_en': 'Atomic_Habits',
        'wiki_fa': 'عادت_اتمی',
        'fidibo_url': 'https://fidibo.com/book/99791-%D8%B9%D8%A7%D8%AF%D8%AA-%D8%A7%D8%AA%D9%85%DB%8C',
        'fidibo_cats': ['/ebooks/psychology-personal-development'],
        'bing_query': 'عادات اتمی جیمز کلیر جلد کتاب',
    },
    {
        'id': 32, 'title': 'خاله سوسکه',
        'wiki_en': None,
        'wiki_fa': 'خاله_سوسکه',
        'fidibo_cats': ['/ebooks/kid'],
        'bing_query': 'خاله سوسکه محمد هاشم اکبریانی جلد کتاب',
    },
    {
        'id': 33, 'title': 'کلیله و دمنه',
        'wiki_en': 'Kalila_and_Dimna',
        'wiki_fa': 'کلیله_و_دمنه',
        'fidibo_cats': ['/ebooks/literature', '/ebooks/kid'],
        'bing_query': 'کلیله و دمنه جلد کتاب',
    },
    {
        'id': 34, 'title': 'مری پاپینز',
        'wiki_en': 'Mary_Poppins',
        'wiki_fa': 'مری_پاپینز',
        'fidibo_cats': ['/ebooks/kid'],
        'bing_query': 'مری پاپینز جلد کتاب',
    },
]

SEARCHABLE_BOOKS = {b['id']: b for b in BOOK_SOURCES}


def extract_cover_urls_from_fidibo(html):
    return re.findall(r'(https://cdn\.fidibo\.com/phoenixpub/content/[^\s"\'?]+\.jpg)', html)


def search_fidibo_cats(book_info):
    for cat_url in book_info.get('fidibo_cats', []):
        try:
            html = get_html(FIDIBO + cat_url)
            covers = extract_cover_urls_from_fidibo(html)
            title = book_info['title'].replace('\u200c', ' ')
            for cover_url in covers:
                if 'width=' in cover_url:
                    cover_url = cover_url.split('?')[0]
                if 'svg' in cover_url.lower():
                    continue
                return cover_url + '?width=600'
        except Exception:
            continue
    return None


def find_cover(book_info):
    bid = book_info['id']
    title = book_info['title']

    print(f'  [1] Wikipedia EN...')
    for page in [book_info.get('wiki_en')]:
        if page:
            url = wiki_cover(f'{WIKI_EN}/summary/{urllib.parse.quote(page)}')
            if url:
                return url, f'wiki-en:{page}'

    print(f'  [2] Wikipedia FA...')
    for page in [book_info.get('wiki_fa')]:
        if page:
            url = wiki_cover(f'{WIKI_FA}/summary/{urllib.parse.quote(page)}')
            if url:
                return url, f'wiki-fa:{page}'

    print(f'  [3] Fidibo direct...')
    if book_info.get('fidibo_url'):
        try:
            html = get_html(book_info['fidibo_url'])
            covers = extract_cover_urls_from_fidibo(html)
            if covers:
                return covers[0] + '?width=600', 'fidibo-direct'
        except Exception:
            pass

    print(f'  [4] Fidibo categories...')
    cover = search_fidibo_cats(book_info)
    if cover:
        return cover, 'fidibo-cat'

    return None, None


def main():
    ok, fail = 0, 0
    for book_info in BOOK_SOURCES:
        bid = book_info['id']
        book = Book.objects.get(id=bid)
        print(f'\n== {bid} {book.title}')

        cover_url, source = find_cover(book_info)
        if cover_url:
            print(f'  downloading from {source}: {cover_url[:120]}')
            jpg = download_cover(cover_url)
            if jpg:
                filename = f'book{bid}.jpg'
                if book.cover:
                    book.cover.delete(save=False)
                book.cover.save(filename, ContentFile(jpg), save=True)
                print(f'  OK  {filename} ({len(jpg)} bytes)')
                ok += 1
                continue

        print(f'  FAILED - no cover found')
        fail += 1

    print(f'\nDone: {ok} OK, {fail} failed.')


if __name__ == '__main__':
    main()