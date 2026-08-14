# Sandrafleetbot — Zero-Pay GrokBot

> **Status: SPEC v2 (pre-approval)** — no code written yet. This document is the architecture spec + buildout plan + gap register. Approve it, then build P0→P8 in order.
> **Goal:** Beat xAI GrokBot (powerful, metered, cloud-locked) with the sandraschi fleet: Muse Glimmer 30B on the RTX 4090, Fritz as the agent, cline-mcp as the spawner, the federation hub as comm bus + board, aiwatcher/arxiv as the senses, and ~190 MCP wrappers as the hands. Zero per-token cost, everything private.
> **Positioning (ratified):** GrokBot = horizontal SaaS (millions of tenants, ~$0 marginal cost/user, metered forever). Sandrafleetbot = vertical sovereign agent (1 user on a 4090 → ~dozen users on one H200-class). Sweet spot 1–20 users.

---

## 1. Target analysis: what GrokBot actually is (Aug 2026)

xAI's agentic stack (verified via web, 2026-08-14):

| GrokBot ability | Detail | Price signal |
|---|---|---|
| Frontier reasoning/coding model | Grok 4.5 GA (2026-07-08); Grok 4.6 = 1.5T param, 80 tps, SWE Marathon 29.0% | $2/M in, $6/M out + sub |
| Agentic coding agent | Grok Build 0.1 (May 2026) + Composer 2.5 — plans, edits repos, opens PRs | Premium sub tier |
| Real-time world knowledge | Native X firehose search | Included, but X-walled |
| Voice | Voice chat in grok.com | Sub |
| Image/video generation | Built-in | Credit-metered |
| Tool use | API + cloud sandbox | Pay-per-action |

**Weaknesses we can exploit:** metered everything (cost scales with work), cloud-locked (no local filesystem, no home automation, no robots), X-walled news, privacy-hostile, no memory of *your* life.

## 2. Fleet component map (all exist TODAY)

| GrokBot ability | Fleet equivalent | Status |
|---|---|---|
| Reasoning LLM (paid) | **Muse Glimmer 30B** — `ollama run muse-glimmer` (18 GB Q4, 128K ctx, text+image, Apache 2.0). Meta Superintelligence Labs' agentic model, **distilled from Muse Spark** for single-GPU agents: tuned for tool use, long tasks, failure recovery (MCP Atlas 75.5, SWE-Bench Verified 76.0). Native Ollama support on NVIDIA since v0.32.8 (2026-08-10). Keep 9B qwen distil as fast tier | ⚠️ update Ollama 0.32.9 → 0.32.11, pull model |
| Agentic coding loop | **cline-mcp** `agent_run` / `agent_team_run` / `agent_session_*` (provider=ollama = zero pay) + **Fritz** `fritz_contribute` (clone→ruff→issue→branch→fix→PR) | ✅ real, needs local-provider default |
| Real-time news (vs X firehose) | **aiwatcher-mcp** (RSS/HF/Readly + LLM distillation + urgency 0-10) + **arxiv-mcp** codehunt/epistemics + openserp | ✅ running |
| Voice | **speech-mcp** (TTS/STT/wake word) + **memops** `adn_audio` (Kokoro + faster-whisper on GPU) | ✅ local, zero pay |
| Image/video gen | **comfyops-mcp** (ComfyUI sidecar on 4090) — replaces paid google-ai-mcp | ⚠️ needs tier wiring |
| Tool use (API integrations) | **mcp-federation-hub** `POST /api/v1/tools/call` — router over ~190 MCP wrappers (fileops, winops, gitops, plex, calibre, blender, robots, …) | ✅ bridge exists |
| Persistent memory | **memops** (advanced-memory-mcp) — knowledge graph, zettel, RAG, external_bridge | ✅ |
| Multi-agent teams + comm | **cline-mcp** `agent_team_run` + **hub** tool router + **memops** `external_bridge` | ✅ pieces exist, no standard path |
| Scheduled/proactive work | **Fritz** coworker (9 scheduled flows) + `agent_schedule_create` | ✅ |
| Chat surface / persona | **learnbot-mcp** personas + Fritz webapp (10997) + Intel Hub (11027) | ✅ |
| Messaging channels | **email-mcp**, **discord-mcp** ✅ · **WhatsApp / Telegram / Signal / Slack** ❌ (comms-mcp spec drafted, not built) | ⚠️ P6 |
| Office documents | **libreoffice-mcp** (26.2.3.2) ✅ · **ms-graph-mcp** (Outlook/calendar/contacts/OneDrive) ✅ · local MS Office COM (Word/Excel/PowerPoint) ❌ easily addable | ⚠️ P6 |

