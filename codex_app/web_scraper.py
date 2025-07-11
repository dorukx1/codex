import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from typing import List


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def scrape_url(url: str, output_dir: str = "scraped") -> None:
    """Download text and images from a webpage."""
    if not is_valid_url(url):
        raise ValueError("Invalid URL provided")

    resp = requests.get(url)
    resp.raise_for_status()

    os.makedirs(output_dir, exist_ok=True)
    soup = BeautifulSoup(resp.text, "html.parser")

    text_path = os.path.join(output_dir, "content.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(soup.get_text())

    img_tags = soup.find_all("img")
    img_dir = os.path.join(output_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    for idx, img in enumerate(img_tags):
        src = img.get("src")
        if not src:
            continue
        try:
            img_resp = requests.get(src)
            img_resp.raise_for_status()
        except Exception:
            continue
        ext = os.path.splitext(src)[1] or ".jpg"
        img_path = os.path.join(img_dir, f"image_{idx}{ext}")
        with open(img_path, "wb") as f:
            f.write(img_resp.content)
