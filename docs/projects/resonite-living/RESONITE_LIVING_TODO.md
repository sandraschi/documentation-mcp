# Resonite Living — TODO

**Last updated**: 2026-07-18 19:48. Living document — update in place, don't
fork timestamped copies of this one (the `.bak` auto-backups on edit are
enough history). Companion: RESONITE_LIVING_STATUS_20260718.md,
RESONITE_HOME_NEKOMIMI_PLAN.md.

## Now (Phase 1 gate — nothing else matters until this is proven)

- [x] **MILESTONE 2026-07-19: moved off the ephemeral Tutorial session
      onto Sandra's own persistent Home.** Sandra's own idea — no reason
      to keep testing somewhere that vanishes when the real destination
      (her Home) already exists and is persistent. Enabled ResoniteLink
      in Home (Dash → Session → Settings), discovered it (port 21789,
      not guessed — confirmed via `discover_sessions()`), and confirmed
      Nekomimi-chan spawns and is now visible there. **Correction
      2026-07-19**: an earlier note here wrongly framed the Marble/
      worldlabs-mcp shrine-house generation as "optional polish" now that
      Home exists — Sandra corrected this directly: the shrine-house is
      still a real, planned part of this project, not cut. What's
      actually true: Home gives a persistent place to iterate *right
      now* while the shrine-house is built properly later — it's a
      reordering (Nekomimi-chan's rig/texture first, house generation
      after), not a scope cut. Tutorial-session test objects (house,
      roscar, audio tones) are still there but no longer the active
      target for Nekomimi-chan work specifically.

