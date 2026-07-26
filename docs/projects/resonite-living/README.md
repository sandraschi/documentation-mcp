# Resonite Living

**Created**: 2026-07-18 · **Updated**: 2026-07-19 · **Status**: Phase 0
CLOSED, Phase 1 IN PROGRESS — Nekomimi-chan visible and spawned in
Sandra's own persistent Home (not a test session), coordinate-handedness
bug found and permanently fixed.
**One line**: a persistent Resonite home, generated once and inhabited
repeatedly — Nekomimi-chan present as an embodied companion, and the home
doubling as a real teaching space for Japanese lessons.

This is the project home for what was, until tonight, three loose docs in
`projects/`. They are not moved (nothing outside them referenced the old
paths, checked 2026-07-18, but no reason to churn working links either) —
this README is the index that ties them together.

## Docs

| Doc | What it is |
|---|---|
| [RESONITE_LIVING_STATUS_20260718.md](RESONITE_LIVING_STATUS_20260718.md) | **Current status** — read this first |
| [RESONITE_LIVING_TODO.md](RESONITE_LIVING_TODO.md) | **Current TODO** — living doc, prioritized, updated in place |
| [RESONITE_BEGINNER_PLAYBOOK.md](RESONITE_BEGINNER_PLAYBOOK.md) | Sandra's own Resonite basics — traveling between worlds, making a world, furniture, audio links, and the real mechanism for making Nekomimi-chan speak |
| [../RESONITE_HOME_NEKOMIMI_PLAN.md](../RESONITE_HOME_NEKOMIMI_PLAN.md) | Master plan — deep analysis, building-block inventory, Phases 0-6, risk register |
| [../RESONITE_PHASE0_RUNBOOK.md](../RESONITE_PHASE0_RUNBOOK.md) | Agent-actionable step-by-step runbook (works cold for Fable/opencode/DS4), execution log |
| [../RESONITE_PHASE0_HANDOFF.md](../RESONITE_PHASE0_HANDOFF.md) | OBSOLETE as a status doc (superseded by RESONITE_LIVING_STATUS above) — kept for the wire-protocol cheat sheet + Phase 0 execution log |
| [PLATFORM_ALTERNATIVES.md](PLATFORM_ALTERNATIVES.md) | Vircadia and VRChat researched as alternatives — why we're not using either right now, and what would change that |

## Status (2026-07-19)

| Phase | State |
|---|---|
| 0 — Reality-check spike | **CLOSED**. All 6 runbook steps GREEN: connect/READ/WRITE/mesh-import/render/material live-verified, Marble export formats enumerated, decision note written. See adn note "Phase 0 decision - PROCEED". |
| 1 — Generate the home | **IN PROGRESS.** Core pipeline (glTF/STL → mesh-JSON → optional decimation → live ResoniteLink import) proven twice, independently, against real non-trivial meshes (Marble colliders, Boomy's chassis, a full 45k-triangle VRM avatar — no decimation needed at that size). Audio pipe (import → StaticAudioClip → AudioClipPlayer → AudioOutput) built and live-verified. Not done: full-size home-shell fixtures never pushed live; texture/UV discriminator unresolved; the actual home-brief generation hasn't started. |
| 2 — Refine in Blender | Not started (scoped: shell refinery + furniture kit-bash, two independent jobs). |
| 3 — World assembly | Not started. |
| 4 — Nekomimi-chan enters | **Sub-goal 1 (static mesh) DONE and confirmed visible.** Sub-goal 2 (bones/blendshapes) has real data-model progress: 197 bones + 399 blendshapes parsed from her actual VRM, wire shapes confirmed live, 197 bone Slots + a real `SkinnedMeshRenderer` built in her Home. Not yet proven: whether a bone rotation actually deforms the mesh, and blendshape deltas (too large to push at full res) still unsent. |
| 5 — The Soul (chat/voice/emote) | Resonite-side audio playback mechanism now built and proven (see Phase 1). Not yet wired to actual learnbot-mcp chat output + speech-mcp TTS. |
| 5b — First use case: the keigo lesson | **Specced** 2026-07-18 — no code yet, but the dependency chain is fully mapped and every tool it calls is verified real. |
| 6 — Polish | Backlog. |

## Why this project exists as its own folder

The three docs above were written in one overnight session under real time
pressure. They are good but sprawling — one 169-line master plan, a 106-line
runbook, a 96-line handoff. As Phase 1+ work starts generating its own
artifacts (Blender scripts, Marble prompt logs, VRM conversion notes, the
lesson content itself), a flat `projects/RESONITE_*.md` naming scheme stops
scaling. This folder is where that grows.

## The use case that justifies the whole build

Sandra's framing, 2026-07-18: *"we will have a japanese lesson in my
resonite home."* That reframes Phase 5 from "she can talk" to "she can
teach," which changes nothing about the technical plan (the chat → OSC
expression → TTS pipeline is identical either way) but changes what counts
as done. Phase 5b in the master plan specs this directly: `lesson_generate`
→ `chat_start(persona="miko")` → `lesson_run` → normal chat turns for
Sandra's responses, optionally `grammar_check` alongside, `lesson_differentiate`
to retune difficulty live. Every one of those is a real, implemented
learnbot-mcp tool (verified against `src/learnbot_mcp/lessons.py` and
`docs/JAPANESE_LEARNING.md` on 2026-07-18, not assumed) — so Phase 5b is
pure integration, no new subsystem. The only new asset is a kotatsu prop.

