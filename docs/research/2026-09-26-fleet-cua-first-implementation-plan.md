# Fleet CUA-first Implementation Plan - cost/time weighed

**Date:** 2026-09-26
**Prior:** research/2026-09-26-fleet-vs-claw-parity.md, research/2026-09-26-openclaw-alternatives-sandbox.md
**Decision:** robofang `cua_ops` goes high (P0). Thin orchestration over existing blocks, not a rebuild.
**Grounding:** pywinauto-mcp 18-22 ops (cua_env, cua_hud, vision, OCR, HITL/kill-switch, 10789/10788), uitars-mcp 8-10 tools (mss+pyautogui, Playwright, VLM qwen2.5-vl:7b Ollama default, 10976/10977), speech-mcp 20-30 tools (FunASR sidecar :10914, voice bus, 10909/10908), secrets-mcp 6 ops (resolve never raw), discord-mcp 43-47 ops (10756/10757), deepfang 2-file gate (10956-10960, fleet-start disabled).

## Principles

1. Reuse, do not rebuild. cua_ops delegates. New code is glue + gates + audit.
2. Local-first = zero marginal cost. Ollama qwen2.5-vl:7b + FunASR default. Cloud only for adjudication (DeepSeek cents) or opt-in Claude SDK.
3. Fail-closed. Every CUA action passes deepfang pipeline + confirm queue. No direct pyautogui from agent context.
4. Max 5 files per commit, .bak for 3+ file edits, claim ports via claim_ports.py (none needed here, all reuse).
5. Prove by running: screenshot -> ground -> gate -> act -> audit, on Goliath, every phase.

## Phase 0 - Hygiene (0.5 day, ~0 cost, unblocks all)

| # | Task | Owner repo | Cost/time | Verify |
|---|---|---|---|---|
| 0.1 | Rotate `EMAIL_MCP_PASSWORD=vienna2026` in aiwatcher, move to secrets-mcp resolve | aiwatcher-mcp | 1h, 0 | grep shows no default, resolve path works |
| 0.2 | Set `CLOUD_PROVIDERS_ALLOWED=false` default everywhere, document override | aiwatcher, fritz, robofang | 1h, 0 | local-only boot passes |
| 0.3 | Pin VLM default `qwen2.5-vl:7b` Ollama + FunASR sidecar docs | uitars-mcp, speech-mcp | 1h, 0 | `screenshot -> ground` local demo |

Why first: cheapest risk reduction, no dependencies.

## Phase 1 - robofang cua_ops (P0, 3-5 days total, ~0 + cents)

Thin portmanteau `cua_ops(operation=...)` in robofang. No new CV, no new VLM. Delegates to pywinauto-mcp:10789 + uitars-mcp:10976 + speech-mcp:10909, gated by deepfang:10956 + secrets-mcp.

### 1A Observe-only (1 day, 0 cost) - ship first

Ops: `status | screenshot | ground | help`
* `screenshot` -> uitars-mcp screenshot (mss) or pywinauto capture.
* `ground` -> uitars vlm_client with qwen2.5-vl:7b local, returns {x,y,label,confidence}. No clicks.
* Read-only, no gate needed except audit log.
* Files: robofang `mcp/tools/cua_ops.py` (new, 1 file), `mcp_server.py` register (1 file), `docs/CUA_OPS.md` (1 file). 3 files max.
* Verify: `cua_ops screenshot + ground "Close button"` on Notepad, confidence logged, zero clicks.

### 1B Gated action (2 days, cents for DeepSeek adjudication)

Ops add: `click | type | browser_navigate | browser_act | approve | deny | audit`
* Flow: agent proposes -> deepfang sanitize/adjudicate -> confirm queue (robofang Hub Inbox, reuse webhooks POST /audit pattern) -> pywinauto/uitars execute -> audit.
* Deterministic grounding: try pywinauto adaptive title/auto_id/OCR first, fall back to VLM. Structured action space only (no free shell strings).
* Safety: HITL from pywinauto safety.py + kill-switch reused, deepfang rules.yaml deny rm-rf/curl|bash/encoded, per-task iteration cap 10.
* Secrets: any credentialed page via secrets-mcp resolve, never paste raw.
* Files: `cua_ops.py` extend (1), `web` Inbox confirm queue (1-2), `POLICIES.cua.yaml` (1). Per-commit <=5.
* Verify: scripted Notepad open -> type -> save -> close, with 1 deny case (blocked rm-rf) + audit entries.

### 1C Voice + CUA loop (1-2 days, 0 cost)

Ops add: `voice_command | watch`
* Reuse speech-mcp voice_bus (openWakeWord -> FunASR -> POST /api/voice/intent) -> robofang cua_ops. Speak back via Edge-TTS/Kokoro.
* `watch` = poll screenshot + VLM diff, optional, capped 30s interval.
* Verify: spoken "open Notepad and type hello" -> executes 1B path -> speaks done.

