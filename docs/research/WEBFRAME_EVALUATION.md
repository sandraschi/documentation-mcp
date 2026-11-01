# webframe Evaluation

**Date:** 2026-10-27
**Status:** Useful niche — trusted-page JS runner + lightweight scraper, not a hostile-content sandbox, not a shot-scraper replacement
**Source:** https://github.com/tractordev/webframe (v0.1, 2026-10-24, ~141 stars, MIT)
**Tested on:** Windows 11 + WebView2, release binary `webframe_v0.1_windows_amd64.zip`
**Local clone:** `D:\Dev\repos\_upstream\webframe`
**Prototypes:** `C:\Users\<user>\AppData\Local\Temp\webframe-test\proto\` (ephemeral, not committed)

---

## 1. What it is

"Run a web page like a program." A ~5 MB single-binary Go CLI over `progrium/glaze`: loads a URL in the **OS webview** (WebKit / WebKitGTK / WebView2) via `purego`, no bundled browser, `CGO_ENABLED=0` (except musl). Three ideas compose the whole tool:

- Page runs hidden at full speed; `console.*` goes to stdout, exceptions / unhandled rejections / resource failures / failed page loads go to stderr (`hooks.js` bridges via a bound `window.__webframe` function, batched to preserve order).
- `-c` console mode: each stdin line is `(0,eval)`'d as a global script, promises awaited, result printed JSON-quoted. `var`/functions persist between lines. stdin close exits.
- Lifecycle: `window.close()` in-page exits 0; `-e` exits 1 on first exception; `WF_FOO=bar` env becomes `window.FOO` before page scripts; `SIGHUP` reloads; `-s`/`-S` silence.

Source is small: `webframe.go` ~200 lines, `cmd/webframe/main.go` ~250, `hooks.js` ~150. The Go library exposes the same engine (`New/Eval/Navigate/Run/Terminate`) with `Console/Exception/Closed/Ready` callbacks — policy deliberately left to the caller.

---

## 2. Verified working (all run, not read)

- `webframe examples/hello.html` → EXIT 0, `Hello, world!`
- `echo 'document.title' | webframe -c https://example.com` → `"Example Domain"`
- `({title: document.title, url: location.href})` → `{"title":"Example Domain","url":"https://example.com/"}`
- `new Promise(done => setTimeout(() => done({title: document.title}), 500))` → awaited correctly
- Dynamic CDN import works absent CSP: `(async () => { const r = await import('https://cdn.jsdelivr.net/npm/@mozilla/readability@0.6.0/+esm'); return typeof r.Readability })()` → `"function"`
- `fetch()` from page works (577 chars from example.com)
- `localStorage` works on real pages, correctly fails on `about:blank` (opaque origin)
- Uncaught throw / unhandled rejection / missing `<img>`/`<script>` all land on stderr with stacks; `-e` exits 1
- `WF_API_KEY=abc-secret` → `window.API_KEY === "abc-secret"` in page mode and `-c` mode
- Page-mode one-shot scrape pattern: `console.log(JSON.stringify({...})); window.close();` → clean EXIT 0
- `;`-separated multi-statement one-liners work (`var a=6; var b=7; a*b` → `42`); stdin buffer 64 KB–16 MB

---

## 3. shot-scraper `javascript` pattern compatibility

| shot-scraper pattern | webframe status |
|---|---|
| Single expression → JSON string | ✅ identical |
| `({…})` object literal | ✅ identical |
| `() => { …; return … }` multi-statement | ⚠️ **must invoke**: `(() => {…})()` — bare arrow returns `[Function: (anonymous)]`, never executes. Touches every migrated script |
| `throw` / failed assert → exit 1 (CI tests) | ⚠️ stderr gets `Uncaught …` but `-c` exit stays 0 (documented: console errors don't count toward `-e`) |
| Promise/setTimeout delay | ✅ |
| `async` + CDN import (Readability) | ✅ unless CSP blocks (below) |
| `--bypass-csp` | ❌ **no equivalent** — github.com blocks the CDN import with the same error shot-scraper gives *without* the flag, and there is no flag |
| `--width/--height` hidden viewport | ❌ hidden default is 624×441 (undocumented); `-w WxH` **shows a window** (and sizes the outer window, not the viewport, on Windows). Go lib can set hidden size; CLI cannot |
| `--raw`, `-o`, `--timeout`, `--user-agent`, `--auth`, `--browser-arg`, `--fail/--skip` | ❌ none exist; workarounds: strip quotes downstream, redirect stdout, pipe script files via stdin |
| `-i file` / `gh:` script loader | ❌ pipe the file in instead |
| Screenshots / video / PDF / HAR / accessibility tree | ❌ out of scope by design — this tool is the `javascript` subcommand only, minus flags |

## 4. As a sandboxing tool

Weaker than the shape suggests. Isolation is inherited, not built:

- **Real:** the OS webview sandbox (WebKit sandbox kept on + non-root user in the Alpine Docker image — the `Dockerfile` is clean). Good for **trusted** browser-only code (WASM/WebGPU/DOM libs from scripts/CI, v86-in-headless, long-lived daemon pages).
- **Missing:** no network allow/deny, no CPU/memory/time limits, no navigation gating, no CSP control either way. The CLI is a terminal↔page pipe; policy is yours to write against the Go lib.
- **Control channel lives in page context:** `window.__webframe_eval`, `window.__webframe`, `window.close` override are plain page JS. A hostile page can redefine them, break `-c` evaluation, or never call `window.close()` and squat forever. No out-of-band control.
- **Hang vectors (confirmed):** `alert()/confirm()/prompt()` hang hidden pages on WebView2 despite docs claiming `[dialog]` + auto-dismiss — `before` printed, never `after`, process had to be killed. Any page calling `alert` is a pipeline hang. Infinite timers/loops are unthrottled by design.
- **Secrets:** `WF_*` globals sit on `window` readable by any page script; nothing redacted from logs.

Verdict: fine runner for trusted pages and first-party scraping. Not a hostile-content sandbox — for untrusted pages prefer Chromium + explicit context isolation + CSP/network policy (the Playwright model shot-scraper sits on).

## 5. Bugs / nits (upstream-worthy)

1. `-v` prints the version but the process **never exits** on Windows (the `--help`/`os.Exit(2)` path is fine; the `return`-from-main path hangs).
2. `alert()` hang above (docs say auto-dismiss).
3. Hidden default viewport 624×441 undocumented — responsive-layout scrapers silently get the narrow variant.
4. Cold start ~6–8 s on Windows — fine for daemons; for one-shot-per-URL loops, keep one `-c` process open and stream lines.

## 6. Recommended patterns

```powershell
# One-shot: page prints its own result, then exits
# page: console.log(JSON.stringify({title: document.title})); window.close();
webframe scrape.html

# REPL drive-by: no page changes, keep process open for many URLs/queries
echo '({title: document.title})' | webframe -c https://example.com
# multi-statement: invoke it yourself, one line
echo '(() => { var ps = document.querySelectorAll("p"); return ps.length })()' | webframe -c https://example.com
```

## 7. Bottom line

Keep in the toolbox for "I need a real DOM/JS engine as a 5 MB pipe." Don't reach for it when you need CSP bypass, viewport control, auth, screenshots, or containment of anything you wouldn't run in your own browser tab.
