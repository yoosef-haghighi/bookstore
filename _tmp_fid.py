import urllib.request, urllib.parse, ssl
ctx = ssl.create_default_context()
def get(url, referer=None):
    h = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}
    if referer: h['Referer'] = referer
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            return r.status, r.read().decode('utf-8', 'ignore')
    except Exception as e:
        return None, f'ERR {e}'

for q in ['تازیانه‌های سبز فروغ فرخزاد', 'شمس تبریزی در کنار دیوان شمس', 'اعداد حرف می‌زنند ناتانیل پاپ']:
    u = 'https://fidibo.com/search?q=' + urllib.parse.quote(q)
    st, body = get(u)
    print('=== fidibo', q, st, type(body))
    if body and not body.startswith('ERR'):
        body = get(u)[1]
        import re
        titles = re.findall(r'<a[^>]*>(.{0,90})</a>', body)
        print('  len', len(body))
        # look for og:image or product links
        imgs = re.findall(r'(https://[^"\']+?(?:jpg|png|jpeg|webp))', body)
        print('  imgs sample:', imgs[:6])
        # book links
        links = set(re.findall(r'/book/\d+', body))
        print('  book links:', list(links)[:10])
