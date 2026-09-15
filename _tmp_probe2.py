import urllib.request, urllib.parse, ssl, json
ctx = ssl.create_default_context()
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120','Accept-Language':'fa-IR,fa;q=0.9'})
    try:
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            return r.geturl(), r.status, r.read().decode('utf-8','ignore')
    except Exception as e:
        return None, None, f'ERR {e}'

tests = {
 'taaghche search': 'https://taaghche.com/search?q=' + urllib.parse.quote('تازیانه‌های سبز'),
 'taaghche search2': 'https://taaghche.com/search/?search_term=' + urllib.parse.quote('تازیانه‌های سبز'),
 'ketabrah search': 'https://ketabrah.ir/search/' + urllib.parse.quote('تازیانه‌های سبز'),
 'fidibo search': 'https://fidibo.com/search?q=' + urllib.parse.quote('تازیانه‌های سبز'),
 'iranketab search': 'https://iranketab.ir/search?q=' + urllib.parse.quote('تازیانه‌های سبز'),
}
for name, url in tests.items():
    fu, st, body = get(url)
    print('===', name, '->', st, '|', fu)
    if body and not body.startswith('ERR'):
        import re
        print('  len:', len(body))
        if 'تازیانه' in body or 'taziane' in body.lower():
            print('  HAS query term')
        imgs = list(dict.fromkeys(re.findall(r'https://[^\"\']+?\.(?:jpg|png|jpeg|webp)', body)))[:8]
        print('  imgs:', imgs)
    else:
        print(' ', body[:150])
