import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files.base import ContentFile
from books.models import Book

FONT = "'Vazirmatn','IRANSansX',Tahoma,'Segoe UI',sans-serif"


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def wrap(text, fs, max_w=520, gap_ratio=0.62):
    cpr = max(6, int(max_w / (fs * gap_ratio)))
    words = text.split(' ')
    lines, cur = [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if len(trial) <= cpr:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def title_block(lines, fs, cx=300, top=360, line_gap=1.2, fill='#ffffff', shadow=True):
    tspans = ''.join(
        f'<tspan x="{cx}" y="{int(top + i * fs * line_gap)}">{esc(l)}</tspan>' for i, l in enumerate(lines)
    )
    sh = ''
    if shadow:
        sh = (f'<text font-size="{fs}" fill="#000000" fill-opacity="0.22">'
              f'<tspan x="{cx + 2}" y="{int(top + 2)}">{esc(" ".join(lines))}</tspan></text>')
    return f'<g text-anchor="middle" font-family="{FONT}" font-weight="bold">{sh}<text font-size="{fs}" fill="{fill}">{tspans}</text></g>'


def header(cx=300):
    return f'''
  <text x="{cx}" y="140" text-anchor="middle" font-family="{FONT}" font-size="28" fill="#ffffff" fill-opacity="0.95" font-weight="bold">کتابفروشی آنلاین</text>
  <text x="{cx}" y="176" text-anchor="middle" font-family="{FONT}" font-size="19" fill="#ffffff" fill-opacity="0.75">پرفروش‌ترین‌ها</text>
  <rect x="{cx-45}" y="196" width="90" height="4" rx="2" fill="#ffffff" opacity="0.55"/>'''


def author_line(text, y=655, fs=28, fill='#ffffff'):
    return f'<text x="300" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" fill="{fill}" fill-opacity="0.92">نوشتهٔ {esc(text)}</text>'


def pill(cat, y=800, fill='#ffffff'):
    return f'''<g transform="translate(300, {y})">
    <rect x="-85" y="-26" width="170" height="52" rx="26" fill="#ffffff" fill-opacity="0.07" stroke="#ffffff" stroke-opacity="0.55" stroke-width="2"/>
    <text x="0" y="6" text-anchor="middle" font-family="{FONT}" font-size="23" fill="{fill}">{esc(cat)}</text>
  </g>'''


# ---------- 26: تازیانه‌های سبز (فروغ فرخزاد) ----------
b26 = Book.objects.get(id=26)
t26 = 'تازیانه‌های سبز'
l26 = wrap(t26, 52)
fs26 = 52
top26 = int(400 - (len(l26) - 1) * fs26 * 1.2 / 2)
whips = ''.join(
    f'<path d="M{x} 230 C {x-14} 360 {x+14} 470 {x} 610" stroke="{c}" fill="none" stroke-width="{w}" stroke-linecap="round" opacity="0.35"/>'
    for x, c, w in [(140, '#4ade80', 5), (215, '#86efac', 3), (370, '#bbf7d0', 4), (455, '#4ade80', 5), (505, '#bbf7d0', 3)]
)
svg26 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="900" viewBox="0 0 600 900">
  <defs>
    <linearGradient id="bg26" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0" stop-color="#15803d"/>
      <stop offset="0.55" stop-color="#14532d"/>
      <stop offset="1" stop-color="#052e16"/>
    </linearGradient>
  </defs>
  <rect width="600" height="900" fill="url(#bg26)"/>
  <circle cx="505" cy="700" r="210" fill="#ffffff" opacity="0.05"/>
  <circle cx="90" cy="180" r="120" fill="#ffffff" opacity="0.05"/>
  {whips}
  {header()}
  {title_block(l26, fs26, top=top26)}
  {author_line('فروغ فرخزاد')}
  {pill('شعر')}
</svg>'''

# ---------- 27: شمس تبریزی در کنار دیوان شمس (مولانا) ----------
b27 = Book.objects.get(id=27)
t27 = 'شمس تبریزی در کنار دیوان شمس'
l27 = wrap(t27, 42, max_w=500)
fs27 = 42
top27 = int(360 - (len(l27) - 1) * fs27 * 1.2 / 2)
rays = ''.join(
    f'<line x1="300" y1="300" x2="{300 + 130 * __import__("math").cos(a):.0f}" y2="{300 + 130 * __import__("math").sin(a):.0f}" stroke="#fcd34d" stroke-opacity="0.5" stroke-width="4" stroke-linecap="round"/>'
    for a in [i * 3.14159265 / 6 for i in range(12)]
)
svg27 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="900" viewBox="0 0 600 900">
  <defs>
    <linearGradient id="bg27" x1="0" y1="0" x2="0.5" y2="1">
      <stop offset="0" stop-color="#312e81"/>
      <stop offset="1" stop-color="#1e1b4b"/>
    </linearGradient>
    <radialGradient id="sun27" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#fde68a"/>
      <stop offset="1" stop-color="#d97706"/>
    </radialGradient>
  </defs>
  <rect width="600" height="900" fill="url(#bg27)"/>
  <circle cx="300" cy="300" r="240" fill="#ffffff" opacity="0.04"/>
  {rays}
  <circle cx="300" cy="300" r="58" fill="url(#sun27)"/>
  <circle cx="300" cy="300" r="74" fill="none" stroke="#fcd34d" stroke-opacity="0.35" stroke-width="2"/>
  {header()}
  {title_block(l27, fs27, top=top27, fill='#fde68a')}
  {author_line('مولانا جلال‌الدین بلخی', y=648)}
  {pill('شعر', fill='#fde68a')}
</svg>'''

# ---------- 30: اعداد حرف می‌زنند (ناتانیل پاپ) ----------
b30 = Book.objects.get(id=30)
t30 = 'اعداد حرف می‌زنند'
l30 = wrap(t30, 52)
fs30 = 52
top30 = int(400 - (len(l30) - 1) * fs30 * 1.2 / 2)
nums = ''.join(
    f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{s}" font-weight="bold" fill="#ffffff" opacity="0.13">{n}</text>'
    for x, y, s, n in [(95, 240, 44, '3'), (500, 260, 34, '7'), (120, 600, 60, '42'),
                       (500, 560, 30, '0.5'), (470, 470, 40, '؟'), (125, 470, 36, '9'),
                       (530, 380, 44, '∞'), (70, 700, 40, 'π')]
)
svg30 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="900" viewBox="0 0 600 900">
  <defs>
    <linearGradient id="bg30" x1="0" y1="0" x2="0.55" y2="1">
      <stop offset="0" stop-color="#0f766e"/>
      <stop offset="1" stop-color="#042f2e"/>
    </linearGradient>
  </defs>
  <rect width="600" height="900" fill="url(#bg30)"/>
  <circle cx="500" cy="140" r="170" fill="#ffffff" opacity="0.05"/>
  <circle cx="80" cy="780" r="190" fill="#ffffff" opacity="0.05"/>
  {nums}
  {header()}
  {title_block(l30, fs30, top=top30)}
  {author_line('ناتانیل پاپ')}
  {pill('روانشناسی و فلسفه', fill='#ccfbf1')}
</svg>'''


def assign(book, name, svg_text):
    book.cover.save(name, ContentFile(svg_text.encode('utf-8')), save=True)
    print(f'  -> book {book.id} cover set to {name}')


assign(b26, 'taziyane_haye_sabz.svg', svg26)
assign(b27, 'shams_dar_kenar_divan_shams.svg', svg27)
assign(b30, 'adad_harf_mizanand.svg', svg30)

for f in ['media/covers/book26.jpg', 'media/covers/book27.jpg', 'media/covers/book30.jpg']:
    if os.path.exists(f):
        os.remove(f)
        print('removed old wrong jpg:', f)

print('done')