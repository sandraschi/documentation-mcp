#!/usr/bin/env python3
r"""Capture ToolBench reference pages for proactive hardening notes.

This is intentionally small-scope and polite:
- grabs a fixed set of "rules/pattern" pages (no broad crawl)
- writes timestamped text snapshots under ./reference_out
- helps detect wording changes over time

Usage:
  python .\scrape_toolbench_reference_pages.py
  python .\scrape_toolbench_reference_pages.py --headed --delay-seconds 4 --jitter-seconds 2
"""

from __future__ import annotations

import argparse
import json
import random
import time
from datetime import UTC, datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "Install Playwright first: pip install -r requirements.txt ; python -m playwright install chromium"
    ) from e

TARGETS: list[tuple[str, str]] = [
    ("methodology", "https://toolbench.arcade.dev/methodology"),
    ("improve", "https://toolbench.arcade.dev/improve"),
    ("submit", "https://toolbench.arcade.dev/submit"),
    ("api_access", "https://toolbench.arcade.dev/api-access"),
    ("agentic_patterns", "https://arcade.dev/patterns"),
]


def _sleep_polite(base: float, jitter: float) -> None:
    extra = random.uniform(0.0, jitter) if jitter > 0 else 0.0
    time.sleep(base + extra)


def _safe_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Capture ToolBench reference pages (fixed set, no broad crawl)."
    )
    ap.add_argument("--out-dir", type=Path, default=Path("./reference_out"))
    ap.add_argument("--delay-seconds", type=float, default=2.0)
    ap.add_argument("--jitter-seconds", type=float, default=1.0)
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = out_dir / stamp
    run_dir.mkdir(parents=True, exist_ok=True)

    summary: list[dict] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()

        for i, (label, url) in enumerate(TARGETS):
            if i > 0:
                _sleep_polite(args.delay_seconds, args.jitter_seconds)

            record: dict = {"label": label, "url": url, "ok": False}
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=120_000)
                try:
                    page.wait_for_load_state("networkidle", timeout=30_000)
                except Exception:
                    pass
                page.wait_for_timeout(1200)

                title = page.title()
                text = page.inner_text("body")
                html = page.content()

                safe = _safe_name(label)
                (run_dir / f"{safe}.txt").write_text(text, encoding="utf-8")
                (run_dir / f"{safe}.html").write_text(html, encoding="utf-8")
                (run_dir / f"{safe}.meta.json").write_text(
                    json.dumps(
                        {
                            "label": label,
                            "url": url,
                            "title": title,
                            "captured_at": datetime.now(UTC).isoformat(),
                            "chars_txt": len(text),
                            "chars_html": len(html),
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                record.update(
                    {"ok": True, "title": title, "chars_txt": len(text), "chars_html": len(html)}
                )
            except Exception as e:
                record["error"] = str(e)

            summary.append(record)

        browser.close()

    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    ok_count = sum(1 for r in summary if r.get("ok"))
    print(f"Captured {ok_count}/{len(summary)} pages -> {run_dir}")


if __name__ == "__main__":
    main()
