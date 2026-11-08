# splatcraft — Dossier (draft 2026-11-04)

**Status:** Approved for creation 2026-11-04  
**Sources:** `D:\Dev\repos\worldlabs-mcp` (Marble API, Spark 2.0 streaming renderer, Godot portals) + `D:\Dev\repos\splatmaker-mcp` (Local Nerfstudio / Splatfacto + Postshot CLI on RTX 4090)  
**Target:** `D:\Dev\repos\splatcraft`  
**MCP key:** `splatcraft` — CLI `splatcraft-cli.exe` (or `uv run splatcraft`) — `splatcraft mcp --allow-path D:\Dev\repos`  
**Democraft family:** `community` (alongside `SolidCraft`). Ports: stdio first (no port required for CLI/MCP). Webapp claimed via `WEBAPP_PORTS.md` if added later.

---

## 1. Model

```python
SplatWorld = {
    "id": str,
    "name": str,
    "format": "ply" | "spz" | "rad",
    "splat_count": int,
    "sh_degree": int,
    "bbox_min": list[float],
    "bbox_max": list[float],
    "camera_path": list[dict],
    "collider_mesh": str | None,
    "provider": "marble" | "local" | "imported",
    "source_uri": str | None,
    "created_at": str,
}
```

All JSON-serializable. `run.json` must record splat count, compression ratio, bounding box, and timings. No credentials in artifacts.

---

## 2. Verb Map (Fusing WorldLabs + Splatmaker)

| splatcraft CLI | Source / Maps from | Mode / Input | Notes |
|---|---|---|---|
| `splatcraft info --file X.ply` | `worldlabs:get_world` / local header parser | PLY, SPZ, RAD file | Read-only. Fast header probe (<10ms). Always safe in CI. |
| `splatcraft convert --in X.ply --to spz --out Y.spz` | `splatmaker:export` / SPZ compressor | File conversion | Headless transformer. Measures size reduction (often 5-10x). |
| `splatcraft collider --in X.ply --out col.glb` | `splatmaker` collider sidecar | Extraction | Extracts oriented bounding box and convex collision hull for `gamecraft` / Godot. |
| `splatcraft create --prompt "..." [--provider marble]` | `worldlabs:generate_world` | Cloud API | Generates from text/image via Marble. Gated by `WORLDLABS_API_KEY`. |
| `splatcraft train --video V.mp4 [--engine nerfstudio]` | `splatmaker:train_splat` | Local RTX 4090 | Subprocess to `ns-train` / `postshot-cli`. Local zero-cost training. |
| `splatcraft render --file X.ply --camera-path P.json` | `worldlabs:render_camera_path` | Trajectory render | Generates flythrough frames / MP4 video or thumbnail PNG. |
| `splatcraft mcp [--allow-path DIR]` | FastMCP stdio server | Stdio bridge | Exposes `splat_*` tools to Antigravity / Claude / OpenCode. |

---

## 3. CLI Spec (Craft-Conformant)

```bash
splatcraft info --file scene.ply [--json]
splatcraft convert --in scene.ply --to spz --out scene.spz
splatcraft collider --in scene.ply --out collider.glb [--format box|hull]
splatcraft create --prompt "A misty redwood forest" --provider marble --out ./forest
splatcraft train --video capture.mp4 --engine nerfstudio --out ./splat.ply
splatcraft mcp [--allow-path D:\Dev\repos]
```

* `--help` functional on all commands.
* `--json` emits clean machine-readable JSON for democraft `run.json` capture.
* Roots: `--allow-path` confines file operations.
* Exit non-zero on error.

---

## 4. Democraft Recipes (3 Required)

1. **`splat/info-inspect`**  
   Runs `splatcraft info --file fixtures/cube_sample.ply --json`.  
   Asserts `splat_count > 0`, `format: "ply"`, valid `bbox_min`/`bbox_max`.  
   Generates `run.json` + inspection markdown report. 100% offline, always runs in CI.

2. **`splat/convert-spz-compression`**  
   Runs `splatcraft convert --in fixtures/cube_sample.ply --to spz --out outbox/sample.spz`.  
   Measures byte size reduction and round-trip fidelity. Emits compression ratio.

3. **`splat/collider-extract`**  
   Runs `splatcraft collider --in fixtures/cube_sample.ply --out outbox/collider.glb`.  
   Verifies generated collision hull and scene bounds for downstream consumption by `gamecraft`.

---

## 5. Ecosystem Role

* Bridges **`artcraft`** (which catalogues 3D Gaussian splats under *Worlds*) and **`gamecraft`** (which requires 3D colliders and level bounds).
* Consolidates cloud API generation (`worldlabs-mcp`) with zero-marginal-cost local 4090 reconstruction (`splatmaker-mcp`).
