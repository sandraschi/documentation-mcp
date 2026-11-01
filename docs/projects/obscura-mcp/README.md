# Obscura MCP (`obscura-mcp`)

FastMCP wrapper server for **Obscura** ([`d:\Dev\repos\external\obscura`](file:///d:/Dev/repos/external/obscura)), the fleet's high-speed Rust-native stealth headless browser engine.

## Status

- **Status**: ACTIVE / INTEGRATED (2026-08-24)
- **Engine Binary**: `d:\Dev\repos\external\obscura\target\release\obscura.exe`
- **Upstream Engine Version**: `v0.2.1`

## Key Capabilities

- **Ultra-Fast Stealth Rendering**: Combines a real V8 engine (`deno_core`) with Chrome 145 TLS fingerprinting (`--stealth`), running **~12x faster** and using **~6x less RAM** than headless Chromium.
- **Bypasses Bot Protection**: Unblocks Cloudflare challenges and executes client-side SPA JavaScript.
- **Python Integration**: Exposes `fetch_with_obscura` for direct Python import across fleet scrapers (`tvtropes-mcp`, `aiwatcher-mcp`, `scraper-mcp`).

## Fleet Integrations

| Consuming Server | Integration Role |
|---|---|
| **`tvtropes-mcp`** | Cloudflare anti-bot bypass & V8 challenge solver in `TvtropesCrawler`. |
| **`aiwatcher-mcp`** | Pre-rendering dynamic SPA AI blogs & bypassing 403/429 feed blocks. |
| **`scraper-mcp`** | Stealth page rendering fallback for ToolBench & LobeHub probes. |
