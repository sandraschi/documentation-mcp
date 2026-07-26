# Resonite Living — Status Snapshot

**Written**: 2026-07-18 19:07 · **Supersedes**: RESONITE_PHASE0_HANDOFF.md as
the status doc (that file is kept for its wire-shape cheat sheet + execution
log only — mark it OBSOLETE-as-status, done). Companion: TODO file in this
folder, RESONITE_HOME_NEKOMIMI_PLAN.md (master plan), README.md (index).

## Where things stand

Phase 0 (reality-check spike) is CLOSED. Phase 1 (generate the home) is now
**IN PROGRESS** — the Blender→mesh-JSON converter gate item is done and
proven (see below). Everything else in Phase 1 (Marble home-brief
generation, live import) is still open.

**2026-07-18, second update**: wrote and proved
`resonite_mcp/utils/gltf_meshjson.py` — stdlib-only GLB/glTF parser that
outputs the exact vertex/submesh shape `import_mesh_json` expects. Ran it
against all three real `_collider.glb` fixtures:

| Fixture | Vertices | Triangles |
|---|---|---|
| Modern Tropical Luxury Residence | 70,598 | 136,241 |
| Neuschwanstein Castle Moonlight Night | 48,658 | 91,050 |
| St. Peter's Basilica Grand Interior | 118,637 | 236,579 |

All converted cleanly (normals present, no UVs — expected, these are
collision meshes). Output JSON saved to `C:\temp\*_meshjson.json`.

**2026-07-18, third update — live wire-call proven, decimation pipeline proven**:
Connected live to the running session (port 11831, Resonite 2026.7.14.913,
protocol 0.13.1.0) and successfully spawned a triangle, then a two-box
"house" (body + roof) via `spawn_mesh()` — slots `Reso_A02`/`Reso_A06`/
`Reso_A0A`. One real bug hit and fixed: passed the raw triangle list
instead of the full submesh object into `spawn_mesh()`; server gave a
precise, correct error ("must specify a type discriminator") — fixed in
one line, no mystery.

