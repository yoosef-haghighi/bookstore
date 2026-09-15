import urllib.request, urllib.parse, ssl, re
ctx = ssl.create_default_context()
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120','Accept-Language':'fa-IR,fa;q=0.9'})
    with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
        return r.read().decode('utf-8','ignore')

body = get('https://taaghche.com/search?q=' + urllib.parse.quote('تازیانه‌های سبز'))
# book links
links = list(dict.fromkeys(re.findall(r'href="(/books/[a-zA-Z0-9\-_]+)"', body)))
print('book links:', links[:15])
# any img tags: data-src, data-srcset, src
for m in re.findall(r'<img[^>]+>', body)[:15]:
    print('IMG:', m[:160])