**The gap is not components — it is glue:** no reasoning loop inside Fritz workflows, no standard agent-to-agent comm path, no board, and the local model tier was one weak 9B distil (Muse Glimmer fixes this).

## 3. Architecture (sense → reason → act → remember)

```
SENSE                          REASON                        ACT                          REMEMBER
aiwatcher (news, urgency) ─┐   ┌──────────────────────┐    mcp-federation-hub         memops
arxiv codehunt             ┼─► │  FRITZ (fleet-agent) │──►  POST /tools/call ──► ~190 MCP wrappers
fritz_surveil (logs, PoL) ─┘   │  YAML workflows +     │    (fileops, winops, gitops,  adn_notes / zettel
device telemetry               │  cline agent steps    │     plex, robots, blender,   vla_diary dev entries
                               │  (muse-glimmer, Ollama)│    email, discord, …)       skills as memory
                               └──────────────────────┘
                                        │
                 SURFACES: Hub Board page · webapp 10997 · Intel Hub 11027 · speech-mcp wake word
                 DISCORD (human mirror, sanitized summaries only): #sfb-work · #sfb-thoughts · #sfb-alerts
```

Rules (ratified ORCHESTRATION_HIERARCHY.md applies unchanged):
1. Hub is the ONE registry and the ONE tool router for cross-server calls.
2. Fritz is a client of the hub — no hardcoded server list in `fleet_bridge`.
3. ALL LLM inference routes local (Ollama/LM Studio). Cloud = documented fallback only, < $20/mo budget, never default.
4. One agent inbox + one board (see P2) — no ad-hoc point-to-point REST between agents.
5. No new repos unless a phase proves one necessary. P6 is pre-justified (comms-mcp P4 spec exists, ports 11028/11029 already reserved).

### 3.1 Installer & pack distribution (design)

**Do NOT embed 20 backends in one Tauri.** Sizing reality: PyInstaller onefile backends run ~30–90 MB each (light MCP ~15 MB, pywinauto/OpenCV ~90 MB) → a 20-server installer is **0.6–1.8 GB**, rebuilt in full on every release, and 20 resident uvicorn processes idle at ~40–80 MB RAM each (1–1.6 GB) — violating the ratified demand-only lifecycle pattern.

**Two-layer model: one shell, managed packs.**

```
SFB Operator (Tauri 2.0, ~15 MB shell + one small supervisor backend, embedded)
  ├── SFB UI = hub control plane (dashboard, board, inbox, agent console, pack manager)
  ├── Supervisor = spawn on demand / idle-shutdown / health / update (hub supervisor pattern)
  └── Pack registry → spawns servers from the installed pack (mcpb-style, NOT embedded)
        ├── SFB Core            (everyone)
        └── + interest packs    (opt-in, per user)
```

- **The Tauri app embeds ONE backend** (the hub/supervisor, ~15–30 MB). The 20 MCP servers are **not embedded** — they install from pack manifests (`.mcpb` bundles / release assets) into a pack directory and are spawned on demand, killed when idle (existing `POST /api/shutdown` mandate + fritz_surveil idle-timeout).
- **One operator, many packs.** The shell is identical for everyone; the *pack selection* is the personalization. This is the "robotics-centered SFB version" — it is not a separate product, it is Core + Robotics pack.
- **Install UX:** NSIS installer asks "which packs?" (component selection) OR ships Core and adds packs via the pack-manager UI at first run (download from GitHub Releases, checksum-verified). Packs update independently of the shell — a freecad fix does not rebuild the operator.
- **Pack definitions** (overlaps allowed; curated from the hub bootstrap tiers, not exhaustive):

| Pack | Servers |
|---|---|
| **Core** (everyone) | hub (control plane + board + inbox), fritz, cline, memops, local-llm (muse-glimmer brain), filesystem, winops, gitops, email, discord, libreoffice, speech, aiwatcher, arxiv, secrets |
| **Robotics** | yahboom, ros-mcp, mujoco, gazebo, vla, teleoperator, windows-computer-use |
| **Engineering** | freecad (CFD/FEM), qcad, kicad, chip-design, codecad, mathops |
| **Creative/Media** | blender, gimp, davinci-resolve, plex, calibre, jellyfin, immich, comfyops, speech |
| **Home** | home-assistant, devices, nuki, nest-protect, telephony, dreame |

- **Mode C (startup):** same packs, per-tenant activation — one H200 runs Core + selected packs for the tenant; auth boundary (§4) decides who may spawn what.
- **Naked-PC bar:** operator installer follows the existing NSIS pipeline (hooks, `.env.example` only, size gates); first-run pack manager is the same pattern as the first-run MCP-registration dialog.

