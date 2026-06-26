"""Fetch and parse public Releasebot product feeds (no API key)."""

from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import quote

import aiohttp
from bs4 import BeautifulSoup

RELEASEBOT_BASE = "https://releasebot.io"
USER_AGENT = "docs-mcp/1.0 (+https://github.com/sandraschi/mcp-central-docs; query_releasebot)"
# URL path segment: letters, digits, hyphen (e.g. cursor, openai, zed)
_SLUG_OK = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$", re.I)
# Date line in feed: "Mar 19, 2026"
_DATE_RE = re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}\b")


def normalize_slug(product_slug: str) -> str | None:
    s = (product_slug or "").strip().lower().strip("/")
    if not s or not _SLUG_OK.match(s):
        return None
    return s


def _headlines_from_ld_json(html: str, limit: int) -> list[tuple[str, str]]:
    """Fallback: JSON-LD ItemList with datePublished + slug name (less readable)."""
    out: list[tuple[str, str]] = []
    for m in re.finditer(
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        html,
        re.DOTALL | re.IGNORECASE,
    ):
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        graphs = data.get("@graph") if isinstance(data, dict) else None
        if not isinstance(graphs, list):
            continue
        for node in graphs:
            if not isinstance(node, dict):
                continue
            if node.get("@type") != "ItemList":
                continue
            elements = node.get("itemListElement")
            if not isinstance(elements, list):
                continue
            for el in elements:
                if not isinstance(el, dict):
                    continue
                item = el.get("item")
                if not isinstance(item, dict):
                    continue
                if item.get("@type") != "SoftwareRelease":
                    continue
                dp = item.get("datePublished")
                name = item.get("name")
                if isinstance(dp, str) and isinstance(name, str):
                    # YYYY-MM-DD -> keep as ISO for display
                    try:
                        parts = dp.split("-")
                        if len(parts) == 3:
                            y, mo, d = int(parts[0]), int(parts[1]), int(parts[2])
                            months = (
                                "Jan",
                                "Feb",
                                "Mar",
                                "Apr",
                                "May",
                                "Jun",
                                "Jul",
                                "Aug",
                                "Sep",
                                "Oct",
                                "Nov",
                                "Dec",
                            )
                            label = f"{months[mo - 1]} {d}, {y}"
                        else:
                            label = dp
                    except (ValueError, IndexError):
                        label = dp
                    slug_title = name.replace("-", " ").strip()
                    out.append((label, slug_title))
                if len(out) >= limit:
                    return out
    return out[:limit]


def parse_releasebot_html(html: str, limit: int) -> list[tuple[str, str]]:
    """Extract (display_date, headline) from Releasebot /updates/{slug} HTML."""
    soup = BeautifulSoup(html, "html.parser")
    results: list[tuple[str, str]] = []

    for li in soup.find_all("li"):
        classes = li.get("class") or []
        cls = " ".join(classes)
        if "grid-cols-[96px_1fr]" not in cls and "sm:grid-cols-[96px_1fr]" not in cls:
            continue
        text_blob = li.get_text(" ", strip=True)
        if "All of your release notes in one feed" in text_blob:
            continue

        h2 = li.find("h2")
        if not h2:
            continue
        headline = h2.get_text(strip=True)
        if not headline:
            continue

        date_str = ""
        for span in li.find_all("span", class_=True):
            sc = " ".join(span.get("class") or [])
            if "select-none" not in sc:
                continue
            raw = span.get_text(" ", strip=True)
            dm = _DATE_RE.search(raw)
            if dm:
                date_str = dm.group(0)
                break
        if not date_str:
            dm = _DATE_RE.search(text_blob[:400])
            if dm:
                date_str = dm.group(0)

        results.append((date_str or "?", headline))
        if len(results) >= limit:
            break

    if results:
        return results

    return _headlines_from_ld_json(html, limit)


async def query_releasebot_http(
    product_slug: str,
    *,
    limit: int = 5,
    timeout_s: float = 25.0,
) -> dict[str, Any]:
    slug = normalize_slug(product_slug)
    if slug is None:
        return {
            "success": False,
            "message": "Invalid product_slug. Use a short slug like cursor, zed, notion (see releasebot.io/updates/alphabetical).",
            "url": f"{RELEASEBOT_BASE}/updates/alphabetical",
            "releases": [],
        }

    url = f"{RELEASEBOT_BASE}/updates/{quote(slug, safe='')}"
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"}

    try:
        timeout = aiohttp.ClientTimeout(total=timeout_s)
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=timeout, allow_redirects=True) as resp:
                if resp.status == 404:
                    return {
                        "success": False,
                        "message": (
                            f"No feed found for slug '{slug}' or no recent releases. "
                            f"Check https://releasebot.io/updates/alphabetical for valid slugs."
                        ),
                        "url": url,
                        "releases": [],
                    }
                resp.raise_for_status()
                html = await resp.text()
    except aiohttp.ClientError as e:
        return {
            "success": False,
            "message": f"Releasebot request failed: {e!s}",
            "url": url,
            "releases": [],
        }
    except TimeoutError:
        return {
            "success": False,
            "message": "Releasebot request timed out.",
            "url": url,
            "releases": [],
        }

    rows = parse_releasebot_html(html, max(1, min(limit, 20)))
    if not rows:
        return {
            "success": False,
            "message": (
                f"No feed found for slug '{slug}' or no recent releases. "
                f"Check https://releasebot.io/updates/alphabetical for valid slugs."
            ),
            "url": url,
            "releases": [],
        }

    lines = [f"{d} — {h}" for d, h in rows]
    summary = "Recent releases: " + "; ".join(lines)
    return {
        "success": True,
        "message": summary,
        "url": url,
        "releases": [{"date": d, "headline": h} for d, h in rows],
    }
