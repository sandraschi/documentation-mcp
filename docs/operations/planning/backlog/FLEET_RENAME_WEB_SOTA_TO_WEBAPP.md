# Fleet rename: `web_sota` → `webapp`

**Priority:** P2  
**Scope:** ~50 fleet repos with Tauri/Vite webapps

## Problem

`web_sota` reads like jargon (`web_superduper`) with no semantic value. Fleet standard `WEBAPP_SOTA_STANDARDS.md` mandates the pattern but the directory name confuses newcomers and scrapers.

## Touch points

- `tauri.conf.json` (`frontendDist: "../web_sota/dist"`)
- `vite.config.ts`, build/start scripts
- CI workflows, docs

## Sweep approach

1. Per-file `.bak` backup (batch mutation safety rule)
2. `rg -l "web_sota" D:\Dev\repos\`
3. Batch rename directory: `web_sota` → `webapp`
4. Update all references
5. Update `standards/WEBAPP_SOTA_STANDARDS.md`
6. Verify build per repo

**Batch limit:** Sub-5-file per commit; multiple commits across fleet.