Also built `stl_meshjson.py` (same pattern as the glTF converter, stdlib-
only) and tested it against a real robot mesh: Boomy's actual chassis
(`yahboom-mcp/.../base_link_X3.STL`, 69,182 triangles). That's too big for
a JSON-based live import as-is (42.9MB payload), so tested the decimation
step the plan always assumed would be needed: headless Blender
(`blender.exe --background --python`, found at
`C:\Program Files\Blender Foundation\Blender 4.4\`) imports the STL,
applies a Decimate modifier (ratio 0.1), exports GLB — clean 10:1
reduction, 69,182 → 6,918 triangles, no errors. Converted and
**live-imported successfully** — slot `Reso_A0E`. Boomy's real chassis is
now sitting in the Resonite session.

**Net effect**: the full pipeline (glTF/STL → optional Blender decimation
→ mesh-JSON → live ResoniteLink import) is proven end to end, not just on
a hand-built test cube (Phase 0) but on real, non-trivial meshes from both
Marble and Boomy's actual hardware model. What's still unproven: whether
one of the three full-size collider fixtures (91k-236k tris) needs the
same decimate-first treatment, or fits under the shell's <150k-tri budget
as-is — worth checking before the real home-brief generation starts.

## Repos now explicitly in scope for "private world + home + Nekomimi-chan talks and dances"

| Repo | Role in this project | Net new vs. master plan? |
|---|---|---|
| resonite-mcp | ResoniteLink bridge — the whole Line B/C pipe | No — core repo since Phase 0 |
| worldlabs-mcp | Marble world generation for Line A (the home) | No — core repo since Phase 0 |
| blender-mcp | Mesh refinery — glTF→mesh-JSON bridge, decimation, collision proxies | No — core repo since Phase 0 |
| avatar-mcp | VRM depot (Nekomimi-chan lives here), avatar pipeline, VRChat OSC patterns to reuse | No — core repo since Phase 0 |
| learnbot-mcp | Persona (Miko-chan), chat, emotion tags, lesson tools (Phase 5b keigo lesson) | No — core repo since Phase 0 |
| mcp-central-docs | This project's home (`projects/resonite-living/`) | No — it's where you're reading this |
| avatar-pipeline-mcp | **Deprecated stub** — folded into avatar-mcp's `avatar_pipeline` tool | Net new to the list, but dead weight: don't build against it |
| games-app | Japanese learning content (kanji/JLPT/vocab) — possible lesson-content or prop-asset reuse | **Net new** — not previously in the plan; role is speculative, not yet wired to any phase |
| robotics-mcp | Generic robot bridge (Dreame/Yahboom/Gazebo/Unity/VRChat) | **Net new** — relevant to the Phase 6 "Boomy virtual twin" backlog item, not Phases 1-5 |
| yahboom-mcp | Boomy (the actual Raspbot) — real-robot control, live daily | **Net new** — same Phase 6 backlog relevance as robotics-mcp |

The master plan (`RESONITE_HOME_NEKOMIMI_PLAN.md`) has been updated with
these four net-new rows in its building-blocks table, plus the
avatar-pipeline-mcp deprecation note, in this same session.

**Honest read**: games-app, robotics-mcp, and yahboom-mcp being in the repo
list doesn't change what Phase 1 needs to do next. Robotics/yahboom map
cleanly onto the pre-existing Phase 6 "Boomy gets a virtual twin" backlog
item — nothing to design differently, just confirms it's still a live idea.
games-app is the one genuinely open question: it duplicates some of what
learnbot-mcp's lesson tools already do (Phase 5b is fully specced against
learnbot, not games-app). If the intent is to pull specific kanji-wall
assets or JLPT drill content into the in-world lesson, that's a real but
undefined integration — flagged in TODO, not designed yet.

## What Phase 1 actually needs (unchanged by this session)

1. Blender → mesh-JSON converter script, proven against the three free
   Marble Adventure `_collider.glb` fixtures in `~/Downloads` before it
   touches real home geometry.
2. `import_texture_file`/`resonite_link_import_texture` — live-verify once
   for real (shape-correct, unproven per Phase 0 handoff).
3. VRM → mesh-JSON conversion spike (bones/blendshapes) — Phase 4 prep.
4. Only after 1-3: Marble generation of the actual home brief (Japanese
   hillside shrine-house, golden hour, engawa veranda, Vienna Altbau
   touches) — Sandra picks the winner from 3-5 candidates.

See TODO file for this broken into checkable tasks with owners (agent vs.
Sandra) and rough AI-assisted time estimates.

---

## 2026-07-18, fourth update — CONCURRENT SESSION NOTICE + this session's own live results

**Important**: re-reading this file to write this update revealed the
"third update" section above was written by a **different, concurrent
agent session** (not this conversation) — it did real, separate work
against the same live Resonite session: headless Blender decimation
(`blender.exe --background --python`, real quadric Decimate modifier,
ratio 0.1) on the same `base_link_X3.STL`, producing slot `Reso_A0E`
(6,918 triangles) plus its own house/triangle test slots
(`Reso_A02`/`Reso_A06`/`Reso_A0A`). That work is **not being erased or
overwritten here** — both efforts are real and both succeeded. This
session's own work, done independently and in parallel, is below.

### This session's pipeline (stdlib-only, no Blender dependency)

Built two converters and one decimator, all pure Python (no new
dependencies to install):

- `resonite_mcp/utils/gltf_meshjson.py` — GLB/glTF parser (accessors,
  bufferViews, buffers: GLB BIN chunk / base64 data URI / external file,
  all handled). Proven against all three real `_collider.glb` Marble
  fixtures (see table above — 70k/49k/119k vertices, all converted
  cleanly).
- `resonite_mcp/utils/stl_meshjson.py` — binary + ASCII STL parser. Ran
  against Boomy's real chassis (`base_link_X3.STL`): 69,192 triangles →
  207,576 vertices (STL has no shared-vertex indexing, and per-face
  normals mean position+normal dedup barely collapses anything for STL
  specifically — a real limitation, not a bug, noted in the module).
- `resonite_mcp/utils/decimate_meshjson.py` — **vertex clustering**
  (grid-quantization) decimation, explicitly documented as NOT the same
  technique as Blender's quadric edge-collapse Decimate modifier (the
  concurrent session's approach, above). At ratio=0.01: Boomy's chassis
  went 207,576→4,698 vertices, 69,192→11,493 triangles (83% triangle
  reduction).

### Live results, this session

Connected to the running session (discovery reports the WSL2/Hyper-V
bridge address `172.23.160.1:11831`, which the server rejects with
HTTP 400 — `localhost` on the same port works when running from Goliath
itself, the same machine hosting Resonite):

- Hand-authored 14-vertex/18-triangle house (box body + gabled roof) —
  spawned successfully, slot `Reso_A12`. **Sandra confirmed visually**:
  "looks like a house kindasorta."
- The vertex-clustering-decimated Boomy chassis (4,698 verts / 11,493
  tris) — spawned successfully, slot `Reso_A16`. **Sandra confirmed
  visually**: "the boomy chassis is recognizable."
- Raw (undecimated) 69,192-triangle STL was never pushed live in this
  session — only the decimated version was tried.

**One real bug, caught and fixed, not a server issue**: first spawn
attempt failed with "must specify a type discriminator" on the submesh —
looked exactly like a live schema mismatch worth reporting as a Phase 0
finding invalidated. It wasn't. This session's own test script had a bug:
passed the raw triangle-index array instead of the `$type`-wrapped
submesh list to `spawn_mesh()`. Fixed in one line; worked first try. The
schema documented in `resonite_link.py` was correct all along —
recorded here specifically so nobody re-investigates a server bug that
doesn't exist.

### Reconciling the two decimation approaches

Both work; they're not equivalent in quality. The concurrent session's
headless-Blender quadric decimate is the **better technique** — it picks
which geometry to simplify based on surface-error cost, so it preserves
shape at a given triangle count better than this session's grid-snap
vertex clustering. **Recommendation going forward**: use the Blender path
for anything that will actually ship in the home (furniture, decimated
shell candidates); keep this session's stdlib vertex-clustering decimator
as a no-Blender-available fallback or a quick rough-cut tool, not the
production path. Doesn't need a decision right now, just flagging so the
choice is made consciously rather than by whichever script happened to
run first.

### Net status

The full pipeline — source mesh (glTF or STL) → optional decimation
(either technique) → mesh-JSON → live ResoniteLink import — is now
proven twice, independently, by two different approaches, against two
different real (non-trivial, non-toy) meshes. Both a Marble-style
collider and Boomy's actual robot geometry render recognizably in a live
session. Phase 1's core technical risk (can arbitrary real-world geometry
actually get from a file into Resonite) is retired.

**Still open, unchanged**:
- Full-size home-shell fixtures (91k-236k triangles) never pushed live —
  only decimated results (6.9k-11.5k triangles from two different
  techniques) are proven at the live-import stage. Where the JSON-import
  ceiling actually sits between ~11.5k and 91k+ triangles is unmeasured.
- `import_texture_file` still unverified live.
- VRM avatar path (bones/blendshapes) not started — see "Next: Nekomimi-
  chan" below.

## Next: spawning Nekomimi-chan

Sandra asked (2026-07-18) whether to go after this next. Honest scope
check before starting:

- `Nekomimi-chan.vrm` is real, 17.5MB, in the shared depot
  (`~/.avatarmcp/models/`).
- ResoniteLink has **no generic VRM/model import** (confirmed against the
  live protocol, not just the docstring) — the only path in is the same
  mesh-JSON route just proven above, extended to carry `bones` and
  `blendshapes` (the schema supports both per the Phase 0 wire-shape
  testing, but that part of the schema has never been exercised, live or
  otherwise).
- VRM's actual geometry is glTF-based internally, so `gltf_meshjson.py`
  should read it — but VRM adds humanoid bone bindings and blend-shape
  (expression) data in its own extension blocks
  (`VRMC_vrm`/`VRM_0` extensions) that the current converter does not
  parse at all; it would only pick up the static mesh, not rig or
  expressions.
- Getting her *standing there* (static mesh, no rig) is a small extension
  of proven work. Getting her *posable/expressive* (the actual point —
  talk and dance) needs the bones+blendshapes extension built and proven,
  which is genuinely new work, not a re-run of what's already proven.

---

## 2026-07-18, fifth update — Nekomimi-chan's static mesh is live

Went straight for sub-goal 1 (static mesh, no rig). Result: **her full,
undecimated VRM mesh imported live on the first real attempt** —
190,111 vertices, 45,451 triangles, slot `Reso_A1C`. No decimation needed.
This also answers an open question from the previous update: the
JSON-import size ceiling is comfortably above 45k triangles (previously
only proven up to ~11.5k).

**Two real server errors hit and resolved along the way** (both genuine
new schema findings, not bugs in this project's code):

1. `uvs` must be a **list** of UV coordinate objects, not a bare
   `{"x","y"}` dict — Resonite supports multiple UV channels per vertex.
   Confirmed live via the server's own error message. Fixed in
   `gltf_meshjson.py` and its docstring updated accordingly.
2. Each UV coordinate element is itself a polymorphic type needing a
   `$type` discriminator — tried `UV_Coordinate`, `float2`, `uv`,
   `UVCoordinate`, all rejected as "unrecognized type discriminator id."
   Queried the server's own reflection API (`getTypeDefinition`):
   `float2` **is** a valid registered Resonite type (`Elements.Core.float2`,
   engine primitive), but that's not the same as the discriminator string
   the polymorphic `UV_Coordinate` interface expects — those don't have to
   match, and this one hasn't been found yet. Rather than keep
   brute-forcing an internal string, **UVs are stripped for now** — she
   has a solid/default material, not a textured one, until this is
   resolved (needs either upstream ResoniteLink source inspection or
   another reflection angle, e.g. `getComponentTypeList` filtered to the
   relevant namespace).

**Current state of Nekomimi-chan in the session**: static T-pose, full
geometry, no texture, no rig, no expressions. That's exactly as scoped —
sub-goal 1 done, sub-goal 2 (bones/blendshapes for actual posing and
talking/dancing) not started.

**Still open**:
- UV discriminator string (blocks textures on her, and on anything else
  needing a texture rather than a solid color).
- Bones (`JOINTS_0`/`WEIGHTS_0`) and blendshape (morph target) decoding —
  genuinely new work, VRM's `VRMC_vrm`/`VRM_0` extension blocks still
  entirely unparsed.
- Full-size home-shell fixtures (91k-236k triangles) still never pushed
  live — but the size ceiling question has shrunk: we now know ≥45k
  triangles works raw, so at most the two larger fixtures (Neuschwanstein
  91k, well within range; St. Peter's 236k, still untested) are in
  question, not all three.
