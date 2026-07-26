# Webapp Directory Standard

**Problem:** Fleet scripts can't find the frontend because repos use different
names: `web_sota/`, `webapp/`, `web/`, `frontend/`, `web_app/`.

**Rule:** The frontend directory MUST be named `webapp/` at the repo root.

## Why `webapp/`

- Simple, obvious, unambiguous
- `web_sota/` was a naming convention from 2025 that served its purpose
- Every repo we build IS SOTA — the directory name doesn't need to prove it

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
