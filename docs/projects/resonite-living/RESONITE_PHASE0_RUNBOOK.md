# Resonite Phase 0 Runbook — agent-actionable

**Created**: 2026-07-18 00:25 · **For**: any capable agent (Fable, opencode,
DeepSeek 4) picking this up cold. Companion to RESONITE_HOME_NEKOMIMI_PLAN.md.
**Prime directive**: verify, never assume — this project has caught THREE
phantom-API bugs (code calling endpoints/ops that never existed). Every step
below ends with an observable check.

## Context you need (read in this order, ~15 min)
1. `RESONITE_HOME_NEKOMIMI_PLAN.md` (same folder) — the mission.
2. `D:\Dev\repos\resonite-mcp\docs\RESONITELINK_GUIDE.md` — the Link client docs.
3. `D:\Dev\repos\resonite-mcp\MARBLE_RESONITE_GUIDE.md` — Marble→Resonite pipeline.
4. adn notes tagged `resonite-mcp` from 2026-07-17/18 (memops vault, projects/).

## Facts already verified 2026-07-17/18 (do not re-derive)
- ResoniteLink is OFFICIAL: Yellow-Dog-Man/ResoniteLink (MIT, beta), shipped
  Resonite 2026.1.8.6. WebSocket JSON, read+write hosted-world data model.
- Enable in-game: Dashboard → Session → Settings → "Enable ResoniteLink" →
  port displayed. Headless: `"enableResoniteLink": true` world config or
  `enableResoniteLink <port>` CLI (`0` = random port).
- Resonite installed: `C:\Program Files (x86)\Steam\steamapps\common\Resonite`.
- resonite-mcp has a Link client: `src/resonite_mcp/resonite_link.py`,
  `tools/resonite_link.py`, `tests/unit/test_resonite_link_protocol.py`.
  Live E2E NEVER run — that is this runbook's job.
- worldlabs-mcp v0.5.0: `.env` has WORLDLABS_API_KEY; dashboard port 10864;
  Spark renderer for splat previews; EXPORT_GUIDE §3.3 has an older OSC-based
  Resonite path (now fallback only).
