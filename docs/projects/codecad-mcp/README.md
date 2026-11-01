# codecad-mcp — Parametric CAD via build123d

**Version:** 0.1.0 (2026-08-15) · **Status:** Active
**FastMCP 3.4.4+** · **Stack:** build123d (OCP/OCCT) · trimesh · FastAPI

Code-as-CAD: mechanical parts are Python source. The LLM writes, edits, diffs,
and version-controls parts natively — no GUI automation. STEP out for
manufacturing; STL/3MF/DXF/GLTF for downstream fleet handoff (kicad-mcp,
blender-mcp).

> ⚠️ **Heavy dependency**: `build123d` pulls the OCP/OCCT wheel (~250 MB).

## Features

- **`cad_part`** — create/edit/validate/list/get_source/delete. User source runs
  in a **dedicated `python -I` subprocess** with an AST import allowlist
  (build123d/math/numpy), jailed workdir, and a 60s timeout
- **`cad_export`** — STEP (the reason this server exists), STL (linear/angular
  deflection), 3MF, DXF (kicad outlines), GLTF (blender/godot handoff),
  technical drawing (SVG orthographic; dimensions honest NotImplementedError)
- **`cad_render`** — preview_png + multi_angle via the trimesh fallback path
- **`cad_library`** — load-bearing `primitives_help` cheatsheet +
  8 parametric standard-part generators (ISO bolts/nuts, washers, 608 bearings,
  T-slot, brackets, plates)
- **`cad_agentic_workflow`** — description → generate → compile → validate →
  error-feedback retry (max 3)
- **Depot** — SQLite metadata + versioned part files (`parts/`, gitignored)
- **Webapp** — Parts depot, Create, Export, Render, Library, Tools, Skills,
  Chat, Settings, Help, Logs

## Quick Start

```powershell
git clone https://github.com/sandraschi/codecad-mcp
cd codecad-mcp
copy .env.example .env
.\start.ps1        # backend :11082 + frontend :11083
```

See [INSTALL.md](INSTALL.md) and [docs/ONBOARDING.md](docs/ONBOARDING.md).

## Ports

| Port | Service |
|------|---------|
| **11082** | Backend (FastAPI + FastMCP HTTP `/mcp`, REST `/api/*`) |
| **11083** | Frontend (Vite React) |

## Tools

| Tool | Ops | Notes |
|------|-----|-------|
| `cad_part` | 6 | subprocess-isolated exec, version chain |
| `cad_export` | 6 | STEP primary; technical_drawing dims = NotImplementedError |
| `cad_render` | 2 | trimesh fallback (stated in response) |
| `cad_library` | 2 | cheatsheet + 8 parametric generators |
| `cad_agentic_workflow` | 1 | sampling retry loop (max 3) |
| `show_part_card` / `show_depot_card` | 2 | Prefab UI |

Full reference: [docs/TOOLS.md](docs/TOOLS.md) · Cheatsheet: [docs/BUILD123D_PATTERNS.md](docs/BUILD123D_PATTERNS.md) · Skill: `skill://codecad-expert`

## Environment

See `.env.example`: `CODECAD_BACKEND_PORT`/`CODECAD_FRONTEND_PORT`,
`CODECAD_EXEC_TIMEOUT_SECONDS` (60), `CODECAD_PARTS_DIR`/`CODECAD_EXPORTS_DIR`,
`LLM_PROVIDER`/`LLM_BASE_URL`/`LLM_MODEL` (Ollama local-first).

## Development

```powershell
just test      # pytest (incl. STEP round-trip acceptance)
just lint      # ruff check + format
just ci        # lint + test + webapp build
```

## Roadmap

- **Deepfang sandbox** hardening for part execution (subprocess isolation is
  sufficient for v0.1 — noted in code)
- OCP offscreen rendering (replaces the trimesh fallback)
- Dimension annotation on technical drawings
- Multi-part assemblies (blocked on build123d assembly maturity)
- STEP re-import → parametric reconstruction (import is static in v0.1)

## Links

- Brief: `mcp-central-docs/architecture/FLEET_GAP_ANALYSIS_2026-07.md` §4 (P2)
- Consumers: kicad-mcp (DXF outlines), blender-mcp (GLTF visualization)
