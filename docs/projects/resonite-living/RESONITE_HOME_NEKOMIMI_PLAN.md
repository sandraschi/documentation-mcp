# Nekomimi-chan's Resonite Home — Master Plan

**Created**: 2026-07-17 · **Updated**: 2026-07-18 · **Status**: Phase 0 CLOSED
(all six runbook steps GREEN — READ/WRITE/mesh-import/render/material
live-verified, Marble export formats enumerated, formal decision note
written) — **Phase 1 open**. Project home:
`projects/resonite-living/README.md`.
**Goal**: A generated, persistent, private Resonite home world with Nekomimi-chan
present as an embodied, persona-driven agent — chatting, emoting, speaking.
This is the culmination project for the avatar/world building-block repos.

---

## 1. Deep analysis — what this actually is

Three production lines that converge in one world:

- **Line A — The Home** (environment): generated 3D space, walkable, collidable, persistent.
- **Line B — The Girl** (avatar): Nekomimi-chan VRM as a rigged, expressive Resonite entity.
- **Line C — The Soul** (presence): learnbot persona driving chat, voice, and emotion in-world.

The three hard truths that shape everything:

1. **Resonite cannot render Gaussian splats.** Marble (worldlabs) outputs splats;
   Resonite renders meshes. Every environment path goes through a splat-or-Marble
   → **mesh** conversion, with Blender as the refinery.
2. **CORRECTED 2026-07-17 (Sandra was right, plan v1 was a year stale):
   Resonite HAS an official external API since 2026.1.8.6 — ResoniteLink.**
   Open WebSocket JSON protocol (Yellow-Dog-Man/ResoniteLink, MIT, beta) to
   READ AND WRITE the hosted world's data model from external tools; imported
   content stays editable in-game. Enable: Dashboard → Session → Settings →
   "Enable ResoniteLink" (port displayed); headless: `enableResoniteLink <port>`
   config/CLI. The hand-built ProtoFlux OSC Hub is DEMOTED to optional fallback
   (possibly still useful for high-frequency emote streaming; measure first).
   Beta caveat: breaking changes possible, ~46 open issues — pin the client
   protocol version and watch YDM releases.
3. **resonite-mcp already implements a ResoniteLink client** (resonite_link.py
   + tools/resonite_link.py + protocol unit tests + docs/RESONITELINK_GUIDE.md
   + MARBLE_RESONITE_GUIDE.md — plan v1 called it "shape only", wrong).
   What remains unproven is the LIVE end-to-end against a running session;
   Phase 0 is still the gate, but it is now cheap: flip the toggle, connect,
   spawn a test object.

### Building blocks and their roles (months of work, mapped)

| Repo | Role | State |
|---|---|---|
| worldlabs-mcp v0.5.0 | Marble world generation (text/image/pano→3D), Spark 2.0 splat renderer for previews, DCC export pipelines incl. Resonite OSC trigger | Mature, 20 tools, competition-tested |
| resonite-mcp | The bridge: OSC/WebSocket → in-world Hub; avatar/world/ProtoFlux tools | Shape complete, **live-untested** |
| blender-mcp v0.11.0 | Mesh refinery: import, decimate, bake, colliders, glTF export | Solid (subprocess bugs fixed 07-14) |
| avatar-mcp | VRM depot (~/.avatarmcp/models/ — Nekomimi-chan lives here), VRM ops, VRChat OSC experience to reuse | Solid |
| learnbot-mcp v0.6.0 | Persona (Miko-chan), chat, **emotion tags** (already drive TTS prosody + robot), TTS via speech-mcp, soundscape module | Live daily |
| speech-mcp | Gemini TTS (Leda/Kore voices) + SAPI5 fallback | Live |
| vbot-mind-mcp v0.2.0 | Behavior-tree runtime, inter-bot comms, WebSocket bridge — autonomous idle behavior | Built 07-12 |
| splatmaker-mcp v0.2.0 | nerfstudio lane: splat→mesh extraction fallback if Marble mesh export disappoints | Real backend verified on 4090 |
| godot-mcp | VRM import pipeline + viewer — proven VRM handling patterns to crib | 0.4.0-beta.1 |
| games-app (AI Game Chest) | Japanese learning content (2,500 kanji, JLPT N5-N1 drills, spaced-repetition vocab) — potential reuse for lesson material/kanji-panel props alongside learnbot's own lesson tools; not yet wired into any phase | Mature, unrelated core purpose (games platform) |
| robotics-mcp / yahboom-mcp | Boomy (Yahboom Raspbot) real robot control — candidate for the Phase 6 "virtual twin in the home" bonus item, not required for Phases 1-5 | robotics-mcp v1.4.1, yahboom-mcp live daily |
| Today's work | VRMViewer expression set (neutral/happy/angry/sad/relaxed/surprised) + viseme cycling = **the canonical emote protocol** to mirror in-world | Live |

