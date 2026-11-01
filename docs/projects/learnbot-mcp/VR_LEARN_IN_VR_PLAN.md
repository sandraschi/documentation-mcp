# Learn in VR — radical VR page plan for learnbot-mcp

**Date:** 2026-10-02 (updated 2026-10-02 with Sandra decisions)
**Status:** DECIDED direction, no code yet — Phase 0 spike next
**Decisions locked:** (1) Resonite first, (2) Overte as third environment via overte-mcp, join-existing v1 then classroom world later, (3) cloud TTS optional OK, local-first via VoiceStudio sidecar, (4) VRChat LAST (EAC Secure Boot/HVCI friction — see §8.2)
**Scope:** learnbot-mcp Dashboard quick-action + new `/vr` page guiding Joe Greybeardy into a Resonite, VRChat, or Overte learning world, with Miko-chan anime avatar welcoming him in Japanese
**Repos touched by plan:** `learnbot-mcp` (owner), `resonite-mcp` (10978/10979), `vrchat-mcp` (10795/10796 — verify, registry also lists 10712 legacy), `overte-mcp` (11110/11111, domain admin 40100), `speech-mcp` (10908/10909) + VoiceStudio sidecar (:3900), `avatar-mcp` (10792/10793), `japanophile-mcp` (11193/11194), `classroom-mcp` (11105/11106), `unity3d-mcp` (10730/10731, only for VRChat world builds v2+)

---

## 1. Idea in one paragraph

A **"Learn in VR" quick-action button on the learnbot-mcp Dashboard** jumps to a new **`/vr` page**. That page does not try to render VR itself — it is a **launchpad + Joe-proof guide**: pick Resonite (recommended) or VRChat, see live connection status, follow numbered onboarding steps (install, account, desktop-vs-headset, join world/session), press "Summon Miko", and get welcomed in-world by an anime avatar girlie speaking Japanese. Lesson content (vocab, JLPT quiz, graded reader line) comes from learnbot; delivery goes through the existing `platform_send` bridge once it stops being a stub.

This is radical because learnbot today is flat-screen: 12 pages (Dashboard, Chat, Personas, Safety, Compliance, Audit, Demos, Japanese, Lessons, Avatar, Voices, Help), VRM viewer is orbit-with-mouse only, and `platforms.py:99-104` explicitly returns `resonite bridge not implemented`. The VR page makes that bridge real and makes onboarding the product.

---

## 2. What exists today (ground truth, checked 2026-10-02)

### learnbot-mcp (11101 backend / 11102 frontend)

- `webapp/src/Layout.tsx`: sidebar nav, 12 entries. No VR entry. Collapse toggle at bottom (already deviates from WEBAPP_SOTA §II which wants it at top — do not fix in this project unless cheap).
- `webapp/src/pages/Dashboard.tsx`: hero (brand + headline + New Chat / Personas CTAs) + 4 KPI cards + Recent Conversations. No quick-action strip, no `onboarding-cue`, no MOCK badges. Health via `api.health()`, conversations via `api.conversations.list()`, compliance via `api.compliance()`.
- `webapp/src/api.ts`: `health, personas, conversations, compliance, lessons.list, safety, audit`. No `vr.*`, no `platform.*` endpoints.
- `webapp/src/pages/Avatar.tsx`: `VRMViewer` orbit/zoom/expressions, persona name input, talk-test cycles visemes. Note at bottom: "real lip-sync from TTS phonemes is on the roadmap. Emotion tags from live chat will drive these same controls next." VR page will reuse these controls, not fork them.
- `src/learnbot_mcp/platforms.py`: `speech_say` works (speech-mcp → SAPI5 fallback). `platform_send` for `discord/resonite/avatar` returns `success: False, error: bridge not implemented`. This is the core backend gap.
- `src/learnbot_mcp/config.py`: already has `resonite_mcp_url` (default `http://127.0.0.1:10978` — note: that is resonite-mcp **frontend** port; backend is 10979. Probe both, see §5), `speech_mcp_url`, `avatar_mcp_url`. No `vrchat_mcp_url` yet.
- `SPEC.md`: P3 already promised "Discord bridge, Resonite bridge, speech-mcp bridge". So this plan fulfills old spec, not scope creep.
- `docs/`: no `ONBOARDING.md` at all (gate HIGH per ONBOARDING_STANDARD §New-repo gate — pre-existing debt). Japanese guide exists (`JAPANESE_LEARNING.md`), distance-learning doc points at `classroom-mcp`.

### resonite-mcp (10978 frontend / 10979 backend, ResoniteLink ws 4242, OSC 9000)

- Live-verified: slot CRUD, OSC sync, cached asset sync, ProtoFlux helpers, World Builder form, inventory spawn, contacts/sessions.
- `RESONITE_ACCESS_GUIDE.md`: full matrix — Steam desktop (Win10+, quad-core, GTX1060+, 2GB), Quest standalone via SideQuest APK, Quest Link/Air Link, Pico 4 store + SteamVR mode, mobile view-only, web experimental. ProtoFlux **editing is PC-only**; viewing works everywhere. This is the source for Joe-proof steps.
- `BEGINNERS_GUIDE.md`, `RESONITE_COMPARISON.md`, `VR_WORLDS_COMPARISON.md`, `BUILD_AND_INHABIT_PIPELINE.md`: already explain Blender/GIMP/Inkscape → Resonite asset flow. VR page links, never duplicates.
- Fleet Crossconnects section exists in README (blender, yahboom, teleoperator, mixx-dj). learnbot is not listed yet — 1-hop addition needed on both sides.
- What ResoniteLink **cannot** do: no server-side spatial `find_nearby` (see README Status — must walk scene graph client-side). Do not promise "Miko finds nearby objects" in v1.

