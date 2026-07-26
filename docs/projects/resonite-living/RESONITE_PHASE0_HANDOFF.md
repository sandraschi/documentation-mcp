> **OBSOLETE as a status doc (2026-07-18 19:06)** — Phase 0 is closed; current
> status lives in `RESONITE_LIVING_STATUS_20260718.md` in this folder. Kept
> here for the wire-shape cheat sheet and execution history, both still
> accurate and useful.

# Resonite Phase 0 — Status & Handoff

**Written**: 2026-07-18 05:00, end of the night session. **For**: any agent
(Fable / opencode / DeepSeek-4) or future session continuing cold.
Companions: `RESONITE_HOME_NEKOMIMI_PLAN.md` (mission),
`RESONITE_PHASE0_RUNBOOK.md` (procedure + execution log).

## STATUS: Phase 0 effectively GREEN

| Check | Result | Evidence |
|---|---|---|
| Session discovery (UDP 12512) | GREEN | 'Tutorial [en-US]', linkPort 11831 (dashboard readout was wrong — always discover) |
| Connect | GREEN | Resonite **2026.7.14.913**, protocol **0.13.1.0**, exact client match, zero fixes |
| READ data model | GREEN | Root slot + components via `getSlot` |
| WRITE | GREEN | slot `phase0-test-cube` (Reso_9DC), readback-verified |
| Mesh import | GREEN | `importMeshJSON` cube → `assetData.assetURL` (local://….meshx) |
| Render wiring | GREEN | StaticMesh(URL:Uri) Reso_9F0 → MeshRenderer Reso_9F1 on slot `phase0-mesh-cube` (0,1.5,2) |
| Material | GREEN | PBS_Metallic Reso_A00, AlbedoColor typed **colorX**, wired via list-member encoding, readback-confirmed |
| Marble export formats | **OPEN** (step 5) | worldlabs key verified; check formats, reuse Marble Adventure worlds first |
| Formal decision note | **OPEN** (step 6) | verdict clear: proceed on ResoniteLink |

Visual confirmation (orange cube) pending Sandra's 5 AM eyes — non-blocking;
every step was protocol-readback-verified.

**Impermanence warning**: the test objects live in the *Tutorial* session and
vanish when it closes (likely not saveable). Irrelevant — the scripts recreate
everything in seconds; that is the entire point.

## Wire-shape cheat sheet (tonight's hard-won gold)

```jsonc
// Mesh import (returns assetData with assetURL, NOT an entity id!)
{"$type": "importMeshJSON",
 "vertices": [{"position": {"x":0,"y":0,"z":0}}],          // + optional normal/tangent/color/uvs/boneWeights
 "submeshes": [{"$type": "triangles",
   "triangles": [{"vertex0Index":0,"vertex1Index":1,"vertex2Index":2}]}]}
// also: "$type": "points" | "trianglesFlat"; bones + blendshapes supported (avatar path!)
// big meshes: use importMeshRawData instead (efficiency, per upstream docstring)

// Render chain (components on a slot)
addComponent StaticMesh    members {"URL": {"$type":"Uri","value": assetURL}}
addComponent MeshRenderer  members {"Mesh": {"$type":"reference","targetId": staticMeshId}}
addComponent PBS_Metallic  members {"AlbedoColor": {"$type":"colorX","value":{"r":1,"g":0.45,"b":0.05,"a":1}}}
updateComponent MeshRenderer {"Materials":
  {"$type":"list","elements":[{"$type":"reference","targetId": materialId}]}}
```

Client: `resonite_mcp.resonite_link.ResoniteLinkClient` (raw `_send` used for
imports — wrapping is the next task). Helpers: `rl_value`, `rl_ref`.
Upstream reference (schemas, all message types): `D:\Dev\repos\_upstream\ResoniteLink`.
Test scripts (rerunnable): `C:\temp\phase0_live_test.py`, `phase0_mesh_test.py`,
`phase0_mesh_render.py`, `phase0_material.py` (+ result JSONs alongside).

## Next work items, in priority order

1. **Wrap the asset path into resonite-mcp** (~half day, no Resonite needed
   for coding, live session for the E2E):
   - `import_mesh_json(vertices, submeshes, bones?, blendshapes?) -> assetURL`
   - `import_mesh_raw(...)`, `import_texture_file(path) -> assetURL`
   - `rl_list(elements)` helper mirroring rl_value/rl_ref
   - convenience `spawn_mesh(mesh_data, position, color?) -> slot_id` doing the
     whole StaticMesh/MeshRenderer/PBS_Metallic chain
   - unit tests in the style of `test_resonite_link_protocol.py` (wire shapes
     from the cheat sheet above); update RESONITELINK_GUIDE capability table
     (⚠ Not yet wrapped → ✅) + docs/TOOLS.md.
2. **Step 5**: Marble export formats via worldlabs-mcp (`just serve`, key in
   .env, port 10864). Reuse Marble Adventure worlds before spending credits.
   Then **step 6**: formal decision note, plan status flip to Phase 1.
3. **Phase 1**: generate home candidates (plan §Phase 1; Sandra picks).
4. **Blender bridge**: blender-mcp exporter → mesh-JSON/raw-mesh converter
   (glTF → the schema above). This is the volume path for the home shell.
5. **Avatar prep spike**: VRM → mesh-JSON with bones/blendshapes (schema
   supports both) — prove on one blendshape before Phase 4.

## Session inventory (what changed tonight, where)

- **resonite-mcp** (`master`): 4a43e21 live-E2E docs, 878eb7a README restructure
  (README 572→~120 lines; docs/TOOLS|CONFIGURATION|DEVELOPMENT|TROUBLESHOOTING.md
  created). Code untouched tonight — wrapping is next.
- **mcp-central-docs** (`main`): b2827a8 master plan, b283d66 Link-first
  correction + runbook, be7a2c5/19c6a03/754251a execution log updates.
- **Upstream clone**: `D:\Dev\repos\_upstream\ResoniteLink` (shallow, reference only).
- **adn notes trail** (vault, projects/): 2026-07-17 23:45 plan → 2026-07-18
  00:28 + 00:30 kickoff/state → 04:35 gate green → 04:52 (+04:55 append) asset
  + material green. Plus the full 07-17 day (advanced-memory v1.10.0, scribe,
  skill factory, avatar webapp — see 19:00 END OF DAY STATUS).

## Open items elsewhere (not this project)

classroom-mcp BUG-C1..C10 (critical, untouched); fleet /health rollout;
contract-tests initiative (FOUR phantom-API instances found in 24h — classroom
LLM bridge, research-chain module paths, SkillCreator op, and resonite-mcp's
pre-1.1.0 fictional wire format as the historical fourth); learnbot manifest
sync; resonite-mcp cleanup trio (mcp-server/ duplicate tree, TROUBLESHOUTING.md
typo file, tool-inventory re-audit).
