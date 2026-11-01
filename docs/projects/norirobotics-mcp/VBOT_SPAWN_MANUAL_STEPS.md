# Manual steps: VRChat vbot spawning (Resonite is now fixed — see below)

**Status**: VRChat only. This document originally claimed Resonite also needed manual,
GUI-driven work — **that was wrong**, caught by Sandra pointing out that a real avatar
(nekomimi-chan.vrm, converted and spawned via `resonite-mcp/scripts/spawn_nekomimi_in_home.py`)
had already been spawned live into her Resonite Home. The earlier research only checked the
dead OSC `vbot_osc_receiver.py` path and missed the actual working mechanism: **ResoniteLink**,
resonite-mcp's real WebSocket protocol client (`resonite_mcp/resonite_link.py`,
target protocol 0.13.1), already exposed as MCP tools (`resonite_link_discover` /
`resonite_link_connect` / `resonite_link_spawn_mesh` / `resonite_link_destroy_slot`, etc.) in
`resonite_mcp/tools/resonite_link.py`. `robotics-mcp` now mounts resonite-mcp in-process
(mirroring the Unity mount) and calls this real API — see "What's already done" below.
VRChat remains genuinely not code-fixable, for the reasons kept below.

**Context**: this surfaced while integrating the Nori A3 (`norirobotics-mcp`) as the fleet's
third physical robot. The A3 itself has no real 3D model/mesh yet — any vbot representation on
either platform will be a generic placeholder (a labeled box/capsule, not a faithful A3 model)
until real CAD/mesh assets exist.

---

## VRChat

**Why this can't be a code fix**: VRChat's OSC protocol can only drive Animator float/int/bool
parameters on **the local user's own already-uploaded avatar** — it has no instantiate/spawn
primitive at all, for any object, ever. `robot_virtual.py` currently sends OSC to
`/avatar/parameters/SpawnRobot`, which only does something if an avatar with that exact
parameter name — wired to real spawn behavior — already exists. None does.

**What it would take**:

1. **Build a VRChat world** (not an avatar) in Unity with the VRChat Creator Companion + VRChat
   SDK3 (Worlds) installed. A world is the right target, not an avatar, because you want to
   spawn an object other people can see, not just animate your own character.
2. Add a **UdonSharp** script implementing an object pool: a fixed number of pre-placed
   "Nori A3 placeholder" prefabs (simple primitives, e.g. capsules with a text label), toggled
   active/positioned via a network-synced Udon behavior.
3. Wire that Udon behavior to **OSC-driven trigger parameters** — i.e. give your own avatar a
   parameter (e.g. `SpawnRobot`, matching what `robot_virtual.py` already sends) that, via an
   Udon `VRCPlayerApi`/parameter-sync listener in the world, calls the spawn function when
   toggled. This is the actual missing link — OSC → avatar parameter → world-side Udon listener.
4. **Upload the world** through the VRChat SDK Control Panel in Unity (Build & Publish). This
   requires your own VRChat account credentials in the SDK panel — an agent cannot do this step;
   it's an explicit account/GUI action.
5. Update `NORI_MCP_URL`... n/a here — this step has no norirobotics-mcp dependency; it's purely
   VRChat-side. Once the world is live, `robot_virtual(operation="spawn", robot_type="nori_a3",
   platform="vrchat")` should reach it via the existing OSC send path in `robot_virtual.py` /
   `vbot_crud.py` — no further code change needed on the robotics-mcp side.

**Reference**: VRChat Creator Companion (creators.vrchat.com), UdonSharp docs
(github.com/vrchat-community/UdonSharp), VRChat OSC docs (docs.vrchat.com/docs/osc-overview).

---

## What's already done (no action needed — correcting the earlier version of this doc)

- **Resonite — fixed for real, via the actual working mechanism**: `robotics-mcp/server.py` now
  mounts `resonite_mcp.server.server` in-process (new `_load_resonite_server()` /
  `_mount_resonite_server_safely()`, mirroring the Unity mount exactly). `robot_virtual.py` and
  `vbot_crud.py`'s Resonite spawn/delete paths now call the real ResoniteLink tool chain:
  `resonite_link_discover` (UDP session discovery, port 12512) → `resonite_link_connect`
  (WebSocket) → `resonite_link_spawn_mesh` (imports a procedural placeholder box mesh — see
  `robotics_mcp/utils/mesh_primitives.py::box_mesh()` — and wires the full
  StaticMesh/MeshRenderer render chain in one call, the exact composition proven live by the
  nekomimi-chan VRM spawn). The returned `slot_id` is persisted on the robot's metadata so
  delete can call `resonite_link_destroy_slot` later. **Not yet verified against a live
  Resonite session** (none was running with ResoniteLink enabled during this pass, same as the
  Unity Editor caveat below) — `resonite_link_discover` returned zero sessions when checked.
  Move/update is intentionally left as "not yet implemented — respawn to move" rather than
  half-wiring an unverified Transform-field write.
- **Unity**: fixed for real — `unity3d-mcp`'s `MCPBridge.cs` `CreateObject`/`TransformObject`
  now apply position/rotation/scale and support `Capsule`/`Sphere`/`Box` primitives;
  `robotics-mcp`'s `robot_virtual.py` and `vbot_crud.py` now call the real `unity_bridge`
  tool instead of the fictional `execute_unity_method`/`VbotSpawner` path. This still needs a
  live Unity Editor with the updated `MCPBridge.cs` copied in to verify end-to-end (no Editor
  was running during this pass) — see `robotics-mcp` CHANGELOG for details.
- Along the way, fixed a real bug that would have silently broken *both* of the above even with
  correct wiring: `call_mounted_server_tool` returns a `CallToolResult` object, not a plain
  dict — code calling `.get()` directly on it would raise `AttributeError`. Also normalized
  `MCPBridge.cs`'s non-standard `"status": "created"`/`"status": "deleted"` returns to the CRUD
  layer's `"status": "success"` convention it actually checks for.
