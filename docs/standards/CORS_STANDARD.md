# CORS Standard

**Established**: 2026-07-13
**Scope**: All fleet webapps with a REST/HTTP backend (FastAPI, Starlette, FastMCP HTTP)

---

## 0. Fundamentals — what CORS actually is

**CORS = Cross-Origin Resource Sharing.** A browser security mechanism, not a server security mechanism — the distinction matters and is the most common source of fleet confusion (see §0.4).

### 0.1 The problem it solves: the same-origin policy

Browsers enforce the **same-origin policy** by default: a page loaded from origin A cannot read the response of a request it makes to origin B, unless B explicitly opts in. "Origin" means the exact triple **scheme + host + port** — all three must match or it's cross-origin:

| Page origin | Request to | Same origin? |
|---|---|---|
| `http://localhost:11092` | `http://localhost:11092/api/health` | Yes |
| `http://localhost:11092` | `http://localhost:11091/api/health` | **No** — port differs |
| `http://localhost:11092` | `https://localhost:11092/api/health` | **No** — scheme differs |
| `http://localhost:11092` | `http://127.0.0.1:11092/api/health` | **No** — host differs (browsers treat `localhost` and `127.0.0.1` as different origins, even though they resolve to the same machine — a frequent gotcha) |

This exists to stop a malicious page from silently reading your bank's response using cookies your browser already sent (the browser attaches cookies/credentials to the request regardless of origin — same-origin policy is what stops the *response* from being readable by the wrong page, not what stops the request from being sent).

### 0.2 What CORS does: the opt-in

CORS is the mechanism a server uses to tell the browser "it's fine, let origin X read my response." It's implemented entirely via response headers:

| Header | Purpose |
|---|---|
| `Access-Control-Allow-Origin` | Which origin(s) may read the response. A literal origin or `*` (wildcard) |
| `Access-Control-Allow-Credentials` | Whether cookies/auth headers are allowed on the cross-origin request. **Cannot be combined with a wildcard origin** — browsers reject `Allow-Origin: *` + `Allow-Credentials: true` outright. This is exactly why the fleet checklist below bans `allow_origins=["*"]`: every fleet webapp needs credentialed requests, so wildcard was never actually an option, not just a hardening choice |
| `Access-Control-Allow-Methods` | Which HTTP methods (GET, POST, PUT, DELETE...) the origin may use |
| `Access-Control-Allow-Headers` | Which request headers the origin may send (custom headers like `Authorization` must be explicitly allowed) |
| `Access-Control-Max-Age` | How long the browser may cache a preflight result before re-checking |

### 0.3 Simple vs. preflighted requests

Not every cross-origin request triggers an extra round-trip:

- **Simple requests** (GET/POST/HEAD with only a small set of "CORS-safelisted" headers, no custom `Content-Type` beyond form-encoded/plain-text) go straight through; the browser checks `Access-Control-Allow-Origin` on the actual response and blocks reading it client-side if the origin isn't allowed. The request still HITS the server — CORS never prevents the server from receiving it, only the browser from exposing the response to the calling page's JavaScript.
- **Preflighted requests** (anything with a JSON body, custom headers like `Authorization`, or methods like `PUT`/`DELETE`) trigger an automatic `OPTIONS` request first, asking permission before the real request is sent. If the server doesn't answer the `OPTIONS` preflight correctly, the browser never sends the real request at all — this is the `405 Method Not Allowed` / "Failed to fetch" failure mode documented in `TAURI_PRODUCTION_PITFALLS.md`, and it's the single most common way fleet webapps break on CORS: the GET requests all work fine in manual testing, then a POST with a JSON body silently fails because nothing handles `OPTIONS`.

### 0.4 The most important special case: CORS is a browser-only mechanism

**CORS does not protect a server from anything.** It's enforced entirely client-side, by the browser, on behalf of the page's JavaScript. A `curl` request, a Python `httpx` call, another MCP server, or any non-browser client **completely ignores CORS headers** — there's no browser present to enforce the policy. This has two fleet-specific implications worth being explicit about:

- Every server-to-server call in this fleet (osc-mcp calling another server's REST endpoint, Fritz polling `report_logs`, admiral's relay, MCP stdio/HTTP transport itself) is **entirely unaffected by CORS** — CORS only ever matters for the webapp dashboards, because they're the only fleet component running inside an actual browser or WebView.
- CORS configuration is NOT a substitute for authentication. A wide-open `allow_origin_regex` (like the fleet's own tailnet-covering pattern below) is safe specifically because the tailnet itself is the access boundary (only devices on Sandra's tailnet can reach the port at all) — CORS here is about making the *browser* cooperate with legitimate cross-device access (phone hitting a Goliath-hosted dashboard), not about keeping anyone out. If a fleet server is ever exposed beyond the tailnet, CORS breadth stops being harmless and needs to be revisited alongside real auth.

---

## Problem

Every fleet webapp needs CORS configured for multiple access modes:

| Mode | Origin example | User |
|------|---------------|------|
| Dev browser | `http://localhost:10701` | Developer on the machine |
| Tauri WebView | `tauri://localhost`, `https://tauri.localhost` | NSIS-installed app |
| Tailscale (phone/tablet) | `https://goliath.tail-abc.ts.net` | Remote access |
| Tailscale direct IP | `http://100.88.12.34:10701` | Remote access |
| LAN from another PC | `http://192.168.1.50:10701` | Home network |

A missing origin causes silent `Failed to fetch` errors that are hard to debug (no console in the Tauri WebView; mobile Safari gives vague "network error").

---

## The Pattern

### `allow_origins` (explicit list)

Include the following in **every** backend's CORS `allow_origins`:

```python
_cors_origins = [
    # Local dev
    f"http://localhost:{FRONTEND_PORT}",
    f"http://127.0.0.1:{FRONTEND_PORT}",
    f"http://localhost:{BACKEND_PORT}",
    f"http://127.0.0.1:{BACKEND_PORT}",
    # Tauri WebView (always include, harmless when not in Tauri)
    "tauri://localhost",
    "http://tauri.localhost",
    "https://tauri.localhost",
]
```

### `allow_origin_regex` (broad LAN + Tailscale)

Apply **unconditionally** (not just when `{REPO}_TAURI=1`):

```python
_cors_regex = r"https?://(?:[a-zA-Z0-9-]+\.ts\.net|.*?\.tail-[a-f0-9]+\.ts\.net|tauri\.localhost|localhost|127\.0\.0\.1|192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|100\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?$|^tauri://localhost$"
```

This covers:
- `*.ts.net` (Tailscale magic DNS, short form)
- `*.tail-xxxx.ts.net` (Tailscale full form)
- `tauri.localhost` (http + https)
- `localhost`, `127.0.0.1`
- `192.168.x.x`, `10.x.x.x` (LAN)
- `100.x.x.x` (Tailscale CGNAT IPs)
- Optionally with any port
- `tauri://localhost` (non-URL scheme)

### `{REPO}_TAURI` env var (legacy, optional)

The `{REPO}_TAURI` env var is **no longer needed** for the regex (it covers Tauri origins unconditionally). Keep it only if the backend needs to branch on desktop-vs-browser behavior (e.g. different log levels, no background GPU jobs).

---

## Implementation

### FastAPI

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_origin_regex=_cors_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Starlette

```python
from starlette.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_origin_regex=_cors_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### FastMCP `run_http_async()` pitfall

> **FastMCP's `run_http_async()` spawns its own internal FastAPI instance that ignores custom middlewares.** If you mount `CORSMiddleware` on your outer app but use `mcp.run_http_async()` for the server, CORS is silently dropped.

**Fix**: Run Uvicorn directly on the fully configured ASGI app:

```python
import uvicorn
from fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

mcp = FastMCP(...)
# ... register tools ...

# Get the ASGI app and add CORS to it
asgi_app = mcp.http_app(path="/mcp")
asgi_app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_origin_regex=_cors_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run manually — do NOT use mcp.run_http_async()
config = uvicorn.Config(asgi_app, host="127.0.0.1", port=PORT, log_level="info")
server = uvicorn.Server(config)
server.run()
```

See `TAURI_PRODUCTION_PITFALLS.md` §IX (FastMCP HTTP routing preflight bug) for the full debugging story.

---

## Per-Repo Checklist

- [ ] `allow_origins` includes `tauri://localhost`, `http://tauri.localhost`, `https://tauri.localhost`
- [ ] `allow_origin_regex` is set and covers Tailscale `*.ts.net`, LAN IPs, localhost
- [ ] Regex applied **unconditionally** (not gated on `{REPO}_TAURI`)
- [ ] FastMCP HTTP servers do NOT use `run_http_async()` — use direct `uvicorn.Server` on `mcp.http_app()` with CORS middleware attached
- [ ] No `allow_origins=["*"]` in any backend — not just hardening, it's a browser-enforced impossibility once `allow_credentials=True` is set (§0.2)
- [ ] If a webapp ever needs to be reachable from outside the tailnet, CORS breadth is re-evaluated alongside real auth (§0.4) — the current regex's safety depends on the tailnet being the actual access boundary

---

## Appendix: quick glossary

| Term | Meaning |
|---|---|
| **Origin** | scheme + host + port triple; all three must match for "same-origin" |
| **Preflight** | automatic `OPTIONS` request the browser sends before certain cross-origin requests, asking permission first |
| **Simple request** | a request that skips preflight (plain GET/POST/HEAD, safelisted headers only) |
| **CGNAT range** | `100.64.0.0/10` — Tailscale assigns tailnet devices addresses in this range (`100.x.x.x`), which is why the fleet regex explicitly covers it alongside standard LAN ranges |
| **MagicDNS** | Tailscale's automatic DNS giving each tailnet device a `<name>.<tailnet>.ts.net` hostname — the `*.ts.net` and `*.tail-[hex].ts.net` regex alternatives both exist because Tailscale has shipped both a short and a fully-qualified hostname form over time; the regex covers both rather than assuming which one any given device/browser will present |
