# Apps page template (APPS_PAGE_STANDARD.md v3)

Canonical vendoring source. Reference impl lives in `git-github-mcp`;
changes land there first, then are copied here, then fanned out with
`mcp-central-docs/scripts/vendor-apps-page.ps1`. Never hand-copy into repos.

## Layout

- `backend/fleet_catalog.py` — registry load, port audit, docs gate, quarantine
- `backend/fleet_common.py` — shared fleet helpers (paths, repos, git)
- `backend/utils/` — `gh_cli` + `response` helpers required by fleet_catalog
- `backend/apps_routes.py` — `register_apps_routes(router)`: GET /apps,
  GET /apps/health, POST /apps/ensure. Package-agnostic (APIRouter or app).
- `frontend/apps.tsx` — **not stored here on purpose**: always vendored
  fresh from the `-From` repo so the newest UX ships. Only backend modules
  (stable logic) are template-homed.

## Target layout after vendoring

- `<pkg>/services/fleet_catalog.py`, `<pkg>/services/fleet_common.py`,
  `<pkg>/services/apps_routes.py`, `<pkg>/utils/{__init__,gh_cli,response}.py`
- one line in the REST module: `register_apps_routes(router)`
- `web|web_sota/src/pages/AppsPage.tsx` (or `apps.tsx`) + `/apps` route