- [ ] **NEXT UP (2026-07-18, Sandra's call): spawn Nekomimi-chan.** Two
      genuinely different sub-goals, don't conflate them:
      1. **Static mesh only** (small extension of proven work): extend
         `gltf_meshjson.py` to read VRM's `VRMC_vrm`/`VRM_0` extension
         blocks for basic geometry — VRM is glTF-based, so the existing
         accessor-decoding core should mostly work as-is for POSITION/
         NORMAL/UV; this gets her *standing there*, no rig, no expression.
      2. **Posable/expressive** (the actual point — talk and dance):
         needs `JOINTS_0`/`WEIGHTS_0` (skinning → `bones` in the mesh-JSON
         schema) and morph-target (blendshape) decoding — glTF encodes
         both differently from static attributes, and this has NOT been
         touched by either concurrent session's work today. Genuinely new
         work, not a re-run of what's proven.
- [x] **Sub-goal 1: static mesh — DONE 2026-07-18.** Her full, undecimated
      VRM mesh (190,111 vertices, 45,451 triangles) imported live on the
      first real attempt — slot `Reso_A1C`. No decimation needed; this
      also answers the JSON-import size-ceiling question from above:
      comfortably above 45k triangles, previously only proven to ~11.5k.
      Two real UV schema findings hit and resolved/parked along the way:
      `uvs` is a LIST of coordinate objects (fixed in gltf_meshjson.py);
      each coordinate needs its own `$type` discriminator, which is
      **still unknown** (`UV_Coordinate`/`float2`/`uv`/`UVCoordinate` all
      rejected live) — UVs stripped for now, she has a solid material, not
      textured. Current state: static T-pose, full geometry, no texture,
      no rig, no expressions.
- [x] **Sub-goal 2: posable/expressive — DATA MODEL BUILT, 2026-07-19.**
      Real, substantial progress, not just a wire-shape test:
      - `gltf_meshjson.py` now decodes `JOINTS_0`/`WEIGHTS_0` (skinning)
        and morph targets (blendshapes) from any glTF/VRM, gated behind
        `include_skinning=True` (default off — untested until today).
      - Nekomimi-chan's VRM has **197 real bones** (VRM humanoid names:
        `J_Bip_C_Hips`, `J_Sec_*` skirt-physics bones) and **399 real
        blendshapes** (VRM expression names: `Fcl_ALL_Joy`,
        `Fcl_ALL_Angry`, etc.) — genuinely parsed, not synthetic test data.
      - **Wire shapes confirmed live**, error-driven the same way uvs/
        submesh were: `bones` (name/parentIndex/position/rotation/scale)
        worked on the first attempt; `blendshapes` needed a `frames`
        wrapper (`{"name","frames":[{"weight","positionDeltas"}]}`) — a
        bare shape threw a server-side NullReferenceException, the
        wrapped one succeeded. `SkinnedMeshRenderer.Bones` is a
        `SyncRefList<Slot>` (list of Slot references, confirmed via
        reflection), `.BlendShapeWeights` a `SyncFieldList<float>`.
      - **Actually built, live**: 197 real bone Slots created (one batch
        call, correct parent-child hierarchy from the bones list),
        `SkinnedMeshRenderer` added referencing all 197 in boneIndex
        order plus a 399-length `BlendShapeWeights` list (all zero =
        neutral), replacing the earlier plain (non-skinned) `MeshRenderer`.
      - **Honest gaps, not glossed over**: blend-shape *deltas*
        (positionDeltas) were never pushed — only the empty weights list
        — because 399 shapes × 190k vertices each is an enormous JSON
        payload, a real scaling problem separate from the now-solved wire
        shape. Whether the skeleton actually *poses* her (moving a bone
        and seeing the mesh deform) has not been tested — only that the
        SkinnedMeshRenderer accepted the Bones/Mesh/BlendShapeWeights data
        without error. **Awaiting Sandra's visual check**: does she still
        render correctly (not glitched) with the new SkinnedMeshRenderer?
      **Owner**: agent, next: prove one bone rotation actually deforms
      her, and solve the blendshape-delta scaling problem (per-blendshape
      sparse deltas, or a smaller test subset, rather than all 399 at
      full resolution).
      **2026-07-19, SETBACK**: rotated the head bone live (server
      accepted the write, no error) — Sandra reported the mesh vanished
      entirely ("nothing shows"), not just failed to visibly pose.
      Investigated: every component checked out structurally correct
      (Mesh/Bones/Materials all correctly referenced, everything
      Enabled=true, 197 bone refs present) — so the cause isn't wiring,
      it's almost certainly that **inverse bind matrices
      (`skin.inverseBindMatrices` in glTF) were never decoded or
      supplied**. Real skinning math needs them to establish the bind
      pose reference frame; without them, `SkinnedMeshRenderer` may be
      computing vertex positions from an undefined/degenerate frame,
      plausibly collapsing the whole mesh somewhere invalid rather than
      just posing it wrong. **Immediate fix**: disabled the
      `SkinnedMeshRenderer` (kept, not deleted, for debugging) and
      restored a plain `MeshRenderer` so she's visible again — priority
      was not leaving Sandra with nothing while this gets solved
      properly. **Real next step**: decode `skin.inverseBindMatrices`
      (a MAT4-per-joint accessor, not yet parsed anywhere in
      `gltf_meshjson.py`) and work out how FrooxEngine expects bind pose
      to be established for `SkinnedMeshRenderer` — this needs research,
      not another guess-and-check pass.
      **2026-07-19, second update**: found `J_Bip_C_Head` at bone index
      42 — cross-confirmed against the earlier sample vertex dump, which
      showed a head-region vertex weighted `{"boneIndex": 42, "weight":
      1.0}`, i.e. the same bone. Rotated it 45° around Y via
      `update_slot` — server accepted with no error. **Awaiting Sandra's
      visual check**: does her head actually turn / does the mesh deform,
      or does it stay static (which would mean the data was accepted but
      isn't being applied by the renderer)?
      **2026-07-19, third update (this session)**: confirmed invisible even
      at neutral pose (reset head rotation, disabled the fallback
      MeshRenderer, re-enabled only SkinnedMeshRenderer) — ruling out the
      earlier rotation math as the cause. Built the smallest possible
      reproducible case (a 4-vertex quad, 2 bones, no VRM complexity at
      all) — **also invisible**, which rules out inverse-bind-matrices/
      VRM-specific complexity as the root cause too. Checked
      SkinnedMeshRenderer's bounds-related members and found a real smoking
      gun: `ExplicitLocalBounds` on the live component reads
      `min=(3.4e38,3.4e38,3.4e38), max=(-3.4e38,-3.4e38,-3.4e38)` — an
      inverted, degenerate bounding box (the engine's "never computed"
      sentinel), with `BoundsComputeMethod="Static"` (compute-once-and-
      cache) that never actually ran for a wire-imported mesh. A renderer
      with inverted bounds gets frustum-culled every frame regardless of
      geometry — fits every observed symptom. **Not yet tried**: setting
      `BoundsComputeMethod` to a mode that recomputes automatically (check
      `SkinnedBounds` enum's other values via `getEnumDefinition`), or
      writing a real `ExplicitLocalBounds` value directly. Paused here —
      Sandra asked to focus on the webapp instead; pick this up with the
      enum check as the first move, not another blind guess.
- [ ] **BUG: Nekomimi-chan still invisible after material fix (2026-07-18,
      ongoing).** Bounding box confirmed normal (1.16m×1.45m×0.56m, origin
      at feet) — not a scale/position/origin issue. Live hypothesis:
      backface culling from a glTF-vs-Resonite coordinate-handedness
      mismatch (this is the first glTF-derived, not hand-authored or
      STL-derived, mesh pushed through this pipeline). Checked
      PBS_Metallic's component definition for a two-sided/cull toggle —
      none exists, so double-sidedness must be controlled elsewhere.
      Spawned a second copy at `(-6,0,5)` (`Reso_A35`) with Z negated
      (position+normal) and triangle winding reversed, next to the
      original at `(-3,0,5)` (untouched) for comparison. **Awaiting
- [x] **BUG RESOLVED 2026-07-19: coordinate-handedness fix confirmed and
      baked in permanently.** The Z-flip + winding-reversal test copy was
      spawned into Sandra's own persistent Home ("sandras Home", port
      21789 — discovered, not guessed) and **visually confirmed visible**
      ("all white, arms outstretched" — correct: no texture since UVs are
      stripped pending the discriminator fix, T-pose since no rig is
      wired yet). The fix is now the default behavior in
      `gltf_meshjson.py`'s `gltf_to_mesh_json()` (new
      `resonite_coordinate_fix: bool = True` parameter) — every future
      glTF/VRM conversion gets it automatically, not just this one-off
      script. Verified clean via `ruff` and a live re-run against the
      same VRM producing identical vertex/triangle counts.
      **Bonus finding along the way**: mathematically confirmed (before
      the visual check) that the source mesh's winding was 99.9%
      self-consistent with its own stored normals — the bug was never in
      the parser, only in the target engine's coordinate convention.
