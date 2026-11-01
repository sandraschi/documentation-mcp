---
title: komga-mcp
repo: https://github.com/sandraschi/komga-mcp
ports: 11187/11188
status: active
version: 0.1.0
fleet: ebook/comics
---

# komga-mcp

**Komga bridge for comics/manga/BD/eBooks — FastMCP 3.4 + Starlette**

- **Backend:** 11187 (FastAPI + FastMCP HTTP \/mcp\ + REST \/api/*\)
- **Frontend:** 11188 (Vite React dashboard — Dashboard, Libraries, Series, Books, Inbox, Tools, Skills, Chat, Settings, Help, Logs)
- **Upstream:** gotson/komga 1.26.3 (NextUI beta), CBZ/CBR/EPUB/PDF
- **Repo:** https://github.com/sandraschi/komga-mcp
- **Local:** D:\Dev\repos\komga-mcp

## Purpose
Lightweight sidecar to calibre-mcp (10720/21). Komga serves comics/manga/BD where Calibre is HQ for curation. MOCK-until-onboarded with Joe Mocky/Sandra Mockinger data.

## Tools
- komga_library (list, get) — pagination limit/offset has_more
- komga_series (list, search, get)
- komga_books (list, get, mark_progress)
- komga_users (list, get)
- komga_system (status) + show_komga_status_prefab (app=True)

## Onboarding
See D:\Dev\repos\komga-mcp/docs/ONBOARDING.md — Docker gotson/komga, create admin, set KOMGA_URL/KOMGA_USER/KOMGA_PASSWORD in .env.

## Fleet links
- Companion: calibre-mcp (10720/21), kavita-mcp (11189/90)
- Comparison: calibre-mcp memop docs/calibre-vs-komga-vs-kavita-comparison-2026-08-31

