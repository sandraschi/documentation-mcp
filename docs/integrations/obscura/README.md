---
title: "Obscura — headless Rust browser for agents and scraping"
category: integration
status: active
audience: mcp-dev
related:
  - operations/WEBAPP_PORTS.md
  - standards/VERIFICATION_STANDARDS.md
  - standards/AGENT_PROTOCOLS.md
last_updated: 2026-11-11
---

# Obscura — headless Rust browser for agents and scraping

**Status**: Active (evaluate) · **License**: Apache-2.0 · **Language**: Rust + V8 · **GitHub**: [h4ckf0r0day/obscura](https://github.com/h4ckf0r0day/obscura)
**Stars**: ~32k · **Forks**: ~2.5k · **Issues**: ~130 open (2026-11-11) · **Default branch**: `main`
**CDP port default**: `9222` (safe, no fleet conflict) · **MCP HTTP default**: `8080` (FORBIDDEN — remap, see §7)

> The open-source headless browser for AI agents and web scraping. Lightweight, stealthy, built in Rust.

Obscura runs real JavaScript via embedded V8, speaks Chrome DevTools Protocol (CDP) well enough to be a
drop-in replacement for headless Chrome under Puppeteer (`puppeteer-core`) and Playwright (`playwright-core`),
and ships its own CLI (`fetch` / `scrape` / `serve`), native renderer (screenshots, screencast, PDF export),
and MCP server (`obscura mcp`). No Chrome, no Node.js, no dependencies at runtime.

Cloudflare's Kitesurf team prototyped on a port of Obscura (see repo README) — credible signal, not proof.

## 1. Why it matters to the fleet

| Metric | Obscura | Headless Chrome |
|---|---|---|
| Memory | ~30 MB | 200+ MB |
| Binary | ~70 MiB | 300+ MB |
| Docker image | ~57 MB (`distroless/cc:nonroot`, uid 65532) | 300 MB – 1 GB |
| Startup | instant | ~2 s |
| Page load (claimed) | ~85 ms | ~500 ms |
| Anti-detect | built-in (`--stealth`) | none |
| Puppeteer / Playwright | yes (CDP) | yes |

Fleet pain it solves: every `web_site_open` / `web_walkthrough_record` / CUA check today needs a full
Chromium. For smoke tests, DOM assertions, markdown dumps, and parallel scraping that is overkill.
Obscura is the **cheap first pass**; Chromium stays the **pixel-truth final gate**
(see `standards/VERIFICATION_STANDARDS.md`).

## 2. What it is / is not

**Is:**
- V8 JS execution + CSS layout/paint renderer (block, inline, flex, grid, table, float, positioning,
  overflow, transform, text, image, SVG, canvas, background, border, animation paths per upstream).
- CDP server (`serve`) covering Target, Page (navigate, screenshot, screencast, printToPDF), Runtime
  (evaluate), DOM, Network, Fetch (live interception), IO (streamed bodies), Storage, Input, plus
  `LP.getMarkdown` (DOM-to-Markdown).
- CLI single-fetch + parallel scrape workers, proxy-aware, SSRF-guarded.
- MCP server (stdio + HTTP) with 14 browser tools (navigate, snapshot, screenshot, pdf, click, fill,
  type, press_key, select_option, evaluate, wait_for, network_requests, console_messages, close).

**Is not:**
- Not Chromium. Long-tail CSS, some Web APIs, media playback, compositor effects, and platform font
  rasterization **will differ**. Upstream says this explicitly. Never certify a visual release on
  Obscura alone.
- MCP transport gives still-image + PDF only. Streaming `Page.startScreencast` needs raw CDP.
- Not a SERP API (that is `openserp`), not a politeness engine (see §9 for the anti-bot posture).

## 3. Install

Release archives carry both `obscura` and `obscura-worker` — keep them in the same directory.

```powershell
# Windows x86_64 only (no 32-bit build). Download obscura-x86_64-windows.zip from Releases,
# extract, keep bundled runtime DLLs beside both exes, add folder to PATH.

# Scoop (default variant = rendering, no stealth):
scoop install https://raw.githubusercontent.com/h4ckf0r0day/obscura/main/scoop/obscura.json

# Linux x86_64:
# curl -LO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-x86_64-linux.tar.gz
# tar xzf obscura-x86_64-linux.tar.gz
# ./obscura fetch https://example.com --eval "document.title"

# Docker (multi-stage, no shell, uid 65532):
$env:OBSCURA_CDP_TOKEN = [Convert]::ToHexString((1..32 | ForEach-Object { Get-Random -Max 256 }))
docker run -d --name obscura -p 127.0.0.1:9222:9222 -e OBSCURA_CDP_TOKEN h4ckf0r0day/obscura
# NOTE: -p 9222:9222 binds all interfaces. Prefer 127.0.0.1:9222:9222 as above.
# A mounted --storage-dir must be writable by uid 65532.
```

Archive suffix matrix (pick at download):

| Suffix | Rendering | Stealth transport |
|---|---|---|
| (none) | yes | no |
| `-stealth` | yes | yes |
| `-no-render` | no | no |
| `-no-render-stealth` | no | yes |

Scoop = default variant. For stealth on Windows, download the `-stealth` zip manually.

Build from source (current stable Rust via rustup; first build ~5 min, V8 compiles once and caches):

```powershell
git clone https://github.com/h4ckf0r0day/obscura.git
cd obscura
# Rendering:
cargo build --release -p obscura-cli --bins --features render
# Rendering + stealth (needs CMake, Clang, libclang/LLVM dev libs; Ubuntu/Debian: build-essential cmake clang libclang-dev llvm-dev):
cargo build --release -p obscura-cli --bins --features render,stealth
# No rendering:
cargo build --release -p obscura-cli --bins --no-default-features
```

## 4. Quick start (CLI)

```bash
# Title / links / rendered HTML / text / markdown / asset inventory
obscura fetch https://example.com --eval "document.title"
obscura fetch https://example.com --dump links
obscura fetch https://news.ycombinator.com --dump html
obscura fetch https://example.com --dump text --output page.txt
obscura fetch https://example.com --dump markdown --output page.md
obscura fetch https://example.com --dump assets          # NDJSON, one record per sub-resource
obscura fetch https://picsum.photos/200/300 --dump original > photo.jpg  # binary-safe raw body

# Dynamic content / slow pages
obscura fetch https://example.com --wait-until networkidle0
obscura fetch https://example.com --timeout 10
obscura fetch https://example.com --wait 3 --selector "#app"
obscura fetch https://example.com --screenshot page.png   # short form: -s page.png

# Proxy (global flag, inherited by fetch/scrape/serve workers)
obscura --proxy socks5://127.0.0.1:1080 fetch https://example.com --dump text
obscura --proxy http://127.0.0.1:8080 scrape https://example.com https://news.ycombinator.com

# Parallel scrape (input order preserved, at most --concurrency active)
obscura scrape url1 url2 url3 --concurrency 25 --eval "document.querySelector('h1').textContent" --format json
obscura scrape https://example.com --quiet --format json   # --quiet suppresses stderr progress

# V8 / SPA budgets
obscura --v8-flags "--max-old-space-size=4096" fetch https://example.com
OBSCURA_SCRIPT_DEADLINE_MS=60000 obscura serve --port 9222   # default script budget 30 s; raise for heavy SPA boot
OBSCURA_MODULE_BUDGET_MS=10000 obscura serve --port 9222     # per-module budget (e.g. Vite HMR client)
```

### Localhost / LAN dev servers (SSRF guard)

Fetches to private/internal IPs are **blocked by default** (DNS-resolution-time checks included).
For fleet dev servers you must opt in:

```bash
obscura fetch http://127.0.0.1:3000 --allow-private-network --dump text
OBSCURA_ALLOW_PRIVATE_NETWORK=1 obscura fetch http://127.0.0.1:10970 --dump markdown
obscura serve --port 9222 --allow-private-network   # applies to CDP clients too
```

Full allow/deny model: `docs/Environment-variables.md` upstream. Key timeouts:
`OBSCURA_SCRIPT_DEADLINE_MS`, `OBSCURA_MODULE_BUDGET_MS`, `OBSCURA_FETCH_TIMEOUT_MS`,
`OBSCURA_NETWORK_BODY_BUFFER_BYTES` (default 2 MiB — raise before `Fetch.takeResponseBodyAsStream`
on large downloads).

## 5. CDP server (`serve`) — Puppeteer / Playwright drop-in

```bash
obscura serve --port 9222
obscura serve --port 9222 --stealth          # anti-detect + tracker blocking
obscura serve --port 9222 --allow-private-network --workers 4
```

| Flag | Default | Notes |
|---|---|---|
| `--port` | `9222` | CDP WebSocket port |
| `--proxy` | — | HTTP/SOCKS5 for all workers |
| `--stealth` | off | needs `-stealth` build |
| `--workers` | `1` | parallel worker processes; crashed children reaped/restarted; 503 when none ready |
| `--worker-max-connections` / `--worker-max-rss` / `--worker-max-age` | off | graceful recycle (replacement starts first, old drains up to `--worker-drain-timeout` 120 s) |
| `--font-dir` | — | repeatable; render build |
| `--obey-robots` | off | respect robots.txt |

```javascript
// Puppeteer (npm i puppeteer-core)
import puppeteer from 'puppeteer-core';
const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:9222/devtools/browser' });
const page = await browser.newPage();
await page.goto('https://news.ycombinator.com');
const stories = await page.evaluate(() =>
  Array.from(document.querySelectorAll('.titleline > a')).map(a => ({ title: a.textContent, url: a.href })));
await browser.disconnect();
```

```javascript
// Playwright (npm i playwright-core)
import { chromium } from 'playwright-core';
const browser = await chromium.connectOverCDP({ endpointURL: 'ws://127.0.0.1:9222' });
const page = await (await browser.newContext()).newPage();
await page.goto('https://en.wikipedia.org/wiki/Web_scraping');
await page.screenshot({ path: 'page.png', fullPage: true });
await page.pdf({ path: 'page.pdf', format: 'A4', printBackground: true });
await browser.close();
```

Media emulation (color-scheme, reduced-motion): upstream `docs/CDP-media.md`.

## 6. MCP server (`mcp`)

```bash
obscura mcp                                   # stdio (Claude Desktop / MCP clients that spawn)
obscura mcp --http --port 10982              # HTTP (example remapped port — DO NOT use 8080, forbidden)
# endpoint: http://127.0.0.1:10982/mcp
# optional (both transports): --proxy <URL> --user-agent <UA> --font-dir <DIR> --stealth
```

```json
{
  "mcpServers": {
    "obscura": { "command": "obscura", "args": ["mcp"] }
  }
}
```

| Tool | Description |
|---|---|
| `browser_navigate` | goto URL (`url`, `waitUntil`: `load` / `domcontentloaded` / `networkidle0`) |
| `browser_snapshot` | URL + title + readable body text + element refs |
| `browser_screenshot` | current page as PNG (render build) |
| `browser_pdf` | current page as embedded PDF (render build) |
| `browser_click` | by snapshot ref or CSS selector |
| `browser_fill` | set input value (fires `input` + `change`) |
| `browser_type` | append text to input |
| `browser_press_key` | keyboard event (`key`, optional `selector`) |
| `browser_select_option` | `<option>` by value or text |
| `browser_evaluate` | JS expression, return result |
| `browser_wait_for` | CSS selector (`selector`, `timeout` s) |
| `browser_network_requests` | requests made by current page |
| `browser_console_messages` | page console log |
| `browser_close` | close page, reset state |

## 7. Fleet wiring — ports, env, hygiene

- **CDP `9222`**: safe default (outside 10700–15000 fleet range, not on the forbidden list).
  When running two instances (e.g. Obscura + Chromium), offset one (`9223`).
- **MCP HTTP**: upstream default `8080` is **FORBIDDEN** (`operations/WEBAPP_PORTS.md`:
  3000, 5000, 5173, 8000, 8080). Always pass an explicit claimed port:
  claim via `fleet-gate/claim_ports.py`, then `obscura mcp --http --port <claimed>`.
- **Bind loopback**: `-p 127.0.0.1:9222:9222`, never bare `-p 9222:9222` on shared hosts.
- **Env**: `OBSCURA_ALLOW_PRIVATE_NETWORK=1` for localhost fleets; `OBSCURA_CDP_TOKEN` for
  Docker CDP auth; `OBSCURA_SCRIPT_DEADLINE_MS` / `OBSCURA_MODULE_BUDGET_MS` /
  `OBSCURA_FETCH_TIMEOUT_MS` / `OBSCURA_NETWORK_BODY_BUFFER_BYTES` for heavy pages.
- **No `.env` commits.** Tokens via env only.
- **Freshness**: stealth builds embed fingerprint lists + tracker blocklist (3,520 domains).
  A 6-month-old binary fights last year's bot war — repull releases on a monthly cadence.

## 8. Usage scenarios per repo

### 8a. `craft-anything` / `codercraft` — ephemeral test browser (original ask)

**Verdict: yes, as the default cheap browser; keep Chromium for final sign-off.**

```powershell
# Per-build ephemeral CDP (allow localhost dev server, 4 workers, auto-recycle)
obscura serve --port 9222 --allow-private-network --workers 4 --worker-max-age 3600
# Drive with existing Puppeteer/Playwright harness — no harness rewrite (CDP drop-in)
# Smoke: DOM assertion + markdown dump + screenshot in one pass
obscura fetch http://127.0.0.1:<app-port> --allow-private-network --dump markdown --output smoke.md
obscura fetch http://127.0.0.1:<app-port> --allow-private-network -s smoke.png
```

Use for: rebuild checks (`rebuild_check` pre-pass), `page_states`-style menu sweeps at low cost,
form/login flows (`page.evaluate` fill + submit, cookies/302 handled), regression diffs across
widths before paying for a full Chromium capture. Promote to Chromium `web_site_capture` /
`web_walkthrough_record` only when the Obscura pass is green — or when the failure smells like
a renderer delta rather than an app bug (long-tail CSS, web fonts, media, canvas).

### 8b. Every `*-mcp` webapp repo (Dashboard / Tools / Chat / Settings / Help / Logs catch-them-all)

Pre-commit smoke script (runs in seconds, no Chromium):

```powershell
obscura fetch http://127.0.0.1:<vite-port> --allow-private-network --wait-until networkidle0 --dump text
obscura fetch http://127.0.0.1:<vite-port> --allow-private-network --eval "document.querySelectorAll('[data-testid]').length"
```

Asserts: all catch-them-all pages route (no blank SPA shell), `data-testid` hooks present
(`onboarding-cue`, etc.), no console-error storm (`browser_console_messages` via MCP).

### 8c. `searchstudio` / `aiwatcher-mcp` — JS-rendered page enrichment

`openserp extract` and raw `fetch` fail on JS-gated pages (bot walls, SPA shells). Receipt-directed
fallback chain: `searchops` first (receipts prove coverage), then Obscura for the uncovered JS page:

```bash
obscura fetch https://js-gated-vendor-blog/post --dump markdown --wait-until networkidle0 --timeout 30
obscura fetch https://js-gated-vendor-blog/post --dump assets   # sub-resource inventory for RAG scoping
```

Respects `--obey-robots` when polite mode matters. Never use high-concurrency `scrape` against a
site you want to stay welcome on (see §9).

### 8d. `arxiv-mcp` / lab-post ingestion

`fetch_lab_post` / `fetch_anthropic_post` cover first-party blogs. For JS-rendered lab pages,
DeepMind blog variants, and interactive figures that the static fetchers return thin:

```bash
obscura fetch <lab-post-url> --dump markdown --wait-until networkidle0
```

Pipe stdout into existing `ingest_paper_to_corpus(markdown=...)` — no new ingest path needed.

### 8e. `reversing-mcp` / REA (`javascript` / `native_overview` kinds)

For Electron `app.asar` / web-bundle targets, `rea_investigate(kind="javascript")` is static analysis.
Obscura adds the **dynamic** half: serve the unpacked bundle on loopback, drive it over CDP,
record `browser_network_requests` + `browser_console_messages` + `Fetch` interception
(`fulfillRequest` to stub C2/update endpoints safely). Complements, does not replace, Ghidra/Hopper.

### 8f. Scheduled fleet polling / digests (`aiwatcher`, morning digest)

Prefer official APIs / RSS / Tavily for scheduled polling (outsourced anti-bot war).
Obscura is the **on-demand** fetcher for the 2–3 JS pages the scheduled pipe could not render —
not the poller itself. Rationale: one IP + robotic cadence = burned IP (see §9).

### 8g. Agent desktop use (Claude Desktop / opencode / Cursor)

```json
{ "mcpServers": { "obscura": { "command": "obscura", "args": ["mcp"] } } }
```

Gives any sampling-capable agent `browser_*` tools with zero Chromium install — handy on
MiniPC / sandbox / Windows Sandbox naked-test runs (`virtualization-mcp win_sandbox_naked_test`).

## 9. Stealth, tracker blocking, and the politeness rule

`--stealth` (needs `-stealth` build): per-session fingerprint randomization (GPU, screen, canvas,
audio, battery), realistic `userAgentData`, `event.isTrusted = true`, hidden internal props,
native-function masking, `navigator.webdriver = false`; plus 3,520-domain tracker blocklist
(analytics, ads, telemetry, fingerprinting scripts never load).

Same arms-race warning as `openserp`: stealth is stale the day it ships. Two postures:

1. **Outsource the race** (scheduled/fleet): vendor APIs, proxies, rotation — pay per call.
2. **Be a polite guest** (personal digging): low volume, cache on, delays, backoff-and-retry,
   `--obey-robots`, per-page blocked accounting. The `tvtropes-mcp` playbook (8–15 s jittered
   delays, 30 s backoff, SQLite accounting) is the template.

What does not work: `scrape --concurrency 25` on a loop against one host from Goliath's IP,
then reading the 403s as truth.

## 10. Limits and failure modes (read before trusting a green check)

- **Renderer deltas**: long-tail CSS, some Web APIs, media playback, compositor effects, platform
  font rasterization may differ from Chromium. A visual diff that fails only under Obscura is a
  renderer bug until proven otherwise — re-run that page under Chromium before filing against the app.
- **Empty/thin dump is not absence**: JS budget expiry (`OBSCURA_SCRIPT_DEADLINE_MS`), body-buffer
  cap (2 MiB), or bot-block all look like "no content". Cross-check with `--dump original` and
  `browser_console_messages` / `browser_network_requests` before concluding.
- **SSRF guard**: forgetting `--allow-private-network` yields a clean refusal on localhost —
  looks like "dev server down". Check the flag first.
- **Large downloads**: raise `OBSCURA_NETWORK_BODY_BUFFER_BYTES`, then stream via
  `Fetch.takeResponseBodyAsStream` + `IO.read`/`IO.close` instead of one giant
  `Network.getResponseBody`.
- **Stale stealth**: repull monthly; log which release served each scheduled run.

## 11. Alternatives considered

| Need | Use |
|---|---|
| Pixel-truth release cert, full CSS/WebAPI/media, screencast video | Chromium + `web_site_capture` / `web_walkthrough_record` / Playwright-Chromium |
| SERP JSON at fleet scale | `openserp` (OSS) → Tavily/Exa/Brave (billed) per `standards/SEARCH_TOOLING_POSTURE.md` |
| Static fetch of docs / llms.txt | `fetch_fetch` (llms-aware) |
| Windows GUI automation (native apps, installers) | `pywinauto-mcp` / CUA driver, not a web browser |
| Full-page politeness scraping with accounting | `tvtropes-mcp` pattern (delays, backoff, SQLite ledger) |

## 12. Background

- [Obscura repo](https://github.com/h4ckf0r0day/obscura) · [Releases](https://github.com/h4ckf0r0day/obscura/releases) · [Docker Hub](https://hub.docker.com/r/h4ckf0r0day/obscura)
- [Benchmarks (separate repo)](https://github.com/h4ckf0r0day/obscura-benchmark) (WPT, obstacle course, vs-Chrome)
- [Cloudflare Kitesurf engineering story](https://blog.cloudflare.com/kitesurf/) (Obscura-inspired prototype)
- [Hermes agent plugin](https://github.com/SGavrl/hermes-plugin-obscura) (session-per-`serve` CDP pattern)
- Upstream docs: `Use-with-Puppeteer.md`, `Use-with-Playwright.md`, `Use-the-MCP-server.md`,
  `CDP-media.md`, `Environment-variables.md`

*Last verified against upstream README 2026-11-11. Re-verify flags/env on upgrade — CLI surface is pre-1.0 and moves.*
