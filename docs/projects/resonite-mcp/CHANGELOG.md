# Changelog

All notable changes to `resonite-mcp` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.2.0] â€” 2026-02-23 â€” Webapp Expansion ðŸŒ

### Added

#### Backend (`http_server.py`)
- `GET /api/sessions` â€” Cloud API proxy to `api.resonite.com/sessions` with name/host/usercount filters
- `GET /api/sessions/{session_id}` â€” Cloud API proxy for individual session details
- `GET /rl/world/root` â€” ResoniteLink convenience shortcut to fetch root node
- `GET /rl/world/children/{slot_id}` â€” Fetch direct children of any slot by refId
- `GET /rl/world/node/{ref_id}` â€” Fetch full node details (position, scale, components)
- `GET /rl/world/vrm-files` â€” Scan `~/.avatarmcp/models/` for `.vrm` files
- `GET /rl/world/asset-files?category=` â€” Multi-category 3D asset scanner across 5 canonical dirs
- `POST /rl/world/import-vrm` â€” Delegate `importFile` message to ResoniteLink for asset injection
- `httpx` async client for outbound HTTP requests (Resonite Cloud API)

#### Frontend (`web_sota/src/`)
- **`pages/world.tsx`** â€” New World Inspector page:
  - Collapsible slot hierarchy tree (lazy-loaded children, depth-indent via Tailwind class map)
  - Inspector panel (position, scale, components for selected slot)
  - `AssetPanel` â€” multi-category injector with tab buttons (Avatars / Props / Furniture / Architecture / Misc)
  - Spawn-position XYZ inputs, target-slot display, real-time toast feedback
- **`App.tsx`** â€” `/world` route added
- **`components/layout/sidebar.tsx`** â€” World nav item with `TreePine` icon

### Fixed
- `aria-expanded` lint in `tools.tsx` and `help.tsx` (boolean â†’ string coercion)
- CSS inline-style lint in `world.tsx` (replaced `style={{ paddingLeft }}` with Tailwind depth-class table)

### Changed
- README: updated FastMCP version badge to 3.1.1+.3+, Python badge to 3.12+, added Webapp section, updated roadmap
- Canonical asset dirs documented: `~/.avatarmcp/models/` (avatars), `~/Documents/ResoniteAssets/{category}/` (props/furniture/architecture/misc)

---

## [0.1.0] â€” 2025-12-xx â€” Initial Release

### Added
- 31 MCP tools (FastMCP 3.1.1+.1+ compliant)
- Dual MCP stdio + FastAPI HTTP interface
- OSC communication (8 tools fully functional)
- Avatar control (3 tools)
- Session management (4 tools)
- ResoniteLink WebSocket client
- Plugin system scaffolding
- Inventory management scaffolding (mock responses)

