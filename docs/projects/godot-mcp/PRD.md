# godot-mcp — PRD (fleet index)

**Canonical PRD:** [`godot-mcp/docs/PRD.md`](file:///D:/Dev/repos/godot-mcp/docs/PRD.md) in the upstream repo.

**Version:** 0.2.1 (2026-05-22)

## Summary

- **Problem:** Agents need programmatic control of Godot for visualization, game prototypes, HTML5 export, and **itch.io shipping** without manual editor work.
- **Solution:** Python FastMCP gateway + GDScript TCP bridge (`9080`) + 14 Godot tools + 6 Butler/itch tools + `/ship` dashboard.
- **Users:** Fleet CAD/CFD pipelines, blender-mcp asset import, hobby “little game” shipping, Cursor/Claude MCP clients.

## Key requirements

1. Lazy bridge connect; server usable before Godot starts.
2. Documented two-step start: `just serve` + `just godot-bridge` (bridge not required for itch ship).
3. Sample games via `just demo-run` with first-run asset import.
4. Export + Butler push: `just ship`, MCP `ship_to_itch`, REST `/api/v1/itch/*`, dashboard `/ship`.
5. Secrets via env only (`BUTLER_API_KEY`, never persisted in UI).

## Status

| Area | State |
|------|-------|
| MCP Godot tools (14) | Implemented |
| MCP itch tools (6) | Implemented |
| TCP bridge | Working (verified `bridge-test`) |
| Webapp | Dashboard incl. `/ship`, workflows, settings |
| Sample demos + export | Cloned; `little-game-export` + Butler ship |
| CI integration test with live Godot | Planned |

See [README](./README.md) for ports and commands · [LITTLE_GAME_GUIDE](./LITTLE_GAME_GUIDE.md) · [AI_AND_INDIE_GAMES](./AI_AND_INDIE_GAMES.md) · repo `docs/ship-to-itch.md`.