## Next work, in priority order

**Canonical, up-to-date task list now lives in
[RESONITE_LIVING_TODO.md](RESONITE_LIVING_TODO.md).** This section is a
brief snapshot only.

Done since Phase 0 closed:

- ✅ `import_mesh_json`, `import_texture_file`, `import_audio_clip_file`,
  `spawn_mesh`, `spawn_audio` all added to `ResoniteLinkClient` and
  live-verified (audio pipe end-to-end 2026-07-19). `import_mesh_raw`
  deliberately left unimplemented (needs a binary WebSocket payload
  frame; raises with guidance).
- ✅ `gltf_meshjson.py`/`stl_meshjson.py`/`decimate_meshjson.py` built,
  stdlib-only, live-verified against real fixtures including a full VRM.
- ✅ Nekomimi-chan's static mesh spawned live (currently invisible,
  debugging a coordinate-handedness hypothesis).
- ✅ `resonite-mcp` bumped to 1.2.0; `CHANGELOG.md`, `CHANGELOG_LATEST.md`,
  and `docs/RESONITELINK_GUIDE.md` updated with tonight's real changes
  (including fixing genuinely wrong example code the guide had — fictional
  template-URL spawning that doesn't exist in the real protocol).

Top priority now:

1. **Fix Nekomimi-chan's invisibility** — bounding box confirmed normal,
   material confirmed present; live hypothesis is a glTF-vs-Resonite
   coordinate-handedness mismatch (first glTF-derived mesh pushed through
   this pipeline). A Z-flip/winding-reversal test copy is spawned,
   awaiting visual confirmation.
2. Resolve the `UV_Coordinate` polymorphic `$type` discriminator (blocks
   textured materials generally, not just on her).
3. VRM bones/blendshapes (sub-goal 2 of Nekomimi-chan: posable/expressive,
   the actual point — talk and dance).
4. Live-verify `import_texture_file` for real (shape-correct, unproven).

## Related fleet docs

- `resonite-mcp/docs/WEBAPP_UPDATE_PLAN.md` — **corrected 2026-07-19**: an
  earlier pass wrongly concluded the webapp's whole backend was
  fictional (checked the wrong server file — `web_sota/backend/server.py`,
  which is never actually launched). The real server, `http_server.py`
  (76 routes, launched via `web_sota/start.ps1`), is mostly genuinely
  wired to the real ResoniteLinkClient. Remaining plan is much smaller:
  path/default fixes, one page (`Logging.tsx`) that's surprisingly broken
  in production because its real code sits in the unused file, and a
  handful of pages with wrong endpoint paths or missing backends. Kept
  as a live document tracking real bugs found, not a rebuild-from-scratch
  plan.
- `standards/HEALTH_ENDPOINT_STANDARD.md` — resonite-mcp doesn't have a
  `/health` endpoint yet; should get one per the fleet standard once Phase 1
  work starts touching that repo again.
- `learnbot-mcp/docs/JAPANESE_LEARNING.md` — the lesson tools Phase 5b calls.
- `learnbot-mcp/docs/DISTANCE_LEARNING.md` — the wider teaching-agent
  architecture this could eventually plug into (not required for Phase 5b).
