import urllib.request, urllib.parse, ssl, re, json
ctx = ssl.create_default_context()
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120','Accept-Language':'fa-IR,fa;q=0.9'})
    with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
        return r.geturl(), r.read().decode('utf-8','ignore')

# 1 taaghche NEXT_DATA
fu, body = get('https://taaghche.com/search?q=' + urllib.parse.quote('تازیانه‌های سبز'))
m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', body, re.S)
print('taaghche has NEXT_DATA:', bool(m))
if m:
    data = json.loads(m.group(1))
    s = json.dumps(data, ensure_ascii=False)
    # find slugs with taziane or book-like paths
    hits = re.findall(r'"(?:slug|alias|key|url)":\s*"([^"]*taziane[^"]*)"', s, re.I)
    print('slug hits:', hits[:10])
    books = re.findall(r'"(?:slug|alias)":\s*"([^"]{4,80})"', s)
    print('slugs sample:', [b for b in books if not b.startswith('/')][:40])

# 2 ketabrah search form
fu, b2 = get('https://ketabrah.ir')
forms = re.findall(r'<form[^>]*action="([^"]*)"[^>]*>', b2)
print('ketabrah forms:', forms[:5])
print('ketabrah action attr search-input:', re.findall(r'(?:class|id)="[^"]*search[^"]*"[^>]*', b2)[:3])
inputs = re.findall(r'<input[^>]*name="([^"]*)"', b2)
print('ketabrah inputs:', inputs[:10])
