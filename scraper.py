import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_html(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"❌ Gagal fetch {url}: {e}")
        return None

def extract_summary(soup, sumber):
    if not soup:
        return "Tidak ada ringkasan."

    selectors = {
        "Kompas": [
            "div.read__content p",      # struktur utama dengan dua garis bawah
            "div.article__body p"       # fallback jika struktur berubah
        ],
        "Viva": [
            "div.article-list-info.content_center h2",
            "div.article-list-desc p"
        ],
        "Detik": [
            "div.detail__body-text p",    # perbaikan selector dua garis bawah
            "div.container__content-detail p"
        ],
    }

    for sel in selectors.get(sumber, []):
        elems = soup.select(sel)
        if not elems:
            continue
        for p in elems:
            t = p.get_text(strip=True)
            if len(t) > 50:
                return t

    return "Tidak ada ringkasan."

def scrape_generic(search_url, domain_keyword, sumber, max_items=10):
    print(f"\n📡 Scraping {sumber} — target: {max_items} artikel")
    soup = fetch_html(search_url)
    if not soup:
        return []

    seen = set()
    articles = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if domain_keyword not in href:
            continue

        title = a.get_text(strip=True)
        if len(title) < 30:
            continue

        if href in seen:
            continue

        seen.add(href)
        detail = fetch_html(href)
        summary = extract_summary(detail, sumber)

        articles.append({
            "sumber": sumber,
            "judul": title,
            "ringkasan": summary,
            "url": href
        })

        print(f"✅ [{sumber}] {title}")
        time.sleep(0.5)

        if len(articles) >= max_items:
            break

    print(f"→ Ditemukan {len(articles)} artikel dari {sumber}")
    return articles


def get_all_viral_news():
    kompas = scrape_generic(
        "https://search.kompas.com/search?q=viral",
        "kompas.com",
        "Kompas",
        max_items=10
    )

    viva = scrape_generic(
        "https://www.viva.co.id/trending",
        "viva.co.id",
        "Viva",
        max_items=10
    )

    detik = scrape_generic(
        "https://www.detik.com/search/searchall?query=viral",
        "detik.com",
        "Detik",
        max_items=10
    )

    all_articles = kompas + viva + detik

    with open("berita_viral.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    return all_articles

if __name__ == "__main__":
    articles = get_all_viral_news()
    print(f"💾 Disimpan {len(articles)} artikel viral ke 'berita_viral.json'")
