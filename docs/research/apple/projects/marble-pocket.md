# Marble Pocket

**Model:** Free + IAP environment packs  
**Comps:** 3D wallpaper / “world viewer” apps

## Product

Import and view **GLB environments** (World Labs Marble exports, blender-mcp handoffs). Orbit camera, screenshot, optional AR Quick Look export. Sell curated environment packs (city block, studio, outdoor).

## Fleet reuse

| Piece | Source |
|-------|--------|
| GLB assets | worldlabs-mcp, blender-mcp → `_exchange/` |
| Pipeline doc | [godot-mcp FLEET_GAME_PIPELINE](../../projects/godot-mcp/FLEET_GAME_PIPELINE.md) (mesh path, not Godot runtime) |
| Dark App Factory #19 | Marble env viewer |

## Monetization

| SKU | Content |
|-----|---------|
| Free | 1 bundled GLB |
| IAP packs | 5 worlds each, themed |
| Optional sub | “New world monthly” |

Creative IAP mirrors VRMDance but **static 3D** — simpler than humanoid dance.

## AI angle

- worldlabs-mcp generates new packs on Windows; you ship baked GLB in app updates — AI is **authoring pipeline**, not in-app chat

## Effort / revenue

- **Effort:** Medium (SceneKit/RealityKit GLB load, IAP catalog)
- **Upside:** Niche aesthetic audience; cross-promote from 3D / VTuber community

## Next step

Prove GLB load + 60fps orbit on iPhone with one `_exchange` mesh before building store.
