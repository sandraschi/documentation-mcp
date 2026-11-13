# GisCraft (formerly QgisCraft) — Assessment

**Repo:** `D:\Dev\repos\giscraft` · **Date:** 2026-11-09 · **Grade: A-** · **Origin:** fleet-owned

> Renamed from `qgiscraft` (`D:\Dev\repos\qgiscraft`) to `giscraft` (`D:\Dev\repos\giscraft`) on 2026-11-08 to avoid trademark friction while keeping the QGIS muscle-memory UX shell.

## What it is

QGIS-class desktop & headless GIS in pure Rust (`v0.2.1 (alpha)`, `13,460 LOC`, `142 tests`, 5 crates + `xtask`): clean-room spatial core with SQLite project files (`giscraft.db`), live Photon geocoding (`Ctrl+G` Go-To-Place), fenced Overpass QL queries, GeoJSON/Shapefile/CSV/GPX layer ingestion, and XYZ raster tile compositing. Track B web ports `11253` (backend) / `11254` (frontend) assigned.

## Model / verbs

- **Model:** map project (SQLite `.db` project file) + vector/raster layers (points/lines/polygons + attributes + CRS) + XYZ tile cache.
- **Verbs (CLI + stdio MCP + L3 GUI):**
  - Geocoding & search: `geocode` (Photon live + offline Vienna demo), `Ctrl+G` Go-To-Place modal in L3 app (`v0.2.1`)
  - Overpass & ingestion: fenced Overpass query (`dry-run` QL or live execute), ingest hits as layers, GeoJSON/GPX/CSV import/export
  - Spatial ops & rendering: bbox clip, buffer, distance/area measurement, render vectors over cached XYZ tiles (`--smoke` BMP preview), 9+ MCP tools on the shared dispatch bus.

## Architecture

5-crate Pure-Rust workspace (`giscraft-core`, `giscraft-store`, `giscraft-mcp`, `giscraft-app`, `giscraft-web` + `xtask`), `13,460 LOC`, `142 tests`, clippy `unwrap_used` + `expect_used` denied. `docs/` holds **26 files** including `PLAN-power-gis.md` (roadmap to full power-GIS spatial joins, projections, and styling), `ECOSYSTEM.md`, `WRAPPEE.md`, and `plugins.md`.

## Strengths

- Best-documented craft in the fleet (`26` markdown files in `docs/`) and second-highest test count (`142` tests, behind only `gamecraft`).
- Rename from `qgiscraft` to `giscraft` (`v0.2.1`) is complete across crates, binary (`giscraft.exe`), launcher (`starts/giscraft-start.bat`), and GitHub (`sandraschi/giscraft`).
- Offline Vienna fixture + dry-run Overpass QL keeps tests deterministic and keyless.

## Gaps / risks

- Power-GIS vector geoprocessing (polygon union/intersection/dissolve, CRS reprojection beyond WGS84/WebMercator) is designed in `docs/PLAN-power-gis.md` and represents the next implementation wave.
- Boundary with `travelcraft` (which added live Overpass `travel_nearby` in `v0.2.0`) should remain clear: `giscraft` is for multi-layer spatial analysis and cartography; `travelcraft` is for Baedeker itineraries, trips, and sensory routing.

## Next 3 steps

1. Execute Phase 1 of `docs/PLAN-power-gis.md` (polygon spatial operations + attribute table filter/expression engine).
2. Wire 3 `democraft` recipes (`gis/geocode-layer`, `gis/overpass-fenced`, `gis/render-preview`).
3. Keep OSM contributor attribution visible in all exported map artifacts.

## Verdict

Grade A-: 13,460 LOC, 142 passing tests, 26 docs files, clean `giscraft` rename (`v0.2.1`), and `Ctrl+G` Go-To-Place shipped.
