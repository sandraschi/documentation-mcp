# QgisCraft — Assessment

**Repo:** `D:\Dev\repos\qgiscraft` · **Date:** 2026-11-05 · **Grade: A-**

## What it is

QGIS-class GIS in pure Rust: clean-room clone shell for QGIS muscle memory
(menus, docks, canvas, shortcuts) with a modern core — CLI + MCP first, no 2005
backend cruft. No QGIS code ships; black-box reference only.

## Model / verbs

- **Model:** map project (SQLite file = the project, "our `.qgz`") + layer
  (points/lines/polygons) + tile cache.
- **Verbs:** geocode (Photon live, Vienna demo offline), fenced Overpass query
  (dry-run QL or live execute), ingest hits as layers, render vectors over cached
  XYZ tiles (per-layer colors, concave fills, labels), 9 MCP tools on the same
  bus as the GUI. Track B webapp ports 11253/11254 reserved, not built.

## Architecture

Rust workspace (core/store/mcp/app/web + `xtask`), clippy `unwrap_used` +
`expect_used` denied, `fleet-start.config.ps1`, `justfile`, `AGENTS.md`,
`INSTALL.md`, `CHANGELOG.md`, `glama.json`, `llms.txt`. Zero ports on the native
track; keyless-first (Photon/Overpass/tiles). `--smoke` BMP preview
(`docs/map-preview.png`: 29 live Vienna pharmacies over OSM tiles).

## Strengths

- Best-documented craft in the fleet: **`docs/` holds 25 files** including
  `ECOSYSTEM.md`, `WRAPPEE.md`, `plugins.md` — the wrappee-capability pattern done right.
- Honest layering: clone shell up front, clean-room core underneath, Track B
  explicitly reserved-not-built.
- Offline demo path (Vienna demo) + dry-run QL = CI-friendly without keys.
- `xtask` + depot + `qgiscraft.db` show real project-file thinking.

## Gaps / risks

- QGIS parity is enormous; the dossier honesty ("muscle memory shell") must hold —
  resist feature-creep toward full QGIS.
- Tile-cache licensing/attribution (OSM contributors) needs to stay visible in every artifact.
- Live Overpass/Photon in CI needs skip-with-receipt (`down`, not fake green).
- Web track (11253/11254) unbuilt — fine, keep reserved until native track has recipes.

## Next 3 steps

1. Three democraft recipes: `qgis/geocode-layer`, `qgis/overpass-fenced`,
   `qgis/render-preview` (all with `--smoke`-style artifacts + `down` receipts).
2. Write the qgiscraft↔travelcraft boundary paragraph (analyze layers vs consume places).
3. Pin live-service versions/rate limits in `docs/` (Photon/Overpass drift).

## Verdict

The documentation exemplar for the whole craft fleet alongside bookcraft. A-
because recipes and the travelcraft boundary are still unwritten — the code and
docs already prove the pattern.