### vrchat-mcp (10795 backend / 10796 SOTA UI per README; registry also shows 10712 — verify before probing)

- Portmanteau tools: `manage_avatar` (get_state/load/set_param/get_param), `manage_world` (get_info/search — **metadata only**), `manage_economy`, `manage_input` (chatbox 144 chars + typing, jump, move/look), `manage_osc` (send/stats), `manage_system` (status/metrics/auth_2fa/secrets).
- Auth is the hard part: `VRCHAT_USERNAME` + `VRCHAT_PASSWORD` via secrets, then **2FA handshake** (Email/TOTP) via `auth_2fa`. Pipeline websocket after login. Joe must create a VRChat account, verify email, handle 2FA code, set trust/privacy so Miko can instance with him. Much heavier than Resonite desktop.
- Explicit non-goal in README: **"runtime control only — it does not build worlds."** Real world building = `unity3d-mcp` + Unity + VRChat SDK, with honest manual steps (Udon, publish) in `docs/Building_VRChat_Worlds_With_Unity3D_MCP.md`. So "have a dedicated Miko classroom world in VRChat" is a **separate Unity project**, not something this plan automates. v1 joins existing instances / sends chatbox + avatar params; it does not publish a world.

### overte-mcp (11110 backend / 11111 frontend, domain admin 40100) — THIRD environment, Sandra decision 2026-10-02

- Open-source High Fidelity descendant: `domain-server.exe` + Interface client ("How it runs": you install both from overte.org; `overte_domain_status` works headless, spawn/inject need Interface + `scripts/overte-mcp-bridge.js` loaded). `docs/ONBOARDING.md` already Joe-shaped — reuse, do not rewrite.
- Tools verified live 2026-07-30: `overte_domain_status` (real `:40100/nodes.json`), `overte_entity_spawn` (WS bridge, `permanent=True` for classroom persistence), `overte_script_inject` (WS bridge). All responses carry `source: live|simulated` — VR page surfaces that label honestly.
- Why it matters for the classroom-later strategy: Overte is the **only** of the three where we can self-host a persistent Miko classroom on localhost/own domain without Unity publish or Resonite cloud session. v1 still join-existing (local domain you already run counts as "existing"); v2 classroom = permanent entities + injected welcome script on our domain.
- Gotchas for the plan: **VRM NOT supported as Overte Model entities — use FBX/glTF** (AGENTS.md). Miko VRM → convert via `scripts/vrm_to_glb_converter.py` (Blender headless) or serve the existing `Nekomimi-chan.glb`-style depot model. Voice/avatar path is entity-spawn + script-inject, not chatbox — different `platform_send(overte)` branch. Local sandbox creds `admin/admin` stay local-only, never committed.

### Fleet standards that constrain the design

- **ONBOARDING_STANDARD.md**: `docs/ONBOARDING.md` with 7 exact headings is mandatory when a wrappee or account exists (here: Steam+Resonite account, VRChat account, money/CC honesty). Dashboard needs **big red under-hero CTA** `data-testid="onboarding-cue"` + **MOCK-until-onboarded** (MOCK badges, Joe Mocky / Sandra Mockinger, dashed rose borders, `mock-data-banner`, clear on success). Missing = HIGH.
- **FLEET_CROSSCONNECT_STANDARD.md**: standalone-by-default, 1-hop only, graceful dialogic errors ("Action Required: ... install https://github.com/sandraschi/resonite-mcp"), README `## Fleet Crossconnects (Companions)` table, INSTALL `## Optional Companions` snippet, webapp health-dot badges (green connected / gray not-running with link), `fleet-registry.json` entry kind `optional`/`recommended` (never `mandatory`).
- **WEBAPP_SOTA_STANDARDS.md**: catch-them-all pages, `data-testid` on primary controls, Zustand LLM store, dark Zinc/Amber theme, no hardcoded tool lists, list-page search/filter/sort/paginate/count where lists are unbounded.

---

## 3. Proposed UX (what Sandra asked for, concretely)

### 3a. Dashboard quick action

In `Dashboard.tsx` hero, next to New Chat / Personas, add third button:

- Label: **"Learn in VR"** with `Headset` (lucide `Headset`) icon. `data-testid="learn-in-vr-cta"`.
- Behavior: `navigate("/vr")`. No health gating — the VR page itself explains what is missing. Button is always visible (it is marketing + entry point, not a status badge).
- Optional v2: small status dot on the button (green if either companion reachable, gray otherwise). Keep v1 simple: plain button, status lives on `/vr`.

### 3b. New `/vr` page (`webapp/src/pages/VR.tsx`, route `/vr`, sidebar entry after Avatar)

Layout top-to-bottom (all dark Zinc, Amber accents, Japanese touch without weeaboo overload):

