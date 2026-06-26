# KiCad MCP — Product Requirements Document

**Author:** Claude, May 2026  
**Status:** Living document  
**Version:** 0.3.0

## Vision

KiCad MCP bridges the gap between LLM-driven software agents and
electronic hardware design. It turns KiCad into a programmable PCB
design engine that AI tools can inspect, modify, and export — with
no human clicking through the GUI.

## Target Users

1. **LLM agents (primary)** — Claude, Gemini, GPT, etc. call MCP tools to
   load boards, inspect designs, run DRC/ERC, export manufacturing files
2. **Hardware engineers** — use the webapp dashboard for quick board
   inspection and export without launching the full KiCad GUI
3. **CI/CD pipelines** — automated DRC checks on pull requests,
   nightly Gerber generation, pick-and-place file export
4. **EDA automation workflows** — cross-tool pipelines with freecad-mcp
   (enclosure from STEP), qcad-mcp (panelization), godot-mcp (3D viz)

## Core Requirements

### 1. Read & Inspect (✅ Complete)
- Load .kicad_pcb and .kicad_sch files
- Extract board metadata (layers, dimensions, counts)
- List components, nets, tracks with full detail
- Run DRC (Design Rule Check) and ERC (Electrical Rules Check)
- List/search libraries for footprints and symbols

### 2. Manufacturing Export (✅ Complete)
- Gerber + drill files for PCB fabrication
- STEP 3D model for enclosure design
- Pick-and-place (CSV) for assembly
- DXF, SVG, PDF for documentation
- VRML, GLB for 3D visualization
- IPC-2581, ODB++ for industry-standard fabrication
- Schematic PDF, SVG, DXF

### 3. PCB Board Editing (✅ Basic)
- Place components from libraries
- Add track segments
- Add through vias
- Save board to file
- Set board outline polygon

### 4. Marketplace (✅ Complete)
- Search GitHub for KiCad projects
- Search Kitspace and SnapEDA
- Download repos and component data
- Find missing footprints/symbols

### 5. BOM Generation (✅ Complete)
- Generate CSV and JSON BOMs
- Group by value or footprint
- Quantities per unique component

## Future Requirements (Not Yet Implemented)

### P1 — IPC API Integration (partial ✅ v0.3.0)
Headless PCB CRUD via kicad-python + KiCad 11 nightly `api-server` is **implemented**
for load/info/list/track/via/save. Remaining: `pcb_place_component` via IPC library API;
retire TCP bridge as default once 11.0 stable ships.

### P2 — Schematic CRUD
KiCad has no eeschema Python API. Implement schematic editing via
S-expression file parsing (.kicad_sch is plain text XML-like format).

### P3 — Interactive Routing
Wire the IPC API's push-and-shove router for AI-driven autorouting.

### P4 — Zone Operations
Create, edit, and fill copper zones/pours via IPC API.

### P5 — Webapp PCB Editor
Browser-based footprint placement using the 3D GLB view as a canvas.

## Non-Goals
- Replace the KiCad GUI for interactive design
- Build a schematic editor (no eeschema API exists)
- Real-time collaborative editing
- Signal integrity simulation
- Thermal analysis

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| MCP tools | 50+ | 39 |
| kicad-cli coverage | 100% of useful commands | ~75% |
| Bridge CRUD operations | 10+ | 5 |
| Playwright e2e tests | 15+ | 12 |
| Webapp pages | 10+ | 9 |
| CI pipeline time | <5 min | N/A |

## Competition

| Tool | Approach | Strengths | Weaknesses |
|------|----------|-----------|------------|
| **kicad-mcp** | MCP server over KiCad | Full CRUD, hybrid IPC+stable, rich export, dual transport, free | Nightly needed for headless CRUD; no schematic API |
| **kicad-python (IPC)** | Direct Python lib | Headless, modern API | No MCP, no webapp, no export wrappers |
| **kicad-cli scripts** | Shell scripting | Zero deps, always works | No CRUD, no webapp, no LLM integration |

KiCad MCP is unique in combining all three: MCP protocol for LLMs,
REST API for webapps, and full kicad-cli + pcbnew backend.

## Release Criteria for v1.0

- [x] IPC API integration — basic headless CRUD (v0.3.0)
- [ ] 50+ total tools
- [ ] Schematic CRUD via S-expression parsing
- [ ] All Playwright tests passing in CI
- [ ] Tauri native app built and installable
- [ ] Cross-tool pipeline demonstrated (kicad-mcp → freecad-mcp)
