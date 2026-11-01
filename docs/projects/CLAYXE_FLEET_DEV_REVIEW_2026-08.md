# Clayxe Fleet Dev Review — Reaction, Plan, Recommendations

**Status:** PLAN (approved to execute in waves)
**Created:** 2026-08-13
**Owner:** sandraschi
**Source:** clayxe external review of `sandraschi` public GitHub footprint (4 recommendations)
**Session notes:** advanced-memory vault, folder `fleet/` — "Clayxe Fleet Dev Review - Raw Recommendations 2026-08" + "Clayxe Fleet Dev Review - Assessment and Plan 2026-08"

---

## Context & Bias Note

clayxe reviewed only the **public GitHub footprint**. It cannot see the internal
standards in this repo, which is why two of its four recommendations describe
things that are already fleet law:

- Rec 2 (Playwright E2E) → already mandatory via
  [playwright_e2e_sota.md](../standards/rules/playwright_e2e_sota.md),
  [cua_webapp_testing.md](../standards/rules/cua_webapp_testing.md), `just e2e`,
  `scripts/playwright-audit.ps1`, and the `certify` macro.
- Rec 4 (dependency isolation) → already solved by per-repo `uv` venvs, the
  PyInstaller SKIP list, NSIS/Tauri single-installer packaging, and containerized
  engines for heavy compute.

That does not make the review worthless. The two genuinely novel items (1 and 3)
are real architectural gaps worth acting on. This document is the reaction,
the plan, and the recommendation set.

---

## Verdict Table

| # | Clayxe recommendation | Fleet verdict | Action |
|---|----------------------|---------------|--------|
| 1 | Cross-server federation / event bus | Real gap, wrong proposed mechanism | Formalize hub-and-spoke contract; **do not build a bus** |
| 2 | `just test-ui` Playwright smoke in Justfile template | 80% already standard | Add only the visual-regression delta |
| 3 | Unified exception-telemetry schema + SQLite ring buffer | Best rec — real, cheap, high leverage | **Priority 1** — spec + shared helper + depot storage |
| 4 | Bootstrap speed / dependency isolation | Already solved | No action; optionally document tiering |

---

## Recommendation 1 — Cross-Server Federation & State Bridging

### Reaction

Half-right. The silo observation is accurate: 120+ independent FastMCP instances
cannot natively share state, and an agent workflow spanning Calibre → database
write → UI test currently requires either manual handoffs or stringly-typed
REST calls. But the proposed remedy — "expand a centralized event-bus or shared
DiskStore" — is the wrong architecture for this fleet.

### What already exists (point-to-point, and working)

| Mechanism | Where | Role |
|-----------|-------|------|
| `ingest_fleet_event` | aiwatcher-mcp | De-facto fleet event sink (`POST /api/fleet/ingest`) |
| `[media-traction]` push | arxiv-mcp → aiwatcher | Structured fleet events from code-hunt pipeline |
| Artifact depot | depot-mcp | Cross-repo artifact lookup (infrastructure tier, no webapp) |
| `external_bridge` | advanced-memory-mcp | Calls tools on other MCP servers by name |
| `vla_fleet call_peer` | vla-mcp | REST tool bridge to simulation peers |
| Fleet orchestration | fleet-agent-mcp | Headless fleet conductor |

### Why not a bus

1. **SPOF.** Every server currently degrades gracefully when a peer is down.
   A central bus makes 120 repos dependent on one daemon's uptime.
2. **Stdio-only servers cannot participate.** Claude Desktop / Cursor spawn
   stdio instances that have no inbound HTTP surface and cannot receive
   push events. The bus would silently only serve the HTTP-daemon tier.
3. **Trust surface.** A bus that accepts arbitrary writes from any fleet
   server is an injection vector. Point-to-point bridges authenticate per hop.
4. **Simplicity-first.** The existing topology already routes the three
   traffic classes that actually occur: events → aiwatcher, artifacts → depot,
   orchestration → fleet-agent. A bus would be a third daemon doing what two
   already do.

### Plan — formalize the hub-and-spoke contract

The gap is not technology, it is **documentation**. Agents and servers don't
know the handoff contracts exist, so every cross-server workflow reinvents
a bespoke bridge.

**Deliverable:** `patterns/FLEET_FEDERATION_CONTRACT.md` — the canonical map:

- **Events** (fire-and-forget telemetry, alerts, cross-server signals) → POST
  to aiwatcher `ingest_fleet_event` with the existing payload shape.
- **Artifacts** (files, datasets, exports that outlive a session) → depot-mcp
  store/lookup operations. No raw file paths across servers.
