from __future__ import annotations

import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlencode

from agent.http_client import get_json

GDELT_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc?"
QUERIES = {
    "space": '(Rocket Lab OR AST SpaceMobile OR Intuitive Machines OR commercial spaceflight) sourcelang:english',
    "memory": '(Micron OR SK hynix OR Samsung memory OR Kioxia OR NAND OR DRAM) sourcelang:english',
    "chemicals": '(Linde OR DuPont OR Dow chemical OR Shin-Etsu OR LG Chem) sourcelang:english',
    "technology": '(NVIDIA OR AMD OR Broadcom OR Microsoft OR Alphabet OR Amazon OR Meta OR Apple) sourcelang:english',
}
OFFICIAL_DOMAINS = {"sec.gov", "investor.nvidia.com", "news.microsoft.com", "aboutamazon.com", "apple.com", "about.fb.com", "blog.google"}
SYMBOL_TERMS = {
    "SPCX": ("spacex", "space exploration technologies"),
    "RKLB": ("rocket lab",), "ASTS": ("ast spacemobile",), "LUNR": ("intuitive machines",),
    "MU": ("micron",), "000660.KS": ("sk hynix",), "005930.KS": ("samsung",), "285A.T": ("kioxia",),
    "NVDA": ("nvidia",), "AMD": (" amd ",), "AVGO": ("broadcom",), "MSFT": ("microsoft",),
    "GOOGL": ("alphabet", "google"), "AMZN": ("amazon",), "META": ("meta ",), "AAPL": ("apple",),
    "LIN": ("linde",), "DOW": ("dow ",), "DD": ("dupont",), "APD": ("air products",),
}


def _parse_date(value: str) -> str:
    for pattern in ("%Y%m%dT%H%M%SZ", "%Y%m%d%H%M%S"):
        try:
            return datetime.strptime(value, pattern).replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        except ValueError:
            pass
    return datetime.now(timezone.utc).isoformat()


def _fetch(category: str, query: str) -> list[dict[str, Any]]:
    params = {"query": query, "mode": "artlist", "maxrecords": "12", "format": "json", "sort": "hybridrel", "timespan": "2d"}
    payload = get_json(GDELT_ENDPOINT + urlencode(params), timeout=18, retries=1)
    items: list[dict[str, Any]] = []
    for article in payload.get("articles", []):
        title = str(article.get("title", "")).strip()
        url = str(article.get("url", "")).strip()
        domain = str(article.get("domain", "")).lower().removeprefix("www.")
        if not title or not url:
            continue
        searchable = f" {title.lower()} "
        symbols = [symbol for symbol, terms in SYMBOL_TERMS.items() if any(term in searchable for term in terms)]
        items.append({
            "id": hashlib.sha1(url.encode("utf-8"), usedforsecurity=False).hexdigest()[:16], "title": title, "url": url,
            "source": domain or "GDELT", "published_at": _parse_date(str(article.get("seendate", ""))),
            "category": category, "symbols": symbols, "is_official": domain in OFFICIAL_DOMAINS or domain.endswith(".sec.gov"),
        })
    return items


def collect_news() -> tuple[list[dict[str, Any]], list[str]]:
    articles: list[dict[str, Any]] = []
    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(_fetch, category, query): category for category, query in QUERIES.items()}
        for future in as_completed(futures):
            try:
                articles.extend(future.result())
            except RuntimeError as error:
                errors.append(f"{futures[future]}: {error}")
    unique = {item["url"]: item for item in articles}
    official = sorted((item for item in unique.values() if item["is_official"]), key=lambda item: item["published_at"], reverse=True)
    regular = sorted((item for item in unique.values() if not item["is_official"]), key=lambda item: item["published_at"], reverse=True)
    return (official + regular)[:32], errors
