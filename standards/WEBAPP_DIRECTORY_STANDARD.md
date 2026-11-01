---
title: "Webapp Directory Standard"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-09
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Webapp Directory Standard

**Problem:** Fleet scripts can't find the frontend because repos use different
names: `web_sota/`, `web-sota/`, `webapp/`, `web/`, `frontend/`, `web_app/`.

**Rule:** The frontend directory MUST be named `webapp/` at the repo root.

## Why `webapp/`

- Simple, obvious, unambiguous
- `web_sota/` was a naming convention from 2025 that served its purpose
- Every repo we build IS SOTA - the directory name doesn't need to prove it

## What Must Be Inside `webapp/`

| File | Purpose |
|------|---------|
| `package.json` | Dependencies + scripts |
| `vite.config.ts` | Vite config with API proxy |
| `tailwind.config.js` | TailwindCSS config |
| `tsconfig.json` | TypeScript config |
| `index.html` | Entry point |
| `src/` | React source |
| `src/pages/` | Page components |
| `src/components/` | Shared components |
| `src/lib/api.ts` | API fetch helper |
| `e2e/` | Playwright tests |
| `playwright.config.ts` | Playwright config |
| `start.ps1` | Dev server startup |

## Fleet Audit

```powershell
# Find repos that still use web_sota (need migration)
Get-ChildItem D:\Dev\repos -Directory | Where-Object { Test-Path "$_\web_sota" }

# Find repos with no frontend at all (may be intentional T1)
Get-ChildItem D:\Dev\repos -Directory | Where-Object {
    -not (Test-Path "$_\web_sota") -and
    -not (Test-Path "$_\webapp") -and
    -not (Test-Path "$_\start.ps1")
}
```

## Migration (`web_sota/` -> `webapp/`)

No exceptions for new repos. For existing repos using `web_sota/`:

1. `Rename-Item web_sota webapp`
2. Update all references in:
   - `justfile` (web-build, web-install, web recipes)
   - `start.ps1` (pushd paths)
   - `native/build.ps1` (frontendDirs array)
   - `native/tauri.conf.json` (frontendDist, beforeDevCommand, beforeBuildCommand)
   - `.github/workflows/ci.yml`
   - `.mcpbignore`
   - `docker-compose.yml`
3. Commit with message: `chore: rename web_sota/ -> webapp/`

## CI during migration

Fleet `ci.yml` is **identical** in every repo (`templates/ci.yml.template`). It detects the frontend at runtime by `package-lock.json` (first match wins):

1. `webapp/` (canonical - wins if both exist)
2. `webapp/frontend/` (nested canonical variant, 16 repos)
3. `web_sota/` (legacy, 96 repos)
4. `web-sota/` (legacy hyphen variant, e.g. devices-mcp)
5. `web/` (legacy, 4 repos: forgejo, git-github, kubernetes, speech)
6. `frontend/` (7 repos)
7. `ui/` (2 repos: ednaficator, moltbot)
8. `web_app/` (documented, 0 repos - future-proof)

Repos with **no** frontend skip Node/Biome/tsc/Playwright steps. Python-only repos still run Ruff (verify + lint + format), pytest (if `tests/`), `ty`, and `pip-audit`.

**`package-lock.json` is required for detection.** Repos with a `package.json` but no lock file silently skip the whole frontend gate (2026-09-06 audit: 24× `webapp/`, 9× `web_sota/`, plus lock-less `web/`, `frontend/`, `ui/` stragglers). Fix: run `npm install` in the web root and commit the lock - do NOT fork `ci.yml` per repo (for directory name OR lock absence); rename the folder to `webapp/` and commit the lock instead.
