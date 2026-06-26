# Fleet Game Pipeline (godot-mcp)

**Canonical:** `D:/Dev/repos/godot-mcp/docs/fleet-game-pipeline.md`

---

## Leverage makers for games

| Maker | Game use |
|-------|----------|
| **blender-mcp** | Props, characters, GLB → `godot_import_glb` |
| **worldlabs-mcp** | AI worlds — **GLB collision today**; splats via Spark/Unity |
| **freecad / qcad** | Hard-surface → STL |
| **`_exchange/`** | Handoff bus between repos |

```
makers → _exchange → godot-mcp → just ship web
```

---

## World Labs splat in Godot?

| Asset | Godot today |
|-------|-------------|
| **Chisel GLB** (mesh) | ✅ `fleet_worldlabs_import_mesh` / `godot_import_glb` |
| **SPZ / RAD splat** | ❌ Staged to `_exchange`; Spark URL returned |
| **Prompt → game (`build_game`)** | 🟡 Phase 1 MCP tools; E2E blocked on staging/id mapping |

**Now (v0.2.1 fleet + v0.3.0 game_builder Phase 1):** Fleet mesh path is production-ready for manual/Just use. Game Builder orchestrates LLM + worldlabs but does not yet reliably import worlds into Godot without manual fleet steps.

Assessment: [FLEET_ASSESSMENT.md](FLEET_ASSESSMENT.md) · Full pipeline: **`godot-mcp/docs/fleet-game-pipeline.md`**
