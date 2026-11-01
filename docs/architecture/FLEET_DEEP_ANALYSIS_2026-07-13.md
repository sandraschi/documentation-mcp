# Fleet Deep Analysis — Security Surveillance + Creative/VR/CAD/Robotics/Sim Chains

**Date:** 2026-07-13
**Status:** Analysis — feeds into build briefs, not itself a brief
**Author:** Claude (Sonnet 5, continuing a Fable session that hit its limit)
**Context:** Written live while aiwatcher-mcp, devices-mcp, tvtropes-mcp, and arxiv-mcp were restarted via NSSM and Fritz began polling their logs through new per-server `report_logs` tools — that pattern is itself the trigger for §1 below.

---

## 0. What changed since ORCHESTRATION_HIERARCHY.md (2026-07-12)

The three-layer hierarchy (hub / Fritz-as-client / domain supervisors) is ratified and holds. This doc doesn't revise it — it specifies what Layer 2 (Fritz) does with its client position now that a **fourth signal path** has appeared organically tonight: NSSM-managed background long-runners exposing `report_logs` tools that Fritz polls directly, outside the hub's health-status channel. That's worth formalizing before three more servers grow their own bespoke version of it.

---

## 1. Fritz upgrade: Security Surveiller

### 1.1 The gap this closes

Fritz today (v0.2.1-pre, 69 tools/15 subsystems, Intel Reports Hub :11027) already ingests aiwatcher and does `devices_watch`. What's new tonight isn't the data sources — it's the *pattern*: NSSM restarts a background service, and instead of waiting for the next scheduled digest, Fritz reaches into that service's own log stream via a tool call the moment it's back up, to answer one question — **does anything in here need a human right now?** That's a distinct capability from "ingest the daily digest" and deserves a named subsystem rather than living as an ad hoc `devices_watch` extension.

### 1.2 Proposed subsystem: `fritz_surveil`

A new portmanteau tool family, ops: `scan_now(server_id)`, `scan_all()`, `set_thresholds(server_id, rules)`, `history(server_id, since)`, `ack(alert_id)`.