**Naked-PC sandbox gate (P8, mandatory before any release) — via the existing cold-install probe infrastructure:**

Reuse `FLEET_COLD_INSTALL_PROBE.md` (meta_mcp orchestrates, virtualization-mcp consumer sandbox executes, Broken\* reinstall-after-fix loop, `fleet-cold-install-report.json` + markdown reports) — SFB is one more "repo" in the probe, but with a pack-aware test matrix:

| # | Step | Verify |
|---|---|---|
| 1 | virtualization-mcp provisions fresh Windows VM (ISO, no dev tools) + baseline snapshot | clean/naked baseline |
| 2 | Install SFB Core NSIS (`/S` silent) | exit 0; **no Python/Node/uv/winget required**; WebView2 bootstrapper path; operator launches |
| 3 | Hub health + board/inbox up | `GET /api/health` 200; `fleet_board` post round-trip |
| 4 | Add Robotics pack via pack-manager UI (checksum-verified download from Releases) | yahboom/mujoco/gazebo spawn on demand; idle shutdown via `POST /api/shutdown` |
| 5 | Reboot VM | supervisor auto-restarts pack (NSSM/task), hub returns, board history intact |
| 6 | Uninstall | clean registry + process kill hooks; no orphan backends |
| 7 | Any failed step → fix → **reinstall-after-fix on fresh snapshot** | probe loop closes |
| 8 | (mode C, later) second tenant on same VM | isolation holds |

Gate: steps 1–7 green on the sandbox before any SFB release ships.

## 4. Auth & tenancy model (deployment-mode-dependent)

**Principle (ratified): auth is a deployment property, not a code property.** The same single-repo server ships authless standalone; in a SFB multi-tenant install it never sees an unauthenticated request because the hub is the only ingress. Do NOT build auth code into every wrapper — build one auth boundary.

| Mode | Who | Auth | Data isolation |
|---|---|---|---|
| **A. Standalone** | one user, one repo (blender-mcp alone) | none — localhost, zero config | none needed |
| **B. SFB solo** | Sandra, full fleet | FLEET_TOKEN on hub management endpoints (exists today) | single-tenant by design |
| **C. SFB multi-tenant** | ~dozen users, H200-class | hub = auth boundary: login → per-request identity | user-scoped state everywhere |

**Architecture:**
1. **Hub is the ONLY ingress.** Servers bind 127.0.0.1 (+ Tailscale for remote); hub authenticates and forwards identity (`X-User-Id`, `X-User-Groups`) on the loopback hop. Servers trust identity only from the hub path — never bind 0.0.0.0.
2. **Stateless wrappers get NO auth code; stateful stores get user scoping.** Blender/GIMP/calibre-as-tool-servers are gated by the hub — zero changes per wrapper. What needs isolation: hub board/inbox, memops memory + vla_diary, comms allowlists (comms spec already has `allowFrom`), fritz schedules, per-user SQLite namespaces (fritz RBAC planned item — becomes a P6b task).
3. **Fleet-synced = ONE user store, no per-server user DBs.** Users+roles live in hub SQLite (secrets-mcp as the vault for keys). Policy (groups, allowlists) read from hub config, never duplicated. A shared `AUTH_SHARED_SECRET` is distributed at install time into each server's `.env` for signature validation when servers must listen beyond loopback.
4. **Implementation ladder, smallest first:** (a) hub strips-and-injects identity headers on the loopback hop → zero server changes, trust by network binding; (b) short-lived signed tokens + tiny middleware, only if a server must bind beyond loopback; (c) full OIDC only when a real customer demands SSO — do NOT build OAuth v0.1.
5. **Timing:** mode C groundwork (user store, identity header, user-scoped board/memory/diary) is a P6b workstream gated on the startup decision. Solo SFB (mode B) needs nothing new — FLEET_TOKEN already covers it.

---

## 5. Protocol posture — preparing for MCP 2026-07-28 & FastMCP 4

**Status (verified 2026-08-14 — corrects fleet docs, which still call it "RC"):**

| Layer | Version | Status |
|---|---|---|
| MCP spec | **2026-07-28** | **STABLE** since 2026-07-28 (RC was 05-29). Stateless core, no sessions/`initialize`, `server/discover`, `subscriptions/listen`, MRTR, CacheableResult (`ttlMs`/`cacheScope`), deterministic `tools/list` order |
| MCP Python SDK | **2.0.0** | **STABLE** since 2026-07-28 — this is the "MCP v2" (v1.29.0 was the last 1.x, same day) |
| FastMCP | **3.4.7** | latest stable remains 3.x; **FastMCP 4.0 stable NOT shipped** (4.0.0b1 beta exists, built on SDK v2) |

