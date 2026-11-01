# Changelog

## [Unreleased] — 2026-08-15

### Added
- **Initial release (P2 gap-analysis build)** — `codecad-mcp` v0.1.0
  - `cad_part` (6 ops): create/edit/validate/list/get_source/delete with
    subprocess-isolated execution (`python -I`, AST import allowlist,
    jailed workdir, 60s timeout), version chain, watertight + volume checks
  - `cad_export` (6 ops): STEP (primary), STL (deflection params), 3MF, DXF,
    GLTF, technical_drawing (SVG orthographic; dimension annotations honest
    `not_implemented`)
  - `cad_render` (2 ops): preview_png, multi_angle (trimesh fallback, stated)
  - `cad_library` (2 ops): load-bearing `primitives_help` cheatsheet +
    8 parametric generators (ISO 4017 bolt, ISO 4032 nut, washers, 608
    bearing, T-slot, corner bracket, base plate)
  - `cad_agentic_workflow`: sampling retry loop (max 3) with error feedback
  - Prefab cards: show_part_card, show_depot_card
  - FastAPI REST + MCP streamable HTTP at /mcp; webapp catch-them-all
  - 18 pytest cases incl. STEP round-trip acceptance (bracket → STEP →
    re-import → volume within 0.1%)
