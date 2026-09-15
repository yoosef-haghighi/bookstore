import urllib.request, urllib.parse, json, ssl
ctx = ssl.create_default_context()
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            return r.read().decode('utf-8', 'ignore')
    except Exception as e:
        return f'ERR {e}'

for q in ['تازیانه‌های سبز فروغ', 'شمس تبریزی در کنار دیوان شمس', 'اعداد حرف می‌زنند']:
    u = 'https://fa.wikipedia.org/w/api.php?action=query&list=search&format=json&srlimit=5&srsearch=' + urllib.parse.quote(q)
    data = get(u)
    print('=== WIKI:', q)
    if not data.startswith('ERR'):
        for item in json.loads(data).get('query', {}).get('search', []):
            print(' -', item['title'])
    else:
        print(data)

for q in ['تازیانه‌های سبز', 'شمس تبریزی', 'اعداد حرف می‌زنند']:
    u = 'https://www.googleapis.com/books/v1/volumes?q=' + urllib.parse.quote(q)
    data = get(u)
    print('=== GBOOKS:', q)
    if not data.startswith('ERR'):
        try:
            items = json.loads(data).get('items', [])[:5]
            for it in items:
                vi = it['volumeInfo']
                print(' -', vi.get('title'), '|', vi.get('authors'))
        except Exception as e:
            print('parse err', e, data[:200])
    else:
        print(data)
