import sqlite3
import os
import urllib.request
import ssl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
COVERS_DIR = os.path.join(BASE_DIR, 'media', 'covers')

os.makedirs(COVERS_DIR, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BOOKS = [
    {
        "title": "1984",
        "author": "جورج اورول",
        "price": 114600,
        "description": "در جهانی که آزادی، حقیقت و عشق تحت نظارت شدید قرار دارند، چه امیدی باقی می‌ماند؟ کتاب 1984 نوشته جورج اورول، یکی از مهم‌ترین و تأثیرگذارترین رمان‌های قرن بیستم است. وینستون اسمیت، کارمند جزء وزارت حقیقت، در دنیایی زندگی می‌کند که «برادر بزرگ» همه چیز را کنترل می‌کند: افکار، احساسات و حتی گذشته. وینستون که در دل خود آرزوی آزادی و حقیقت را حفظ کرده، تصمیم می‌گیرد علیه این سیستم سرکوبگر قیام کند. اورول با نگاهی ژرف و پیش‌بینانه، خطرات حکومت‌های تمامیت‌خواه را به شکلی ماندگار به تصویر می‌کشد.",
        "cover_url": "https://cdn.fidibo.com/phoenixpub/content/f7ceb30b-110e-4808-8cc9-6225fa7bbfe5/0c6e882a-2396-45de-95bc-fcbfb01b8f46.jpg",
        "filename": "1984.jpg"
    },
    {
        "title": "برادران کارامازوف",
        "author": "فئودور داستایفسکی",
        "price": 510000,
        "description": "کتاب برادران کارامازوف یکی از بزرگ‌ترین شاهکارهای ادبیات جهان و آخرین رمان داستایفسکی است. داستایفسکی در این رمان، داستان خانواده کارامازوف و کشمکش‌های پیچیده میان پدری فاسد و سه پسرش را روایت می‌کند. دیمیتری، پسر بزرگ خانواده، به اتهام قتل پدر بازداشت می‌شود. ایوان، برادر روشنفکر و شکاک او، با پرسش‌های عمیق درباره ایمان و اخلاق دست و پنجه نرم می‌کند و آلیوشا، برادر کوچک‌تر و راهبی مهربان، تلاش می‌کند میان اعضای خانواده صلح برقرار کند.",
        "cover_url": "https://cdn.fidibo.com/phoenixpub/content/65b22c64-5917-4cfd-a2cb-ad5a564f141b/1c61e52d-ea91-4c23-b178-109e32431495.jpg",
        "filename": "bararan_karamazov.jpg"
    },
    {
        "title": "صد سال تنهایی",
        "author": "گابریل گارسیا مارکز",
        "price": 65000,
        "description": "کتاب صد سال تنهایی یکی از مشهورترین و تأثیرگذارترین رمان‌های قرن بیستم است که با تلفیق واقعیت و عناصر جادویی، داستان چند نسل از خانواده بوئندیا را در دهکده خیالی ماکوندو روایت می‌کند. مارکز در این اثر، مفاهیمی مانند تنهایی، عشق، سرنوشت و تکرار تاریخ را در قالب روایتی عمیق و ماندگار به تصویر می‌کشد. این رمان برنده جایزه نوبل ادبیات و یکی از برجسته‌ترین آثار رئالیسم جادویی است.",
        "cover_url": "https://cdn.fidibo.com/phoenixpub/content/43c99879-8f92-4254-afe9-251a3e259632/76c05bce-47f1-467b-ad90-a8d0a4662004.jpg",
        "filename": "sad_sal_tanhaei.jpg"
    },
    {
        "title": "شازده کوچولو",
        "author": "آنتوان دوسنت اگزوپری",
        "price": 44100,
        "description": "شازده کوچولو اثر آنتوان دوسنت اگزوپری، اثری ماندگار در ادبیات جهان است که مرزهای سنی را درنوردیده و به اثری برای کودکان و بزرگسالان تبدیل شده است. داستان از زبان یک خلبان روایت می‌شود که هواپیمایش در صحرای آفریقا سقوط کرده و در آنجا با پسربچه‌ای کوچک به نام شازده کوچولو ملاقات می‌کند. این کتاب با زبانی شاعرانه به مسائلی چون عشق، دوستی، تنهایی و معنای زندگی می‌پردازد و ترجمه به بیش از ۲۵۰ زبان دنیا رسیده است.",
        "cover_url": "https://cdn.fidibo.com/phoenixpub/content/0778c069-de7f-4fe1-85ee-8230a2d27190/bc62ce99-b996-4c0f-88d7-fd9ee9e42230.jpg",
        "filename": "shazde_koochooloo.jpg"
    },
    {
        "title": "مغازه خودکشی",
        "author": "ژان تولی",
        "price": 52200,
        "description": "کتاب مغازه خودکشی یکی از متفاوت‌ترین رمان‌های کوتاه معاصر فرانسوی است. ژان تولی در این اثر، جهانی را ساخته که در آن غم و ناامیدی به یک تجارت تبدیل شده است. خانواده‌ای مغازه‌ای عجیب دارند؛ مغازه‌ای که به جای فروش کالاهای معمولی، وسایلی برای کسانی عرضه می‌کند که تصمیم گرفته‌اند به زندگی خود پایان دهند. اما آیا واقعاً می‌توان امید را برای همیشه از بین برد؟ این رمان با ترکیب طنز سیاه و فانتزی فلسفی، پرسش‌هایی عمیق درباره ارزش زندگی و قدرت امید مطرح می‌کند.",
        "cover_url": "https://cdn.fidibo.com/phoenixpub/content/1a680bec-114f-4687-b602-1e359cf5d21e/2f0853cc-69d3-4510-a6e0-84b4d4bedf98.jpg",
        "filename": "maghaze_khodkoshi.jpg"
    },
    {
        "title": "کیمیاگر",
        "author": "پائولو کوئیلو",
        "price": 55000,
        "description": "کیمیاگر نوشته پائولو کوئیلو داستان چوپان جوانی به نام سانتیاگو است که رؤیای یافتن گنجینه‌ای در نزدیکی اهرام مصر را در سر می‌پروراند. او سفری طولانی را از اسپانیا تا مصر آغاز می‌کند و در طول این مسیر با انسان‌های مختلفی آشنا می‌شود که هر کدام درسی درباره زندگی، عشق و سرنوشت به او می‌دهند. این رمان الهام‌بخش میلیون‌ها نفر در سراسر جهان بوده و پیام آن این است که باید به دنبال رؤیاهای خود رفت.",
        "cover_url": "https://cdn.fidibo.com/phoenixpub/content/a62e6ae2-c01c-48dd-b8ab-dfac46221c97/81874bfc-553f-4db1-bb1e-68c0729078f1.jpg",
        "filename": "kimiyagar.jpg"
    },
    {
        "title": "وقتی نیچه گریست",
        "author": "اروین یالوم",
        "price": 88000,
        "description": "وقتی نیچه گریست اثر اروین یالوم، رمانی فلسفی و روان‌شناختی است که در وین قرن نوزدهم اتفاق می‌افتد. داستان درباره پزشک جوانی به نام یوزف بروئر است که با فریدریش نیچه، فیلسوف بزرگ آلمانی، آشنا می‌شود. بروئر تلاش می‌کند با استفاده از روش‌های درمانی خود، نیچه را از بحران روحی و افسردگی عمیق نجات دهد. اما به زودی متوجه می‌شود که نه تنها نیچه، بلکه خود او نیز به درمان نیاز دارد. یالوم با ترکیب فلسفه، روان‌شناسی و داستان‌سرایی، اثری خلق کرده که هم آموزنده و هم سرگرم‌کننده است.",
        "cover_url": "https://cdn.fidibo.com/phoenixpub/content/8138a9d3-d9a8-48c7-8efa-9296ecc959d1/ae05eb42-7860-4e9d-8d30-1a6ebc35b290.jpg",
        "filename": "vaghti_nietzsche.jpg"
    },
    {
        "title": "ملت عشق",
        "author": "الیف شافاک",
        "price": 120000,
        "description": "ملت عشق نوشته الیف شافاک یکی از پرفروش‌ترین رمان‌های معاصر ترکیه و جهان است. این رمان داستان دو خط زمانی را روایت می‌کند: یکی در قرن هفدهم مربوط به شمس تبریزی و مولانا، و دیگری در دوران معاصر مربوط به زنی به نام لیلا که زندگی‌اش دستخوش تغییرات بزرگی می‌شود. شافاک با تلفیق عرفان و زندگی مدرن، داستانی عاشقانه و تأمل‌برانگیز خلق کرده که به بیش از ۵۰ زبان ترجمه شده و میلیون‌ها نسخه فروش داشته است.",
        "cover_url": "https://cdn.fidibo.com/phoenixpub/content/652b9afe-3df8-425c-ac74-112be1749c88/2453d709-1889-4bf7-a391-fc48054fb432.jpg",
        "filename": "melat_eshgh.jpg"
    },
    {
        "title": "کتابخانه نیمه شب",
        "author": "متیو جی. کریک",
        "price": 78000,
        "description": "کتابخانه نیمه شب اثر متیو جی. کریک، رمانی جذاب و الهام‌بخش درباره زندگی، انتخاب‌ها و پشیمانی است. نora سید، زنی جوان که از زندگی خود ناامید شده، پس از یک اتفاق ناگهانی خود را در کتابخانه‌ای عجیب می‌یابد؛ کتابخانه‌ای که در آن هر کتاب نشان‌دهنده زندگی‌ای است که می‌توانست داشته باشد. نora در هر کتاب زندگی متفاوتی را تجربه می‌کند و به تدریج درمی‌یابد که معنای واقعی زندگی در چیز دیگری نهفته است. این رمان پرفروش، خوانندگان را به تأمل در انتخاب‌های زندگی خود دعوت می‌کند.",
        "cover_url": "https://cdn.fidibo.com/phoenixpub/content/100cb4e8-0825-42c7-a946-fde86e825d15/df85312f-b44a-4f29-b98c-7a818f7dce2f.jpg",
        "filename": "ketabkhane_nimeh_shab.jpg"
    },
    {
        "title": "جزء از کل",
        "author": "استیو تولتز",
        "price": 203400,
        "description": "جزء از کل اثر استیو تولتز، رمانی طولانی و پیچیده است که داستان رابطه پدر و پسری را روایت می‌کند که از نظر فکری و عقیدتی در دو قطب مخالف قرار دارند. مارتین، پدر، فردی بدبین و منتقد جامعه است و فرزندش تلاش می‌کند عکس پدرش باشد. این رمان با زبانی طنزآمیز و گاهی تلخ، به موضوعاتی مانند هنر، تروریسم، پدر و پسری، و پیچیدگی‌های زندگی مدرن می‌پردازد. تولتز با روایتی غیرخطی و سرشار از جزئیات، اثری خلق کرده که خواننده را تا آخرین صفحه درگیر نگه می‌دارد.",
        "cover_url": "https://cdn.fidibo.com/phoenixpub/content/93ea555b-c4b4-4f4f-add5-d2269c257f2f/af293fdc-675b-4912-b6ac-5717c9d8b244.jpg",
        "filename": "joz_e_az_kol.jpg"
    },
]

def download_cover(book):
    """Download a book cover image from Fidibo CDN."""
    filepath = os.path.join(COVERS_DIR, book['filename'])
    
    if os.path.exists(filepath) and os.path.getsize(filepath) > 100:
        print(f"  Cover already exists: {book['filename']}")
        return f"covers/{book['filename']}"
    
    try:
        print(f"  Downloading cover...")
        req = urllib.request.Request(book['cover_url'], headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response = urllib.request.urlopen(req, context=ctx, timeout=15)
        data = response.read()
        if len(data) > 100:
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"  Downloaded: {book['filename']} ({len(data)} bytes)")
            return f"covers/{book['filename']}"
    except Exception as e:
        print(f"  Failed: {e}")
    
    print(f"  WARNING: Could not download cover for {book['title']}")
    return ""


def populate_database():
    """Add books to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Clear existing books
    c.execute("DELETE FROM books_book")
    conn.commit()
    print("Cleared existing books.\n")
    
    for i, book in enumerate(BOOKS, 1):
        print(f"[{i}/{len(BOOKS)}] {book['title']} - {book['author']}")
        
        cover_path = download_cover(book)
        
        c.execute("""
            INSERT INTO books_book (title, author, description, price, cover)
            VALUES (?, ?, ?, ?, ?)
        """, (book['title'], book['author'], book['description'], book['price'], cover_path))
        
        conn.commit()
        print(f"  Added to database (ID: {c.lastrowid})\n")
    
    conn.close()
    print(f"\nDone! {len(BOOKS)} books added to database.")


if __name__ == '__main__':
    import io, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    populate_database()
