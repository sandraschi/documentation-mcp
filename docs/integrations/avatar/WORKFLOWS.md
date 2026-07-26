# Avatar MCP Workflows

Operational recipes for **avatar-mcp** and the creative pipeline chain.

Central overview: [docs/avatars/FLEET_VRM_PIPELINE.md](../../docs/avatars/FLEET_VRM_PIPELINE.md)

## Workflow 1: VRoid Hub → VTube

**Goal:** Download a published Hub character and stage for VTube Studio.

**Prerequisites:** Hub OAuth app, blender-mcp optional, avatar-mcp running.

```json
{ "operation": "hub_auth", "auth_step": "start" }
```
Open `authorize_url`, complete login (callback hits `/api/v1/pipeline/hub/callback`).

```json
{
  "operation": "hub_download",
  "character_model_id": "MODEL_ID_FROM_HUB_URL",
  "vrm_filename": "my_avatar.vrm"
}
```

```json
{ "operation": "blender_validate", "vrm_filename": "my_avatar.vrm" }
```

```json
{ "operation": "stage_for_vts", "vrm_filename": "my_avatar.vrm", "label": "main_avatar" }
```

Check `model_type` in registry metadata — quadrupeds need different motion tooling.

## Workflow 2: VRoid Studio brute-force → full pipeline

**Goal:** Default anime gal from desktop VRoid without Hub.

**Prerequisites:** windows-computer-use-mcp (10789), vroidstudio-mcp (10881), blender-mcp (10849), VRoid Studio installed.

```json
{ "operation": "full_pipeline", "vrm_filename": "anime_gal.vrm", "pick_sample": true }
```

Calibrate sample model click: `VROID_SAMPLE_MODEL_X`, `VROID_SAMPLE_MODEL_Y` on vroidstudio-mcp host.

## Workflow 3: Booth purchase → registry

**Goal:** Import paid/local VRM.

```json
{
  "operation": "hub_stage_file",
  "source_path": "D:/Downloads/creature_dragon.vrm",
  "vrm_filename": "creature_dragon.vrm"
}
```

Metadata auto-written with `model_type` detection.

## Workflow 4: MMD PMX → VRM (via Blender)

**Goal:** Use legacy MMD model in VRM toolchain.

See [MMD_EXPLAINER.md](../../docs/avatars/MMD_EXPLAINER.md).

1. Import PMX in Blender (MMD tools addon).  
2. Clean materials/bones; export VRM via VRM addon.  
3. blender-mcp `script_execute` or VRM tool surface for validate.  
4. avatar-mcp `hub_stage_file` with output path.

VMD dances: retarget/bake in Blender — not yet automated in avatar-mcp.

## Workflow 5: VRM → Godot game character

**Goal:** Playable GLB in Godot — **not** live VRM in engine.

1. Complete Workflow 1 or 3 (staged VRM).  
2. blender-mcp: export GLB from same armature.  
3. godot-mcp: `godot_import_glb`.

See [GODOT_AND_AVATARS.md](../../docs/avatars/GODOT_AND_AVATARS.md).

## Workflow 6: Creature import with type override

When auto-detection is wrong:

```json
{
  "operation": "hub_download",
  "character_model_id": "MODEL_ID",
  "model_type_override": "quadruped"
}
```

## Environment variables

| Variable | Service | Purpose |
|----------|---------|---------|
| `VROID_HUB_CLIENT_ID` | avatar-mcp | Hub OAuth |
| `VROID_HUB_CLIENT_SECRET` | avatar-mcp | Hub OAuth |
| `VROID_HUB_ACCESS_TOKEN` | avatar-mcp | Skip OAuth (dev) |
| `VROIDSTUDIO_MCP_URL` | avatar-mcp | Default `http://127.0.0.1:10881` |
| `BLENDER_MCP_URL` | avatar-mcp | Default `http://127.0.0.1:10849` |
| `AVATAR_PIPELINE_WORK_DIR` | avatar-mcp | Staging root |

## Web UI

`http://127.0.0.1:10792/pipeline` — Hub connect, download, VRoid export, validate, full pipeline.

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Hub download 401 | Re-run `hub_auth` start/complete |
| VRoid export fails | windows-computer-use-mcp + VRoid window focused |
| Blender validate 0 meshes | VRM addon installed in headless Blender |
| Wrong model_type | Set `model_type_override` or edit `.meta.json` |
| Godot shows T-pose | Bake animations to GLB in Blender first |

---
*Last updated 2026-05-28*