**Mechanism:**
1. On NSSM start/restart event (or on a tight poll cadence — 60–120s — for servers that don't emit restart events), Fritz calls that server's `report_logs` tool.
2. A per-server **triage rule set** (small YAML, not code) maps log content to severity. Two rule types cover tonight's examples:
   - **Sensational/urgency rule** (aiwatcher): already has urgency 0–10 scoring built in — `fritz_surveil` just subscribes to items ≥ threshold instead of waiting for the daily digest. This is thin — mostly wiring, not new intelligence.
   - **Threshold/comfort rule** (devices-mcp): "bathroom temp > X°C" is a **new class** for Fritz — a numeric sensor-log condition, not an LLM-scored urgency. This needs a small rules-matching layer: `{server: devices-mcp, metric_path: "sensors.bathroom.temp_c", op: ">", value: 28, severity: "notice"}`. Straightforward but distinct code path from the urgency-score path.
3. Triage classifies each hit into: `informational` (logged, no push), `notice` (batched into next digest), `urgent` (immediate push via **admiral-mcp `notify`**, §0.3 of the iOS plans doc — this is the concrete use for that op beyond Benny FM).
4. Everything lands in the Intel Reports Hub as before — `fritz_surveil` doesn't create a new data store, it creates a new *ingestion trigger and severity path* into the one that exists.

**Effort:** ~1.5 d. Mostly the triage-rules engine (generic enough to cover aiwatcher's existing 0–10 score AND devices-mcp's numeric thresholds AND — see 1.4 — tvtropes/arxiv content flags) plus the NSSM-event or poll hook plus the admiral `notify` wire-up.

### 1.3 Why "Security Surveiller" is the right frame, not "log watcher"

Calling it a log watcher undersells it and misses the actual security posture question, which is two-sided:

- **Outward-facing (the tonight scenario):** is something in the world worth waking Sandra up for? Sensational AI news, an overheating bathroom, eventually: an unexpected device on the LAN, a failed login somewhere, a webhook that shouldn't have fired.
- **Inward-facing (fleet self-defense):** deepfang already does sanitize→adjudicate→dispatch with hard Docker isolation for *executed actions*. Fritz's new surveillance layer is the natural place to watch the fleet's own logs for the precursors deepfang doesn't see — a server logging repeated auth failures, a webapp's `/api/health` starting to fail, an NSSM restart loop (3 restarts in 10 min = something's wrong, not transient). This doesn't duplicate deepfang; deepfang gates *actions*, Fritz-surveil watches *state*.

Recommend the subsystem name make this explicit: `fritz_surveil` handles both `domain: "external"` (news, environment, security-adjacent world events) and `domain: "fleet"` (service health precursors, restart loops, auth anomalies) sources, sharing one triage/severity/notify pipeline. One engine, two source categories — not two subsystems, because the escalation logic (informational/notice/urgent → admiral notify) is identical.

### 1.4 Immediate candidate sources beyond tonight's four

Once the engine exists, wiring a new source is a YAML rule file, not new code:
- **tvtropes-mcp** — its curl_cffi crawler logs are a natural `fleet`-domain source (crawl failures, rate-limit hits); its extracted content is not really a `fritz_surveil` candidate (no urgency signal there).
- **arxiv-mcp** — the `codehunt` and `firefront` scans already produce structured digests; a `notice`-tier rule ("open-weight repo drop matching a watched author") turns this into a push instead of waiting for Benny FM's next scheduled read.
- **deepfang** — its adjudicator bridge logs are the highest-value `fleet`-domain source not yet wired: an adjudicator override or a sanitizer catching something above its threat-score threshold should be `urgent`, always.
- **devices-mcp** beyond temperature: door/motion sensors already in the Tapo/Hue/Ring/Nest/Shelly inventory are one rule-file addition each, not new integration work.

### 1.5 What this is *not*

Not a rebuild of aiwatcher's LLM distillation (keep that where it is), not a new dashboard (Intel Reports Hub already exists), not a replacement for the hub's `/api/health` polling (that's liveness; this is content-aware triage of servers that are already healthy). Scope discipline matters here — the temptation is to let `fritz_surveil` grow into a SIEM. Resist; it's a triage router with one destination (admiral notify) and one store (Intel Reports Hub).

### 1.6 Addendum (2026-07-13): Proof-of-Life as a `fritz_surveil` mode

**The pitch (Sandra):** camera sees no movement for N hours, mailbox overflowing, no reaction to a spoken liveness check ("hello, how are you") — gated by a known-absence calendar (shopping, café, holiday in Japan) so it doesn't cry wolf. "Everybody should have that" — agreed; this is a real safety feature disguised as a fleet curiosity, worth building properly rather than bolting on as an afterthought rule.

**Why it's not just another `fritz_surveil` rule:** every source in §1.4 is stateless — a log line crosses a threshold, triage fires, done. PoL requires **state that persists across the absence window**: a presence/absence machine, not a threshold check. Model it as its own mode, not a YAML rule:

- **States:** `present-normal` → `present-no-signal` (movement/response absent, timer running) → `pol-check` (escalating: camera re-check → speech liveness prompt → phone call/push to a trusted contact, e.g. [[brother]] as the existing backup-contact relationship) → `resolved` or `escalated`.
- **Known-absence gate:** a simple calendar/manual toggle ("away until Tuesday", set from admiral-pager or Benny FM's existing push channel with one tap) suppresses the whole state machine. Source data: devices-mcp already tracks door/motion; a manual "I'm heading out" toggle is the cheapest correct answer — don't try to infer absence from GPS/calendar automatically as v1, that's a false-negative risk in exactly the scenario that matters.
- **Signal sources:** camera motion (devices-mcp, existing), mailbox sensor (devices-mcp, if not already wired — check inventory), speech liveness check (speech-mcp TTS prompt + STT listen, reusing the FunASR pipeline already used elsewhere in the fleet).
- **Escalation destination:** admiral `notify` first (self-check: "you've been still for 6h, tap to confirm you're OK"), then — only past a second threshold with no response — an actual contact, not silently logged. This is the one `fritz_surveil` source where `urgent` severity must be able to bypass the phone entirely if the phone itself is the non-responding device.

**Scope discipline:** this is explicitly NOT a general eldercare/health monitoring platform — no vitals, no fall-detection ML, no cloud health-data anything (that would collide with the fleet's own privacy posture). It's presence-liveness plus absence-gating, built from sensors and pipelines that already exist. Estimate: 1–1.5 d once `fritz_surveil`'s core engine (§1.2) exists, since PoL is a state-machine mode on top of it, not a parallel system.

#### 1.6.1 Refinement (2026-07-13, same session): location-aware stillness, not just stillness

Sandra's own example sharpens the design: **stillness alone isn't the signal — stillness plus location context is.** Eight hours motionless in bed at night is Tuesday. Twenty minutes motionless on the living-room floor is very possibly a fall. Same raw sensor input (no movement), opposite meaning, because *where* the stillness is changes everything. This means the state machine from §1.6 needs a **location/posture classifier as a precondition**, not just a duration timer:

- **Zone-aware thresholds, not one global timer.** Each camera-covered zone gets its own stillness threshold and normal-hours profile: bedroom — long threshold (hours), only alarming outside expected wake time; living-room floor, hallway, bathroom floor — short threshold (minutes), alarming any time, since "on the floor, not on furniture" is itself close to the signal regardless of duration. This is a per-zone YAML config, not new ML — devices-mcp's existing camera feed plus a simple "which zone, on-furniture-or-floor" heuristic (even a coarse one: motion-zone bounding box vs known furniture regions) gets most of the value without pose-estimation modeling.
- **Two severity tiers inside PoL, not one.** "Not moving in bed for N hours during expected sleep" — low tier, self-check nudge only ("still asleep? tap if you're up"), long fuse. "Not moving on the floor for N minutes" — high tier, short fuse, skips the self-check-first step and escalates straight to a phone call to [[brother]] — a text or push is the wrong instrument for a possible fall; a ringing phone forces attention in a way a notification doesn't. Sandra's own sequencing ("alert Steve for a phone call, we escalate from there") is the right order: phone call is the escalation, not the last resort after a delay.
- **Why this stays in scope despite sounding like fall-detection:** it isn't pose-estimation or vitals — it's zone-and-duration logic layered on the motion signal devices-mcp already has, plus routing rules. The line to hold: no ML model classifying "this looks like a fall" from video (that's a real health-tech product, out of scope here); just "stillness in a floor-zone for longer than a normal person would voluntarily lie on a floor" as a threshold rule. Cheap, honest about its own crudeness, and privacy-preserving in the same way the rest of devices-mcp already is — motion/zone events, not stored video analysis.

---

## 2. The four production chains

The fleet has quietly assembled four multi-server chains that are each individually SOTA-compliant but have never been described as chains. Naming them matters for two reasons: it reveals where the *connective tissue* between servers is thin or missing, and it's the honest answer to "what does this fleet actually do" that a single alphabetical FLEET_INDEX can't convey.

### 2.1 Artistic / creative chain

```
 IDEATION            GENERATION              REFINEMENT           OUTPUT/DELIVERY
┌──────────┐      ┌───────────────┐      ┌───────────────┐    ┌──────────────────┐
│ (prompt/  │─────▶│ comfyops-mcp   │─────▶│ blender-mcp    │──▶│ tahoma2d-mcp      │
│  photo)   │      │ (image/video,  │      │ (3D mesh from  │   │ (headless render, │
└──────────┘      │  4090, VRAM     │      │  Tripo/Rodin/  │   │  .tnz → ffmpeg)   │
                   │  guard)         │      │  Hunyuan, GP)  │   └──────────────────┘
                   └───────┬────────┘      └───────────────┘
                           │                                       ┌──────────────────┐
                           │ (audio side)                          │ songgeneration-   │
                           ▼                                       │ mcp (jingles,     │
                   ┌───────────────┐      ┌───────────────┐        │ scoring)          │
                   │ vcv-rack-mcp   │◀────▶│ osc-mcp        │      └──────────────────┘
                   │ (patch author, │  OSC │ (transport,   │
                   │  depot, Phase  │      │  live control)│
                   │  5 complete)   │      └───────┬───────┘
                   └───────────────┘               │
                                                    ▼
                                            (pocket-patch, planned —
                                             phone as performance surface)
```

**What's real:** comfyops (MVP, image/video), blender-mcp (mature — 48+ tools, AI mesh, vision loop), tahoma2d (render orchestrator, explicitly documented as "renders blender-mcp GP output" — this is the fleet's only server whose README already names another server as its upstream, which is exactly the pattern the rest of this doc argues for generalizing), vcv-rack-mcp (Phase 5 complete, webapp done, gated only on Sandra's reference patches).

**What's thin:** no server owns "ideation" — prompts and photos enter by hand at comfyops or blender. That's fine (Ekphrasis, from the iOS plans doc, is exactly this entry point via phone camera). More importantly: **comfyops and vcv-rack don't talk to each other**, and there's no obvious reason they should yet — but a generated video (comfyops) with a generated score (vcv-rack, rendered via a Lane 3 audio-render path that's explicitly deferred per the gap analysis) is a natural fusion point once both are unblocked. Flag, don't build.

**Gap:** songgeneration-mcp exists (referenced in the iOS backlog for Benny FM jingles) but isn't in FLEET_INDEX's visible chain language anywhere — worth a one-line README cross-reference from vcv-rack-mcp and comfyops-mcp pointing at it, per the tahoma2d precedent, so the chain is discoverable from any node in it.

### 2.2 VR / social-presence chain

```
        AVATAR LAYER                    WORLD LAYER                  SOCIAL LAYER
┌────────────────────────┐      ┌──────────────────────┐      ┌───────────────────┐
│ avatar-mcp              │      │ worldlabs-mcp         │      │ resonite-mcp       │
│ (VRM mgmt, Unity/       │◀────▶│ (Marble: text/image/  │─────▶│ (social VR, Agent  │
│  VRChat, OSC anim,      │  OSC │  video/multi-image →  │ DCC  │  Lab Phase 6,      │
│  16 portmanteau tools)  │      │  3D Gaussian splat;   │export│  voice, strict E2E)│
└───────────┬─────────────┘      │  Spark 2.0 viewer;    │      └───────────────────┘
            │                    │  DCC export to        │
            │                    │  Blender/Unity/        │      ┌───────────────────┐
            ▼                    │  Resonite; Painting    │      │ VRChat (via        │
┌────────────────────────┐       │  Portals ×14)         │      │  avatar-mcp/        │
│ unity3d-mcp             │◀──────┴──────────────┬────────┘      │  myvrworlds)        │
│ (Hands-In/Off, import,  │                      │               └───────────────────┘
│  validation)            │                      ▼
└────────────────────────┘              🏆 Marble Adventure
            ▲                            (Godot 4.4 hub game,
            │                             8 portals, itch build —
            └────────── unifying dashboard ────────┘
                    myvrworlds (React/Tailwind control
                    center: Avatar + Blender + VRChat +
                    Resonite + OSC + Unity3D + dual-STT
                    chatbot)
```

**What's real:** this is the fleet's most mature multi-server chain — myvrworlds already exists specifically as the unifying control surface, which is unusual foresight (most chains in this fleet were discovered after the fact, this one was built as a chain deliberately). worldlabs-mcp's DCC export to three different targets (Blender/Unity/Resonite) makes it the connective hub of the whole thing, not avatar-mcp — worth correcting the mental model if "avatar-mcp is central" was the assumption; it isn't, worldlabs is.

**Gap, concretely:** Séance (iOS backlog §5.3) is the missing *outward* channel — everything above is desktop/headset-bound; nothing pushes to the phone. That's the correct next increment, not a new desktop server.

**Cross-chain note:** worldlabs → Blender is a second entry point into the artistic chain above (2.1) that the diagram there doesn't show. A photographed courtyard can become a Marble world (VR chain) OR get Blender-refined into a mesh (artistic chain) from the *same* worldlabs export. Worth a shared "export destinations" note in worldlabs-mcp's README rather than duplicating the DCC-export logic conceptually in two chain docs.

### 2.2.1 Worked example (2026-07-13, Sandra): a Louis XIV settee in a Marble room, then hop into Resonite

Grounded against actual tool inventories, not invented — blender-mcp's README already draws resonite-mcp as a downstream node in its own architecture diagram ("resonite-mcp (world injection, ResoniteLink, OSC)"), and worldlabs-mcp's DCC export explicitly targets Resonite (OSC), Unity3D, and Blender. The pipeline exists at the tool level today; nobody's walked it end to end as a named example, which is worth doing once so the §3 contract has a concrete case to apply to.

1. **Room:** worldlabs-mcp generates the room as a Marble Gaussian-splat world (text/image prompt, optionally LLM-refined into worldlabs' 20-line technical description format).
2. **Splat → workable scene:** worldlabs' asset response for a generated world **already includes `assets.mesh.collider_mesh_url` — a collision mesh in GLB format returned alongside the splat**, per worldlabs-mcp's own README ("World assets returned" section). Correction from an earlier pass of this doc, which had Blender's `blender_splatting` generating the collision mesh from scratch — wrong: **the real risk at this step is a plumbing failure, not a missing capability.** The pipeline must (a) explicitly request mesh assets in the generation call (verify this isn't a flag that defaults off), (b) actually fetch `collider_mesh_url` alongside the splat rather than only pulling `spz_urls`, and (c) hand the downloaded GLB off to Blender/Resonite as its own tracked artifact — not regenerate it. `blender_splatting`'s collision-mesh tool remains useful as a **fallback** (hand-authored splats, or a worldlabs response where mesh generation was skipped) but should not be the default path when a room comes from worldlabs. This is exactly the §3.2 manifest/ack contract's job: `collider_mesh_url` is a second artifact in the same job's manifest, and "was it actually downloaded and handed off" is a checkable pass/fail, same as everything else in that contract — the failure mode shifts from "nobody computed a collision mesh" to "the collision mesh existed on worldlabs' server the whole time and the pipeline code just didn't ask for it or lost it in transit," which is a more mundane and more likely bug.
3. **Settee:** `blender_ai_generate` (Tripo/Rodin/Hunyuan backend) from a period-styled prompt — cabriole legs, serpentine back, scrollwork, whatever the LXIV brief calls for. Optionally: generate reference texture images (gilt wood, brocade/damask upholstery) via **comfyops-mcp** and feed them into Blender's shader graph for materials — a real instance of the artistic-chain fusion point §2.1 flagged as "worth naming, not built": comfyops feeding blender-mcp's material pipeline is exactly that fusion, occurring naturally in this example rather than needing a bespoke bridge.
4. **Refine + verify:** `blender_vision_refine` (screenshot-based agent review loop) is blender-mcp's own built-in answer to §3.4's CUA-verification point for this stage — use it, don't skip it, since "the AI-generated settee looks like a settee and not a geometry-error blob" is not knowable from a tool-call return value.
5. **Compose:** place the settee into the room scene in Blender (manual or geonodes-snap-to-floor using the collision mesh from step 2 as the placement surface).
6. **Export decision (open choice, not resolved here):** `blender_export` supports Resonite directly. Two options: (a) export the composed room+settee as one combined asset — simpler, one handoff, but the settee can't be independently grabbed/moved once in Resonite; (b) export room and settee **separately**, let resonite-mcp's world-injection place the settee into the already-imported room — more idiomatic for social VR (users expect to pick things up and move them) but means the manifest/ack contract from §3.2 needs to track two artifacts with a positional dependency, not one. Recommend (b) for anything meant to be lived-in rather than viewed, but this is a real design decision to make at build time, not a default to assume.
7. **Into Resonite:** resonite-mcp's world-injection (ResoniteLink, OSC) imports the room and settee per the choice in step 6. Agent Lab Phase 6 already covers Marble integration, voice, and strict E2E per FLEET_INDEX — worth checking at build time whether "import a worldlabs room" is already a tested path there rather than assuming it needs building from scratch.
8. **Hop in:** putting on the headset and walking into the space is correctly outside the pipeline's scope — the terminal step is a human enjoying the result, not something to automate.

**One concrete finding surfaced by tracing this, not hypothesized:** worldlabs-mcp's README lists its Blender DCC export bridge as port **10740**; blender-mcp's own README lists its ports as **10848/10849**. That's either a stale reference in one README or an actual second bridge port nobody's documented the purpose of — worth a 10-minute check next time either repo is touched, before anyone tries to build this pipeline and gets a connection-refused error tracing back to a three-digit typo from some earlier port reshuffle.

**Correction log (2026-07-13, Sandra):** the collision-mesh step above was rewritten after Sandra pushed back — worldlabs already returns a collider mesh, the earlier draft wrongly had Blender computing one from scratch. Left the correction inline rather than silently editing it out, since the wrong version's reasoning (artifact-level verification matters at this step) was right even though the specific mechanism was wrong — worth remembering the pattern, not just the fix.

**Forward note (2026-07-13, Sandra):** worldlabs isn't cheap, and a FOSS Gaussian-splat generation MCP (Postshot/gsplat/Nerfstudio-class tooling, not yet a fleet repo but flagged as coming soon) is a live possibility for a self-hosted, cheaper alternative. When/if that lands: **`blender_splatting`'s collision-mesh generation stops being a fallback and becomes the primary path again** — FOSS splat pipelines generally don't ship an API-side collider mesh the way worldlabs' Marble does. The "Fleissaufgabe" (make-work) framing only applies to worldlabs specifically; the tool itself is exactly right for a self-hosted splat source. Worth a one-line note on whichever future FOSS-splat-mcp README says "no collider mesh in the response — route through blender-mcp's `blender_splatting` before Resonite, this is not optional the way it is for worldlabs."

### 2.3 CAD / robotics (real + virtual) chain

> **Correction (2026-07-13, Sandra):** chip-design-mcp is an odd-duck/joke repo — no ASIC ambitions at present — and does NOT belong in a real pipeline with yahboom-mcp. It stays filed under the CAD *category* but isn't chained to anything below. The diagram below is retained for the orchestration-layer and virtualization-mcp framing, which is still accurate, but chip-design-mcp's box should be read as "parallel, unrelated hobby project," not as a pipeline partner to yahboom.
>
> **The real CAD-robotics link, if built:** a new `kicad-mcp` — simple sensor-carrier/breakout PCB design for boards mounted directly on Boomy (custom sonar/IMU carriers, new-sensor breakouts) — chained to yahboom-mcp on the hardware side. Design a board → mount it → ROS2 bridge picks up the sensor. Not briefed or sized here, just flagged as the honest answer to "what CAD tool would actually feed the robot," replacing chip-design-mcp in that role.
>
> **Joke-repo tier, named for the record:** openbci-mcp (v0.2.0, real BrainFlow/OSC integration, but genuinely dormant pending affordable skull-sensor caps — worth re-evaluating, not deleting, if that hardware improves; would slot into §2.1's artistic chain as a control-signal source, i.e. mind-controlled VCV patch, the day it's justified) and a hypothetical quantum-mcp, which **does not exist** in FLEET_INDEX — confirmed absent, filed here so a future search for it finds this note instead of nothing.

```
   VIRTUAL/SIM SIDE                              REAL-HARDWARE SIDE
┌────────────────────────┐               ┌────────────────────────────┐
│ chip-design-mcp         │               │ yahboom-mcp                 │
│ (RTL→GDSII: Yosys,      │               │ (ROS2 bridge, Boomy robot;  │
│  cocotb/iverilog sim,   │               │  sonar/vision/IMU, PTZ,     │
│  OpenLane, Magic/       │               │  Ollama Gemma 3 1B          │
│  netgen/OpenSTA;        │               │  autonomous missions)       │
│  37+ tools)             │               └──────────┬──────────────────┘
└────────────────────────┘                           │
                                                        ▼ (planned, gap analysis §7)
┌────────────────────────┐               ┌────────────────────────────┐
│ virtualization-mcp      │               │ boomy nav Phase N1          │
│ (Gold Standard —        │               │ (ArUco marker map,          │
│  VirtualBox/Hyper-V,    │               │  EKF localization —         │
│  60+ ops)               │               │  Boomy's Leash Lane B       │
└────────────────────────┘               │  supplies the survey data)  │
                                          └────────────────────────────┘
       ORCHESTRATION LAYER (RoboFang domain — one node in the hub)
┌──────────────────────────────────────────────────────────────────────┐
│ universal-actuator-mcp (gateway, 10744/45) + robofang (supervisor,   │
│ 10870/71/72) — council reasoning, hands, safety preflight            │
└──────────────────────────────────────────────────────────────────────┘
```

**What's real:** this is the fleet's most *disconnected* chain despite the name — chip-design-mcp (silicon simulation) and yahboom-mcp (physical robot) share no data path today, and arguably shouldn't force one; they're both "CAD/robotics" by category, not by pipeline. The honest structure here is two parallel verticals under one orchestration layer, not a chain like 2.1/2.2.

**What connects them, if anything does:** virtualization-mcp is the closest thing to connective tissue — VM-hosted CI for chip-design's cocotb sim runs, and potentially a VM sandbox for yahboom mission scripts before they touch the real robot (RoboFang's safety-preflight concept already gestures at this, per FLEET_CONTROL_PLANE.md's Phase 4 Sentinel roadmap). That's a real gap worth naming: **there's no "sim before real" gate for yahboom missions today** — Ollama Gemma 3 1B composes an autonomous mission and it runs directly on hardware. chip-design has cocotb between RTL and physical synthesis; yahboom has nothing between mission-composition and the actual motors. Given deepfang and RoboFang's safety-preflight doctrine already exist, this is a **documented pattern the robotics vertical hasn't adopted yet**, not a missing capability — closing it means wiring yahboom mission dispatch through the same preflight gate chip-design conceptually enjoys via simulation.

**Recommendation:** don't build a "digital twin of Boomy" server — that's overscoped for what's needed. Instead: RoboFang's existing safety-preflight (Phase 4 Sentinel) should gain a yahboom-specific check — mission script static analysis (bounding-box / velocity limit check against the known flat map) before dispatch, same spirit as cocotb's compiler-feedback loop, much cheaper to build. ~1 d once Sentinel Phase 4 is touched.

### 2.4 Simulators (cross-cutting, not a pipeline)

Unlike 2.1–2.3, "simulators" isn't a chain — it's a *capability* that shows up inside three unrelated verticals, worth naming once so future briefs don't reinvent the wheel:

| Server | What it simulates | Feedback loop pattern |
|---|---|---|
| chip-design-mcp | Digital logic (cocotb/iverilog) | Compile → simulate → assert → loop, before physical synthesis |
| leanforge-mcp | Formal proof search (not physical, but structurally identical) | N parallel subagents → Lean compiler feedback → tier escalation (Ollama/DeepSeek/Fable) |
| virtualization-mcp | Whole-OS / whole-machine | VM boot → test → snapshot/rollback |
| (proposed, §2.3) | Robot mission pre-check | Static analysis against known map → pass/fail before dispatch |

The pattern all four share: **cheap, fast, reversible check before an expensive/irreversible real action** (silicon fab, published proof, production deploy, motor movement). This is worth codifying as a named fleet pattern — something like `patterns/SIMULATE_BEFORE_COMMIT.md` — because it's currently implemented four different ways with zero shared vocabulary between the teams (agents) that built each one. Not urgent, but cheap: mostly a naming/documentation exercise (~0.5 d) that pays off the next time a new domain (robotics, per §2.3) needs the pattern and an agent can be pointed at one doc instead of reverse-engineering cocotb's structure.

---

## 3. Chain reliability & the orchestration contract

**Addendum (2026-07-13, Sandra):** every chain in §2 is only as good as its weakest handoff. A furniture piece built to spec in blender-mcp is worthless if the export to Unity/Resonite/MuJoCo/Godot silently fails, or the target never checks its inbox, or Fritz never triggers the next step because the heavy CAD/DCC backend wasn't even running (most of these are **demand-only**, not long-runners — a Blender or Unity instance idling 24/7 to catch an occasional export is wasteful; but demand-only means someone has to reliably wake it, wait for readiness, and verify the handoff completed). This section names the failure mode and proposes a contract, generalized from the one server that already does it right.

### 3.1 The reference implementation already exists: mujoco-mcp

Before proposing anything new, worth noting the fleet already has a correct pattern, undersold in FLEET_INDEX's one-liner: **mujoco-mcp** ships a `state_machine.py` standard, a **file-protocol runner that's e2e-verified including offscreen PNG export**, and Playwright e2e on top of its 22 unit tests. That's the shape every chain handoff in §2 should copy — not "call the export tool and trust the return value," but a runner that (a) has an explicit state machine for the job lifecycle, (b) verifies the *artifact*, not just the tool call's exit status (the PNG actually rendered, not just "render_scene returned 200"), and (c) has e2e coverage that would catch a silent break. simbench-mcp (P4, not yet scaffolded) is explicitly meant to generalize this across mujoco/gazebo/isaac/unitree/limx — worth ensuring simbench inherits mujoco-mcp's state-machine pattern rather than reinventing verification per-simulator.

**Also worth flagging while here:** unitree-mcp already exists — Go2/H1/H1-2/G1/B2 via MuJoCo + ROS 2, the fleet-sim pattern, 12 tests. The G1 dream from earlier this session isn't starting from zero: the *simulation* side of "a G1 running around with me" is already a working fleet server, years ahead of the hardware being affordable. Worth remembering next time that conversation comes up — the simulator exists today; only the robot and the BCI are 2030-and-a-lottery-win.

### 3.2 Proposed contract: outbox/inbox with acknowledgment, not fire-and-forget

Generalizing mujoco-mcp's pattern into a fleet-wide chain contract, three parts:

1. **Producer writes artifact + manifest, doesn't consider the job done on export success alone.** The manifest (small JSON: artifact path, checksum, source job id, intended consumer) lands in a known per-consumer inbox location. "Export succeeded" means the manifest was written and matches the artifact on disk — not that the DCC app's export dialog didn't throw.
2. **Consumer acknowledges receipt, not just presence.** A target checking its inbox and finding a manifest isn't the same as successfully importing it. The consumer writes back an ack (or nack-with-reason) before the producer's job is marked complete. This is the piece most chains in §2 currently lack entirely — tahoma2d rendering blender-mcp's GP output is the closest existing example of a named producer→consumer relationship, and even that isn't documented as having an ack step; worth checking when tahoma2d is next touched.
3. **Timeout → `fritz_surveil`, not silence.** If a manifest sits un-acked past a reasonable window, that's a `fritz`-domain event, same engine as §1 (log triage, PoL, Beweisstück) — a stalled chain is exactly the kind of "fleet health precursor" §1.3 already scoped Fritz to watch for. This is the sixth consumer of that one triage engine now; worth treating `fritz_surveil` as fleet-critical infrastructure once it exists, not a nice-to-have.

### 3.3 Demand-only backend lifecycle

Heavy CAD/DCC backends (Blender, Unity Editor, Resonite bridge, MuJoCo/Godot when not already running) need an explicit wake/ready/idle-shutdown cycle, owned by whichever component dispatches the job (today: ad hoc; should be: a documented responsibility, likely Fritz's, since it already polls health and now owns triage):

- **Health-check before dispatch** — don't assume the backend is up.
- **Start-on-demand** — NSSM or direct process launch if the health check fails, same mechanism already in use for the long-runners from tonight's session.
- **Wait-for-ready probe** — a started process isn't an immediately-usable one, especially for GUI apps with splash/load time.
- **Dispatch, then verify per §3.2**, not fire-and-forget.
- **Idle-timeout shutdown** — demand-only means shutting back down after a quiet period, not staying warm indefinitely; the threshold is a per-backend tuning question, not a fleet-wide constant (Blender's model-load cost differs wildly from Godot's).

### 3.4 CUA testing requirement for GUI-driven stages

This is the sharpest edge in the whole contract. Several chain stages (Blender GUI bridge, Unity Editor, Resonite desktop/headset) are exactly the class of app AGENT_PROTOCOLS/VERIFICATION_STANDARDS already warns about for webapp work ("desktop UI tools are not a substitute for browser verification," PYWINAUTO_MCP_SAFETY's multiplicative-risk warning) — but for these specific pipeline stages, desktop automation isn't optional, it's the only way to verify some failure modes exist at all. A blocking dialog (license prompt, "file already exists, overwrite?", a crashed-but-still-running process) can leave a tool call reporting success while the GUI is silently stuck. The fix isn't more pywinauto in general (that guidance stands, multiplicative risk is real) — it's that **chain-stage verification must check actual state, not trust the return value**: screenshot diff against an expected post-export state, file-exists-with-matching-checksum (ties back into §3.2's manifest), or an app log tail confirming the specific operation completed. mujoco-mcp's offscreen-PNG-export e2e verification (§3.1) is the existence proof this is achievable without heavyweight CUA tooling for every stage — checking the *output artifact*, not the *screen*, is usually cheaper and just as reliable when the artifact itself is verifiable (a PNG rendered or it didn't; a checksum matches or it doesn't). Reserve actual screenshot/pywinauto-style verification for stages where no artifact-level check is possible — e.g., confirming Unity's Editor didn't get stuck behind a modal with no failed-import artifact to detect.

### 3.5 What NOT to build

Not proposing a general-purpose workflow/DAG orchestrator (Airflow-for-MCP) — overscoped for a fleet this size, and Layer 1/2/3 (ORCHESTRATION_HIERARCHY.md) already has a registry and a triage-capable agent; the missing piece is specifically the producer→consumer handoff contract (§3.2) and the demand-lifecycle discipline (§3.3), not a new supervisory layer. Generalize mujoco-mcp's pattern into a short standards doc (`standards/CHAIN_HANDOFF_STANDARD.md`, candidate name) rather than building new infrastructure to enforce it.

---

## 4. Cross-cutting recommendations, ranked

1. **`fritz_surveil` (§1.2)** — 1.5 d, unblocks tonight's actual working pattern and gives admiral's `notify` op its second real consumer.
2. **`SIMULATE_BEFORE_COMMIT.md` pattern doc (§2.4)** — 0.5 d, pure documentation, high future leverage.
3. **yahboom mission preflight via RoboFang Sentinel (§2.3)** — ~1 d, real safety gap, currently zero simulation between mission composition and physical execution.
4. **worldlabs-mcp README cross-reference as shared VR/artistic entry point (§2.2)** — 15 min, prevents the two chains from silently diverging in agents' mental models.
5. **songgeneration-mcp discoverability from vcv-rack-mcp / comfyops-mcp (§2.1)** — 15 min, same rationale.
6. **kicad-mcp (new, not yet briefed)** — scope tbd; real candidate for simple sensor-carrier PCBs mounted on Boomy, correcting the chip-design-mcp mis-framing in §2.3. Flag for a future brief, not sized here.
7. **openbci-mcp re-evaluation trigger** — no action now; noted as "revisit when affordable skull-sensor caps exist" so the fleet remembers it's dormant, not dead.
8. **`standards/CHAIN_HANDOFF_STANDARD.md` (§3)** — generalize mujoco-mcp's state-machine + artifact-verification pattern into a short fleet standard; this is the highest-leverage item on this list despite being pure documentation, because every chain in §2 currently lacks a documented producer→consumer contract and is one silent export failure away from a wasted CAD/DCC job nobody notices. ~1 d to write well (needs real examples from tahoma2d/blender-mcp's actual current behavior, not just mujoco-mcp's, to be credible as a fleet-wide standard).

Nothing here proposes a new server. Every recommendation strengthens the mesh between servers that already exist, which is the right shape of finding for a fleet at 149+ repos — the growth problem now is connective tissue, not more nodes.
