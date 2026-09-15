import urllib.request, urllib.parse, ssl
ctx = ssl.create_default_context()
def probe(name, url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            data = r.read(2000)
            print(f'{name:16s} OK {r.status} len~{len(r.read()) if hasattr(r,chr(114)) else 2000}')
    except Exception as e:
        print(f'{name:16s} FAIL {e}')

probe('fidibo home', 'https://fidibo.com')
probe('fidibo api search', 'https://fidibo.com/api/v1/search/?q=' + urllib.parse.quote('تازیانه'))
probe('taaghche', 'https://taaghche.com')
probe('ketabrah', 'https://ketabrah.ir')
probe('ketab.ir', 'https://ketab.ir')
probe('iranketab', 'https://iranketab.ir')
probe('openlibrary', 'https://openlibrary.org')
probe('wikipedia fa', 'https://fa.wikipedia.org')