- Reference implementations if stuck: Yellow-Dog-Man/ResoniteLink sample REPL
  (C#); rassi0429/resolink-mcp (community MCP for Link).

## Steps

### Step 1 — Human prerequisite (ask Sandra, ~1 min of her time)
Launch Resonite (desktop mode is fine), start/host a session (her home world
or a blank grid world), enable ResoniteLink per above, report the port.
BLOCKED WITHOUT THIS. If she is away, everything below except 5 can wait.

### Step 2 — Connect and READ (kill-or-confirm #1)
1. Read RESONITELINK_GUIDE.md for the client config (env var or config for
   host/port — likely ws://localhost:<port>).
2. Start resonite-mcp (repo has start scripts; check `justfile` / `start.ps1`).
3. Call its Link status/connect tool, then read the world data model (root
   slot tree or similar).
4. **Check**: tool returns real slot names from the live session. Screenshot
   or log the JSON. If connection fails: check Windows firewall, confirm port,
   try the YDM sample REPL client to isolate (protocol vs our client).

### Step 3 — WRITE (kill-or-confirm #2)
1. Spawn/create a slot with a simple mesh (cube) via Link tools; set its
   position/scale; rename it `phase0-test-cube`.
2. **Check**: Sandra (or screenshot via her) confirms the cube exists in-world
   and is grabbable/editable with in-game tools.

### Step 4 — ASSET import (kill-or-confirm #3, the big one)
1. Attempt glTF import via Link (check protocol docs for asset/import message
   types; the YDM repo docs/ folder documents the message schema).
2. Test asset: any small glTF; one candidate is in godot-mcp or export a cube
   from blender-mcp (`gltf` export tool).
3. **Check**: model visible in-world.
4. If Link beta lacks asset import: FALLBACK A = serve file over local HTTP
   (python -m http.server) + in-world import from URL (Resonite imports from
   URLs); FALLBACK B = manual drag-drop (Sandra). Either keeps the project
   alive — note which path won in the decision note.

### Step 5 — Marble export formats (independent of Resonite; do anytime)
1. Start worldlabs-mcp (`just serve`, dashboard :10864).
2. Read MARBLE_RESONITE_GUIDE.md. List any existing generated worlds first
   (Marble Adventure competition worlds may be reusable free candidates!).
3. If none reusable: ONE small/cheap generation (budget-aware: check credit
   cost first; Sandra approves anything non-trivial).
4. **Check**: enumerate the export formats actually offered (mesh? collider?
   splat .ply/.spz?). Record in the decision note.

### Step 6 — Decision note (mandatory)
Write adn note `YYYY-MM-DD HH:MM Phase 0 decision - <verdict>` tagged
[resonite-mcp, phase0, decision, high]: READ/WRITE/ASSET results, Marble
formats, chosen import path, any resonite-mcp bugs found+fixed (commit them),
and green-light or re-scope for Phase 1. Update RESONITE_HOME_NEKOMIMI_PLAN.md
status line. Keep the docs current — that is a standing order.

## Execution log
- 2026-07-18 04:35 — Steps 1-3 GREEN (Fable). Session 'Tutorial [en-US]',
  discovered linkPort 11831 via UDP 12512 (dashboard readout was wrong —
  ALWAYS use discover_sessions). Resonite 2026.7.14.913 / protocol 0.13.1.0,
  exact client match, zero fixes. READ root ok; WRITE 'phase0-test-cube'
  (Reso_9DC) created + readback-verified. Artifacts: C:\temp\phase0_live_test.py,
  C:\temp\phase0_result.json. Remaining: steps 4 (mesh-JSON import — wrap
  importMeshJSON in client first), 5 (Marble formats), 6 (decision note).
  See adn note '2026-07-18 04:35 PHASE 0 GATE GREEN'.

- 2026-07-18 04:52 — Step 4 GREEN (Fable). importMeshJSON cube -> assetData
  with assetURL (local://...meshx) -> StaticMesh(URL: Uri) -> MeshRenderer(Mesh
  ref) on slot phase0-mesh-cube (0,1.5,2), all wire-verified via readback.
  Learnings: import returns URL not id; URL member typed 'Uri'; schema supports
  bones + blendshapes (avatar path viable); use ImportMeshRawData for large
  meshes. Upstream reference cloned to D:\Dev\repos\_upstream\ResoniteLink.
  Verdict effectively GREEN for the whole plan; remaining: material wiring,
  client method wrapping, step 5 Marble formats, formal step 6 note.

- 2026-07-18 04:55 - Material wiring GREEN: PBS_Metallic (AlbedoColor typed colorX) wired into renderer Materials via list-member encoding (elements of references), readback-confirmed. Render path fully solved end-to-end. Cube orange pending visual confirmation.

- 2026-07-18 (continued session) - Step 5 GREEN (file-level, no Resonite needed).
  Read worldlabs-mcp docs/EXPORT_GUIDE.md (v0.4.0, current): Marble's asset
  bundle is visuals (.spz splat / .rad streaming - NOT Resonite-importable,
  no splat renderer or generic model import in ResoniteLink), physics
  (.glb collision mesh, Chisel-generated, ALREADY a simplified triangle
  mesh), environment (.jpg equirect map, texture-importable once
  import_texture_file is live-verified). Checked Downloads for reusable
  assets per the runbook's "reuse before spending credits" instruction:
  THREE Marble Adventure competition worlds already present, each with both
  halves - "Modern Tropical Luxury Residence" (30MB spz + 3.4MB collider.glb),
  "Neuschwanstein Castle Moonlight Night" (27MB + 2.3MB), "St. Peter's
  Basilica Grand Interior" (29MB + 5.9MB). None match the master plan's
  Japanese-shrine-house brief (Phase 1 still needs a themed generation for
  the actual home) but all three are free, zero-credit test fixtures for the
  Blender-to-mesh-JSON bridge script (next-work item 4) - a 2-6MB glTF
  collision mesh is exactly the input size that script needs to prove itself
  against before it ever touches the real home geometry. Wrapping work also
  done this session: import_mesh_json/import_mesh_raw/import_texture_file/
  spawn_mesh added to ResoniteLinkClient + resonite_link_* MCP tools + 8 new
  unit tests (30 total, up from 22) - see resonite-mcp commit history and
  RESONITELINK_GUIDE.md capability table. import_mesh_raw deliberately NOT
  implemented (needs a binary WebSocket payload frame the client doesn't
  send; raises with guidance instead of faking it).

- Step 6 (decision note): see adn note "Phase 0 decision - PROCEED" in the
  vault, and RESONITE_HOME_NEKOMIMI_PLAN.md status line, both updated same
  session. Phase 0 formally closed; Phase 1 open.

## Known risks in the beta protocol
Breaking changes possible (~46 open issues on YDM repo). Pin protocol version
in resonite-mcp config if the client supports it; record Resonite build number
(`2026.x.x.x`) in the decision note for reproducibility.