**Note (2026-07-18)**: `avatar-pipeline-mcp` is a deprecated stub — its creative-pipeline
functionality was folded into `avatar-mcp`'s `avatar_pipeline` portmanteau tool
(webapp `/pipeline` on 10792, API 10793). Do not run it alongside avatar-mcp;
any Phase 4 VRM-pipeline work should target avatar-mcp directly.

### Key architectural decision: NPC, not player avatar

Nekomimi-chan "appearing in the home" means an **embodied agent** (NPC driven by
learnbot), not Sandra's wearable avatar. Both come from the same import, but the
NPC path avoids Resonite's full avatar-creator anchoring work in v1 and lets
Line C drive her directly. Wearable version is a Phase 6 bonus.

### Two-stage engagement (confirmed 2026-07-18)

Sandra's acceptance framing for "it works," in order:

1. **Desktop, outside VR** — host the session on Goliath, watch Nekomimi-chan
   idle/dance in the client window, talk to her (mic → STT → persona → TTS,
   no HMD). This is Phase 4 (static expression cycling) + Phase 5 (chat/voice/
   emote) as already scoped — no new subsystem, just the bar for "phase 5 is
   done": conversation works from outside the world before anyone straps on
   a headset.
2. **Embodied, in-world** — Sandra enters via Pico 4 HMD in her own avatar,
   walks up to Nekomimi-chan, and she reacts to presence/proximity/gaze (not
   necessarily true vision — Resonite already tracks proximity and look-at,
   which is the honest first implementation; a live vision model reading her
   camera feed is a distinct, much larger scope and should not be assumed as
   part of v1 "she sees you"). This is the existing wearable-avatar Phase 6
   item, but promoted conceptually to "the actual point of Phase 5" rather
   than a bonus — same reasoning as the Phase 5b keigo-lesson promotion.

### LLM backend for the persona (Line C)

Local inference on Goliath's 4090, zero marginal cost per turn. Candidate
family: Jackrong's Qwen-based distills (see `models/JACKRONG_DISTILL_FACTORY.md`
for the full hardware-fit table). Two things to reconcile before committing:
- That doc's current recommendation is **Qwopus 3.6 27B (Coder-MTP variant)**
  as the 4090 sweet spot (MTP speculative decoding, 1.4-2.2x speedup).
- A different sub-family, `Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled`,
  has a community tool-calling benchmark (tester "Chris Klaus") showing only
  the **27B** size holds stable structured tool-calling among Qwen3.5 quants —
  relevant here because the conductor needs the model to emit gesture/dance
  triggers alongside dialogue, not just free text. Worth checking whether the
  3.6/MTP line has an equivalent benchmark before assuming it inherits that
  stability; if not, the 3.5-27B-Opus-distill may be the safer pick for the
  tool-calling path specifically, at some cost in raw speed vs. the MTP model.

### The emote protocol (reuse today's webapp work)

