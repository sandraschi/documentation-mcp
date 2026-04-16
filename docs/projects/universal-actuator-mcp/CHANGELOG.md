# Changelog â€” Universal Actuator MCP Hub

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] â€” 2026-03-02

### ðŸŒ Frontend â€” New Pages & Live Data

#### Added
- **`/library` page** (`frontend/src/app/library/page.tsx`): Federated media browser wired to `GET /library`. Supports full-text search + domain filter tabs (`All / Media / Books / Photos`). Responsive card grid with source badges.
- **`/chat` page** (`frontend/src/app/chat/page.tsx`): Command dispatch terminal with live response stream from `POST /chat`.
- **Library** and **Chat** navigation links added to the sidebar (`Sidebar.tsx`).

#### Changed
- **Dashboard** (`/`): Upgraded from static mock data to live data:
  - Polls `GET /telemetry` every 5 seconds for real CPU/memory/uptime.
  - Fetches `GET /milestones` on mount and displays last 5 milestones as a timeline.
  - Online/Connecting status indicator with formatted uptime display.
- **Fleet page** (`/fleet`): Fixed data shape mismatch â€” backend returns `discovered_servers[].name`, frontend was reading `servers[].id`. Corrected mapping to use `discovered_servers` array and `name`, `url`, `active` fields.

#### Fixed
- Progress bar components: removed incorrect CSS-variable inline-style pattern; replaced with direct `style={{ width: '...' }}` (standard React dynamic-width pattern).
- Removed stale `eslint-disable-next-line react/forbid-component-props` comments that were wrongly referencing the rule name.

---

### ðŸ”§ Backend â€” New REST Endpoints

#### Added
- **`GET /milestones`** (`@mcp.app.get("/milestones")`): REST HTTP endpoint exposing milestone history so the dashboard can poll it. Previously `get_milestones_history` was only available as an MCP tool.

---

## [1.0.0] â€” 2026-02-28

### ðŸš€ Initial Release

#### Backend (`backend/server.py`)
- FastMCP 3.1.1+.5 server with SSE transport on port **10857**.
- MCP Tools:
  - `search_federated(query, domain)` â€” fan-out search to Calibre + Plex subservers.
  - `glom_on()` â€” auto-discover all active MCP servers in port range 10700â€“10900.
  - `universal_milestone(title, description, type)` â€” persistent milestone logging to `backend/state/milestones.json`.
  - `get_milestones_history()` â€” retrieve full milestone log.
  - `get_fleet_telemetry()` â€” real-time psutil metrics + node count.
  - `federated_search(query)` â€” cross-node structured search.
- REST Endpoints:
  - `GET /glom_on` â€” fleet discovery.
  - `GET /telemetry` â€” CPU, memory, uptime, milestone count.
  - `GET /library` â€” federated media search (Calibre + Plex fan-out, demo fallback).
  - `POST /chat` â€” command dispatch with fleet search.
  - `POST /launch` â€” detached-process launch via registered `start.ps1` scripts.
- App launch registry (`APP_LAUNCH_REGISTRY`) cross-referenced with `apps-catalog.ts`.

#### Frontend (`frontend/`)
- Next.js 16 + Tailwind CSS dashboard on port **10720**.
- Pages: `/` (Dashboard), `/fleet`, `/tools`.
- Glassmorphism design system with `glass-card`, `btn-primary`, CSS custom properties.
- Sidebar navigation with real-time status indicator.
- Dynamic font (Geist) via `next/font`.

#### DevOps
- `frontend/start.ps1` + `frontend/start.bat` for one-click launch.
- Next.js 16.1.6 (Turbopack) â€” clean production build verified.
- `glama.json` manifest for Glama.ai marketplace registration.
- `.pre-commit-config.yaml` for Ruff linting gate.

---

**Legend:**
- **Added** â€” new features
- **Changed** â€” changes to existing functionality
- **Fixed** â€” bug fixes
- **Removed** â€” removed features
- **Security** â€” security patches

