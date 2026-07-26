# iOS App Plans — Fleet Companion Apps

**Date:** 2026-07-12
**Status:** RUNNING PLAN — living document, update statuses in place
**Tags:** [ios, fleet, apps, admiral, running-plan, medium]
**Audience:** Sandra + coding agents (Cursor on Mac for Swift, DeepSeek V4/OpenCode on Goliath for server-side). Each plan is agent-executable given this doc + the fleet standards docs + the referenced repos.

Design thesis: every app instrumentalizes fleet capabilities that already exist on Goliath. The phone is a **peripheral of the fleet** — its sensors (camera, LiDAR, GPS, mic, motion) feed the fleet, and the fleet's outputs (audio, images, approvals, telemetry) land in the pocket. No app duplicates server logic.

---

## 0. Shared chassis & conventions (prerequisite for everything)

### 0.1 FleetKit — extract the admiral-pager chassis (2 d, DO THIS FIRST)

admiral-pager already contains the plumbing every app below needs. Extract into a Swift package:

- **Repo:** `sandraschi/fleetkit-swift` (Mac). Local path convention: `~/Dev/fleetkit-swift`.
- **Modules:**
  - `FleetRelay` — bearer-token URLSession client, base-URL from config (Tailscale IP), typed error handling, retry/offline states
  - `FleetPush` — APNs registration, device-token capture, notification category registration helper
  - `FleetLive` — Live Activity start/update/end helpers (generic phase/progress model, the admiral `RunProgressEntry` generalized)
  - `FleetConfig` — per-app plist/keychain: tailnet host, port, token. Token in **Keychain**, not source (admiral currently hardcodes `"admin"` in `RelayClient.swift` — fix during extraction, do not copy the anti-pattern)
  - `FleetOSC` — UDP OSC message sender (needed by Pocket Patch; evaluate SwiftOSC vs ~150 lines hand-rolled at build time — OSC 1.0 encode is trivial, a dependency may not be worth it)
- **Acceptance:** admiral-pager rebuilt ON FleetKit with zero behavior change; package has unit tests for OSC encoding and relay auth header.

### 0.2 Conventions for all apps