1. **Hero**: "Learn in VR" + one-liner ("Step into a world where Miko-chan welcomes you in Japanese and quizzes you on your lesson.") + three platform cards: **Resonite (Start here — recommended)**, **VRChat (advanced)**, **Overte (self-hosted, classroom future)**. Order is deliberate per Sandra decision: Resonite first, Overte third.
2. **Companion status strip** (the crossconnect health dots): three cards probing backend health:
   - Resonite: `GET http://127.0.0.1:10979/health` (backend; fall back to 10978 if 10979 moves — verify at build time) → Connected green / Not running gray with "Install / Start resonite-mcp" link + `just serve` hint.
   - VRChat: `GET http://127.0.0.1:10795/...status` (confirm path from `manage_system status`; README says backend 10795) → same pattern. If ports disagree with registry (10712 vs 10796), resolve once and document, do not probe three ports forever.
   - Overte: `GET http://127.0.0.1:11110/health` (+ domain `:40100` live flag via overte-mcp) → Connected green / Not running gray / `simulated` amber when backend is up but bridge/Interface not connected (surface overte's `source` label, do not hide it).
   - learnbot backend itself exposes `GET /api/vr/status` aggregating all three probes + `platform_send` capability flags, so the page makes **one** call to learnbot, not CORS calls to three other origins. Direct browser→companion fetch is forbidden by SOTA local-LLM proxy reasoning (Tauri/CORS) — same principle applies.
3. **Guided path stepper** (tabs or accordion, Resonite default open):
   - Step 1: Install & account (Steam → Resonite free demo/full, create Resonite account; or VRChat account + 2FA).
   - Step 2: Desktop or headset (emphasize: **no headset required** — desktop mode is the Joe path; Quest/Pico optional).
   - Step 3: Connect bridge (enable ResoniteLink Dashboard → Session → Settings; or VRChat OSC + login via vrchat-mcp secrets).
   - Step 4: Join the classroom (session/instance name or link, e.g. `resonite:?world=...` / VRChat instance ID; v1 can be "Miko will invite you — keep learnbot open").
   - Step 5: Meet Miko (press "Summon Miko" → `POST /api/vr/summon` with persona + lesson id → in-world chatbox greeting in Japanese + TTS + avatar load).
4. **"Summon Miko" panel**: persona picker (default `miko`), lesson picker (from `lessons.list`), language pair display, button `data-testid="vr-summon-miko"`. Result area shows greeting script (JP + romaji + EN), delivery receipts per platform (sent/failed with dialogic error + install link), and "Continue in Chat" link.
5. **Onboarding cue + mocks**: if neither companion is reachable AND no VR session has ever succeeded, show big red under-hero button `data-testid="onboarding-cue"` ("Complete VR onboarding — connect Resonite") linking to `#setup` anchor + `docs/ONBOARDING_VR.md`. Sample session list may show Joe Mocky / Sandra Mockinger with MOCK badges + `mock-data-banner`; clears permanently once a real `vr/session` succeeds. No toggle to keep mocks.
6. **Safety + comfort footer**: one paragraph + link to Safety page: AI disclosure ("You are talking to an AI"), what is logged (audit), how to mute/block/report in-world, comfort (motion sickness, take breaks, desktop fallback), cost honesty (both platforms free; no CC for core path).

Sidebar: add `{ to: "/vr", icon: Headset, label: "VR" }` after Avatar. Keep 12 existing entries untouched.

---

## 4. The Joe Greybeardy test (the real spec)

Joe = smart adult, zero VR background, Windows PC, no headset, limited patience, will quit at the second unexplained error. Every step must pass:

| Joe moment | What must be true |
|---|---|
| "What do I install?" | One link: Steam → Resonite (free). No SideQuest, no APK, no Unity, no SDK in the happy path. VRChat path explicitly labeled "advanced". |
| "Do I need a headset?" | No. Desktop mode is the default screenshots path. Headset is "later, optional". |
| "Do I need an account / money?" | Resonite account (free) — cost table says so up front. No credit card for core path. VRChat path warns about account + 2FA + trust ranks. |
| "Where do I click in Resonite?" | Numbered clicks with Dashboard → Session → Settings → Enable ResoniteLink, plus screenshot or exact label. No "just enable the bridge". |
| "How do I find Miko?" | Either a clickable session link or "keep this page open and press Summon Miko — she messages you". No raw IDs to copy unless unavoidable, and then with copy button. |
| "She speaks Japanese and I don't" | Every JP line ships with romaji + EN gloss on the VR page. TTS replay button. Listening is the lesson, not a barrier. |
| "Something failed" | Dialogic error with one action: "Resonite bridge not detected. Install https://github.com/sandraschi/resonite-mcp then `just serve`." No traceback, no silent `success: false`. |
| "Is this a real person?" | AI disclosure before first in-world message + persona name clearly bot-marked, per EU AI Act pattern already in learnbot Compliance. |
| "I feel sick / overwhelmed" | Comfort note + "switch to desktop mode / take a break / continue in Chat" — no shame, always an exit. |

If any step needs SteamVR, Unity, Udon, SideQuest, or a headset, it is **not** the Joe path — it goes under "Advanced".

---

## 5. Backend + bridge design (learnbot remains orchestrator, companions stay optional)

Principles: learnbot boots and passes health with zero companions (Rule 1). Every VR tool degrades to a dialogic message with install link (Rule 3). learnbot documents only resonite-mcp + vrchat-mcp directly (1-hop); Unity/SDK details live in vrchat-mcp/unity3d-mcp docs and are linked, not copied.

### New / changed in learnbot-mcp

- `config.py`: add `vrchat_mcp_url` (default `http://127.0.0.1:10795`, verify) + `overte_mcp_url` (default `http://127.0.0.1:11110`), keep `resonite_mcp_url` but probe **backend 10979** first (fix the current frontend-port default or add `resonite_mcp_backend_url` — decide at build; do not break existing env users silently, support both with backend preferred).
- `platforms.py`: implement `resonite`, `vrchat`, and `overte` branches in `platform_send` (currently stub). Each branch: HTTP probe with short timeout → on miss return dialogic Action Required + URL; on hit dispatch minimal v1 payload:
  - Resonite v1: send text via ResoniteLink/chat endpoint (confirm exact route from resonite-mcp `docs/TOOLS.md` + `RESONITELINK_GUIDE.md` at build; likely session message or chatbox equivalent) + optional avatar-load + TTS line. Do **not** promise slot walking / nearby search (no primitive).
  - VRChat v1: `manage_input chatbox` (≤144 chars, chunk longer greetings) + `manage_avatar set_param` for a wave/expression if a known parameter exists; document chunking. Auth errors surface as "VRChat login/2FA needed — open vrchat-mcp Settings" with link, never a stack trace.
  - Overte v1: `overte_entity_spawn` (welcome sign / Miko GLB, `permanent=False` for join-existing) or `overte_script_inject` (greeting behavior) via overte-mcp WS bridge. Surface `source: simulated` as amber "bridge not connected — load `overte-mcp-bridge.js` in Interface" instead of fake success. No VRM — convert to GLB first.
- New REST (Starlette, consistent with existing `/api/*`):
  - `GET /api/vr/status` → `{ resonite: {reachable, url, hint}, vrchat: {reachable, url, hint}, overte: {reachable, url, hint, source}, can_summon: bool, Miko persona exists: bool }`.
  - `POST /api/vr/summon {persona="miko", lesson_id?, platform="resonite"|"vrchat"|"overte"|"auto"}` → runs persona lookup + lesson snippet + `platform_send` + audit log turn (platform=`resonite|vrchat|overte`, safety verdict) → returns `{ greeting_ja, greeting_romaji, greeting_en, receipts }`. `auto` order: resonite → overte → vrchat (Resonite first per decision).
  - `GET /api/vr/sessions` (or reuse conversations filtered by platform) → feeds the VR page recent-sessions list; needed for mock-clear signal.
- `server.py`: register `vr_status`, `vr_summon` MCP tools (thin wrappers over the same functions the REST uses — one implementation, two surfaces), keep `platform_send`/`platform_status` semantics, add vrchat + overte URLs to `platform_status`.
- Audit/compliance: VR turns logged like any turn (user_id, verdict, platform). Disclosure string injected before first VR message. No new retention logic.
- Voice (Sandra decision 2026-10-02: cloud optional OK, local-first): Sandra is right that local is possible now. Stack: **VoiceStudio sidecar** (`debpalash/VoiceStudio`, 43.9k stars 2026-09-29, **646 languages claimed**, 17 engines incl OmniVoice default, IndexTTS 2.5, CosyVoice 3, VoxCPM2 — clone at `D:/Dev/repos/_upstream/VoiceStudio`) via speech-mcp `provider="voicestudio"` (opt-in `VOICESTUDIO_ENABLED=true`, backend `:3900`, AGPL-3.0 process boundary — speech-mcp stays MIT, never embed); in-process small local **Kokoro / Qwen3-TTS** where they cover JP; **Gemini cloud TTS** as optional fallback for the Miko voice if local JP quality disappoints. Phase 0 spike must A/B the actual JP line (VoiceStudio JP engine vs Gemini JP voice vs Kokoro JP) and lock one default + document voice id in ONBOARDING_VR + Voices page hint. Do not hardcode `heart`/`Leda` for JP.
- `avatar-mcp` / VRM: Miko VRM already served at `GET /api/avatar.vrm` for web preview. For in-world avatar: Resonite inventory spawn or avatar-load via resonite-mcp; VRChat avatar switch via `manage_avatar load` (requires the avatar ID to be pre-approved/accessible — document whose avatar, do not promise arbitrary anime avatar loading on VRChat in v1 given trust/API limits); Overte via GLB depot (`/models/*.glb`) + `overte_entity_spawn` (convert VRM→GLB with `vrm_to_glb_converter.py`).

### Companion-side changes (small, 1-hop)

- `resonite-mcp`: add learnbot row to Fleet Crossconnects table (feature: "guided language lessons + Miko persona summon"), link to learnbot. No code change expected unless a minimal "send session message" endpoint needs hardening for non-Resonite callers — verify at build.
- `vrchat-mcp`: same — learnbot row (feature: "lesson prompts via chatbox + avatar params"). No auth-flow change; learnbot never stores VRChat creds, it only reports "login needed in vrchat-mcp".
- `overte-mcp`: add learnbot row (feature: "lesson welcome entities + greeting scripts via spawn/inject"). No bridge change; learnbot respects `live|simulated` and links `docs/ONBOARDING.md` for bridge setup instead of duplicating it.
- `fleet-registry.json`: add `crossconnects` entries on learnbot (`resonite-mcp` optional, `vrchat-mcp` optional, `overte-mcp` optional, with ports + repo URLs + features). Verify `check-fleet-crossconnects.py` passes.
- `japanophile-mcp` / `classroom-mcp`: no code dependency in v1. VR page links lesson content from learnbot's own `lessons` + `jlpt_vocab_by_level`/`example_sentences`; classroom-mcp pairing stays as documented in `DISTANCE_LEARNING.md` (courses/teaching agents) and can be deepened in v2 (assign VR homework, report scores back).

---

## 6. Onboarding artifacts (the bulk of the work, deliberately)

1. **`learnbot-mcp/docs/ONBOARDING_VR.md`** (new; the general `docs/ONBOARDING.md` debt stays separate — do not block VR on it, but note it):
   Exact headings per ONBOARDING_STANDARD: What this is for / Cost and accounts / Prerequisites outside this repo / First-timer setup steps / Pitfalls / Sanity check / Declared doubles. Three tracks inside §4 (Track A Resonite desktop-first happy path — DEFAULT; Track B VRChat advanced; Track C Overte self-hosted). Cost table honest: Resonite free (+ Steam free), VRChat free, Overte free self-hosted, no CC for core; headset optional €0 extra if desktop; TTS local-first (VoiceStudio sidecar free after setup + model download; Kokoro/Qwen in-process free), Gemini cloud key optional fallback — state this explicitly so Joe never hits a paywall by surprise.
2. **`INSTALL.md`**: near-top `> First time? Complete docs/ONBOARDING_VR.md before expecting Miko to appear in-world.` + `## Optional Companions` combined-config snippet (learnbot + resonite-mcp + vrchat-mcp `claude_desktop_config.json`).
3. **`README.md`**: `## Fleet Crossconnects (Companions)` table (resonite-mcp: in-world lesson delivery + Miko summon / Optional; vrchat-mcp: chatbox lesson prompts + avatar params / Optional) + Documentation-table row for VR onboarding.
4. **Webapp Help**: VR section pointer (Help is currently a page — add anchor/section, not a new system).
5. **Miko welcome script** (content, not code): 3 short JP lines with romaji + EN, e.g. `こんにちは！ミコです。一緒に日本語を練習しましょう！ / Konnichiwa! Miko desu. Issho ni nihongo o renshuu shimashou! / Hello! I'm Miko. Let's practice Japanese together!` + one N5 vocab hook from the active lesson + "reply in English anytime — I'll switch". Final script at build with japanophile-mcp content check (politeness level, furigana policy).

---

## 7. Phasing (small commits, max 5 files each, `.bak` on 3+ file batches) — world strategy: join-existing v1, classroom world v2 (Sandra decision)

- **Phase 0 — Spike (no UI):** verify probes + exact companion endpoints. Confirm resonite-mcp message-send route, vrchat-mcp chatbox/auth behavior, overte-mcp spawn/inject against local domain (live vs simulated), JP TTS A/B (VoiceStudio JP engine vs Gemini JP vs Kokoro JP — lock default voice id), VRM→in-world avatar path per platform (incl VRM→GLB for Overte). Output: 1-page spike note appended to this plan. Kill or reshape Phase 1 if spike fails.
- **Phase 1 — Page shell + status (webapp only, mocks declared):** `/vr` route + sidebar + Dashboard "Learn in VR" button + `GET /api/vr/status` (3 companions) + status cards + onboarding-cue + mock sessions (Joe Mocky, MOCK badges, banner). No summon yet. Verify: `just ci`, `cua-webapp-test` nav walk includes `/vr`, `data-testid` present.
- **Phase 2 — Resonite text summon (FIRST):** implement `platform_send(resonite)` + `POST /api/vr/summon` (resonite/auto) + Summon panel (persona+lesson pickers, receipt list, Continue-in-Chat). `docs/ONBOARDING_VR.md` Track A complete. Manual Joe walkthrough on desktop Resonite joining an existing session.
- **Phase 3 — Voice + avatar:** JP TTS line (VoiceStudio default, Gemini fallback) + avatar load/param per platform best-effort; Voices page hint; greeting script finalized. If lip-sync/phonemes not ready, ship TTS audio + expression preset and say so (declared, not silent).
- **Phase 4 — Overte text summon:** `platform_send(overte)` with live/simulated surfacing; Track C onboarding; domain-join instructions. Still join-existing only — no permanent classroom yet.
- **Phase 5 — Classroom loop + classroom world (LATER):** Run one vocab/lesson step in VR (ask → user answers in-world or in Chat → `vocab_submit` scores → next prompt). Report score back to Lessons page. Deepen classroom-mcp link here. Classroom world spin-up here, not earlier: Overte persistent domain first (cheapest: `permanent=True` entities + welcome script on our domain), Resonite hosted session second, VRChat custom world last (Unity/SDK/Udon project of its own).
- **Phase 6 — VRChat summon LAST + polish/gate:** `platform_send(vrchat)` with chunking + auth/2FA dialogic errors; Track B onboarding; instance-join instructions (no world publish). VRChat goes last deliberately: EAC now requires Secure Boot + HVCI (see §8.2) — Goliath itself has Secure Boot OFF, and Joe-grade users should never start with a BIOS change. Then README/INSTALL crossconnects (3 companions), fleet-registry, crossconnect checker green, screenshots (`docs/screenshots/cua-vr*.png`), BUILD_LOG entry, mock-clear verified, Help section, assfix-zero self-check (expect zero CRITICAL/HIGH; residual MEDIUM documented).

Out of scope v1: publishing a custom VRChat world (Unity/SDK/Udon), spatial `find_nearby` tutoring, headset-only interactions, ProtoFlux lesson scripting, storing VRChat creds in learnbot, auto-posting to public instances. Classroom world is v2 (Phase 5), not v1.

---

## 8. Risks & honest difficulties (why Sandra is right that this is difficult)

1. **Three moving platforms, none owned by us.** ResoniteLink protocol, VRChat API/OSC/2FA, Overte domain/bridge script, trust ranks, instance privacy, and rate limits can break the bridge without learnbot changing. Mitigation: thin bridge, exact-version pinning in docs, dialogic errors, never hard-require companions.
2. **VRChat auth + moderation + EAC/BIOS friction.** 2FA, chatbox 144-char limit, avatar-search trust gates, public-instance bot etiquette, potential kicks/mutes — plus, since ~2025, the EOS Easy Anti-Cheat build requires **Secure Boot enabled in BIOS/UEFI AND HVCI (Memory Integrity) on in Windows**. This is exactly what bit Sandra last time: VRChat refuses to start, and the fix is a BIOS change + reboot + Windows Security toggle, i.e. the opposite of Joe-proof. Measured 2026-10-02: **Goliath itself has `UEFISecureBootEnabled=0` and no HVCI key** — VRChat would refuse here today. Mitigation: VRChat goes LAST (Phase 6), private/friends instances only, chunked messages, disclosure, Safety page linkage, no auto-posting. When the track goes live, ONBOARDING Track B must include the Secure Boot check (`msinfo32` → BIOS Mode UEFI; motherboard manual for the toggle) with the Linux-dual-boot caveat (shim re-enrollment) stated up front.
3. **ResoniteLink enablement is the Joe cliff.** If ResoniteLink is off, everything silently fails. Mitigation: pre-flight checklist on `/vr` ("Is Resonite running? Is ResoniteLink enabled?") + probe that distinguishes "resonite-mcp down" from "Resonite client not connected" if the API allows; both states get different hints. Overte has the same cliff shape (bridge script not loaded → `simulated`); surface it amber, same pattern.
4. **No-headset vs headset divergence.** Desktop, Quest standalone, Quest Link, Pico, SteamVR all differ (see ACCESS_GUIDE matrix). Mitigation: desktop-first happy path; headset tracks labeled advanced with links, not rewritten instructions.
5. **Avatar expectations vs reality.** "Anime avatar girlie" is easy on web (VRMViewer) and plausible in Resonite (VRM/inventory), convertible in Overte (VRM→GLB pipeline), but VRChat avatar switching has ownership/trust constraints. Mitigation: promise Miko's presence + voice + text in v1; avatar-switch documented as best-effort per platform.
6. **Japanese TTS quality (now with a local path).** VoiceStudio sidecar gives local JP without cloud (646 langs claimed — verify JP quality in spike, claims are not ears), Kokoro/Qwen cover small-local, Gemini cloud stays as fallback. Mitigation: spike A/B picks the real JP voice; ship replay + romaji/EN gloss so comprehension never depends on audio alone. Watch VoiceStudio costs: ~2.3GB first model download, GPU queue timeouts, AGPL boundary (HTTP/MCP only, never embed).
7. **Safety in immersive context.** Immersion raises pseudohuman dynamics (see `docs/chatbot-ethics.md`) + motion-sickness/comfort + logging expectations. Mitigation: disclosure, audit logging unchanged, mute/block/report instructions, comfort footer, no dark-pattern retention.
8. **Port/config drift.** resonite frontend/backend (10978/10979), vrchat (10795/10796 vs 10712), overte (11110/11111 + domain 40100), VoiceStudio :3900, learnbot env defaults (currently frontend port in `resonite_mcp_url`). Mitigation: Phase 0 locks exact ports/paths; config supports both with backend preferred; registry updated once.
9. **Scope sprawl into Unity/world-building.** The moment someone says "custom Miko classroom world in VRChat", the project explodes (Unity version, SDK, Udon, publish, testing). Mitigation: explicitly v2 Phase 5, join-existing in v1; Overte persistent domain is the cheap classroom path when we get there.

---

## 9. Open questions for Sandra (to talk through) — decisions 2026-10-02 recorded

1. **Platform order:** ~~Resonite-first ... or both equal?~~ DECIDED: Resonite first (Track A v1), VRChat advanced (Track B Phase 4), Overte third self-hosted track (Track C Phase 4, classroom future).
2. **World strategy:** ~~join existing ... or persistent hosted classroom?~~ DECIDED: join existing v1 (existing Resonite session, existing VRChat instance, existing/own Overte domain); classroom world spin-up LATER in Phase 5 (Overte persistent domain first, Resonite hosted session second, VRChat custom world last).
3. **Miko canon:** same Miko persona as Chat/Avatar (shared backstory + voice), or a VR-specific variant (more genki, simpler Japanese, listening-first)? Who approves the 3-line welcome script + politeness level? — STILL OPEN.
4. **Voice:** ~~which JP voice ... cloud acceptable?~~ DECIDED: cloud optional OK. Local-first: VoiceStudio sidecar (646 langs claimed — spike must verify JP with ears, not README) → Kokoro/Qwen small-local → Gemini cloud fallback. You called it: local should be possible these days; spike proves it.
5. **Classroom depth:** v1 = guided join + greeting + one vocab hook, lesson continues in Chat/Lessons — or must v1 already run a full quiz loop in-world? — STILL OPEN (proposal: greeting + hook v1, loop Phase 5).
6. **Headset stance:** desktop-first with headset as advanced — or do you want Quest/Pico screenshots and headset QA in v1? — STILL OPEN (proposal: desktop-first).
7. **ONBOARDING debt:** ship `docs/ONBOARDING_VR.md` now and leave general `docs/ONBOARDING.md` for later, or fix both together (bigger diff)? — STILL OPEN (proposal: VR doc now).
8. **Success metric:** what proves this worked — Joe completes desktop join + Miko greeting unaided? Screenshots + BUILD_LOG? `cua-webapp-test` green with `/vr`? All three? — STILL OPEN.

---

## 10. Phase 0 spike results (2026-10-02, static analysis, no webapp edits)

Live-port check: only speech-mcp backend :10909 listening. learnbot :11101, resonite :10979, vrchat :10795, overte :11110 all down — expected; spike is code+docs truth, not live calls.

### (1) Resonite send path — NO chat primitive, workaround locked

`docs/TOOLS.md` + src grep: ResoniteLink (0.13.1) offers slot CRUD, `spawn_mesh`, `import_mesh_json`, `set/get`, `call_method`; legacy tools offer `session_start/status/end`, `world_load`, `avatar_load`, `parameter_set`, `protoflux_execute`, inventory (currently timing out even on list — webapp folder buttons disabled honestly), OSC send/receive. **There is no send-chat-message tool.** v1 Miko greeting on Resonite = three-part workaround, declared as such: (a) spawn a welcome sign entity near spawn (`link_spawn` / `spawn_mesh` with greeting text as its name), (b) `avatar_load` Miko VRM + `parameter_set Happy 0.8`, (c) TTS audio line via speech-mcp (played on Joe's desktop, not positional in-world — say so). ProtoFlux lesson scripting stays v2. ResoniteLink enablement (Dashboard → Session → Settings) remains the Joe cliff — `/vr` pre-flight checklist must separate "resonite-mcp down" from "Resonite client not linked".

### (2) VRChat chatbox + auth — confirmed, constraints locked

`server.py:381-396`: `manage_input chatbox` → OSC `/chatbox/input`, **max 144 chars** — greeting script must be chunked (3 short lines, sent sequentially with typing indicator). `avatar_manager.load_avatar(avatar_id)` + `set_parameter` with interpolation exist, but avatar must be a valid `avtr_...` ID Joe's account can access — no arbitrary anime-avatar promise in v1. Auth: `manage_system secrets` stores `VRCHAT_USERNAME/PASSWORD`, then `auth_2fa` (Email/TOTP), pipeline websocket auto-starts after 2FA. learnbot never stores these creds — it only reports "login/2FA needed in vrchat-mcp" with link. Private/friends instances only v1.

### (3) Overte live vs simulated + GLB — confirmed, classroom-cheap path validated

`docs/TOOLS.md` + `models/README.md`: `domain_status` live against `:40100/nodes.json` (headless OK); `entity_spawn` (Box/Sphere/Web/Model, `permanent` flag) + `script_inject` need Interface + `overte-mcp-bridge.js` WS bridge, else labeled `simulated` + warning — `/vr` surfaces amber, never fake green. Depot already proves the pattern: `Nekomimi-chan.glb` (11.6MB, VRM→GLB converted, spawns via `model_url=http://localhost:11110/models/...`) + living-room collider/pano skybox. **VRM unsupported directly — Miko VRM must go through `vrm_to_glb_converter.py` (Blender 4.4 headless) once, then depot-host.** v1: temporary welcome entity (`permanent=False`) on existing/own domain; v2 classroom: `permanent=True` entities + welcome script on our domain.

### (4) JP TTS A/B — local path real, default ranking locked (ears still required)

- **VoiceStudio sidecar** (`providers/voicestudio.py`, `:3900/mcp`, `VOICESTUDIO_ENABLED` opt-in): 17 engines incl **CosyVoice 3 + IndexTTS 2.5** — both ZH/JP-strong per `CHINESE_AI_RESEARCH.md`; per-agent binding via `X-VoiceStudio-Client-Id`; files-mode avoids base64-in-context. First call downloads ~2.3GB — onboarding must say so. AGPL boundary respected (HTTP/MCP only). **Default pick for Miko JP, pending ear test.**
- **Gemini cloud** (100+ langs, 31 voices + custom, expressive tags): guaranteed JP quality today. **Fallback pick.** Needs `GOOGLE_API_KEY` — allowed as optional per Sandra decision, never required for Joe path.
- **Kokoro in-process**: VOICES are `af_heart/af_sky/am_adam` only, `KOKORO_LANG` defaults `a` — **English-only as wired; no `jf_*` JP voices. Excluded for Miko JP** (keep for EN gloss fallback).
- **Qwen3-TTS in-process** (`Qwen3-TTS-12Hz-0.6B-Base`, VOICES=`[default]`): zh/en-first; JP support unverified — bench candidate only, not default.
- Spike ranking: **VoiceStudio JP engine → Gemini JP fallback → Qwen bench → Kokoro EN-only.** Phase 2 must A/B the actual 3-line greeting with ears and lock the voice id in `ONBOARDING_VR.md` + Voices hint. 646-language claim is not a quality claim.

### (5) Miko A/B personas — both shipped as requested, desktop default + headset-later UX

Sandra: "dunno which miko, make both." So v1 ships a persona picker on `/vr` with two first-class options (same voice pipeline, different backstory + script + difficulty):

- **A. Miko Classic (same Miko):** shared backstory with Chat/Avatar persona `miko`, calm polite desu/masu, full lesson continuity ("we continue your N5 set from Lessons"). Welcome: `こんにちは！ミコです。一緒に日本語を練習しましょう！` + romaji + EN + one vocab hook from active lesson. Best for existing learnbot users; zero canon fork.
- **B. Miko Genki VR (listening-first):** VR-specific variant `miko-vr`, brighter, shorter sentences, slower TTS rate, furigana-first JP + immediate EN gloss, comprehension checks ("もういちど？ もう一度言いますね" + replay button). Best for Joe-first-timers; documented as `persona_create(name="miko-vr", ...)` fork with `knowledge_base` pointing at the same lesson but `languages`/`skills` tuned to listening. `/vr` default selection: **A for returning users (persona exists), B for first-timers** — one radio, remembered in localStorage.
- Politeness: desu/masu throughout v1 (no plain-form drift); japanophile-mcp content check at script-freeze.

### (6) Desktop-default + Meta/Pico-later viewer path (as requested)

Desktop is the Joe happy path on all three tracks (Resonite Steam desktop, VRChat desktop, Overte Interface desktop). Headset is **not** v1 QA — but `/vr` must still provide the path so Quest/Pico owners are not dead-ended. UI/UX contract for later (design now, build Phase 4+):

- On `/vr`, under each platform stepper, a collapsed-by-default **"Headset (Meta / Pico) — later"** accordion (`data-testid="vr-headset-path"`): no duplicated steps, just deltas from desktop (Quest standalone via SideQuest APK vs Quest Link/Air Link; Pico Store vs SteamVR mode; controller vs mouse/keyboard note; comfort + battery + WiFi notes). Content links `RESONITE_ACCESS_GUIDE.md` matrix — never copied.
- **vr-in-viewer teaser:** `/vr` includes a disabled-until-connected **"Preview in viewer"** card (`data-testid="vr-in-viewer"`): shows the same Miko VRM web preview (`VRMViewer` orbit/zoom/expressions reused from Avatar page) with caption "flat preview — the real Miko is in-world". When a session is live, the card flips to session status + "Return to world" deep-link (`resonite:?world=...` / VRChat instance link / Overte `localhost` domain note). No WebXR in v1 — the card is honest about that.
- Headset QA deferred explicitly: no Quest/Pico screenshots required for Phase 1–2 gate; add when Track C/B matures. Desktop screenshots + `cua-webapp-test` `/vr` walk gate v1.

---

## 11. Updated open items (after 2026-10-02 decisions + spike)

- RESOLVED: order (Resonite → Overte → classroom → VRChat last), world strategy (join-existing v1, classroom Phase 5, Overte-domain-first), voice policy (local-first VoiceStudio, cloud fallback OK; Phase 3 A/B locked gemini/Leda, samples in `learnbot-mcp/docs/audio/`), headset stance (desktop default, headset accordion later).
- RESOLVED: vrchat-mcp ports (transport default + registry agree on **10712**; README 10795/10796 stale — companion-side fix, not learnbot).
- STILL OPEN: Miko default heuristic (shipped: genki default for first-timers, classic for returning — confirm by feel); ONBOARDING debt (VR doc shipped, general doc still missing); success metric (proposal: unaided desktop join + greeting + screenshots + green `cua-webapp-test`).
- NEXT: all phases DONE 2026-10-02 (commits through Phase 6b). Remaining: VR screenshot via cua-webapp-test, vrchat-mcp README port fix (their repo), VoiceStudio sidecar run + ear test, Sandra's ear check of Leda samples.

---

*Filed under `mcp-central-docs/projects/learnbot-mcp/` as the discussion base. Companion cross references: resonite-mcp `docs/TOOLS.md` + `RESONITE_ACCESS_GUIDE.md`, vrchat-mcp `src/vrchat_mcp/server.py` chatbox/auth, overte-mcp `docs/TOOLS.md` + `models/README.md` + `docs/ONBOARDING.md`, speech-mcp `docs/providers/voicestudio.md` + `docs/FOSS_SPEECH_SURGE_2026.md` + `providers/{voicestudio,kokoro,qwen_tts}.py`, fleet `standards/ONBOARDING_STANDARD.md` + `standards/FLEET_CROSSCONNECT_STANDARD.md` + `standards/WEBAPP_SOTA_STANDARDS.md`.*
