# Graphs in Pure Rust (Charts + Graph Structures)

"Graphs" means two things; this doc covers both with one crate each.

## Charts

| Crate (version) | Use when |
|---|---|
| `egui_plot` 0.37 (verified 2026-10-17) | Plotting **inside** an egui app — version tracks egui 1:1 (0.37 ↔ egui 0.37). Multi-series, legends, box-zoom, log scales. First choice for dashboard telemetry pages. |
| `plotters` 0.3.7 (verified 2026-10-17) | Plotting to **files** (PNG/SVG) or WASM — reports, digests, README charts, headless CI artifacts. No egui needed. |
| Hand-rolled `ui.painter()` | Sparklines/bars under ~50 lines (proven in rust-devices-mcp: power history + 24h temperature). Zero new crates, instant compile — prefer this until the chart needs axes/legends/zoom, then graduate to `egui_plot`. |

Ladder: painter sparkline → `egui_plot` → (full engine needs `bevy`, never
for charts). Do not add `egui_plot` for a single sparkline.

## Graph structures

`petgraph` 0.8.3 (verified 2026-10-17): the graph data-structure library —
directed/undirected graphs, Dijkstra, topo sort, SCC, serialization hooks.
Fleet fits: dependency graphs, device topologies, citation lineage,
knowledge-graph indices, mesh5727058 routing. Stable 0.x, generous docs.
Pair with `egui` custom node rendering for visual graph editors (or
`egui_plot` for metric overlays, not topology).
