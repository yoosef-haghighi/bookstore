import urllib.request, urllib.parse, ssl, json
ctx = ssl.create_default_context()
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120','Accept':'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            return r.status, r.read().decode('utf-8','ignore')
    except Exception as e:
        return None, f'ERR {e}'

for q in ['تازیانه‌های سبز فروغ', 'شمس تبریزی در کنار دیوان شمس', 'اعداد حرف می‌زنند']:
    st, body = get('https://api.digikala.com/v1/search/?q=' + urllib.parse.quote(q))
    print('=== digikala', q, '->', st)
    if st == 200:
        try:
            d = json.loads(body)
            prods = d.get('data', {}).get('products', [])
            for p in prods[:5]:
                print('  -', p.get('title_fa'), '|', p.get('url', {}).get('uri', ''), '|', p.get('images', {}).get('main', {}).get('url', '')[:80])
        except Exception as e:
            print('  parse err', e, body[:200])
    else:
        print(' ', body[:150])