**Deprecations (all have a minimum 12-month deprecation window — no panic):** Sampling, Roots, Logging (SEP-2577), HTTP+SSE transport, `includeContext` `thisServer`/`allServers`. `ctx.sample()` keeps working on FastMCP 3.x through the window; migration is planned, not urgent.

**SFB is protocol-forward by design — nothing in the new spec breaks it:**

| Deprecated / removed | SFB posture |
|---|---|
| `ctx.sample()` (server-side sampling) | Not used. Brain tier = **direct local LLM calls** (Ollama muse-glimmer via local-llm-mcp, `fleet-llm` post-sampling pattern — protocol-independent, Anthropic-independent) |
| SSE transport | Not used — all fleet transports are streamable HTTP (`/mcp`) |
| Sessions / roots | Stateless by design — hub routes stateless tool calls; state lives in SQLite (board.db, inbox, memory), not protocol sessions |
| MRTR (`InputRequiredResult`) | Not adopted — spec + both official SDKs (Python 2.0.0, TypeScript 2.0.0) implement it, but **no shipping client does** (verified 2026-08-14: Claude Desktop ✗ probe, Zed ✗ still on 2025-11-25, opencode ✗, Cline ✗). It's a dependency-bump away for clients, not a hard gap — but today a server emitting it gets ignored. Fleet stays on 3.x + direct LLM calls |

**FastMCP 4 / SDK v2 actually help SFB when adopted:** enterprise auth + Client ID Metadata Documents → mode-C tenancy (§4) gets first-class protocol hooks; background tasks / stateless interactivity → fritz_surveil + surge candidates; `server/discover` → hub capability discovery (versions, caps, identity — future hub registry upgrade); multi-era serving → one binary serves 2025-11-25 and 2026-07-28 clients during transition; CacheableResult → cacheable `tools/list` (hub tool router cache).

**Migration triggers (fleet decision, `fastmcp/fastmcp-4-assessment.md`):** do NOT adopt beta. When FastMCP 4.0 stable ships → canary learnbot-mcp (2 weeks) → mechanical fleet upgrade. SFB rule: P0–P5 build against 3.4.x; P6/P7 must not introduce new `ctx.sample()` usage; only adopt FastMCP 4 post-canary.

**References (fleet-internal, mcp-central-docs):** `fastmcp/2026-07-28-spec-migration.md` · `fastmcp/fastmcp-4-assessment.md` · `fastmcp/sampling-migration-plan.md` · `analysis/mcp-2026-07-28-fastmcp-4-fleet-impact.md` · `analysis/fleet-llm-post-sampling-design.md` · `operations/MCP4_MRTR_PROBE_CASE_REPORT.md`. Spec canonical: `modelcontextprotocol.io/specification/2026-07-28` (+ `/changelog`).

---

## 6. Buildout plan (P0→P8, each phase = one gate, ≤ 5 repos touched)

### P0 — Local brain tier (Muse Glimmer) · ~1 day
| Task | Repo / file |
|---|---|
| Update Ollama v0.32.9 → v0.32.11 (drops the llama-server workaround; NVIDIA support landed v0.32.8) | host |
| `ollama pull muse-glimmer` (18 GB → fits 24 GB 4090, ~5 GB headroom; BF16/FP8 of Spark is what does NOT fit) | host |
| Smoke test: chat + vision (screenshot) + function calling + long context | host |
| cline-mcp: default provider `ollama`, default model `muse-glimmer` | `cline-mcp/src/index.ts`, README |
| local-llm-mcp: tier routing (muse-glimmer=heavy, qwen3.5-9b distil=fast) | `local-llm-mcp/src/...` |
| comfyops-mcp: verify ComfyUI sidecar on 4090 for local image gen; google-ai-mcp becomes documented cloud fallback | `comfyops-mcp` |

**Gate:** `agent_run("2+2", provider=ollama, model=muse-glimmer)` sane in < 30 s; vision round-trips; `ollama list` shows muse-glimmer.

### P1 — Fritz reasoning loop (the brain) · ~2-3 days
| Task | Repo / file |
|---|---|
| flowforge YAML: new step type `agent` → cline-mcp `agent_run` (ollama/muse-glimmer); JSON output feeds next step | `fleet-agent-mcp/workflows/`, step executor |
| `fleet_bridge` hardcoded server list → hub discovery API (rule 2) | `fleet-agent-mcp/src/fleet_agent/bridge*.py` |
| Wire `heartbeat_wake` → `workflow_start('coworker')` (known gap) | `fleet-agent-mcp` scheduler |
| Bonus: `ollama launch opencode --model muse-glimmer` scaffold as dev-day loop | host |

