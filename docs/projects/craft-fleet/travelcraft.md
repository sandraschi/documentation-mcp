# TravelCraft — Assessment

**Repo:** `D:\Dev\repos\travelcraft` · **Date:** 2026-11-05 · **Grade: C+**

## What it is

ArtCraft-tier chrono-cartography studio and local-first travel-guide platform —
the Baedeker revival. Offline guides, sensory routing, JapanCraft/AustriaCraft
editions per the expansion matrix. Wraps country guides + chrono-cartography
concepts rather than an existing fleet MCP (greenfield studio, not a consolidation).

## Model / verbs

- **Model:** place/route/guide (Baedeker entry + map layer + itinerary).
- **Crates:** `travelcraft-baedeker`, `travelcraft-core`, `travelcraft-mcp`, `travelcraft-app`.
- **Verbs (README):** guide search/render, route planning, offline pack export (exact
  surface still forming — README feature list, no `docs/TOOLS.md` yet).

## Architecture

Pure-Rust ArtCraft 3-tier (L1 core, L2 MCP/CLI, L3 app), MIT/Apache, workspace
resolver 2. `start.ps1`/`start.bat` present. No `docs/`, no `justfile`, no `tests/`
visible at triage. Last commit 2026-11-04 (real-time search filter, fly-to,
scale bar, regional intel — app-side momentum).

## Strengths

- Clear differentiator (Baedeker 2030 + offline sensory routing) — not a clone of anything.
- Standard 4-crate shape; app crate already getting real map features.
- Zero-runtime-tax posture consistent with fleet doctrine.

## Gaps / risks

- No `docs/` (no PRD/TOOLS/PARITY), no test evidence, no clippy-gate proof at triage.
- Data story unclear: OSM/tile caching, offline pack format, guide data licensing
  (Baedeker content is the moat — where does it come from?).
- Overlap risk with `qgiscraft` (real GIS) — boundary needs one paragraph:
  travelcraft consumes places/routes, qgiscraft analyzes layers.
- `KIBITZ.md` present; treat as scratch, not spec.

## Next 3 steps

1. Add `docs/PRD.md` (model + verbs + qgiscraft boundary) and `docs/TOOLS.md`.
2. `just ci` equivalent: fmt + clippy-deny + 3 headless tests (guide render → artifact).
3. One democraft recipe: `travel/guide-pack` (fixture places → offline pack + report).

## Verdict

Promising greenfield studio with real app momentum, but still a scaffold:
no docs, no tests, no recipes. Keep grade C+ until the PRD and one green recipe land.