- **Two-repo pattern** (per admiral): Goliath repo = FastMCP server or extensions to existing servers; Mac repo = SwiftUI app. Machines talk over **Tailscale** only.
- Mac machine: currently unnamed. Suggestion on the table: **David** (Goliath's natural counterpart). Sandra to ratify.
- **Distribution:** AltStore PAL (EU/DMA path), source JSON per app, same as admiral-pager.
- **Toolchain:** Xcode 27 beta, iOS 19 minimum, Swift 6, SwiftUI. Cursor on Mac drives Swift codegen; treat admiral-pager's "Zero-to-App" prompt as the template for each new app's build prompt.
- **Ports:** any new Goliath-side HTTP surface reserves its pair in `operations\WEBAPP_PORTS.md` IN THE SAME COMMIT as first use (mcd section 0 rule). Do not pre-reserve from this doc.
- **Push:** apps do NOT each build an APNs relay. admiral-mcp grows one generic op (see 0.3) and becomes the fleet's single push gateway.
- **Security:** bearer tokens per app (not shared), rotated from `admin` defaults; localhost bind + Tailscale IP exposure only; no fleet endpoint ever leaves the tailnet.
- **Honesty rules:** mcd section 0 applies — no stubs presented as done, manual gates need evidence in each repo's `docs/ACCEPTANCE_EVIDENCE.md`, agents do not self-certify device testing.

### 0.3 admiral-mcp extension: generic `notify` op (0.5 d, server-side)

New tool op `notify`: `{title, body, category?, thread_id?, payload?, live_activity?}` → APNs push to registered device(s). Auth per calling server via relay token. This turns admiral from "approvals only" into the fleet's pager backbone — Benny FM, Ekphrasis, and Stethoscope-class features all push through it. Register calling-app identifiers in the payload so the phone can route taps to the right app/screen (universal links per app).

---

## 1. Pocket Patch — VCV performance surface (STATUS: planned, GATED)

**The pitch:** vcv-rack-mcp patches are born with an OSC receiver wired to headline params, and `vcv_live.address_map` emits the map. Pocket Patch fetches that map and **renders a control surface from it** — knobs, faders, XY pads generated per patch — multitouch OSC over the tailnet. CoreMotion as the idiosyncratic layer: tilt sweeps a mapped param, shake triggers sample-and-hold chaos. Dani demo: one command produces a patch AND its bespoke hardware-free controller.

**Gate:** BLOCKED until vcv-rack-mcp clears BLOCKER-0 + manual gate P2 (real Rack round-trip). Do not start the app before a patch demonstrably plays and its address map is verified against osc-mcp. This app is deliberate pressure to clear that gate.

**Architecture:**
- Goliath: NO new server. vcv-rack-mcp HTTP `/mcp` serves depot list + address maps. Two OSC transport paths, both supported:
  - **Performance path (default):** phone → UDP OSC **directly to Rack's OSC receiver module** (cvOSCcv/OSCelot port, from the address map). Lowest latency, no hop.
  - **Orchestration path:** phone → osc-mcp REST → Rack. Use when recording automation or when osc-mcp needs to observe/log the performance.
- Mac repo: `sandraschi/pocket-patch`. FleetKit (FleetRelay + FleetOSC + FleetConfig).

**iOS features (v0.1):**
- Depot browser (patch list from vcv depot, persona badges, sidecar .md rendered)
- Surface renderer: address map entry → control widget. Mapping rules: continuous param → knob or fader (range from catalog param min/max); two related params → XY pad; trigger/gate → momentary button. Layout auto-generated, manually re-arrangeable, layout saved per patch (local).
- Motion mapping screen: assign tilt-X/tilt-Y/shake to any mapped param, with sensitivity + latch.
- Panic button (all mapped params → catalog defaults).

**Phases:** P1 map-fetch + static surface + OSC send (2 d) → GATE: filter sweep audible from phone against the vcv P2 acceptance patch → P2 motion + XY + layouts (1 d) → P3 polish + AltStore ship (0.5 d).

**Effort:** 3–3.5 d app-side once vcv gates are green.
**Acceptance:** Dani-scenario: performance-persona patch playing in Rack; phone controls ≥4 params with <50 ms perceived latency on the tailnet (Wi-Fi, same LAN); tilt-to-cutoff demo recorded to evidence doc.

---

## 2. Boomy's Leash — robot remote + AR surveying (STATUS: planned, partially gated)

**The pitch:** drive Boomy from the phone — live camera, joystick, PTZ, headlight, speak-through-robot (speech-mcp TTS out of Boomy's speaker). The 20% nobody else would build: **ArUco surveying via ARKit**. yahboom nav Phase N1 needs a hand-measured marker map of the flat; the iPhone has LiDAR. Walk the flat once, tap each printed marker in AR, app computes marker poses in a common frame and emits the marker-map YAML. The phone replaces the tape measure — iOS hardware doing fleet metrology.

**Gates:** Teleop lane (Lane A) buildable NOW against yahboom-mcp v2.4.2. Surveying lane (Lane B) lands together with yahboom nav Phase N1 (gap analysis §7) — coordinate, don't block: the YAML format is defined by the N1 brief, so agree the schema first, build in parallel.

**Architecture:**
- Goliath/Boomy: yahboom-mcp HTTP surface (existing dashboard backend 10892). Additions needed server-side (0.5–1 d): MJPEG or WebRTC camera stream endpoint if the dashboard doesn't already expose one consumable by iOS (verify first — do not rebuild what exists); `nav/save_map_markers` accepts the YAML (part of N1 anyway).
- Mac repo: `sandraschi/boomys-leash`. FleetKit + ARKit + RealityKit.

**iOS features:**
- Lane A (teleop, v0.1): camera view, virtual joystick (drive), PTZ pad, headlight toggle, sonar readout strip, TTS text field ("Boomy says…"), emergency stop as a persistent oversized control. Deadman behavior: joystick release or app background → stop command, always.
- Lane B (surveying, v0.2): AR session with plane detection; user taps a detected ArUco marker (or its printed location), app records marker id + ARKit world-frame pose; on completion exports YAML (id → x, y, θ in a floor frame anchored at marker 0) and POSTs to yahboom-mcp. Include a re-survey diff view (old vs new poses).

**Phases:** A1 teleop core (2 d) → GATE: Boomy driven around the flat from the phone, e-stop verified physically → B1 AR capture + YAML export (2 d) → GATE: `where_am_i` after N1 EKF+ArUco agrees with phone-surveyed map within 15 cm at 3 test points.

**Effort:** 4 d app-side + 0.5–1 d server-side stream work.
**Idiosyncrasy note:** the surveying lane makes this the fleet's first case of iOS sensors feeding robot autonomy — record it as such in the repo README, it is the point.

---

## 3. Benny FM — the generated morning briefing (STATUS: planned, unblocked)

**The pitch:** a narrated personal radio show for the Benny walk. Fleet PR/issue status, overnight code drops from arXiv scans, AI-news digest, Alsergrund weather — composed into a 4–7 minute script, spoken by speech-mcp TTS, delivered as a push at a scheduled time. Optional 10-second songgeneration jingle. Zero new sensors; pure orchestration over servers that already work.

**Architecture:**
- Goliath composer: a scheduled job in **fleet-agent-mcp (Fritz)** — this is persona-layer work per ORCHESTRATION_HIERARCHY.md, so it belongs to Fritz, not a new repo. New tool `fritz_briefing`: ops `compose_now`, `schedule` (Windows Scheduled Task via winops), `history`.
  - Sources (each optional, degrade gracefully — a source being down produces a one-line "no news from X", never a failed briefing): gitops `fleet_morning_digest`; arxiv-mcp `codehunt_stats_tool` + firefront digest; aiwatcher; netatmo-weather-mcp; calendar/todo if myconf exposes one.
  - Compose: local model (Qwen3.5 via Ollama) writes the script from structured source JSON with a fixed rundown (cold open → fleet → papers/code → AI news → weather → sign-off). Script + audio archived to SQLite + a static `briefings/` dir.
  - Voice: speech-mcp TTS (pick the default voice once, config not code). Jingle: pre-generate a handful with songgeneration-mcp, rotate — do NOT generate per-briefing (slow, pointless).
  - Deliver: admiral-mcp `notify` (§0.3) with the audio URL; file served from Fritz's existing HTTP surface or a static mount.
- Mac repo: `sandraschi/benny-fm`. FleetKit. Thin app: push → background audio player (lock-screen/CarPlay controls via MPNowPlayingInfoCenter), briefing archive list, transcript view, "regenerate now" button.

**Phases:** F1 composer + one real end-to-end briefing as MP3 on disk (1.5 d, server only — testable without any app) → F2 notify + app player (1.5 d) → F3 scheduling + archive UI (0.5 d).

**Effort:** ~3.5 d total, most of it server-side.
**Acceptance:** three consecutive mornings of scheduled briefings delivered and played without touching Goliath; one source deliberately taken down and the briefing still ships with the degradation line.

---

## 4. Ekphrasis — camera-to-comfyops (STATUS: planned, soft-gated)

**The pitch:** point the phone at anything, pick a treatment, the 4090 does the work. Photo → comfyops i2i restyle / upscale / i2v video; push when the result is ready; auto-ingest to Immich. Benny-to-Ghibli is the demo. The strategic hook: once comfyops Phase 2 (LoRA) lands, Ekphrasis becomes the **dataset-capture front end** — shoot 30 photos of a subject, tag as a dataset, `dataset_prep` picks the album up. The app gives comfyops's missing Immich integration a concrete consumer.

**Gates:** core lane needs comfyops MVP (exists) + an upload path; the ingest lane depends on comfyops remediation item "Immich/Plex auto-ingest" (gap analysis §11 status update) — build them together. Dataset lane waits for comfyops Phase 2.

**Architecture:**
- Goliath: comfyops-mcp additions (1 d): REST upload endpoint (multipart → input image on disk, returns image ref) on the existing backend :11087; job-completion hook fires admiral `notify` with result ref; implement the pending Immich ingest op (it was already specced).
- Mac repo: `sandraschi/ekphrasis`. FleetKit + PhotosUI.

**iOS features (v0.1):** camera/library picker → treatment sheet (workflow list fetched live from `comfy_workflows`, with the sidecar .md's exposed params rendered as simple controls; prompt field for restyle) → submit → job appears in a jobs list with Live Activity progress (ws progress relayed through the backend) → push on done → result viewer with save-to-Photos + "in Immich" link. Seed shown on every result; "rerun with same seed" and "variations" (seed++) buttons.
**v0.2 (post comfyops Phase 2):** dataset mode — burst capture, per-shot keep/discard, caption field, submit as named dataset → `dataset_prep`.

**Phases:** E1 upload + generate + poll (1.5 d) → GATE: Benny photo → styled PNG on the phone, seed-reproducible → E2 Live Activity + push + Immich (1 d) → E3 video (i2v Wan/LTX treatments, longer jobs) (0.5 d) → E4 dataset mode (1 d, gated on comfyops P2).

**Effort:** 3 d app v0.1 + 1 d server-side.
**Acceptance:** end-to-end under 90 s for a Z-Image/klein treatment on an idle 4090; vram_guard refusal surfaces as a readable message on the phone, not a spinner.

---

## 5. Backlog — next four (described, not yet planned in detail)

Promote by moving into §1–4 format above. Ordered by current gut ranking within each batch (5.1–5.4 first batch, 5.5–5.8 added later same session).

### 5.1 Weltenbummler — photo-to-walkable-world
Snap a Vienna courtyard → worldlabs-mcp Marble generates a 3D world → view it on the phone (Spark viewer web view, or export path), optionally hand off to resonite-mcp so the world becomes a visitable Resonite location. The fleet already has the whole pipeline (worldlabs-mcp audited 2026-07-12, Tauri app exists); the app is capture + gallery + share targets. Multi-image capture guidance in-app (the azimuth caveat from the worldlabs work becomes UX: the app coaches the user's shooting angles). Effort guess: 3 d. Idiosyncrasy: maximal — "I photographed my Hinterhof and now it's a world."

### 5.2 Denkzettel — voice-to-zettelkasten
Dictate on the walk; FunASR STT on Goliath (speech-mcp) transcribes; a small LLM pass structures it into an advanced-memory note — title sanitized to fleet filename rules, tags per the memory tagging convention, linked into the zettel graph (memops `adn_zettel`); push-back shows the filed note for a correct/amend loop. Kills the "had a thought on the Gürtel, lost it by the front door" failure mode. Watch-app stub worth considering (one-button record). Effort guess: 2 d (almost all exists server-side). Idiosyncrasy: the note-discipline rules in this very fleet become an app.

### 5.3 Séance — social-VR presence pager
resonite-mcp v1.1.0 speaks the real protocol; VRChat server exists too. Séance is the out-of-world bridge: see who's online in your worlds, get pushed when a named contact enters Resonite, send a message or spawn a marker item in-world from the phone, "I'll be in in 10" quick replies. Push via admiral `notify`. Effort guess: 2.5 d, mostly server-side presence-watch loop + contact rules. Idiosyncrasy: a pager for a VR social life, run off your own infrastructure. Gated on resonite-mcp live E2E (still pending).

### 5.4 Stethoscope — fleet vitals in the Dynamic Island
Goliath's pulse in the pocket: GPU temp/VRAM/queue depth as a **Live Activity while long jobs run** (LoRA training, Wan renders, simbench matrices), pushes on OOM/service-death/disk-threshold, and a small set of approval-gated recovery actions (restart service X, kill job Y) that route through admiral's existing approval flow — the safety model is already built. Sources: winops perf/svc ops, monitoring-mcp, docker-mcp, comfyops/leanforge job queues. Effort guess: 2.5 d. Idiosyncrasy: moderate (ops apps exist) but the admiral-gated actuation + per-job Live Activity ties the fleet's own approval philosophy into its ops loop.

### 5.5 Beweisstück — proof-search pager for leanforge
leanforge proof searches run for hours on the 4090 and mostly need a human at exactly two moments: when the search is stuck and when it finds QED. Beweisstück puts both on the phone: Live Activity with search-tree depth / nodes expanded / best partial progress, push on QED or stall, and — the idiosyncratic part — **human-in-the-loop tactic selection through admiral's approval flow**: when the agent has 2–3 candidate lemma routes and low confidence, it raises an approval-style card and Sandra picks a branch from the sofa. Mathematician-as-oracle, formalized as pager infrastructure. Sources: leanforge job queue + admiral approvals + notify. Effort guess: 2 d (approval plumbing exists). Gated on leanforge's job/progress surface exposing tree stats — verify before promoting.

### 5.6 Messwarte — the electronics bench in your pocket
The fleet has MCP wrappers for an entire bench — oscilloscope, multimeter, logic analyzer, function generator, bus pirate, JTAG/SWD — which is a set-of-size-one situation begging for a companion app. Messwarte: live waveform/measurement view, **push when a long logic-analyzer capture finally triggers** (the killer feature — armed captures can wait hours), function-generator control from the couch, and a measurement logbook that files annotated captures to advanced-memory. Long-capture arm/trigger as Live Activity. Effort guess: 3 d, heavily dependent on which instrument servers are actually production vs scaffold — do a 0.5 d bench-server truth pass first (same honesty rules as everywhere).

### 5.7 Flohmarkt — crate-digging companion
At the record stand: record 10 seconds on the mic → Goliath identifies the track (audio fingerprinting server-side; evaluate a self-hosted Chromaprint/AcoustID pass before reaching for anything cloud) → checks the media archive (plex-mcp) for **"do I already own this?"** → pulls metadata/pressing info → one-tap wantlist entry, and for hits: stems-availability check via the DJ tooling (dj-media-hub) so [[dani]] gets a "found X, stems ready by tonight" handoff. Anti-double-purchase as a service, with a DJ pipeline attached. Effort guess: 2.5 d, the fingerprint lane is the only genuinely new server work. Vienna Flohmarkt field-tested by design.

### 5.8 Tropenfieber — spoiler-aware second screen
plex-mcp knows what's playing and the timestamp; tvtropes-mcp knows the tropes; a local-model pass (Qwen3.5) composes **spoiler-gated** companion notes — tropes, cast context, anime-adaptation deltas — that unlock progressively as playback passes each point, never ahead of it. Phone is the second screen: now-playing card, trope feed that grows with the episode, "explain this reference" button, watch-log filed to advanced-memory. The spoiler gate is the hard and interesting part (trope pages are spoiler minefields — the composer must filter by episode/chapter markers and fail closed). Effort guess: 3 d, mostly server-side composition + caching. Weeb utility: maximal.

### Previously floated, parked (from the 2026-07-12 session, keep on radar)
- **Flâneur** — GPS walking-tour narrator over the personal knowledge stack + vienna-live; whimsy king, latency/battery questions open.
- **Registrant** — iPad stop-jamb console for grandorgue-mcp with native RTP-MIDI for the latency-critical path; the treat, pairs with the parked music-notation server.

---

## 6. Sequence & roll-up

| Item | Effort | Depends on | Status |
|---|---|---|---|
| §0.1 FleetKit extraction | 2 d | admiral-pager building | NEXT |
| §0.3 admiral `notify` op | 0.5 d | — | NEXT (server) |
| §3 Benny FM | 3.5 d | notify op | unblocked |
| §1 Pocket Patch | 3–3.5 d | vcv BLOCKER-0 + gate P2 | GATED (Sandra: 4 reference patches) |
| §4 Ekphrasis | 4 d | comfyops upload + Immich op | soft-gated |
| §2 Boomy's Leash lane A | 2 d + 0.5 server | camera stream check | unblocked |
| §2 Boomy's Leash lane B | 2 d | yahboom nav N1 | gated |
| §5 backlog | — | promotion | ideas |

**Recommended order:** FleetKit + notify → Benny FM (proves the whole chassis end-to-end with the least risk) → Pocket Patch the moment vcv P2 clears → Leash A → Ekphrasis alongside comfyops remediation → Leash B with nav N1.

**Running-plan hygiene:** when a plan starts, its section gets a STATUS line with repo links; when it ships, move acceptance evidence pointers here; when an idea dies, mark it DROPPED with one line of why — do not delete.
