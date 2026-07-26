# Local LLM First — Fleet Doctrine

**Established**: 2026-07-05  
**Status**: Active  
**Target hardware**: NVIDIA RTX 4090 (24 GB VRAM)  
**Complementary to**: `LOCAL_LLM_STANDARDS.md` (operations manual — this file is doctrine)

---

## 1. The Rule

Local is the default. Cloud is an explicit opt-in, a line item on budget.

Every agent session starts with Ollama on `:11434`. Cloud APIs (DeepSeek V4, Claude, GPT) are used only when:

- The local model demonstrably fails at the task
- The task requires frontier reasoning (novel architecture, dissertations, adversarial edge cases)
- The user explicitly selects a cloud model with `/models`

The marginal cost of an agent hour on a 4090 is ~$0.06 (power). The marginal cost of an agent hour on DeepSeek V4 Pro is $6-20 (tokens). That is a **100-300x multiplier** for tasks that run unsupervised for hours.

---

## 2. Economics: Overnight Runner

This is local's killer advantage.

| Scenario | Local (4090, 350W) | DeepSeek V4 Pro |
|---|---|---|
| 8h unsupervised agent | ~$0.50 power | $50-150 tokens |
| Retry 5 times | $0.00 | 5x cost |
| "Restart from scratch" | $0.00 | Full cost again |
| 100 parallel retries (sweep) | $0.50 | $500-1500 |
| Monthly always-on agent (24/7) | ~$36 power | $4500-13000 |

**The threshold**: ~2 hours of continuous agentic work. Beyond that, local is strictly cheaper. For overnight runs (6-10h), the savings are 1-2 orders of magnitude.

The 4090 at 350W costs ~$0.06/hr at EU residential rates (~$0.17/kWh). GPU fans are the only audible cost. No token meter. No rate limit. No "context window exceeded" restart needed — just swap the model in Ollama and re-run.

---

## 3. Model Lineup

For a 24 GB RTX 4090. Only ONE model loaded at a time — Ollama auto-swaps in 2-4 seconds.

| Role | Model | VRAM | Tok/s | Notes |
|---|---|---|---|---|
| **Primary** | `qwen3.6:27b` (Q4_K_M) | ~16 GB | ~40 | Coding + thinking mode (built-in CoT). Best quality/speed balance for 24 GB. |
| **Fast / high-volume** | `gemma4:12b` | ~8 GB | ~80+ | Fleet standard daily driver. Multimodal (text + images). Apache 2.0. |
| **Reasoning** | Same as primary | — | — | `qwen3.6:27b` in thinking mode replaces `deepseek-r1:32b` — same CoT quality with 8 GB headroom. |
| **Future** | `deepseek-v4-*` quantized | ~18-20 GB* | TBD | When DS4 ships a Q4_K_M that fits 24 GB with KV cache headroom. Expected ~3-6 months. |

### What NOT to run

- **`deepseek-r1:32b`** — 20 GB weights + 4 GB KV cache = 24 GB, zero headroom. Windows DWM + Chrome will push it into DDR5 swap. Use `qwen3.6:27b` thinking mode instead.
- **Any 70B model** — Won't fit at usable quantization. CPU offload drops to <5 tok/s.
- **Two models simultaneously** — VRAM doesn't allow it. Ollama swaps are fast enough.

### VRAM budget

```
24 GB total
├── 16 GB  qwen3.6:27b weights (Q4_K_M)
├──  4 GB  32K context KV cache
├──  2 GB  Windows + browser + IDE overhead
└──  2 GB  Free headroom (the "Last Byte" rule)
```

Never exceed 22 GB. Drop `num_ctx` to 16384 if VRAM pressure appears.

---

## 4. opencode Configuration

### Provider setup

