from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import html

# Hány autó / modell
MAX_PER_MODEL = 3

# Márkák, modellek, szűrt keresési URL-ek (DE, 2023+, 50k+, VATded)
MODELS = [
    # ==== AUDI ====
    {"brand": "Audi", "model": "A5", "search_url": "https://www.autoscout24.hu/lst/audi/a5?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=21e342j244y&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Audi", "model": "A6", "search_url": "https://www.autoscout24.hu/lst/audi/a6?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=2bjv0uuaytd&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Audi", "model": "A7", "search_url": "https://www.autoscout24.hu/lst/audi/a7?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=lm0q9zh3vr&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Audi", "model": "A8", "search_url": "https://www.autoscout24.hu/lst/audi/a8?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=3rltuecshf&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Audi", "model": "Q5", "search_url": "https://www.autoscout24.hu/lst/audi/q5?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=3udv6m959a&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Audi", "model": "Q7", "search_url": "https://www.autoscout24.hu/lst/audi/q7?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=voatce075y&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Audi", "model": "Q8", "search_url": "https://www.autoscout24.hu/lst/audi/q8?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=zvlkw590fj&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},

    # ==== BMW ====
    {"brand": "BMW", "model": "3", "search_url": "https://www.autoscout24.hu/lst/bmw/3-as-(mind)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=16gphmkzg2h&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "BMW", "model": "4", "search_url": "https://www.autoscout24.hu/lst/bmw/4-es-(mind)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=r21syclft7&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "BMW", "model": "5", "search_url": "https://www.autoscout24.hu/lst/bmw/5-%C3%B6s-(mind)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=fft3rthp9x&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "BMW", "model": "7", "search_url": "https://www.autoscout24.hu/lst/bmw/7-es-(mind)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=2cfd4nojz6o&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "BMW", "model": "8", "search_url": "https://www.autoscout24.hu/lst/bmw/8-as-(mind)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=qgs3dnp0yw&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "BMW", "model": "X3", "search_url": "https://www.autoscout24.hu/lst/bmw/x3?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=18rpn7rmorx&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "BMW", "model": "X5", "search_url": "https://www.autoscout24.hu/lst/bmw/x5?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=3hua7u4o67&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "BMW", "model": "X6", "search_url": "https://www.autoscout24.hu/lst/bmw/x6?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=1imlu1ydjew&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "BMW", "model": "X7", "search_url": "https://www.autoscout24.hu/lst/bmw/x7?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=22jv3leq3u3&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},

    # ==== MERCEDES ====
    {"brand": "Mercedes", "model": "C osztály", "search_url": "https://www.autoscout24.hu/lst/mercedes-benz/c-oszt%C3%A1ly-(mind)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=17m3yfbgkha&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Mercedes", "model": "E osztály", "search_url": "https://www.autoscout24.hu/lst/mercedes-benz/e-oszt%C3%A1ly-(mind)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=n996fom8m8&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Mercedes", "model": "S osztály", "search_url": "https://www.autoscout24.hu/lst/mercedes-benz/s-oszt%C3%A1ly-(mind)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=1gi0qo37k0l&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Mercedes", "model": "GLC", "search_url": "https://www.autoscout24.hu/lst/mercedes-benz/glc-(%C3%B6sszes)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=11oqipzlw7a&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Mercedes", "model": "GLE", "search_url": "https://www.autoscout24.hu/lst/mercedes-benz/gle-(%C3%B6sszes)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=9sgife0utc&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Mercedes", "model": "GLS", "search_url": "https://www.autoscout24.hu/lst/mercedes-benz/gls-(%C3%B6sszes)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=12r3a65s2qh&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},

    # ==== VOLVO ====
    {"brand": "Volvo", "model": "XC60", "search_url": "https://www.autoscout24.hu/lst/volvo/xc60?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=41lhecsm1p&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Volvo", "model": "XC90", "search_url": "https://www.autoscout24.hu/lst/volvo/xc90?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=q3r3nrhhe6&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Volvo", "model": "S90", "search_url": "https://www.autoscout24.hu/lst/volvo/s90?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=1vej94e8pwq&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},

    # ==== LEXUS ====
    {"brand": "Lexus", "model": "NX", "search_url": "https://www.autoscout24.hu/lst/lexus/nx-series-(%C3%B6sszes)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=2ebitzryd9g&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Lexus", "model": "RX", "search_url": "https://www.autoscout24.hu/lst/lexus/rx-sorozat-(mind)?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=5r9k1u2dtg&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},

    # ==== PORSCHE ====
    {"brand": "Porsche", "model": "Panamera", "search_url": "https://www.autoscout24.hu/lst/porsche/panamera?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=w6gawxdhjy&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Porsche", "model": "Macan", "search_url": "https://www.autoscout24.hu/lst/porsche/macan?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=vqhq0meet3&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Porsche", "model": "Taycan", "search_url": "https://www.autoscout24.hu/lst/porsche/taycan?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=t1p9c0y4ac&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
    {"brand": "Porsche", "model": "Cayenne", "search_url": "https://www.autoscout24.hu/lst/porsche/cayenne?atype=C&cy=D&desc=0&fregfrom=2023&kmto=100000&powertype=kw&pricefrom=50000&search_id=g72znyugfv&sort=standard&source=detailsearch&ustate=N%2CU&vatded=true"},
]


def generate_html(cars):
    """Egyszerű, Elementor-kompatibilis grid inline stílusokkal."""
    parts = []
    parts.append(
        '<link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@400;600;700&display=swap" rel="stylesheet">\n'
    )
    parts.append(
        '<div style="background:#000;padding:40px 20px;"><div style="max-width:1400px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.5rem;">\n'
    )

    for car in cars:
        title = html.escape(car["title"])
        price = html.escape(car["price"])
        img_url = html.escape(car["image_url"])
        detail_url = html.escape(car["detail_url"])

        card_html = f'''
<div style="background:#111;color:#fff;padding:1rem;border-radius:12px;text-align:center;">
  <img src="{img_url}" alt="{title}" style="width:100%;height:200px;object-fit:cover;border-radius:8px;">
  <h3 style="font-family:'Red Hat Display';font-weight:700;margin:0.5rem 0;">{title}</h3>
  <p style="font-size:1.1rem;font-weight:600;margin:0;">{price}</p>
  <a href="{detail_url}" target="_blank" style="display:inline-block;margin-top:12px;padding:10px 20px;background:#fff;color:#000;font-weight:bold;border-radius:6px;text-decoration:none;">Megnézem</a>
</div>
'''
        parts.append(card_html)

    parts.append("</div></div>\n")
    return "".join(parts)


def scrape():
    cars = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/129.0 Safari/537.36"
            )
        )
        page = context.new_page()

        for cfg in MODELS:
            brand = cfg["brand"]
            model = cfg["model"]
            url = cfg["search_url"]

            print(f"[INFO] Modell indul: {brand} {model}")

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
            except PlaywrightTimeoutError:
                print(f"[WARN] Timeout: {brand} {model} URL kihagyva")
                continue

            # Kis várakozás JS-re
            page.wait_for_timeout(3000)

            # Cookie banner, ha van
            for text in ["Összes elfogadása", "Minden cookie engedélyezése", "Accept all", "I agree"]:
                try:
                    page.locator(f"button:has-text('{text}')").click(timeout=2000)
                    print("[DEBUG] Cookie banner elfogadva.")
                    page.wait_for_timeout(1000)
                    break
                except Exception:
                    pass

            # Csak az első oldal, mert MAX_PER_MODEL miatt úgyis elég
            cards = page.locator("article")
            count = cards.count()
            print(f"[DEBUG] {brand} {model}: {count} találat ezen az oldalon")

            taken = 0

            for i in range(count):
                if taken >= MAX_PER_MODEL:
                    break

                card = cards.nth(i)

                # Link
                try:
                    link_el = card.locator("a[href]").first
                    href = link_el.get_attribute("href") or ""
                except Exception:
                    href = ""

                if not href:
                    continue

                if href.startswith("http"):
                    detail_url = href
                else:
                    detail_url = "https://www.autoscout24.hu" + href

                # Kép – csak valódi listing image-et engedünk át
                try:
                    img_el = card.locator("img").first
                    img_url = img_el.get_attribute("src") or ""
                except Exception:
                    img_url = ""

                if not img_url or "listing-images" not in img_url:
                    # ha nincs normális kép, átugorjuk
                    continue

                # Cím
                try:
                    title = card.locator("h2, h3").first.inner_text().strip()
                except Exception:
                    title = f"{brand} {model}"

                # Ár
                try:
                    price_el = card.locator("text=€").first
                    price = price_el.inner_text().strip()
                except Exception:
                    price = ""

                cars.append(
                    {
                        "brand": brand,
                        "model": model,
                        "title": title,
                        "price": price,
                        "image_url": img_url,
                        "detail_url": detail_url,
                    }
                )
                taken += 1
                print(f"  -> hozzáadva: {title}")

        browser.close()

    return cars


def main():
    cars = scrape()
    print(f"[INFO] Összes autó: {len(cars)}")
    html_output = generate_html(cars)
    with open("autoscout_widget.html", "w", encoding="utf-8") as f:
        f.write(html_output)
    print("[OK] Elkészült: autoscout_widget.html")


if __name__ == "__main__":
    main()