**Gate:** `coworker_fleet_pulse` runs end-to-end with an `agent` step composing the report (not a hand-written template); deliverable lands by 07:15.

### P2 — Agent comm bus + private bulletin board · ~2-3 days
Two distinct surfaces — do not conflate (moltbot's channel insight: history is first-class, delivery is not a board):

| Surface | Component | What it is |
|---|---|---|
| **Board (broadcast + archive)** | `fleet_board` in mcp-federation-hub bridge (SQLite `board.db`, REST + FastMCP tool) | channels (`#fleet-pulse`, `#dev-worklog`, `#handoffs`), posts, threads (`parent_id`), full history, FLEET_TOKEN auth |
| **Durable log (queryable)** | **vla_diary dev notebook (the fleet agent diary — already exists in vla-mcp)** + memops notes | structured entries (`category=repo_fix/decision/blooper/note`, `repo:` tag, `metrics`), three notebooks (dev/personal/news), queryable via `vla_diary` list/get/summary |
| **Delivery (addressed)** | hub inbox `POST /api/v1/inbox/send` + `GET /api/v1/inbox/poll` | point-to-point handoffs (`voice_command_bus.yaml` entities: fritz, miko, boomy) |

**Board stays private, Discord is the human window.** The board is a moltbot-style *pattern* reimplemented fleet-private: the hub bridge (NSSM 24/7, already the router, already authed) hosts `fleet_board` portmanteau (post/list/reply/search/subscribe) over SQLite. Humans read it on the hub webapp Board page + Intel Hub HTML digest (iPad/Tailscale). Everything bound 127.0.0.1 + Tailscale.

**Discord human layer — "our own moltbot" (via discord-mcp, existing fleet infra):**

| Channel | Content | Cadence |
|---|---|---|
| `#sfb-work` | Task boundaries + deliverables: "started X", "X done — PR #n, report at hub link". One-liners derived from board `#dev-worklog` summaries | max 2 per task (start + end) |
| `#sfb-thoughts` | Ideas, observations, open questions — the agent persona voice. Non-secret brainstorm | on insight, ≤ 1/h/agent |
| `#sfb-alerts` | Urgent only: fritz_surveil hits, spend-watch thresholds, high-urgency aiwatcher items | on trigger |
| (existing `#general` / `#announcements`) | Weekly fleet pulse, release summaries — keep the DISCORD_FLEET_BOT pattern as-is | per schedule |

**Posting policy (non-secret, non-spammy — enforced in the same workflow hooks as the board protocol):**
1. Discord carries **sanitized human summaries only** — never raw tool output, tokens, paths, credentials, or payload data. Raw state stays in board/diary (third-party cloud rule applies to data; summaries are derived).
2. **Posting budget:** ≤ 2 posts per task (start + end), ≤ 1 thought per hour per agent, alerts only on real thresholds. Routine successes are NOT posted — they live on the board; only deltas and decisions reach Discord.
3. Posts are generated from the board entry (same hook writes board + Discord), so the machine record is always the source of truth.

**Crosspost → agent diary (vla_diary dev notebook):** every Discord post also lands in the diary in the same hook — three writes, one event:

| Discord post | vla_diary dev entry |
|---|---|
| `#sfb-work` start | `category=note`, title "started X", tags `agent:<name>`, `repo:<repo>`, metrics `board_post_id` |
| `#sfb-work` done | `category=repo_fix` (or `decision`), title "X done", metrics: outcome, board_post_id, discord_message_id |
| `#sfb-thoughts` | `category=note` (promoted to `decision` if it becomes one), tags `agent:<name>` |
| `#sfb-alerts` | `category=blooper` (anomaly caught) or `decision` (threshold action), metrics: urgency, board_post_id |

`author` is always the posting agent; the board post id and Discord message id ride along in `metrics` so the three surfaces stay traceable to one event. The diary is the queryable archive — "what did agent X work on yesterday" is a `vla_diary list` with `category`/tag filters, no Discord scroll needed.

**Canonical posting protocol (written, enforced in workflows):**
1. Post WIP to the board channel **and** a durable diary entry on completion — never channel-only, never inbox-as-board.
2. Inbox is addressed delivery only; it carries no browsable history by design.
3. Agents read board history before starting new work (prevents duplicate ownership).
- Cross-server tool calls: hub router. memops `external_bridge` stays for memory-context calls only (documented, not duplicated).
- Fritz `agent_send` / `agent_poll` tools over the inbox.

**Gate:** agent A posts WIP; agent B (fresh context) reproduces A's state from channel history + diary query; handoff passes A→B via inbox with zero direct REST; diary entry's `board_post_id`/`discord_message_id` metrics trace to the same event.

### P3 — Senses (fritz_surveil + surge) · ~2-3 days
| Task | Repo |
|---|---|
| Build `fritz_surveil` per FLEET_DEEP_ANALYSIS_2026-07-13 §1: one triage engine, two domains (`external` news, `fleet` logs/health precursors); urgency → inbox → admiral notify. Triage router, NOT a SIEM | `fleet-agent-mcp` |
| aiwatcher surge mode: urgency ≥ threshold → inbox immediately (not only daily digest) | `aiwatcher-mcp` |
| arxiv codehunt repoll hits → inbox fan-out (already push to aiwatcher) | `arxiv-mcp` |

**Gate:** test high-urgency event (`ingest_fleet_event` urgency 9) reaches a surface in < 5 min.

### P4 — Memory + persona · ~2 days
| Task | Repo |
|---|---|
| End-of-task memory hooks: every cline agent task ends with memops `adn_notes quick` + `vla_diary` dev entry (`repo:` tag) | `cline-mcp` (wrap agent loop) |
| Skills as first-class memory (Viktor steal #2): Fritz `memory_card_create(type=skill)`; proactive cron suggestions (steal #1) on repeated manual asks | `fleet-agent-mcp` |
| learnbot persona `fritz` for chat surface | `learnbot-mcp` |

**Gate:** after one P1 run, `adn_search` finds yesterday's pulse; repeated manual ask auto-suggests a schedule.

### P5 — Surfaces + hardening · ~1-2 days
- Hub webapp Board page + Fritz webapp 10997 (live agent runs + inbox) primary; Intel Hub 11027 keeps reports; **Discord `#sfb-work` / `#sfb-thoughts` / `#sfb-alerts` as the human notification window** (sanitized summaries per the P2 posting policy — zero raw agent data on third-party infra).
- speech-mcp wake word → `agent_run` voice-in/voice-out loop.
- Security: FLEET_TOKEN on hub management endpoints; single `.env` source of truth per repo (plex-mcp lesson).
- **Gate:** full "morning briefing" demo — wake word → briefing spoken → report in Hub + board — zero cloud calls.

### P6 — Channel & office gaps (user-flagged) · ~1 week
| Gap | Plan | Notes |
|---|---|---|
| **WhatsApp** (no wrapper) | Build **comms-mcp** per existing P4 spec (`operations/planning/specs/P4-comms-mcp.md`, ports 11028/11029 reserved). v0.1 Telegram (Bot API, easiest headless E2E) → v0.2 Signal → **v0.3 WhatsApp via baileys** (self-hosted, private — NOT the Meta Business API, which is verify-heavy and cloud-bound). Adapters behind one `comms_ops` portmanteau; secrets via P1 `secrets_resolve`; 7-day message-body TTL; inbound sanitization (email-mcp pattern) | This is the ONE new repo the plan needs; spec already drafted |
| **MS Office** (libreoffice only) | Add local Office COM bridge: `win32com` automation of Word/Excel/PowerPoint/Outlook — either ops in winops-mcp or a thin `ms-office-mcp`. ms-graph-mcp (11148/11149) already covers Outlook/calendar/ToDo/OneDrive via Graph for the cloud side | COM = classic pywin32, ~1 day; decide repo placement during P6 kickoff |
| **Slack** | comms-mcp v0.2 Socket Mode (spec exists) | only if needed; Viktor analog |

**Gate:** WhatsApp message in/out round-trip via baileys self-hosted; Word doc create/edit via COM; zero data leaves the box except the message itself.

### P7 — Crunch hardening (90%-ready repos) · ongoing, ~1-2 weeks first pass
Known crunchy inventory (honest, dated — verify before trusting):

| Item | Evidence | Fix |
|---|---|---|
| **myconf / teleconference-mcp untested** | tauri-pitfalls-scan: myconf CRITICAL Bug#2 (no TCP health check), Bug#6 (backend spec missing), Bug#8 (no size gate); HIGH #1/#3/#4/#9 | Fix spec + health check + size gate; then `just cua-nsis-test`; then real conference test |
| **Monitoring runs "in theory"** | `status/FLEET_MONITORING_STATUS.md` (2026-07-06): aiwatcher HTTP ❌, arxiv codehunt not running, fritz not persistent. Doc is 5+ weeks old — re-verify first | Re-audit liveness; Fritz as NSSM service (hybrid NSSM already supported); wire scheduler |
| **Gate-sweep FAILs** | `audits/gate-sweep-2026-08-06.csv` (e.g. fritz-pipeline-test pyright FAIL) | `assfix` per repo in severity order |
| **"Planned" webapps / reserved frontends** | Port registry rows marked "planned", "not yet built" | Only build the ones SFB actually calls; the rest stay dormant — do not gold-plate |
| **Runt webapps** (catch-them-all gate) | Repos shipping < 7 real pages | fakefind audit + fill only where SFB routes through it |

**Hardening pass order:** (1) myconf/teleconference test + Tauri bug fixes, (2) monitoring liveness + fritz NSSM, (3) gate-sweep FAIL repos assfix, (4) verify hub core (bridge + supervisor) under SFB load. Never more than 5 repos per batch.

**Packaging (P8, follows §3.1):** operator shell (hub + supervisor embedded) → pack manifests per §3.1 table → NSIS installer with pack component selection → pack-manager UI for post-install packs. Gate: clean-PC install of Core; pack add without shell rebuild — both run in the virtualization-mcp consumer sandbox (naked-PC matrix above) before any release.

**Gate:** `fleet_board` health post shows all P7 items with status; every SFB-critical repo passes its `assfix` terminal gate + cua test where applicable.

---

## 7. Cost model (the zeropay claim)

| Item | GrokBot | Sandrafleetbot |
|---|---|---|
| LLM tokens | $2/$6 per M | €0 (4090) — electricity ~€0.10/day heavy use |
| Agent runs | metered | €0 |
| Image gen | credits | €0 (ComfyUI local) |
| Voice | sub | €0 (Kokoro/whisper local) |
| News | X sub | €0 (RSS + scraping) |
| Messaging | bundled | €0 (baileys self-hosted; WhatsApp account required) |
| Office | bundled | €0 (LibreOffice + COM) |
| Floor | ~$50–200+/mo realistic | **€0 + electricity** |

Cloud fallback (cursor-mcp spend watch already exists): budget < $20/mo, alert at threshold — mirror of `coworker_cursor_spend_watch`.

## 8. Positioning & scaling envelope (vs GrokBot)

Correct fundamental split: **GrokBot = horizontal SaaS** (millions of concurrent tenants, hyperscale serving, marginal cost ~0/user); **Sandrafleetbot = vertical sovereign agent** (single-tenant local, integration-depth moat, zero metering).

| Envelope | Hardware | What limits it |
|---|---|---|
| Solo dev (Sandra) | RTX 4090, 24 GB | nothing — muse-glimmer Q4 fits, fleet is single-tenant by design |
| Dozen-user startup | one H200-class (141 GB HBM3e, ~4.8 TB/s) | **not VRAM — multi-tenant hygiene** (§4 mode C): hub auth boundary, user-scoped board/inbox/memory/diary, per-user SQLite, FastMCP concurrency safety. Isolation work, not compute |
| Hundreds of users | fleet of GPUs | GrokBot's economics win; SFB stays a private niche — do not chase |

**Sweet spot:** 1–20 users, where cloud metering hurts and integration depth + data locality matter. Beyond that, the model+serving moat wins and SFB's position is privacy/sovereignty, not cost.

### 8.1 Capability asymmetry — hands GrokBot does not have

Beyond cost, SFB ships capabilities GrokBot structurally lacks: its hands are a cloud sandbox; ours are the local hardware, the licensed toolchain, and the physical world. GrokBot's model may be 50× bigger — it still cannot click your EDA tool or drive your robot.

| Capability class | Fleet repos (all exist) | Why GrokBot can't |
|---|---|---|
| **EDA / VLSI** | kicad-mcp (11016/11017, schematic/PCB via KiCad), chip-design-mcp (11022/11023, EDA orchestration) | Cloud agent has no KiCad install, no license seat, no local project tree |
| **CAD / CFD / FEM / BIM** | freecad-mcp (10944/10945 — CAD, CFD velocity fields, FEM, BIM), qcad-mcp, codecad-mcp (build123d) | Multi-hour meshing/solving loops on local cores; results are files on this disk |
| **Robotics / simulation** | yahboom-mcp (10892/10893), ros-mcp (11050/11051), mujoco-mcp (11046/11047), gazebo-mcp (10990/10991), vla-mcp | Physical actuators + local sim state; no cloud round-trip can steer a real wheel |
| **Computer use (Win32)** | windows-computer-use-mcp (10788/10789), ocr-mcp, pywinauto | GrokBot's ToS sandbox ≠ your session; CUA runs on the actual desktop |
| **Home / devices** | home-assistant-mcp (10778/10834), devices-mcp (10716/10717), nuki-mcp, nest-protect-mcp | Your house is not in their datacenter |
| **Local media + content** | plex-mcp, calibre-mcp (full-text RAG), jellyfin-mcp, immich-mcp | Private libraries the cloud never sees |
| **OS control plane** | winops-mcp, filesystem-mcp, system-admin-mcp, virtualization-mcp | Cloud agent gets no admin over this box |

Honest boundary: a user *could* wire Grok's API to local MCP servers manually — the asymmetry is not that Grok can never touch these, it's that SFB ships the entire chain **pre-wired and priced at zero**, while Grok requires assembling MCP configs and paying per token for every step of every long-horizon task (an EDA run is hundreds of reasoning calls). The model-ceiling tradeoff (muse-glimmer 30B vs 1.5T) is real, but it operates *within* a capability envelope the competitor cannot enter at all — the "kicad or CFD work" argument is the strongest line in the pitch.

## 9. Risks & guardrails

- **Model quality ceiling:** muse-glimmer (30B, Spark-distilled) is NOT Grok 4.6 (1.5T). Accept and weaponize: GrokBot cannot touch the fleet's local surfaces; we compete on integration sovereignty + zero cost, not raw benchmark. Glimmer's MCP Atlas 75.5 / SWE-V 76.0 is already agent-grade; heavy single-shot reasoning stays a documented cloud fallback.
- **VRAM pressure:** ComfyUI + muse + whisper on one 24 GB card — P0 verifies headroom; if tight, time-share (comfyops on demand + shutdown hook).
- **Agent runaway:** every destructive action keeps the existing confirmation gates (SOUL policy, workflow branches, DESTRUCTIVE annotations).
- **Board spam / stale posts:** retention policy on board channels (TTL per channel); diary is the durable record, board is prunable.
- **baileys ToS risk:** WhatsApp's web protocol is unofficial; treat comms-mcp as a convenience adapter with clear failure modes (re-link QR) — acceptable for a private single-tenant stack, documented in the P4 spec.
- **Batch rule:** each phase touches ≤ 5 repos; `.bak` copies for batch edits; checkpoint commits.
- **No new repos** beyond the pre-justified comms-mcp (P6) — everything else is glue over existing infra.

## 10. Success criteria (measurable)

- [ ] muse-glimmer serves all fleet LLM calls; monthly cloud spend **€0** (or documented exception)
- [ ] `coworker_fleet_pulse` runs 7 days unattended with an agent-composed (not template) report
- [ ] One end-to-end agentic PR lands via cline + fritz_contribute on a test repo
- [ ] fritz_surveil flags a real fleet anomaly before a human notices
- [ ] Cross-agent comm happens only through hub inbox + board (audit: zero ad-hoc REST)
- [ ] Voice briefing demo works end-to-end, local-only
- [ ] WhatsApp + Telegram round-trip via comms-mcp; Word/Excel via COM
- [ ] myconf/teleconference passes CUA smoke test; Tauri Bug#2/#6/#8 fixed
- [ ] SFB-critical repos all green on the terminal assfix gate
- [ ] (mode C) two users on the same hub have fully isolated boards/memory/diaries; policy enforced via hub identity — no per-server auth code
- [ ] Discord human layer live: task start/end posts in `#sfb-work`, at least one agent "thought" in `#sfb-thoughts`, alert in `#sfb-alerts` — all sanitized summaries, no raw tool output
- [ ] Installer demo: Core pack installs on a clean PC in one NSIS run; Robotics pack adds yahboom/mujoco/gazebo without reinstalling the shell; idle servers shut down and cold-start in < 60 s

## 11. Related docs

| Location | Content |
|---|---|
| `../fritz-coworker/` | Coworker pilot — 9 flows, current gaps |
| `../../standards/VOICE_COMMAND_BUS.md` | Agent addressing scheme |
| `../../operations/planning/specs/P4-comms-mcp.md` | comms-mcp PRD (WhatsApp/Telegram/Signal/Slack) |
| `../fleet-agent-mcp.md` | Fritz canonical page |
| *(fleet-internal)* `architecture/ORCHESTRATION_HIERARCHY.md` | Hub/Fritz/domain layering rules — mcp-central-docs, private |
| *(fleet-internal)* `architecture/FLEET_DEEP_ANALYSIS_2026-07-13.md` | fritz_surveil spec §1 — mcp-central-docs, private |
| *(fleet-internal)* `status/FLEET_MONITORING_STATUS.md` | Liveness baseline (re-verify in P7) — mcp-central-docs, private |
| *(fleet-internal)* `audits/gate-sweep-2026-08-06.csv` + `logs/tauri-pitfalls-scan.csv` | Crunchy-repo evidence — mcp-central-docs, private |

*Tags: #sandrafleetbot #grokbot #zeropay #agent #orchestration #spec*
