---
title: kavita-mcp
repo: https://github.com/sandraschi/kavita-mcp
ports: 11189/11190
status: active
version: 0.1.0
fleet: ebook/comics
---

# kavita-mcp

**Kavita bridge for eBooks/comics/manga — FastMCP 3.4 + Starlette**

- **Backend:** 11189 (FastAPI + FastMCP HTTP \/mcp\ + REST \/api/*\)
- **Frontend:** 11190 (Vite React dashboard — Dashboard, Libraries, Series, Reading Lists, Inbox, Tools, Skills, Chat, Settings, Help, Logs)
- **Upstream:** Kareadita/Kavita v0.9.1.0 (28 Aug 2026), EPUB variable fonts, Kavita+ overhaul
- **Repo:** https://github.com/sandraschi/kavita-mcp
- **Local:** D:\Dev\repos\kavita-mcp

## Purpose
All-rounder ebook+comic server alongside calibre-mcp HQ. Best reading UX + OIDC sharing. MOCK-until-onboarded.

## Tools
- kavita_library (list, get, scan)
- kavita_series (list, search, get, get_chapters)
- kavita_reading (get_progress, mark_progress, get_bookmarks)
- kavita_users (list, get)
- kavita_system (status) + show_kavita_status_prefab (app=True)

## Onboarding
See D:\Dev\repos\kavita-mcp/docs/ONBOARDING.md — Docker jvmilazz0/kavita, admin + KAVITA_API_KEY.

## Fleet links
- Companion: calibre-mcp, komga-mcp
- Comparison: calibre-mcp memop docs/calibre-vs-komga-vs-kavita-comparison-2026-08-31

