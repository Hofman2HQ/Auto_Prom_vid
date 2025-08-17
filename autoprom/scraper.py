"""Web scraping utilities for product pages."""
from __future__ import annotations

import requests
from bs4 import BeautifulSoup
from typing import Dict, List


def scrape_product(url: str) -> Dict[str, any]:
    """Scrape basic product info from an e-commerce page.

    This function is intentionally simple. It retrieves the page and attempts
    to extract the title, description and image URLs.  Different shops will
    require custom scraping logic – this serves as a starting point.
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.text.strip() if soup.title else "Product"

    # Try to find meta description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""

    images: List[str] = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and src.startswith("http"):
            images.append(src)

    return {
        "url": url,
        "title": title,
        "description": description,
        "images": images,
    }
