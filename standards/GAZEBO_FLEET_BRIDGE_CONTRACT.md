---
title: "Gazebo Fleet Bridge Contract — sim/hardware/VR/CAD sync schema"
category: standard
status: draft
audience: mcp-dev
last_updated: 2026-09-21
---

# Gazebo Fleet Bridge Contract

> **2026-10-23 — relay retired.** `ag-gazebo-bridge` (this doc's "outbound relay")
> was deleted: an unpushed local fork whose receiving endpoints never existed on
> any target (verified: no repo serves `POST /api/v1/gazebo/*`). Its two genuinely
> useful CLI tools (`topic_list`, `service_call`) were ported into `gazebo-mcp`
> (now 17 tools); cross-repo health/starts live in gazebo-mcp's Dashboard mesh
> panel (`/api/mesh/*`). The payload shapes below remain the reference IF the
> mesh receivers are ever implemented — nothing below is live today.

**Status**: DRAFT — defines the payload contract for the Gazebo simulation mesh (gazebo-mcp, unity3d-mcp, resonite-mcp, yahboom-mcp, freecad-mcp). Implement against this doc rather than inventing per-repo shapes; that drift is what broke the mesh the first time (see `troubleshooting/BUGS_DEPOT.md` — unity3d-mcp's `fleet_pipeline.py` expected a `gazebo_export`/`export_model` tool gazebo-mcp never had).

## Why this exists

`ag-gazebo-bridge` relays Gazebo simulation state outward to five other fleet repos via REST. As of 2026-09-21, only `unity3d-mcp` implements a receiving endpoint, and even that one expects a tool name that doesn't exist on the sending side. This doc is the single source of truth both sides must agree on before either implements anything.

## Repos in scope

| Repo | Role | Owns state for |
|------|------|-----------------|
| `gazebo-mcp` | Simulation owner | Worlds, jobs, physics stepping, model poses/joint states |
| `ag-gazebo-bridge` | Outbound relay | Nothing — pure pass-through from gazebo-mcp to targets |
| `unity3d-mcp` | Visualization target | Rendered scene only (read-only mirror of sim) |
| `resonite-mcp` | VR target | VR session state; user-driven transform edits (source of push-back) |
| `yahboom-mcp` | Hardware target | Physical robot telemetry (source of push-back) |
| `freecad-mcp` | CAD target | Exported/edited CAD files (manual round-trip, not automated push-back) |

## Direction 1 — sim → target (`POST /api/v1/gazebo/import`)

Sent by `ag-gazebo-bridge`'s `sync_to_unity` / `sync_to_resonite` / `sync_to_yahboom` tools. Every receiving repo (`unity3d-mcp`, `resonite-mcp`, `yahboom-mcp`) MUST implement this exact path and shape.

**Request body:**

```json
{
  "schema_version": "1.0",
  "source": "gazebo-mcp",
  "world": "warehouse",
  "timestamp": "2026-09-21T14:32:00Z",
  "models": [
    {
      "name": "scout",
      "model_type": "sdf",
      "pose": { "position": [0.0, 0.0, 0.0], "orientation_quat": [0, 0, 0, 1] },
      "geometry_uri": "file:///worlds/warehouse/models/scout/model.sdf",
      "joint_states": { "wheel_fl": 0.0, "wheel_fr": 0.0 }
    }
  ]
}
```

- `pose.position` is `[x, y, z]` in meters, Gazebo's own ENU-derived world frame — no coordinate conversion happens at the bridge. Each target (Unity is Y-up left-handed, Resonite is Y-up left-handed) is responsible for converting from Gazebo's Z-up right-handed frame on its own receiving side. State this conversion explicitly in each target repo's handler; do not silently assume frames match.
- `geometry_uri` may be `file://` (same machine) or omitted if the target already caches the model by name from a prior sync.
- Response: `{"success": true, "imported": ["scout"], "errors": []}` on partial success — a rejected model goes in `errors`, not a thrown exception, so one bad model doesn't fail the whole batch.

## Direction 2 — target → sim, state push-back (`POST /api/v1/fleet/state`)

**New. Does not exist yet.** Owned by `gazebo-mcp` directly (not `ag-gazebo-bridge` — the bridge stays a pure relay; state ownership belongs with the simulation owner). Lets `yahboom-mcp` and `resonite-mcp` correct the digital twin from real-world/VR-side truth.

**Request body:**

```json
{
  "schema_version": "1.0",
  "source": "yahboom-mcp",
  "model": "scout",
  "timestamp": "2026-09-21T14:32:05Z",
  "pose": { "position": [1.2, 0.4, 0.0], "orientation_quat": [0, 0, 0.1, 0.99] },
  "sensor_readings": { "imu_accel": [0.0, 0.0, 9.81], "battery_v": 11.8 }
}
```

- `gazebo-mcp` applies this as a corrective `set_pose` against the matching model in the running world — it does NOT step physics on receipt; the next simulation tick reconciles from there.
- `resonite-mcp` push-back uses the same shape with `sensor_readings` omitted (VR has no sensors — it has user-driven transform edits instead, so send updated `pose` only).
- `freecad-mcp` deliberately has no push-back path — CAD edits are a manual export/import cycle by design (see main analysis: automated round-trip isn't a real use case here, don't build one just for symmetry).

## Health contract (already partially followed)

Every target already exposes `/health` or `/api/health` per `WEBAPP_PORTS.md` conventions — `fleet_status`/`fleet_status_app` in `ag-gazebo-bridge` rely on this. No change needed here; noted for completeness since `/api/v1/gazebo/import` and `/api/v1/fleet/state` should live alongside it under the same auth/CORS posture.

## Implementation order

1. `ag-gazebo-bridge` — fix its own branding/port bugs first (done 2026-09-21, see `CHANGELOG.md`).
2. `gazebo-mcp` — add `POST /api/v1/fleet/state` receiving handler.
3. `unity3d-mcp` — fix `fleet_pipeline.py`'s tool-name mismatch against this contract's `import` shape (no push-back needed — Unity is display-only).
4. `yahboom-mcp` — add `/api/v1/gazebo/import` receiver + a telemetry push loop calling `gazebo-mcp`'s new `/api/v1/fleet/state`.
5. `resonite-mcp` — same as Yahboom, VR-transform push-back instead of telemetry.
6. `freecad-mcp` — add `/api/v1/gazebo/import`/`export` receivers only; no push-back per above.

Each step is its own repo, its own commit, its own test — do not attempt this as one fleet-wide sweep (see `BATCH_MUTATION_SAFETY` in the global agent rules).