In `opencode.json` (project or global):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": {
        "baseURL": "http://localhost:11434/v1"
      },
      "models": {
        "qwen3.6:27b": {
          "name": "Qwen3.6 27B (coding + thinking)"
        },
        "gemma4:12b": {
          "name": "Gemma 4 12B (fast)"
        }
      }
    }
  },
  "model": "ollama/qwen3.6:27b"
}
```

Model IDs in `models` must match `ollama list` output exactly. Add more as you pull them.

### Anti-leak: lock to local only

```json
{
  "enabled_providers": ["ollama"],
  "experimental": {
    "policies": [{
      "effect": "deny",
      "action": "provider.use",
      "resource": "deepseek"
    }]
  }
}
```

`enabled_providers` is the whitelist — only Ollama loads. `policies` is the belt-and-suspenders: even if someone adds a cloud provider key, it's blocked.

### Switching to cloud

On the rare occasion you need frontier reasoning:

```
/models
```
Select `deepseek/deepseek-v4-pro` from the list. It coexists with the Ollama provider.

### Known caveat: tool calling

Local models need enough context in Ollama to hold tool schemas. Set `num_ctx` high enough (~32K) in Ollama:

```
ollama run qwen3.6:27b
/?
PARAMETER num_ctx 32768
```

Or bake it into a Modelfile (see `LOCAL_LLM_STANDARDS.md`). Without enough context, tool call schemas get truncated and the model returns text instead of function calls.

---

## 5. Fleet Integration Requirements

Every fleet webapp chat page MUST:

1. **Detect** Ollama on `:11434` on mount
2. **Default** the provider dropdown to Ollama when detected
3. **Fall back** to cloud ONLY when Ollama is offline AND user has a cloud API key configured
4. **Show** provider status (green/red dot) in chat controls
5. **Never hardcode** a cloud provider URL — always use the provider settings

See `LOCAL_LLM_STANDARDS.md` for technical implementation (auto-detection, localStorage persistence).

---

## 6. Silent Paid-API Audit Checklist

Run this checklist on every fleet repo with LLM features:

- Chat page: does it hardcode a cloud provider URL or fall back to one without explicit user config?
- RAG embeddings: using local LanceDB + FastEmbed, or silently calling OpenAI embeddings?
- MCP sampling (`ctx.sample()`): routing through a paid endpoint, or through Ollama?
- Skills: do any `SKILL.md` files instruct the agent to use cloud-only tools?
- `llms-full.txt`: does any example code show hardcoded cloud API keys or URLs?
- Settings page: is the default provider "Ollama" or "OpenAI"?

Fix any violations. Power users can enable cloud; it must never be the silent default.

---

## 7. When Cloud Wins

```
Is local quality sufficient for the task?
  ├─ YES → Ollama on 4090. Zero cost.
  └─ NO  → Is the task:
      ├─ Multi-step fleet audit (5+ MCP servers)?
      │
      ├─ Novel architecture / dissertation-tier writing?
      │
      ├─ Adversarial edge case (security, prompt injection)?
      │
      └─ Task where prompt alone is 20K+ tokens?
          └─ YES to any → Switch to DeepSeek V4 Pro.
             NO to all  → Try local first. Cloud is a retry, not a default.
```

The prompt size filter is important: CLAUDE.md + 13 standards files + repo context can hit 15-20K tokens before the first user message. Local 27B models degrade significantly beyond 32K total context. If the session is context-heavy and quality-critical, cloud is justified.

---

## 8. Future: DeepSeek V4 Quantized

Once DeepSeek V4 ships a Q4_K_M quantization that fits in 24 GB with KV cache headroom (~18-20 GB weights), this doctrine's primary model becomes `deepseek-v4:q4_k_m` instead of `qwen3.6:27b`. Expected timeline: ~3-6 months (late 2026 / early 2027).

At that point the quality gap between local and cloud narrows to near-zero for most coding tasks. The overtight model fit concern (currently 20 GB for R1-32B, zero headroom) should be resolved by newer quantization techniques and model architecture improvements.

Until then, `qwen3.6:27b` is the pragmatic choice — it fits, it has thinking mode, and it leaves 8 GB for the IDE.

---

## Cross-References

- `LOCAL_LLM_STANDARDS.md` — Technical operations: inference engines, model quantization, Modelfiles, ngrok tunnels, edge (Pi 5) deployment
- `LLM_AND_INSTALL_TIERS.md` — User tiers A-D: what gets bundled in Tauri installers vs documented
- `not-mcp-related/general-ai/models/open-source.md` — Cost comparison table (archived, superseded by §2 above)
