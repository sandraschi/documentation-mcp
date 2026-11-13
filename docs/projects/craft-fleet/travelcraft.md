# TravelCraft — Assessment

**Repo:** `D:\Dev\repos\travelcraft` · **Date:** 2026-11-09 · **Grade: B+** · **Origin:** fleet-owned

## What it is

ArtCraft-tier chrono-cartography studio and local-first Baedeker travel-guide platform in pure Rust (`v0.2.0 (alpha)`, `6,771 LOC`, `27 tests`, 4 crates, 13 MCP tools). Combines curated historical/modern Baedeker regional guides, durable SQLite trip/bookmark/itinerary storage, sensory routing, and live OpenStreetMap Overpass POI discovery (`travel_nearby`).

## Model / verbs

- **Model:** place / POI + historical Baedeker layer + durable SQLite trip itinerary & bookmarks + live Overpass nearby query.
- **13 MCP tools / CLI verbs (`v0.2.0`):**
  - Guide & cartography: `travel_status`, `travel_search`, `travel_place`, `travel_regions`, `travel_epochs`, `travel_route`, `travel_pack`
  - Durable SQLite user state (`v0.2.0`): `travel_bookmark_add`, `travel_bookmark_list`, `travel_bookmark_remove`, `travel_trip_create`, `travel_trip_list`, `travel_trip_add_stop`
  - Live POI discovery (`v0.2.0`): `travel_nearby` (live OSM Overpass API query around lat/lon + radius with graceful offline receipt).

## Architecture

4-crate Pure-Rust ArtCraft 3-tier workspace (`travelcraft-baedeker`, `travelcraft-core`, `travelcraft-mcp`, `travelcraft-app`), `6,771 LOC`, `27 tests`, `clippy -D warnings` clean. Includes `CHANGELOG.md`, `HANDOVER.md`, `INSTALL.md`, and `docs/`.

## Strengths

- Shipped `v0.2.0` on 2026-11-08: replaced ephemeral in-memory state with durable SQLite storage (`bookmarks`, `trips`, `trip_stops`) and expanded to 13 MCP tools and 27 passing tests.
- Live OSM Overpass integration (`travel_nearby`) enriches curated Baedeker entries with real-world nearby amenities while preserving offline-first operation.

## Gaps / risks

- Keep the boundary with `giscraft` explicit: `travelcraft` owns human-scale itineraries, historical Baedeker guides, and POI discovery; `giscraft` owns multi-layer GIS geoprocessing and cartographic projections.

## Next 3 steps

1. Wire 3 `democraft` recipes (`travel/baedeker-search`, `travel/sqlite-trip-roundtrip`, `travel/nearby-overpass`).
2. Add GPX/GeoJSON itinerary export so `travelcraft` trips open directly as a layer in `giscraft`.
3. Expand regional Baedeker packs (Vienna 1900 / Tokyo / Kyoto fixtures).

## Verdict

Grade B+: with `v0.2.0`, 6,771 LOC, 27 tests, durable SQLite trip/bookmark persistence, and live Overpass POI queries, `travelcraft` has graduated from C+ scaffold to a rich B+ studio.
