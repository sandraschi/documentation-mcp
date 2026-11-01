---
title: "Tooling Cost Model - Fleet Doctrine"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Tooling Cost Model - Fleet Doctrine

**Established**: 2026-08-16
**Status**: Active
**Complements**: `LOCAL_LLM_FIRST_DOCTRINE.md` (runtime economics; this file is the tooling layer on top)
**Target hardware**: NVIDIA RTX 4090 (24 GB VRAM), Goliath

---

## 1. The Three Pricing Models

Every AI build tool in the fleet falls into exactly one of three billing models.
Understanding which model a tool uses is the whole game: it decides what runs
where, when, and at what marginal cost.

| Model | Pricing | Example tools | Character |
| --- | --- | --- | --- |
| **Sunk-cost local** | Hardware already paid; marginal cost = power | opencode, Cline, Zed + Ollama/llama.cpp/LM Studio on the 4090 | Free beer: slow pours, infinite refills |
| **Capped subscription** | Fixed monthly fee, throughput-limited (rate windows) | Claude Desktop Pro ($20/mo) | Three minutes of premium model per window, then a hard stop |
| **Usage-based metering** | Per-token / per-session through a gateway | Cursor, Antigravity, Windsurf | Nickel-and-dimed: the meter runs invisibly, cost compounds per session |

The fleet rule: **local for the bulk, subscription for the spike, usage-based
only when a tool's own features justify its meter.**

---

## 2. The Tool Matrix (2026-08)

Six build tools, three of which can run local models directly. The split is
structural, not arbitrary: the three open-source/self-hostable editors expose a
raw model endpoint you can point anywhere; the three commercial ones gate
models behind their own backend.

| Tool | Local model (4090) | Cloud-gated | Local capability |
| --- | --- | --- | --- |
| **opencode** | Yes | No | Ollama provider, fleet MCP stack, permission-gated agent loop. Primary build tool. |
| **Cline** | Yes | No | BYOK - Ollama/LM Studio are first-class providers in settings. MCP-friendly agent. |
| **Zed** | Yes | No | Native Ollama provider in `settings.json`. Fast editor + MCP (zed-mcp). |
| **Cursor** | No | Yes | Model list served from cloud gateway. Supports **Self-Hosted Machines/Pools** (local tool/shell execution; see `SELF_HOSTED_WORKER_STANDARD.md`). |
| **Antigravity** | No | Yes | Gemini-only by design; skills via `.agents/skills` + agy-mcp bridge. |
| **Windsurf** | No | Yes | Cloud gateway models only. First agentic IDE (Cascade), now the legacy guest. |

"Cloud-gated" is a capability statement, not a quality judgment: Cursor's IDE
integration is genuinely good. But every session through a gated gateway is a
session on a meter. With self-hosted machines, local execution is free, but reasoning
tokens are still metered—governed by `standards/SELF_HOSTED_WORKER_STANDARD.md`.

---

## 3. The Hybrid Ladder (how to actually use this)

The winning pattern is a three-rung ladder, not a single tool:

```
Rung 1: LOCAL (bulk)          opencode / Cline / Zed + muse-glimmer-65k on 4090
Rung 2: SUBSCRIPTION (spike)  Claude Desktop Pro - the one hard problem of the day
Rung 3: USAGE-BASED (feature) Cursor / Antigravity - only when their IDE features
                              beat what rungs 1-2 can do locally
```

| Task class | Rung | Why |
| --- | --- | --- |
| Mechanical edits, lint-fix, renames, long agent loops | 1 | Volume is free; speed is not critical |
| Overnight / background agent runs (6-10h) | 1 | 100-300x cheaper than any metered alternative (see `LOCAL_LLM_FIRST_DOCTRINE.md` sec 2) |
| Novel architecture, dissertation-tier writing, adversarial edge cases | 2 | Frontier reasoning pays for itself in minutes; the rate window is the constraint |
| Screenshot analysis, UI state review | 1 | muse-glimmer vision (`attachment: true`) covers still images |
| Anything needing Cursor's specific IDE integration | 3 | Pay only while the feature is in use |

Escalation is a decision, not a default: start local, escalate on demonstrable
failure. Never start on the meter.

---

## 4. The 4090 as a Fixed-Cost Asset

The strategic value of the 4090 is that it **converts a variable cost into a
fixed one**. Every task kept local is a task that never appears on a bill.

| | Local (4090, ~350W) | Cloud (per-token) |
| --- | --- | --- |
| 8h unsupervised agent | ~$0.50 power | $50-150 |
| Retry 5 times | $0.00 | 5x cost |
| Monthly always-on agent (24/7) | ~$36 power | $4500-13000 |

The ~2 hour threshold: beyond that, local is strictly cheaper for continuous
agentic work. The 4090 is the only fleet asset that gets *more* valuable the
longer it runs.

---

## 5. Current Local Lineup (2026-08-16)

For a 24 GB RTX 4090. One model loaded at a time (Ollama swaps in seconds).
The crown is changing hands at weekly cadence (tit-for-tat): Muse Glimmer-30B
(Meta, USA, ~08-10) then Qwen3.8-27B (Alibaba, PRC, 08-14). Champion status is
provisional until the A/B (planned 2026-08-17); treat the table as current
best-known, not gospel.

| Role | Model | Size | Capabilities | Notes |
| --- | --- | --- | --- | --- |
| **Primary** | `qwen3.8:27b` | ~18 GB | thinking (reasoning_effort) + tools + vision + **video** | 262K native context (1M ext). Vendor-reported SWE-bench Pro 61.7 beats Muse's 51.2. Apache 2.0. A/B pending. |
| **Contender** | `muse-glimmer-65k` (27.85B Q4_K_M) | 18 GB | thinking + tools + vision | 65k = ~3.4 GB KV, fits 4090. MCP Atlas leader (75.5) - best tool orchestration. |
| **Fast fallback** | `gemma4:12b` | ~8 GB | tools + vision | Fleet daily driver for high-volume work |

