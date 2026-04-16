# glance-mcp — RSS, Open-Meteo, fleet probes

**FastMCP 3.1 · No API keys for weather · Minimal attack surface**

> Fetch RSS/Atom feeds, grid weather from Open-Meteo, and parallel GET `/health` checks against your local MCP fleet. SSRF-aware defaults for RSS (public internet; opt-in LAN); probes allow localhost + RFC1918; block cloud metadata IP.

---

## Summary

| Item | Details |
|------|---------|
| **Repo** | [github.com/sandraschi/glance-mcp](https://github.com/sandraschi/glance-mcp) · `D:\Dev\repos\glance-mcp` |
| **Backend** | **10776** — FastAPI `/health`, `/docs`, REST `/api/*`, MCP streamable HTTP **`/mcp`** |
| **Frontend** | **10777** — Vite `Webapp` (proxy to backend) |
| **Start** | `uv run glance-mcp --serve` or `.\web_sota\start.ps1` |
| **Tools** | `rss_fetch_feed`, `open_meteo_forecast`, `fleet_http_probe` |

---

## Tools

- **rss_fetch_feed** — Parse Atom/RSS (titles, links, summary); size cap; `GLANCE_RSS_ALLOW_PRIVATE_HOSTS=1` for LAN/dev feeds.
- **open_meteo_forecast** — WGS84 lat/lon → `api.open-meteo.com` (no key).
- **fleet_http_probe** — Batch GET URLs (e.g. `http://127.0.0.1:10746/health`); max 64 URLs.

---

## Documentation (in repo)

- **README.md** — Config, env, run.
- **docs/EXAMPLE_FEEDS.md** — Curated Atom/RSS list (Simon Willison default, Bruce Schneier, hnRSS, etc.).
- **CHANGELOG.md** / **docs/PRD.md**

---

**Last updated:** 2026-03-20