The Avatar page shipped today established the contract: expression ∈ {neutral,
happy, angry, sad, relaxed, surprised}, talking on/off (visemes), look-at
target. The in-world Hub should accept exactly this vocabulary over OSC
(`/nekomimi/expression s`, `/nekomimi/talking i`, `/nekomimi/lookat fff`), so
webapp, robot (Boomy mapping already exists), and Resonite all speak one
emotion language driven by learnbot's existing emotion tags.

---

## 2. Phases

### Phase 0 — Reality-check spike (REVISED: ResoniteLink-first, ~half a day)
Recon done 2026-07-17: Resonite IS installed (Steam, C: library), worldlabs
API key configured, resonite-mcp Link client exists. Remaining steps — see
**RESONITE_PHASE0_RUNBOOK.md** (agent-actionable, works for Fable/opencode/DS4):
1. Sandra (30s, in-client): launch Resonite desktop mode, host a session,
   Dashboard → Session → Settings → Enable ResoniteLink, note the port.
2. Agent: read docs/RESONITELINK_GUIDE.md + configure resonite-mcp with the
   port; connect; read the world data model (prove READ).
3. Agent: spawn/modify one test object (prove WRITE). Then import one glTF
   test asset (prove ASSET path — this is the make-or-break capability;
   if Link's beta doesn't do asset import yet, fallback = local HTTP bridge
   serving the file + in-world import, or manual drag-drop).
4. Agent: one small Marble generation via worldlabs-mcp (key verified) to
   confirm which export formats the account offers (mesh/collider/splat).
   Study MARBLE_RESONITE_GUIDE.md first — the pipeline is pre-designed.
5. **Decision gate**: READ+WRITE+ASSET all green → Phases 1-5 proceed on
   Link. ASSET red → drag-drop fallback for imports, Link keeps runtime
   control (emotes/chat still fully automated). Reference implementations
   to crib from: Yellow-Dog-Man/ResoniteLink sample REPL client (C#, MIT)
   and rassi0429/resolink-mcp (community MCP server for Link).

### Phase 1 — Generate the home (1 day, after gate)
0. **Before spending any Marble credits**: three free test fixtures already
   exist in `~/Downloads` from the Marble Adventure competition (each a
   `.spz` splat + `_collider.glb` mesh pair — "Modern Tropical Luxury
   Residence", "Neuschwanstein Castle Moonlight Night", "St. Peter's
   Basilica Grand Interior"). None match the brief below, but each
   `_collider.glb` is a real Chisel-generated simplified triangle mesh
   (2-6MB) — exactly the input the Blender-to-mesh-JSON bridge script
   (handoff next-work item 4) needs to prove itself on before it ever
   touches the actual home geometry. Run the bridge against these first.
1. Prompt-engineer 3–5 Marble candidates (PROMPT_GUIDE.md). Suggested brief:
   Japanese hillside shrine-house at golden hour, engawa veranda, paper lanterns,
   Vienna Altbau touches (parquet, double doors) — the miko theme resonite-mcp's
   README already carries. Sandra picks the winner (taste gate — hers).
2. Export: mesh + textures if Marble offers it; splat always (keep for WebXR
   preview via Spark — she can walk the candidate on Quest before committing).
3. Fallback if mesh export is poor: splatmaker nerfstudio lane (splat→Poisson/
   TSDF mesh) — quality gate applies.

### Phase 2 — Refine in Blender (1–2 days)
Two distinct jobs for blender-mcp, not one:
1. **Shell refinery**: import Marble's splat-adjacent mesh/collider export →
   cleanup (fill holes, delete floaters) → decimate to Resonite-friendly
   budget (target <150k tris for the shell) → bake lighting/AO into
   textures → separate simplified collision mesh → glTF export. Carve door
   openings / flatten floor where generation is mushy.
2. **Furniture kit-bash**: blender-mcp's own asset construction (not Marble
   object-mode) builds the kotatsu, low table, and other interior props —
   Marble generates the shell, Blender populates it. Same export pipeline
   as the shell (glTF → mesh-JSON), just a second, independent set of
   source geometry.
Script both as a repeatable `just home-refine` / `just furniture-build` so
regeneration is cheap.

### Phase 3 — World assembly (1 day)
Import shell + colliders via Hub (or drag-drop fallback), ground per EXPORT_GUIDE
(collision proxies auto-grounded), lighting pass, spawn point, world permissions
(private home), install Hub permanently, **save world**. Deliverable: the home
exists and persists.

**World/session decision (researched 2026-07-18, wiki.resonite.com)**: the
home is its own dedicated World, hosted as its own Session — not a room
bolted onto an existing world. This matches how Resonite actually models
"home": a Session is a live instance of exactly one World with exactly one
host, and closes when the host quits. Two consequences to design around:
- **Access level**: Private (invite-only), likely also ticking "Don't show
  in session lists" — this is a personal home with an embodied AI persona,
  not something that should be Registered/Anyone-discoverable. If Sandra
  ever wants to show it to Marion or Steve, invite them directly; don't
  make it publicly joinable to get there.
- **Persistence**: a session dies when its host quits. For "always there"
  the way a home should be, the world needs either Sandra's client hosting
  it whenever she's playing (fine for now), or a headless server hosting it
  in the background later if 24/7 availability matters (revisit once Phase
  3 actually ships — not a Phase 0-3 blocker).

**Getting there ("teleport") has two different meanings, and ResoniteLink
covers neither directly**:
1. *Moving to a spot inside the home* (e.g., to the kotatsu) — Resonite's
   real mechanism is an `AvatarAnchor` component + a trigger (touch trigger
   or the "Anchor User" ProtoFlux node), which sets the user's root slot's
   global position/rotation to a reference slot. Buildable via
   `add_slot`/`add_component` (untested — next spike item, not yet proven
   like the mesh-render chain was).
2. *Moving from wherever Sandra currently is into the home session* — this
   is session-level, not a data-model operation, so it is NOT something
   ResoniteLink's WebSocket exposes at all (its messages only operate on an
   already-connected session). The real options are: join via Dash → World
   browser/session list, a direct session invite/link, launching with
   `-Join <url>` (scriptable), or an in-world "world orb" portal placed
   somewhere she already spends time.

