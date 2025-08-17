from __future__ import annotations

import re
import requests  # type: ignore[import-untyped]
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ProductMedia:
    images: List[str] = field(default_factory=list)


@dataclass
class ProductData:
    url: str
    title: str
    price: Optional[str]
    description: str
    specs: Dict[str, str]
    media: ProductMedia


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}


def fetch_html(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_images(soup: BeautifulSoup, base_url: str) -> List[str]:
    imgs: List[str] = []
    for img in soup.select("img"):
        src_attr = img.get("data-src") or img.get("src")
        if not isinstance(src_attr, str):
            continue
        src = src_attr
        if src.startswith("//"):
            src = "https:" + src
        if src.startswith("/") and base_url:
            # naive join
            src = base_url.rstrip("/") + src
        if any(ext for ext in [".jpg", ".jpeg", ".png", ".webp"] if ext in src.lower()):
            if src not in imgs:
                imgs.append(src)
    return imgs[:12]  # limit for MVP


def extract_price(soup: BeautifulSoup) -> Optional[str]:
    price_candidates = soup.find_all(string=re.compile(r"\$\s?\d"))
    if price_candidates:
        return clean_text(str(price_candidates[0]))
    # meta tags
    meta_price = soup.find("meta", property="product:price:amount") or soup.find(
        "meta", itemprop="price"
    )
    if isinstance(meta_price, Tag):
        content = meta_price.get("content")
        if isinstance(content, str):
            return content
    return None


def extract_specs(soup: BeautifulSoup) -> Dict[str, str]:
    specs: Dict[str, str] = {}
    # try definition lists
    for dl in soup.select('dl'):
        dt_tags = dl.find_all('dt')
        dd_tags = dl.find_all('dd')
        if len(dt_tags) and len(dt_tags) == len(dd_tags):
            for dt, dd in zip(dt_tags, dd_tags):
                k = clean_text(dt.get_text(':'))
                v = clean_text(dd.get_text(' '))
                if k and v and k not in specs:
                    specs[k] = v
    # tables
    for row in soup.select('table tr'):
        cells = row.find_all(['th','td'])
        if len(cells) == 2:
            k = clean_text(cells[0].get_text(':'))
            v = clean_text(cells[1].get_text(' '))
            if k and v and k not in specs:
                specs[k] = v
    return specs


def extract_description(soup: BeautifulSoup) -> str:
    # heuristic: longest paragraph block
    paragraphs = [clean_text(p.get_text(' ')) for p in soup.find_all('p')]
    paragraphs = [p for p in paragraphs if len(p.split()) > 4]
    paragraphs.sort(key=len, reverse=True)
    if paragraphs:
        return paragraphs[0][:1200]
    return ""  # fallback


def extract_title(soup: BeautifulSoup) -> str:
    if soup.title and soup.title.string:
        return clean_text(soup.title.string.split('|')[0])
    h1 = soup.find('h1')
    if h1:
        return clean_text(h1.get_text(' '))
    return "Product"


def scrape_product(url: str) -> ProductData:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")
    match = re.match(r"https?://[^/]+", url)
    base_url = match.group(0) if match else ""

    title = extract_title(soup)
    price = extract_price(soup)
    specs = extract_specs(soup)
    description = extract_description(soup)
    images = extract_images(soup, base_url)

    return ProductData(
        url=url,
        title=title,
        price=price,
        description=description,
        specs=specs,
        media=ProductMedia(images=images)
    )


if __name__ == "__main__":
    test_url = "https://majorworld.com/inventory/2015-ram-1500-express-rwd/"
    data = scrape_product(test_url)
    print(data)
