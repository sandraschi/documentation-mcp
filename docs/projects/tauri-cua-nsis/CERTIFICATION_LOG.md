# Fleet Tauri CUA-NSIS Certification Log

**Updated**: 2026-06-15

## Status

| Phase | Count |
|-------|-------|
| Total repos with Tauri wrappers | 72 |
| Certified 11/11 (CUA smoke pass) | 13 |
| tsc-clean (0 TS errors) | 5 |
| Need TS fix + rebuild + cert | 14 |
| Need complex type fix | 1 (multi-backup-mcp) |
| Pre-existing blockers | 3 |

## Certified Repos (13)

windows-computer-use-mcp, devices-mcp, calibre-mcp, plex-mcp, speech-mcp, bookmarks-mcp, arr-mcp, chip-design-mcp, freecad-mcp, google-ai-mcp, email-mcp, jellyfin-mcp, videogen-mcp

## tsc-Clean, Ready for Build + Cert (5)

filesystem-mcp, fleet-agent-mcp, observability-mcp, obsidian-mcp, ocr-mcp

Each needs: `npx vite build` in frontend dir → `build.ps1` in native/ → `cua-smoke.py`

## Need TS Fix Then Cert (14)

| Repo | Errors | Type |
|------|--------|------|
| nest-protect-mcp | 2 | Logging.tsx setSort |
| notepadpp-mcp | 3 | Logging.tsx setSort + settings.tsx unused |
| qbt-mcp | 2 | Logging.tsx setSort |
| notion-mcp | 6 | apps-catalog imports + help.tsx + Logging.tsx + settings.tsx |
| osc-mcp | 4 | dashboard.tsx + help.tsx + Logging.tsx |
| tailscale-mcp | 6 | 2x Logging.tsx + logs.tsx setSort + settings.tsx |
| rustdesk-mcp | 8 | apps-catalog + control + Logging + status |
| monitoring-mcp | 7 | apps-catalog + control + help + Logging + settings |
| netatmo-weather-mcp | 8 | apps-catalog + sidebar(Activity) + chat + Logging + settings + trends |
| obs-mcp | 10 | Logging + settings + stage(CustomTrigger/DEFAULT_TRIGGERS) |
| ring-mcp | 6 | apps-catalog + api.ts(TS2352) + chat(TS2345) + settings |
| sdr-mcp | 4 | use-sdr-ws.ts(TS2345) + Logging + stations(TS2345) |
| limx-robotics-mcp | 3 | Logging + Models.tsx(TS2339) |
| multi-backup-mcp | 24 | jobs.tsx(TS2322/2345) + tools-hub.tsx(TS2339/2322) + Logging + settings + help |

## Common Fix Patterns

### 1. Logging.tsx setSort (10 repos)
```tsx
// Remove unused setSort from destructuring OR fix the call:
// BAD: setSort()
// GOOD: setSort("desc")
```

### 2. Unused imports in apps-catalog.ts (8 repos)
Remove `Github`, `Box`, `Scan`, `Archive` from the lucide-react import.

### 3. Missing import names
- `Activity` — add to lucide-react import in sidebar.tsx
- `repo` — add `const repo = "multi-backup-mcp"` in help.tsx (3 occurrences)
- `CustomTrigger`, `DEFAULT_TRIGGERS` — define constants or import in stage.tsx

### 4. Complex type fixes
- ring-mcp api.ts: `import.meta as ImportMeta` → `import.meta as unknown as { env: ... }`
- sdr-mcp use-sdr-ws.ts: `Float32Array<ArrayBufferLike>` → `Float32Array`
- limx-robotics Models.tsx: add type assertions for `path`, `name`
- multi-backup-mcp jobs.tsx, tools-hub.tsx: type the API response objects

## Build Pipeline

```powershell
# Per clean repo:
cd web_sota && npx vite build
cd ../native && .\build.ps1
python scripts\cua-smoke.py --installer "target\release\bundle\nsis\*setup.exe"
```

## HTML Dashboard

`projects/tauri-cua-nsis/index.html` — sortable table, filterable, screenshots per repo, links to GitHub.

Dashboard is served by `mcp-central-docs` webapp at port 10794. Open in browser.