**Etiquette note, worth keeping in mind for any automation we build**: the
Resonite community treats non-consensual movement between worlds as a real
problem — world/session orbs can pull a user in by accident, and there's an
open community request (Yellow-Dog-Man/Resonite-Issues #2808) for a setting
to prevent being forced into worlds unwillingly. That norm is about *other*
people being moved without asking; Sandra scripting her own avatar's
movement with her own tools is normal and expected in Resonite's
automation-friendly culture (ProtoFlux exists for exactly this). It only
becomes a real etiquette question if the home ever has visitors and we're
tempted to auto-pull them in rather than letting them walk through the door
themselves.

### Phase 4 — Nekomimi-chan enters (1–2 days)
1. VRM from avatar depot → Blender (VRM addon) → glTF/FBX export tuned for
   Resonite (MToon → approximated toon shader; check community VRM importer
   first — research item, may skip Blender leg entirely).
2. In-world: rig as NPC entity, springbones/wiggle for ears + tail + hair
   (Resonite dynamic bones), expression setup mapping blendshapes to the six
   canonical emotes + visemes.
3. Static test: cycle expressions via OSC from resonite-mcp. Same test matrix
   as today's webapp page.

### Phase 5 — The Soul (2–3 days)
1. **Chat**: learnbot conversation → resonite-mcp → in-world text panel above
   her head (Hub renders incoming text).
2. **Voice**: speech-mcp TTS → bridge serves WAV/stream URL → Resonite audio
   stream component at her position (spatial). Latency target: <2s utterance start.
3. **Emotes**: learnbot emotion tags → OSC expression (protocol above) +
   talking flag during TTS playback (viseme cycling in-world, real phoneme
   lip-sync later — same roadmap item as the webapp).
4. **Idle life**: vbot-mind behavior tree — wander waypoints, look at visitor,
   greet on join, sit on engawa at "evening" (world clock).
5. Deliverable: walk in, she turns, greets you in Japanese, and means it.

### Phase 5b — First use case: the keigo lesson (promoted 2026-07-18, was
Phase 6 pick-and-mix — Sandra wants this as the actual first thing the home
is *for*, not a demo afterthought)
Nekomimi-chan (voiced by learnbot's Miko-chan persona) teaches a real lesson
at a kotatsu in the home. This is not a new subsystem — it is Phase 5's
chat/voice/emote wiring pointed at learnbot-mcp's existing, **verified-real**
lesson tools (checked 2026-07-18 against `src/learnbot_mcp/lessons.py` —
no phantom-API risk here, unlike three other fleet instances this project
already caught):

1. `lesson_generate(title="basic keigo", language="ja", level="N4")` — LLM
   drafts a structured lesson (sections/vocab/quiz) and saves it.
2. `chat_start(persona="miko")` — opens the conversation that will carry the
   lesson; this is the same conversation whose turns already drive the
   emote/TTS pipeline from Phase 5 steps 1-3.
3. `lesson_run(lesson_id, conversation_id)` — injects the lesson as active
   curriculum; each section becomes an assistant turn, so the existing
   chat→OSC-expression→TTS chain speaks and emotes the lesson content
   with zero new plumbing.
4. Sandra's replies go through normal chat turns; `grammar_check(text,
   source_lang="ja")` can run alongside for corrective feedback rendered as
   a second text panel or spoken aside.
5. `lesson_differentiate(lesson_id, target_level=...)` on the fly if the
   pacing is wrong — same conversation, harder or easier version swapped in.

Staging: a kotatsu prop + low table (Marble object-mode or Blender kit-bash,
Phase 6 furniture item) and a second text panel for corrections. Everything
else — her presence, voice, expressions — already exists once Phase 5 lands.
**This is the reason Phase 5 is worth building**, not a bonus on top of it.

### Phase 6 — Polish & fleet tie-ins (ongoing, pick-and-mix)
Furniture/prop generation (Marble object mode or Blender — kotatsu now
promoted to Phase 5b, not deferred), photo frames fed by immich-mcp,
bookshelf mirroring calibre-mcp library, aiwatcher news panel, soundscape
module ambience, wearable avatar variant, Boomy the robot getting a
virtual twin.

**Total to "she greets you in your generated home": ~7–10 AI-assisted days,
of which day 1 (Phase 0) decides everything.**

---

## 3. Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| In-world Hub bootstrap (ProtoFlux OSC) harder than documented | HIGH | Phase 0 gate; drag-drop fallback keeps all phases alive minus automation |
| resonite-mcp aspirational code paths (fleet phantom-op pattern!) | HIGH | Live-test each tool in Phase 0; expect fixes; budget half a day |
| Marble mesh export quality/availability | MED | splatmaker nerfstudio fallback; worst case Blender kit-bash using splat as reference |
| VRM fidelity loss (MToon, springbones) in Resonite | MED | Community VRM importer research; godot-mcp pipeline as reference; acceptable v1 = flat toon |
| TTS streaming latency in-world | MED | Pre-generated greeting lines cached; streaming only for conversation |
| Marble API cost | LOW-MED | Budget-aware: batch candidate generation once, preview via free Spark renderer before regen |
| Resonite platform changes | LOW | Everything file-based (glTF) survives; only Hub/OSC layer is platform-coupled |

## 4. What to do first
Phase 0, step 1: install/launch Resonite, then run resonite-mcp against it and
build the debug Hub together (guided ProtoFlux, screenshot-verified). One
evening, and the whole plan becomes either concrete or honestly re-scoped.
