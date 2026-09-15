import io
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

GOOD_HOST_HINTS = [
    'fidibo.com', 'cdn.fidibo.com',
    'taaghche.com', 'cdn.taaghche.com',
    'iranketab', 'adinehbook', 'bookroom', 'zoodkitab',
    'noorlib', 'ketab', 'fidilia', 'vaykart', 'digikala',
]

SKIP_HOST_HINTS = [
    'instagram', 'facebook', 'twitter', 'aparat',
    'gstatic.com', 'googleusercontent', 'quiz', 'pinterest',
]


def fetch(url, timeout=40):
    last = None
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            return urllib.request.urlopen(req, timeout=timeout)
        except Exception as e:
            last = e
    raise last


def bing_candidates(query, limit=12):
    q = urllib.parse.quote(query)
    html = fetch('https://www.bing.com/images/search?q=' + q + '&form=HDRSC2').read().decode('utf-8', 'ignore')
    murls = []
    for m in re.finditer(r'murl&quot;:&quot;(.*?)&quot;', html):
        url = m.group(1)
        url = url.replace('\\/', '/').replace('&amp;', '&')
        if url in murls:
            continue
        murls.append(url)
    return murls[:limit]


def score(url):
    s = 0
    low = url.lower()
    for h in GOOD_HOST_HINTS:
        if h in low:
            s += 3
    for h in SKIP_HOST_HINTS:
        if h in low:
            s -= 5
    if re.search(r'\.(jpe?g|png|webp)(\?|$)', low, re.I):
        s += 1
    if 'logo' in low or 'icon' in low:
        s -= 3
    return s


def download_valid(url):
    _, ext = os.path.splitext(urllib.parse.urlparse(url).path)
    ext = ext.lower()
    if ext in ('.svg', '.gif', '.ico'):
        return None
    data = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': UA,
                'Referer': 'https://www.bing.com/',
                'Accept': 'image/webp,image/*,*/*;q=0.8',
            })
            data = urllib.request.urlopen(req, timeout=50).read()
            break
        except Exception:
            continue
    if not data or len(data) < 2000:
        return None
    try:
        img = Image.open(io.BytesIO(data))
        img.load()
        w, h = img.size
        if w < 180 or h < 250:
            return None
        if h < w:
            return None
        if w / h < 0.55:
            return None
        buf = io.BytesIO()
        img.convert('RGB').save(buf, 'JPEG', quality=88)
        return buf.getvalue()
    except Exception:
        return None


def get_cover(book):
    title = book.title.replace('\u200c', ' ').strip()
    author = book.author.replace('\u200c', ' ').strip()
    queries = [
        f'جلد کتاب {title} {author}',
        f'کتاب {title} {author}',
        f'{title} {author} book cover',
    ]
    seen = set()
    attempts = 0
    for query in queries:
        for url in bing_candidates(query):
            if url in seen:
                continue
            seen.add(url)
            if score(url) < 1:
                continue
            attempts += 1
            if attempts > 10:
                return None, None
            print(f'      try[{attempts}]: {url[:130]}')
            jpg = download_valid(url)
            if jpg:
                return jpg, url
    return None, None


def main():
    books = [b for b in Book.objects.all() if b.cover and b.cover.name.endswith('.svg')]
    ok, fail = 0, 0
    for book in books:
        print(f'== {book.id} {book.title}')
        jpg, src = get_cover(book)
        if jpg:
            filename = os.path.basename(book.cover.name).replace('.svg', '.jpg')
            book.cover.delete(save=False)
            book.cover.save(filename, ContentFile(jpg), save=True)
            print(f'  OK  {book.id} | {filename} | {src[:120]}')
            ok += 1
        else:
            print(f'  --  {book.id} | {book.title}  (no valid cover found)')
            fail += 1
    print(f'Done: {ok} downloaded, {fail} left as SVG.')


if __name__ == '__main__':
    main()