- **Control** (orchestrated multi-server workflows) → fleet-agent-mcp only.
- **Peer calls** (one-off tool invocation on another live server) →
  advanced-memory `external_bridge` or vla `call_peer`; allowed but discouraged
  for anything stateful.

**Supporting changes:**

1. Add the contract to the assfix checklist (one check: "does this repo's
   cross-server code follow FLEET_FEDERATION_CONTRACT?").
2. Add a fleet-wide grep audit for bespoke bridge patterns (servers calling
   sibling servers' REST endpoints directly) — flag, don't fix.
3. Extend `fleet_ops registry_load` payload with per-repo bridge roles so
   fleet-agent can answer "who consumes X" without a bus.

**Non-goal:** any new daemon, any pub/sub infrastructure, any Tailscale-mesh
shared filesystem. Tailscale already provides the transport; the CORS regex
already covers `*.ts.net` origins.

---

## Recommendation 2 — Automated GUI/E2E Regression Coverage

### Reaction

Already 80% fleet law. The `just test-ui` recipe clayxe proposes exists in
substance as:

- `playwright_e2e_sota.md` — mandatory Playwright e2e per webapp repo
- `just e2e` → `scripts/playwright-audit.ps1` (backend health + frontend loads,
  zero-tolerance console errors)
- `cua-webapp-test` — headless browser walk: stack start → Connected badge
  wait → title-matching nav click-through → per-page screenshots
- `certify` macro runs `npx playwright test` as a gate
- CI runs Playwright on push

### The real gap — visual regression

Nobody does **pixel-diff regression**. The CUA walk captures screenshots, and
Playwright asserts DOM state, but a CSS/Tailwind refactor that breaks layout
without breaking selectors slips through both. That is the only novel delta in
this recommendation, and it is small:

**Plan:**

1. Extend `playwright-audit.ps1` with an optional baseline mode:
   `-Baseline` captures per-page PNGs into `webapp/e2e/screenshots/`;
   default mode diffs current run against baseline with a threshold
   (proposal: ≥ 2% changed pixels = FAIL with diff PNG written to reports).
2. Add the recipe to the fleet justfile as `test-ui-baseline` / `test-ui-diff`
   (do NOT create a new `just test-ui` name — `just e2e` already occupies
   that namespace; rename would break muscle memory across 100+ repos).
3. Roll out to the 5 flagship webapps first (pywinauto-mcp, calibre-mcp,
   plex-mcp, windows-computer-use-mcp, opencode-cli-mcp), then template-sync.

**Non-goal:** replacing Playwright with a commercial visual-diff service;
per-pixel flakiness on animated dashboards (health dots pulse — the diff region
must exclude elements with animation classes, or the check goes flaky forever).

---

## Recommendation 3 — Unified Error Recovery & Self-Healing Telemetry

### Reaction

The best recommendation in the list. Genuinely new, genuinely high leverage,
and it costs a spec + one shared helper — not new infrastructure.

### Current state

- Per-server `query_logs` ring buffers exist (aiwatcher, arxiv, advanced-memory)
  but each has its own schema and its own query tool.
- CUA (windows-computer-use-mcp) already captures DOM trees and OCR snapshots
  on failure and exposes `analyze_failures` — but only CUA-side.
- Nothing lets an agent ask "why did the last three attempts fail across
  similar tools" because the failure records are (a) unstandardized and
  (b) scattered across repos.

### Plan — one schema, one sink, one query

**Deliverable 1: schema spec** — `patterns/FLEET_ERROR_TELEMETRY.md` defining
the canonical `fleet_error` JSON record:

```json
{
  "schema": "fleet_error/v1",
  "ts": "2026-08-13T09:00:00Z",
  "server": "windows-computer-use-mcp",
  "tool": "automation_elements",
  "operation": "click",
  "error_type": "element_not_found",
  "message": "...",
  "params": {"title": "Save", "fallbacks_tried": 3},
  "failure_state": {"dom_tree": "...", "ocr_text": "...", "screenshot_path": "..."},
  "recovery": ["use title= instead of text=", "maximize window first"]
}
```

**Deliverable 2: shared helper** — `templates/fleet_error_telemetry.py`, one
copy-paste module with `record_fleet_error()` (writes local SQLite ring buffer)
and `query_fleet_errors(tool=..., error_type=..., last_n=...)`. Server-local
first: each repo keeps its own ring buffer exactly like today, so no new
daemon and no SPOF.

**Deliverable 3: cross-server aggregation** — depot-mcp gains two operations:
`fleet_errors_ingest` and `fleet_errors_query`. Servers that run as HTTP
daemons POST their ring buffer entries on a schedule (or on shutdown); the
depot becomes the "why did the last three attempts fail" query point, reusing
its existing SQLite. Stdio-only servers stay local-only — acceptable, since
they are not the ones running autonomous missions.

**Deliverable 4: agent loop integration** — in windows-computer-use-mcp (the
flagship autonomous runner), wire `query_fleet_errors` into the retry path:
before retrying a failed element interaction, the mission runner queries the
depot for the same `error_type + tool` pattern and prefers the recorded
`recovery` hint over blind retry.

### Rollout order

1. Schema + helper template (touches only mcp-central-docs)
2. Adopt in the 3 servers with existing ring buffers (aiwatcher, arxiv,
   advanced-memory) — migrate their `query_logs` to emit `fleet_error/v1`
3. depot-mcp ingest/query ops
4. CUA retry-path integration
5. Add to new-repo gate: "tool errors return `error_type` and
   `recovery_options`" (already partially law via TOOL_DESIGN_STANDARDS §7)

---

## Recommendation 4 — Dependency Footprint & Bootstrap Speed

### Reaction

Already solved by existing architecture. Nothing to do.

| clayxe concern | Existing solution |
|----------------|-------------------|
| ocr-mcp / ML-heavy repos bloat the environment | Per-repo `uv` venvs — heavy deps never enter another repo's environment |
| Heavy deps inflate shipped binaries | PyInstaller SKIP list (`torch`, `grpc`, `pyarrow`, ...) filtered from `a.binaries` |
| Naked-PC installs | NSIS/Tauri single-installer; no Python/Node required on target |
| GPU/ML engines | Containerized (ai-games-collection engines, Magenta RT, etc.) per docker-containerization.md |
| `just bootstrap` isolation | Already per-repo; heavy extras are `[project.optional-dependencies]`, not core |

**Optional polish (low priority):** document a two-tier dependency policy in
`standards/` — "utility tier" (FastMCP + httpx only) vs "compute tier" (GPU/ML
allowed) — so new-repo reviews have a one-line rule to enforce instead of
judgment calls. One section, not a new standard.

---

## Execution Waves

| Wave | Item | Scope | Risk |
|------|------|-------|------|
| **W1** (DONE 2026-08-13) | Rec 3 deliverables 1-2: `patterns/FLEET_ERROR_TELEMETRY.md` + `templates/fleet_error_telemetry.py` (smoke-tested) | mcp-central-docs only | None |
| **W2** (DONE 2026-08-13) | Rec 3 deliverable 3: depot-mcp `FleetErrorStore` + `fleet_errors` tool + REST router + 5 tests | 1 repo | Low |
| **W3** (DONE 2026-08-13) | Rec 2: `-Baseline` visual regression in playwright-audit.ps1 + `scripts/visual-regression.mjs` + `visual-regression-diff.py` (verified 0.00% drift live). Baselines captured: pywinauto-mcp, opencode-cli-mcp, calibre-mcp, plex-mcp (`e2e/visual-baseline/dashboard.png`). Audit script now framework-aware (Vite/Next), backend-module + health + cwd auto-detection | mcp-central-docs + 4 flagships | Medium (solved: animation-kill CSS) |
| **W4** (DONE 2026-08-13) | Rec 1: `patterns/FLEET_FEDERATION_CONTRACT.md` + assfix 1T check + fleet audit (2 findings: rustdesk 10806 port bug, yahboom-dreame bridge) | mcp-central-docs | None |
| **W5** (DONE 2026-08-13) | Rec 3 deliverable 4: pywinauto-mcp `fleet_error_hints.py` + mission `_run_steps` failure branch (record + depot hints, fail-soft) + 12 tests | 1 repo | Medium |
| **W6** | Rec 4: optional dependency-tiering doc section | mcp-central-docs | None |
| **Backlog** | Bridge-pattern fleet audit (grep, flag, don't fix) | Fleet-wide read-only | None |

## Non-Goals

- No new daemons (no event bus, no pub/sub broker, no telemetry server)
- No external services, no SaaS visual-diff tooling
- No changes to public visibility or outreach (per clayxe's own constraint)
- No rewrite of existing ring buffers — migration, not replacement
- No work on repos that already pass their gates — every wave is additive

## Open Questions

1. Visual-regression threshold: 2% pixel delta too strict for dashboard
   animation? Resolve empirically on the 5 flagship apps before templating.
2. Should `fleet_error` screenshot payloads store paths or base64 in the
   depot? Paths are cheap but break when the source machine is offline —
   propose paths + optional base64 flag for critical failures.
3. Does fleet-agent-mcp consume the depot error feed for its weekly retro,
   or stay out of the loop? Propose: consume, read-only.