Why not `muse-glimmer-131k`: 131k context needs ~6.8 GB KV cache; 18 GB weights
+ 6.8 GB KV exceeds 24 GB VRAM, spilling to system RAM and crawling. Why not
`muse-glimmer-kquant`: it ships without the vision encoder AND without
thinking - it fails both the multimodality and the agentic requirements.

VRAM budget at 65k:

```
24 GB total
+-- 18 GB  primary weights (Q4)
+--  3.4 GB 65k KV cache
+--  2 GB   Windows + browser + IDE overhead
+-- ~0.5 GB free headroom
```

Never exceed 22 GB. Drop to 32k context if VRAM pressure appears.

---

## 6. Configuration Reference

### opencode (`~/.config/opencode/opencode.json`)

```json
"muse-glimmer-65k": {
  "name": "Muse Glimmer 27B 65K",
  "tools": true,
  "attachment": true,
  "options": { "num_ctx": 65536, "think": true },
  "limit": { "context": 65536, "output": 8192 }
}
```

Verified behaviors (2026-08-16):
- `think: true` is the Ollama-native switch; `reasoning_effort` is silently ignored by Ollama. Thinking output lands in `message.reasoning` on the `/v1` endpoint.
- `attachment: true` enables image input (screenshots) - still images only, no video.
- Tool calling verified working against `muse-glimmer-65k`.
- The base `muse-glimmer` tag defaults to ~4K context in Ollama; always set `num_ctx` explicitly.

### Cline

Settings > API provider: Ollama (or OpenAI-compatible pointing at
`http://127.0.0.1:11434/v1`). Same model, same 4090.

### Zed

`settings.json` assistant provider: Ollama. Model: `muse-glimmer-65k`.

### GPU arbitration (InvokeAI vs dev models)

InvokeAI web (`D:\InvokeAI`, port 9090) is a plaything that holds up to 8 GB
VRAM (`max_cache_vram_gb: 8` in `invokeai.yaml`) and will fight Ollama dev
models for the 4090. Arbitrate with the fleet script:

```powershell
just gpu-free        # kick InvokeAI web + unload Ollama models (frees ~17 GB)
just invokeai-up     # bring InvokeAI web back after dev work
just gpu-status      # who holds the 4090 right now
```

Backing script: `mcp-central-docs/scripts/just/gpu-arbitration.ps1`
(`-Kick` / `-Restore` / `-Status`, `-DryRun` supported). InvokeAI has no
graceful shutdown API (405s on all shutdown routes) - the script kills the
process tree by port 9090 owner, which is the sanctioned method (not NSSM).

### LM Studio (chat companion + alternate local backend, not a build tool)

LM Studio has its own MCP client (`~/.lmstudio/mcp.json`) - useful for
research chat with fleet tools, but it applies **no permission gating**. It is
an MCP-augmented chatbot, not a coding agent: no diff review, no verification
loop, no permission system. Do not use it for build work; do not give it
unguarded `winops` / `filesystem` access.

As of 0.4.0 (2026-01-28, verified 2026-10-26) it is also a viable local
inference backend alongside Ollama: `llmster` headless daemon, native REST
`/api/v1/chat` (stateful, `stats`, MCP via `integrations`), OpenAI-compat
(`/v1/chat/completions`, `/v1/responses`, `/v1/embeddings`) and
Anthropic-compat (`/v1/messages`) for Cline/opencode/Zed/Codex/Claude Code,
parallel requests via continuous batching (default 4 slots, Unified KV).
Point any OpenAI/Anthropic client at `http://localhost:1234` (+ permission-key
auth). Single-writer VRAM still applies: never co-reside with Ollama/vLLM.
Details: `integrations/lmstudio/` (README, TECHNICAL, WORKFLOWS).

---

## 7. Decision Rules

```
Is the task mechanical or high-volume?
  +- YES -> Rung 1: local model on the 4090. Zero marginal cost.
  |        Can a local 27B model do it well enough? (usually yes)
  |          +- NO -> escalate
  |
  +- NO  -> Is this the one hard problem of the day?
  |          +- YES -> Rung 2: Claude Desktop Pro subscription. Rate window is the budget.
  |          +- NO  -> Rung 3 only if a gated tool's IDE features justify the meter.
  |
  Does the task run unattended for 2+ hours?
    +- YES -> local, always. The threshold where local is strictly cheaper.
```

Guardrails:
- Local is the default. Cloud is an explicit opt-in, a line item on budget.
- Never leave a gated gateway as a silent default (see `LOCAL_LLM_FIRST_DOCTRINE.md` sec 6).
- Usage-based tools are for their features, not for the model. If you are on
  Cursor for the model, move the model local and keep the IDE.
- Claude Desktop Pro is a spike tool: one hard problem per window, then back to local.

---

## Cross-References

- `LOCAL_LLM_FIRST_DOCTRINE.md` - Runtime economics, model lineup history, silent paid-API audit checklist
- `LOCAL_LLM_STANDARDS.md` - Technical operations: inference engines, quantization, Modelfiles
- `LLM_AND_INSTALL_TIERS.md` - User tiers A-D: what gets bundled in Tauri installers
- `operations/WEBAPP_PORTS.md` - Port registry (Ollama 11434, LM Studio 1234, llama.cpp 11435)
- Funnel landing: `https://goliath.<tailnet>.ts.net/tooling-cost/` (public mirror)