- [x] **Nekomimi speech mechanism — AUDIO PIPE BUILT AND LIVE-PROVEN,
      2026-07-18.** Reflected first, not guessed (learned from the
      UV_Coordinate lesson): `getComponentDefinition` on `AudioClipPlayer`
      and `AudioOutput` gave real member names before any code was
      written. Added to `resonite_link.py`:
      - `import_audio_clip_file(file_path)` — same shape as
        `import_texture_file` (plain `filePath` message, by analogy — not
        yet cross-checked against upstream C# source the way
        `import_texture_file` was, but now live-tested and it works).
      - `spawn_audio(file_path, position, name, loop, volume, spatialize)`
        — composes `StaticAudioClip` (holds the imported clip's asset URL,
        same pattern as `StaticMesh`) → `AudioClipPlayer` (`Clip`
        reference to it) → `AudioOutput` (`Source` reference to the
        player, spatialized) → triggers playback automatically.
      **Live-verified end to end**, twice: generated a stdlib-only test
      WAV (440Hz beep, no dependencies), imported it, spawned the full
      chain, and triggered play — no errors on any step. `playback`
      turned out to be a nested object (`{"play","loop","position",
      "speed"}`), confirmed by reading a live component back rather than
      guessing, matching the UV_Coordinate lesson from earlier tonight.
      **What's proven**: every wire call succeeds, the component graph is
      wired correctly per reflection. **What's NOT proven**: actual
      audibility — that needs a human physically listening in the
      session; there's no way to verify sound reaches a listener from
      here. Two test tones are live in the Tutorial session right now,
      awaiting Sandra's confirmation: one looping at `(0,1.5,8)`, one
      one-shot at `(2,1.5,8)`.
      **Still separate, not done**: wiring this to actual learnbot-mcp
      chat output + speech-mcp TTS (this proves the Resonite-side half of
      the pipe only — the generate-text-then-TTS half already exists
      elsewhere in the fleet but isn't triggering this yet).
- [ ] **UV discriminator string — unresolved, blocks textures generally**
      (not just on her). `getTypeDefinition('float2')` confirms `float2`
      is a valid Resonite type (in `[Elements.Core]Elements.Core`, not
      `FrooxEngine` — confirmed 2026-07-19), but that's not the
      polymorphic discriminator id `UV_Coordinate` expects. **2026-07-19,
      deeper attempt**: the original server error text was
      `ResoniteLink.UV_Coordinate` — a type in the ResoniteLink protocol
      library's own namespace, not FrooxEngine's data model, which means
      `getTypeDefinition`/`getComponentDefinition` (engine reflection)
      were never going to find it — confirmed by testing:
      `getTypeDefinition('ResoniteLink.UV_Coordinate')` → "not a valid
      type". Found and read the actual open-source ResoniteLink repo
      (github.com/Yellow-Dog-Man/ResoniteLink, protocol 0.13.1 matches
      exactly) — its docs describe `getSlot`/`addSlot`/`addComponent`
      etc. in detail but don't document the `Submesh`/`UV_Coordinate`
      polymorphic discriminators directly; would need the actual C#
      source in the `Models` folder, which GitHub's crawler blocked
      fetching this session. Tried `getSyncObjectDefinition` as a more
      targeted reflection angle — got a real, specific error ("Value
      cannot be null, Parameter 'key'") meaning the message exists but
      its parameter shape isn't `{"key": "<name>"}` either; didn't chase
      further blind guesses on a second undocumented message shape.
      **Next real angle** (not yet tried): browse the Models folder
      directly via GitHub's raw file URLs (not the blocked tree/blob
      UI), or ask in the Resonite Discord — this is genuinely buried
      deep enough that guessing further isn't productive use of time.
      **Owner**: agent (raw-file browse) or Sandra (Discord ask).
      **Estimate**: unknown — this is the second session this has
      resisted resolution.

- [x] **Blender → mesh-JSON converter script** — DONE 2026-07-18. Lives at
      `resonite-mcp/src/resonite_mcp/utils/gltf_meshjson.py`, stdlib-only
      (no new dependency). Proven against all three free `_collider.glb`
      fixtures in `~/Downloads` (70k-236k triangles each, see prior entry
      for the table) — output saved to `C:\temp\*_meshjson.json`.
- [x] **Live wire-call proof** — DONE 2026-07-18. Connected to the running
      session (port 11831, Resonite 2026.7.14.913, protocol 0.13.1.0) and
      spawned, in order: a flat triangle (slot `Reso_A02`), a house body box
      (slot `Reso_A06`), a house roof box (slot `Reso_A0A`) — all via
      `spawn_mesh()` with the converter's output shape. One real bug caught
      and fixed along the way: the test script passed the raw triangle list
      instead of the full submesh object (with its `$type` discriminator)
      into `spawn_mesh()` — server error was specific and correct
      ("must specify a type discriminator"), fixed in one line. Test script:
      `C:\temp\phase1_live_import_test.py`.
- [x] **STL → mesh-JSON converter** — DONE 2026-07-18, net-new (not in the
      original gate item, added because a real STL test case existed).
      Lives at `resonite-mcp/src/resonite_mcp/utils/stl_meshjson.py`,
      stdlib-only. STL has no shared-vertex indexing, so output vertex
      count is always 3x triangle count — stated as a known limitation,
      not hidden. Proven against Boomy's real chassis mesh
      (`yahboom-mcp/webapp/dist/assets/meshes/base_link_X3.STL`):
      69,182 triangles → 207,576 vertices, 42.9MB mesh-JSON (too big for a
      live JSON push as-is).
- [x] **Decimation pipeline proven** — DONE 2026-07-18. Headless Blender
      (`blender.exe --background --python`, found at
      `C:\Program Files\Blender Foundation\Blender 4.4\`) imports the STL,
      applies a Decimate modifier, exports GLB. Script:
      `C:\temp\decimate_boomy_test.py`. Result: Boomy's chassis
      69,182 → 6,918 triangles at ratio=0.1 (clean 10:1, no errors).
      Converted through gltf_meshjson.py (16,653 vertices, 3.5MB JSON) and
      **live-imported successfully** — slot `Reso_A0E`. Full pipeline
      (STL → Blender decimate → glTF → mesh-JSON → ResoniteLink) proven
      end to end on a real, non-trivial mesh.

**Note**: the two "Live wire-call proof" / "STL → mesh-JSON" entries below
this point (and the duplicate above) were written by two different,
concurrent agent sessions working independently against the same live
Resonite session around the same time — both are real, neither
overwritten. See RESONITE_LIVING_STATUS_20260718.md's "fourth update" for
the full reconciliation (short version: Blender's real quadric decimate,
above, is the better technique; this session's own stdlib vertex-
clustering decimate, below, is a viable no-Blender fallback, not the
recommended production path).

- [ ] **Live-verify `import_texture_file`** (resonite-mcp) for real — currently
      shape-correct but unproven per the Phase 0 handoff. Needed for the
      `.jpg` equirect environment maps Marble also outputs.
      **Owner**: agent, needs live Resonite session (have one now — port
      11831). **Estimate**: 1-2 hours.
- [ ] **VRM → mesh-JSON conversion spike** (bones/blendshapes) — prove on one
      blendshape before Phase 4 avatar work starts. Schema already supports
      both per the Phase 0 wire-shape cheat sheet. **Checked 2026-07-18**:
      `Nekomimi-chan.vrm` (17.5MB) is real, sitting in the shared depot
      `~/.avatarmcp/models/`. resonite-mcp already has a
      `/rl/world/import-vrm` endpoint, but it's an honest stub — returns
      `not_implemented` because ResoniteLink 0.13.1 has no generic VRM/file
      import over the wire (not a phantom-API bug, it correctly reports its
      own limit). blender-mcp already has mature VRM tooling
      (`export_vrm`, `blender_vrm_metadata` with visemes + spring bones) —
      the missing piece is specifically bridging that VRM-aware export into
      the same mesh-JSON converter built for the home shell/furniture, fed
      bone/blendshape data instead of static geometry. **No code written
      for this yet** — but gltf_meshjson.py's accessor-decoding core is
      now proven and directly reusable; the remaining work is specifically
      JOINTS_0/WEIGHTS_0 (skinning) and morph-target decoding, which glTF
      encodes differently from POSITION/NORMAL/UV and hasn't been touched.
      **Owner**: agent. **Estimate**: 0.5 day, mostly reuse.
- [ ] **Un-tested still**: whether one of the full-size (91k-236k tri) home
      shells needs the same decimate-first treatment before its own live
      import, or whether the shell budget (<150k tris, per the master plan)
      makes at least the smallest one (Neuschwanstein, 91k) importable
      as-is. Worth checking before Phase 1's actual home-brief generation.

- [x] **Live wire-call proof** — DONE 2026-07-18. Connected to the running
      session (discovery reports the WSL2/Hyper-V bridge IP
      `172.23.160.1:11831`, which gets rejected with HTTP 400 — `localhost`
      on the same port works). Spawned a hand-authored 14-vertex/18-triangle
      "house" (box + gabled roof) live: slot `Reso_A12`, full render chain
      (StaticMesh/MeshRenderer/PBS_Metallic) confirmed. Script at
      `resonite-mcp/scripts/live_house_and_roscar_test.py`.
      **Bug found and fixed in the test script itself, not the server**:
      first attempt failed with "must specify a type discriminator" —
      looked like a schema mismatch, but was actually this script passing
      the raw triangle-index array instead of the properly-wrapped
      `{"$type": "triangles", "triangles": [...]}` submesh list. Once
      fixed, it worked first try — the documented schema in
      `resonite_link.py` was correct all along.
- [x] **STL → mesh-JSON + decimation, live** — DONE 2026-07-18. New module
      `resonite_mcp/utils/stl_meshjson.py` (binary + ASCII STL, stdlib
      only). Converted Boomy's real chassis mesh
      (`yahboom-mcp/webapp/dist/assets/meshes/base_link_X3.STL`, 3.46MB):
      69,192 triangles → 207,576 vertices (STL has no shared-vertex
      indexing, and per-face normals mean this project's dedup-by-position
      +normal barely collapses anything for STL — noted as a real
      limitation, not a bug). Ran `decimate_meshjson.py` (vertex-clustering,
      ratio=0.01): **207,576 → 4,698 vertices, 69,192 → 11,493 triangles**
      (83% triangle reduction). Pushed the decimated mesh live —
      succeeded, slot `Reso_A16`. **Not yet tried**: pushing the raw
      (undecimated, 69k-triangle) STL live, so the actual JSON-import size
      ceiling is still unmeasured — only known-good so far is ~11.5k
      triangles.

## Next (Phase 1 proper, blocked on the above)

- [ ] Prompt-engineer 3-5 Marble candidates for the actual home brief
      (Japanese hillside shrine-house, golden hour, engawa veranda, Vienna
      Altbau touches — parquet, double doors). **Owner**: agent drafts,
      **Sandra picks the winner** (taste gate, hers alone).
      **Estimate**: half a day incl. her review.
- [ ] Export mesh + textures (if Marble offers them) + splat (always, for
      WebXR/Spark preview on Quest before committing).
- [ ] Fallback check: if mesh export quality is poor, splatmaker-mcp
      nerfstudio lane (splat→mesh) as the quality-gated alternative.

## Backlog / not blocking Phase 1

- [ ] **Boomy virtual twin** (robotics-mcp / yahboom-mcp) — Phase 6 item,
      confirmed still live by today's repo list but not designed. Real robot
      control (yahboom-mcp) vs. generic bridge (robotics-mcp) — pick one
      as the actual integration point when this gets picked up.
- [ ] **games-app Japanese content integration** — undefined. Phase 5b's
      keigo lesson is fully specced against learnbot-mcp's own lesson tools
      (`lesson_generate`, `chat_start`, `lesson_run`, `grammar_check`,
      `lesson_differentiate` — all verified real). Before touching games-app,
      decide: is this about reusing specific kanji-wall/JLPT assets as
      in-world props, or actually routing lesson content through games-app's
      engine instead of learnbot's? Those are different amounts of work.
      Don't start this without that decision made explicit.
- [ ] Kotatsu prop + low table (Marble object-mode or Blender kit-bash) for
      the Phase 5b lesson staging, + second text panel for grammar-check
      corrections.
- [ ] `AvatarAnchor` + trigger spike for in-home teleport-to-kotatsu — untested
      ProtoFlux pattern, not yet proven like the render chain was.
- [x] resonite-mcp fleet standard: add `/health` endpoint per
      `standards/HEALTH_ENDPOINT_STANDARD.md` — **DONE 2026-07-19**.
      `/health`/`/api/health`/`/api/v1/health` now return real
      `version`/`git_sha`/`started_at`/`uptime_seconds`/`shutting_down`/
      `transport`/`port` per the standard. `git_sha` verified live
      against the actual repo (`25a6a87`) — matched exactly, not assumed.

## Explicitly not doing (until reconsidered)

- avatar-pipeline-mcp — deprecated stub, do not build against it; use
  avatar-mcp's `avatar_pipeline` tool instead.
- Vircadia / VRChat as the platform — researched and parked, see
  PLATFORM_ALTERNATIVES.md. Resonite stays the platform.