Total Phase 1: ~4 days solo + agents, 0 infra cost, DeepSeek adjudication cents per 1k actions. Impact: AutoGLM parity without Zhipu lock-in, using your own stack.

## Phase 2 - Shared sandbox executor (2-3 days, ~0)

Make deepfang the mandatory gate for fritz + cua_ops.

| # | Task | Cost/time | Verify |
|---|---|---|---|
| 2.1 | `POLICIES.yaml` endpoint (L1 zones workspace/controlled/protected/forbidden, L3 blocklist) | 4h | fritz + robofang query same file |
| 2.2 | `checkpoint/restore` snapshot API (copy OpenAkita L4, per-group dir) | 1d | file write -> restore demo |
| 2.3 | Per-agent container lease (extend worker:10960, not single shared) | 1d, Docker existing | two agents isolated, no cross-mount |
| 2.4 | Enable fleet-start (currently Kind none, Backend 0) or document why disabled | 2h | `just` health passes |

## Phase 3 - Fritz hardening (2 days, ~0)

| # | Task | Cost/time |
|---|---|---|
| 3.1 | Route `destructive:true` ops through deepfang pipeline + confirm queue UI (copy CC pattern: internal auto, external needs confirmed=true) | 1d |
| 3.2 | Path zoning enforcement + self-protect deny data/src/identity/memory | 4h |
| 3.3 | Agent templates `templates/` + `/add-<channel>` installer (copy NanoClaw, seed from SKILL.md importer) | 1d |

## Phase 4 - Robofang hardening (2 days, ~0 + cents)

| # | Task |
|---|---|
| 4.1 | Finish Bastio sign/verify + DefenseClaw enforce (docs say planned) - 1d |
| 4.2 | Container-per-skill default (container_runtime 512m already exists, flip default) - 4h |
| 4.3 | Per-task budgets token/cost/duration/iter + thrashing detect (copy OpenAkita) - 4h |
| 4.4 | QR scan-to-bind via discord-mcp:10756 + comms-mcp (biggest UX gap) - 1d, separate from cua_ops |

## Phase 5 - Aiwatcher + memory + marketplace (2 days, optional)

* Aiwatcher send gate + keep local-only default - 4h.
* Fritz graph memory layer on LanceDB (entity/timeline) - 1d.
* Proactive engine frequency feedback (extend morning_brief/fleet_pulse) - 4h.
* CN channels Feishu/WeCom/DingTalk only if needed - 1d, else explicit non-goal.

## Critical path (fastest to CUA parity)

```
0 (0.5d) -> 1A (1d) -> 1B (2d) -> 2.1 (4h, parallel with 1B) -> 3.1 (1d) -> 1C (1-2d)
= ~6-7 days to voice-driven gated CUA + fritz safe by default.
4.x + 5 can follow without blocking CUA.
```

## Cost table

| Item | Local cost | Cloud cost | Notes |
|---|---|---|---|
| VLM grounding qwen2.5-vl:7b Ollama | 0 (RTX 4090) | 0 | default, no API key |
| STT FunASR sidecar | 0 | 0 | :10914 existing |
| TTS Edge-TTS/Kokoro | 0 | 0 | fallback chain exists |
| DeepSeek adjudication | 0 idle | cents/1k actions | only for HIGH-risk, LOW auto-allow |
| Claude Agent SDK | 0 | $$ opt-in | NanoClaw parity only if wanted, not needed for cua_ops |
| Docker workers | 0 (disk/RAM) | 0 | 512m cap already in robofang |

## Risks + mitigations

* VLM mis-grounding clicks wrong button -> deterministic locator first, confidence threshold + confirm queue + HITL kill-switch + snapshot restore.
* Prompt injection via screen OCR -> deepfang sanitizer on OCR text + encoded-payload deny + container boundary.
* Scope creep (rebuild CV/VLM) -> forbidden. Glue + gates only. Any PR adding a new model trainer rejected.
* 5-file rule -> split 1A/1B/1C commits, .bak for batch edits.

## Verification gates (each phase must demo)

* 1A: ground-only log, no clicks.
* 1B: allow + deny + audit triple.
* 1C: voice -> act -> speak roundtrip.
* 2: two agents isolated, snapshot restore.
* 3: destructive op blocked without confirm.
* 4: unsigned spec rejected, over-budget task killed.

## What NOT to do

* No new VLM training, no new OCR engine, no new vault (reuse secrets-mcp), no Rust rewrite (ZeroClaw skip), no Zhipu dependency (AutoGLM complement, not clone), no AGPL import (OpenAkita patterns only).
