# Tools Reference

All tools are portmanteaus: `{success, message, ...}` returns, `error_type`
on failure. The cheatsheet is `docs/BUILD123D_PATTERNS.md`.

## cad_part — part CRUD

| Op | Inputs | Output |
|----|--------|--------|
| `create` | source, name?, density? | part record (id, volume, watertight, mass) |
| `edit` | part_id, source | new version (vN+1), version chain kept |
| `validate` | part_id | checks: volume>0, watertight, mass |
| `list` | — | depot parts (latest 100) |
| `get_source` | part_id | current source text |
| `delete` | part_id | removed |

Execution: dedicated `python -I` subprocess, AST import allowlist
(build123d/math/numpy), jailed workdir, 60s timeout. Source MUST bind `result`.

## cad_export

| Op | Output | Notes |
|----|--------|-------|
| `step` | .step | manufacturing BREP (the reason this server exists) |
| `stl` | .stl | tolerance 0.1 mm / 0.5 deg (configurable) |
| `3mf` | .3mf | additive manufacturing |
| `dxf` | .dxf | 2D profile — kicad-mcp board outlines |
| `gltf` | .gltf | blender-mcp / godot-mcp handoff |
| `technical_drawing` | .svg | orthographic projection; dimension annotation = honest `not_implemented` |

## cad_render

| Op | Output | Notes |
|----|--------|-------|
| `preview_png` | PNG + base64 thumbnail | trimesh fallback path (stated in response) |
| `multi_angle` | front/top/right/iso grid | mirrors blender-mcp render contract |

## cad_library

| Op | Output |
|----|--------|
| `primitives_help` | the BUILD123D_PATTERNS.md cheatsheet (LOAD-BEARING — read before generating) |
| `standard_parts` | 8 generators: hex_bolt_iso4017, hex_nut_iso4032, flat_washer, bearing_608, t_slot_profile, corner_bracket, base_plate — source templates for cad_part.create |

## cad_agentic_workflow

`description` (NL) → generate source (sampling) → create → validate →
error feedback → retry (max 3). Returns part + attempts + errors.

## Prefab cards

- `show_part_card(part_id)` — mass properties + version
- `show_depot_card()` — depot listing
