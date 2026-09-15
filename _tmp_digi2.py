import urllib.request, urllib.parse, ssl, json
ctx = ssl.create_default_context()
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 Chrome/120','Accept':'application/json'})
    with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
        return r.read().decode('utf-8','ignore')

def search(q, pages=1):
    out = []
    for pg in range(1, pages+1):
        body = get('https://api.digikala.com/v1/search/?q=' + urllib.parse.quote(q) + f'&page={pg}')
        try:
            d = json.loads(body)
            prods = d.get('data', {}).get('products', [])
        except Exception:
            prods = []
        for p in prods:
            out.append((p.get('title_fa'), p.get('url', {}).get('uri', ''), p.get('images', {}).get('main', {}).get('url', '')))
        # stop if fewer than 40 (last page)
        if len(prods) < 40: break
    return out

for q in ['تازیانه های سبز', 'شمس تبریزی در کنار دیوان', 'اعداد حرف می زنند']:
    print('===== SEARCH:', q)
    res = search(q, 2)
    print('  total:', len(res))
    for t, u, img in res[:12]:
        print('   -', t, '|', u[:70])
