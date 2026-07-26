# ToolBench Playwright scraper

Use when the [Scoring API](https://toolbench.arcade.dev/api-access) is unavailable: load the [SCORED search](https://toolbench.arcade.dev/?q=sandraschi&status=SCORED) (or any query) in a real browser, collect assessment URLs, then fetch each page with **rate limiting** so ToolBench is not hammered.

## Setup (once)

From this folder:

```powershell
cd D:\Dev\repos\mcp-central-docs\toolbench\scripts
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
```

Use the **venv’s** `python` for `playwright install` so Chromium lands where Playwright expects. If **`discover`** returns **0 URLs**, the results table may require **sign-in** or different timing: copy assessment links from the browser (paths like `/tools/...`) into `urls.txt` and use **`scrape`** only, or retry with **`--headed`**.

## Modes

### 1. Discover links from search (pagination)

Walks the results table, follows “next” while enabled, collects `a[href]` that look like server detail pages (hostname `toolbench.arcade.dev`, path not in the exclude list). Writes `urls.txt` and optional JSONL snapshots. **`/api/auth` links are excluded** (they are not assessments).

```powershell
python .\scrape_toolbench_assessments.py discover --search-url "https://toolbench.arcade.dev/?q=sandraschi&status=SCORED" --out-dir ".\out_sandraschi" --delay-seconds 4 --jitter-seconds 2 --max-pages 20
```

Tune **`--delay-seconds`** (base pause between page loads) and **`--jitter-seconds`** (random extra 0–N s) if you see throttling or want to be extra polite.

### 2. Scrape known URLs

Put one assessment URL per line in `urls.txt`, then:

```powershell
python .\scrape_toolbench_assessments.py scrape --urls-file ".\urls.txt" --out-dir ".\out_scrape" --delay-seconds 3 --jitter-seconds 1.5
```

### 3. Combined (discover then scrape)

```powershell
python .\scrape_toolbench_assessments.py full --search-url "https://toolbench.arcade.dev/?q=sandraschi&status=SCORED" --out-dir ".\out_full" --delay-seconds 4 --jitter-seconds 2
```

### 4. Reference pages (rules/pattern drift watch)

Capture a fixed set of ToolBench/Arcade pages we rely on for hardening guidance (no broad crawl):

```powershell
python .\scrape_toolbench_reference_pages.py --out-dir ".\reference_out" --delay-seconds 2 --jitter-seconds 1
```

This writes timestamped `txt` + `html` snapshots for:

- `toolbench.arcade.dev/methodology`
- `toolbench.arcade.dev/improve`
- `toolbench.arcade.dev/submit`
- `toolbench.arcade.dev/api-access`
- `arcade.dev/patterns`

Use this to detect wording/rule drift and update fleet checklists proactively.

### 5. Drift report (latest two snapshots)

After you have at least two runs in `reference_out/`, generate a human-readable diff:

```powershell
python .\report_reference_drift.py --out-dir ".\reference_out"
```

Optional explicit run IDs + JSON artifact:

```powershell
python .\report_reference_drift.py --out-dir ".\reference_out" --base-run "20260326T120000Z" --new-run "20260327T120000Z" --write-json
```

## Outputs

Under `--out-dir`:

- **`urls.txt`** — deduplicated list (discover / full).
- **`pages/*.json`** — per URL: `url`, `title`, `fetched_at`, `grade_guess`, `main_text_excerpt`, `links_internal`.
- **`pages/*.html.gz`** — optional gzip of `inner_html` of `main` or `body` if `--save-html` (large).

Use excerpts + your [TEMPLATE.md](../improvements/TEMPLATE.md) to fill [TRACKER.md](../improvements/TRACKER.md).

## DOM notes

ToolBench may change markup. If discover finds zero links, paste URLs manually into `urls.txt` and use **`scrape`** only. Adjust in-script constants `LINK_HINT_PATH_PARTS` / `EXCLUDE_PATH_SUBSTR` if Arcade adds new routes.

## Web UI (fleet)

**toolbench-mcp** (`D:\Dev\repos\toolbench-mcp`) exposes the same script via **`http://127.0.0.1:10816`** (Vite) → **`/api/scraper/*`** on the backend (**10817**). Use it to run discover / scrape / full and inspect `scrape_out/` without the shell. See that repo’s README for `TOOLBENCH_SCRAPER_SCRIPT` and Playwright install.

## Ethics

- Default delays are conservative; do not run dozens of parallel browsers against production.
- Prefer **API access** for bulk scoring when approved.
- Keep scope to your own fleet workflows; avoid broad third-party harvesting.
