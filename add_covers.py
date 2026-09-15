import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files.base import ContentFile

from books.models import Book

CATEGORY_STYLE = {
    'sher': {
        'c1': '#7c3aed', 'c2': '#2e1065',
        'accent': '#c4b5fd', 'pill_text': '#ede9fe',
    },
    'ravanshenasi': {
        'c1': '#0d9488', 'c2': '#083338',
        'accent': '#99f6e4', 'pill_text': '#ccfbf1',
    },
    'ketabe-koodak': {
        'c1': '#fb923c', 'c2': '#881337',
        'accent': '#fed7aa', 'pill_text': '#ffedd5',
    },
    'roman': {
        'c1': '#2563eb', 'c2': '#1e1b4b',
        'accent': '#bfdbfe', 'pill_text': '#dbeafe',
    },
}
FALLBACK_STYLE = CATEGORY_STYLE['roman']

SLUGS = {
    24: 'divan_hafez',
    25: 'shehre_sohrab_sepahri',
    26: 'taziyane_haye_sabz',
    27: 'shams_tabrizi_dar_kenar_divan_shams',
    28: 'ensan_dar_jostojooye_mana',
    29: 'honar_e_zoog_zistani',
    30: 'adad_harf_mizanand',
    31: 'adat_atomi',
    32: 'khale_suske',
    33: 'kalile_va_demne',
    34: 'mary_popins',
}

FONT_FAMILY = "'BYekan+','Vazirmatn','IRANSansX',Tahoma,'Segoe UI',sans-serif"


def esc(text):
    return (
        text.replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
    )


def wrap_lines(text, font_size, max_width=470):
    chars_per_line = max(4, int(max_width / (font_size * 0.62)))
    words = text.split(' ')
    lines, cur = [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if len(trial) <= chars_per_line:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def estimate_font_size(text_length):
    if text_length <= 12:
        return 56
    if text_length <= 20:
        return 48
    if text_length <= 30:
        return 42
    return 38


def title_block(lines, font_size, top, cx=300, line_gap=1.16):
    n = len(lines)
    tspans = []
    for i, line in enumerate(lines):
        y = top + i * font_size * line_gap
        tspans.append(
            f'<tspan x="{cx}" y="{y:.0f}">{esc(line)}</tspan>'
        )
    fs = font_size
    tspans_text = '\n      '.join(tspans)
    return (
        f'<g text-anchor="middle" font-family="{FONT_FAMILY}" font-weight="bold">'
        f'<text font-size="{fs}" fill="#ffffff" fill-opacity="0.18">'
        f'<tspan x="{cx+2}" y="{top+2}">{esc(" ".join(lines))}</tspan>'
        f'</text>'
        f'<text font-size="{fs}" fill="#ffffff">'
        f'      {tspans_text}\n'
        f'    </text>'
        f'</g>'
    )


def build_cover(book, style):
    c1, c2 = style['c1'], style['c2']
    accent = style['accent']
    pill_text = style['pill_text']
    cat_name = esc(book.category.name if book.category else '')

    title_text = book.title.strip()
    author_text = esc(book.author.strip())

    fs = estimate_font_size(len(title_text))
    lines = wrap_lines(title_text, fs)
    n = len(lines)
    total_h = (n - 1) * fs * 1.16 + fs
    title_top = 430 - total_h / 2 + fs * 0.5

    author_y = 640 if fs > 40 else 630
    pill_y = 800

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="900" viewBox="0 0 600 900">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.55" y2="1">
      <stop offset="0" stop-color="{c1}"/>
      <stop offset="1" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect width="600" height="900" fill="url(#bg)"/>

  <circle cx="505" cy="120" r="185" fill="#ffffff" opacity="0.07"/>
  <circle cx="70" cy="770" r="225" fill="#ffffff" opacity="0.06"/>
  <circle cx="525" cy="640" r="80" fill="#ffffff" opacity="0.10"/>
  <circle cx="120" cy="200" r="26" fill="#ffffff" opacity="0.10"/>
  <circle cx="525" cy="350" r="14" fill="#ffffff" opacity="0.14"/>

  <rect x="0" y="110" width="14" height="520" fill="#ffffff" opacity="0.85"/>

  <text x="300" y="205" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="30"
        fill="#ffffff" fill-opacity="0.95" font-weight="bold">کتابفروشی آنلاین</text>

  <text x="300" y="245" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="20"
        fill="{accent}" fill-opacity="0.85">پرفروش‌ترین‌ها</text>

  <rect x="255" y="275" width="90" height="5" rx="2.5" fill="#ffffff" opacity="0.7"/>

  {title_block(lines, fs, title_top)}

  <text x="300" y="{author_y}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="30"
        fill="#ffffff" fill-opacity="0.9">نوشتهٔ {author_text}</text>

  <g transform="translate(300, {pill_y})">
    <rect x="-85" y="-26" width="170" height="52" rx="26"
          fill="#ffffff" fill-opacity="0.06" stroke="#ffffff" stroke-opacity="0.55" stroke-width="2"/>
    <text x="0" y="5" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="24"
          fill="{pill_text}">{cat_name}</text>
  </g>
</svg>
'''
    return svg


def main():
    created = 0
    books = Book.objects.filter(cover__isnull=False) | Book.objects.filter(cover__exact='')
    books = [b for b in Book.objects.all() if not b.cover]
    for book in books:
        style = CATEGORY_STYLE.get(book.category.slug, FALLBACK_STYLE) if book.category else FALLBACK_STYLE
        slug = SLUGS.get(book.id, f'book{book.id}')
        filename = f'{slug}.svg'
        svg = build_cover(book, style).encode('utf-8')
        book.cover.save(filename, ContentFile(svg), save=True)
        print(f'  + {book.id} | {filename} | {book.title}')
        created += 1
    print(f'Done: {created} covers created.')


if __name__ == '__main__':
    main()