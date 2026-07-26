# Fleet Usage — DiffusionGemma on Goliath

## Fleet doctrine: catch them all

The acronym du jour changes quarterly. The fleet doctrine does not: **catch them all.**

Not Pokémon cosplay — a coverage requirement. Every serious inference paradigm gets a fleet integration path, a Goliath eval, an MCP routing slot, and an entry in `meta_mcp` SOTA scans. We do not pivot the fleet to whatever LinkedIn is screaming about this week. We add the new pocket monster and keep the rest in the party.

| Paradigm | Acronym | Fleet home (current / planned) | Status |
|----------|---------|-------------------------------|--------|
| Autoregressive LLM | AR LM | `local-llm-mcp` — Ollama, LM Studio | ✅ Production |
| Cloud frontier | — | `google-ai-mcp` — Gemini | ✅ Production |
| Diffusion LLM | **dLLM** | **`diffusion-llm-mcp`** — ports 10834/10835 | 🔄 Doc phase; this repo |
| Vision-Language-Action | **VLA** | `ros-mcp`, `gazebo-mcp`, `robotics-mcp` | 🔄 Partial |
| Large World Model | **LWM** | `worldlabs-mcp`, video-gen stack | 🔄 Partial |
| Multimodal diffusion | MMaDA-class | TBD — watch PRC releases | 👀 Scout |

**Why catch them all:**

1. **Capabilities are paradigm-specific.** dLLM wins batch/HLE-shaped tasks; AR wins streaming chat; VLA wins embodied action; LWM wins environment prediction. One paradigm cannot replace the party.
2. **Surprises come from the variant you ignored.** HLE on DiffusionGemma is the lesson — the hype object wasn't the AR flagship. Fleet must be wired for the next acronym before it tops HLE.
3. **PRC labs will ship all of the above in parallel.** DeepSeek/Qwen won't pick one religion. Neither should we.
4. **Provider plugin pattern scales.** `@register_llm("diffusion-gemma")` today, `@register_vla("...")` tomorrow — one file, one decorator, zero rewrites of existing MCP servers.

**`meta_mcp` responsibility:** SOTA scanner tracks each paradigm independently. New dLLM GGUF drops → alert. VLA checkpoint on HuggingFace → alert. LWM paper with open weights → alert. The fleet catches them; agents route them.

**This project's role in catch-them-all:** dLLM is the June 2026 capture ball. DiffusionGemma is the first specimen worth keeping. Windows scaffold + routing rules + HLE assessment = entry in the fleet Pokédex.

**Fleet repo:** [`diffusion-llm-mcp`](https://github.com/sandraschi/diffusion-llm-mcp) (ports 10834/10835) — canonical integration owner. This MCD folder = assessment archive.

**Next captures:** FastMCP sidecar in `diffusion-llm-mcp`, PRC dLLM fine-tunes, MMaDA if multimodal diffusion fits Goliath VRAM.

```
Fleet inference party (target state)
┌─────────────────────────────────────────────────────────┐
│                    MCP Agent Layer                       │
│              (task-based routing, not hype-based)        │
└──────────────────────────┬──────────────────────────────┘
                           │
     ┌─────────┬───────────┼───────────┬─────────┐
     ▼         ▼           ▼           ▼         ▼
  google-ai   AR LM       dLLM        VLA       LWM
  -mcp      local-llm   diffusion-  ros/      worldlabs
  (cloud)   -mcp        llm-mcp     robotics  -mcp
     │         │           │           │         │
   chat/     default     batch/     embodied   world
   quality   local       fast       action     model
```

Gotta catch 'em all — because the gap closes from whichever one you left in the tall grass.

---

| Component | Role | DiffusionGemma fit |
|-----------|------|-------------------|
| **Goliath** | RTX 4090 24 GB local inference workstation | Primary target — Q4_K_M |
| **`local-llm-mcp`** (port 10833) | Ollama / LM Studio bridge for MCP agents | **Blocked** until Ollama/LM Studio adopt llama.cpp diffusion |
| **`google-ai-mcp`** (port 11014) | Cloud Gemini for quality-critical tasks | Stays primary for chat, reasoning, multimodal |
| **`meta_mcp`** (port 10719) | Fleet orchestration, SOTA scanning | Track dLLM ecosystem maturity |
| **Ednaficator pipeline** | Synthetic data / content generation | **Strong fit** — throughput over prose polish |
| **Batch MCP tasks** | Non-interactive tool-driven generation | **Strong fit** — no streaming needed |

---

## Use Case Matrix

| Workload | Fit | Rationale |
|----------|-----|-----------|
| Synthetic training data generation | ✅ **Deploy** | Speed 5–10× vs 32B AR; quality bar tolerates noise |
| Batch MCP tool output (summaries, transforms, JSON) | ✅ **Deploy** | Block output acceptable; parse downstream |
| Ednaficator content pipelines | ✅ **Deploy** | Offline batch; human reviews output anyway |
| Code infill / constrained formatting | ✅ **Try** | Bidirectional canvas wins over AR here |
| Interactive agent chat (Cursor, OpenCode) | ⚠️ **Poor** | No streaming; 256-token chunks break UX |
| Primary `local-llm-mcp` default model | ❌ **Wait** | Tooling + quality not ready |
| High-concurrency MCP serving | ❌ **Wrong tool** | AR wins at batch 32+ |
| Multimodal image→text on Goliath | ⚠️ **VRAM tight** | Vision encoder adds ~550M params + activations |

---

## Recommended Fleet Architecture

```
                    ┌─────────────────────┐
                    │   MCP Agent Layer   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
    ┌─────────────────┐ ┌───────────┐ ┌─────────────────┐
    │  google-ai-mcp  │ │ local-llm │ │ diffusiongemma  │
    │  (quality/chat) │ │   -mcp    │ │  (batch/fast)   │
    │  Gemini API     │ │ Ollama AR │ │ llama-diffusion │
    └─────────────────┘ └───────────┘ └─────────────────┘
         streaming          default         secondary
         high quality       32B AR          26B dLLM
```

### Routing rules (proposed)

| Task signal | Route to |
|-------------|----------|
| `interactive=true` or `stream=true` | `google-ai-mcp` or AR via `local-llm-mcp` |
| `batch=true` or `throughput=priority` | DiffusionGemma on Goliath |
| `quality=critical` | `google-ai-mcp` |
| `constraint=sudoku\|infill\|format` | DiffusionGemma (test first) |
| `modality=image` input | Cloud for now — VRAM headroom uncertain on Goliath |

---

## Integration Path for `local-llm-mcp`

### Phase 0 — Manual (now)

Run `llama-diffusion-cli` as a standalone process on Goliath. MCP agents invoke via shell wrapper or a thin FastAPI sidecar. No Ollama dependency.

### Phase 1 — Sidecar (near-term)

Add optional `diffusion-backend` to `local-llm-mcp`:

```
POST /api/v1/diffusion/generate
  { "prompt": "...", "max_tokens": 512, "quant": "Q4_K_M" }
```

Wraps `llama-diffusion-cli` subprocess or direct GGUF binding.

### Phase 2 — Native (when upstream merges)

- llama.cpp PR #24423 merges → LM Studio picks it up
- Ollama integrates diffusion runner → `local-llm-mcp` gets it for free
- Retire sidecar

### Phase 3 — Smart routing

`local-llm-mcp` provider plugin:

```python
@register_llm("diffusion-gemma")
class DiffusionGemmaProvider(LLMProvider):
    ...
```

With automatic task-based routing per the rules above.

---

## VRAM Budget on Goliath

Typical desktop baseline (verified): ~3 GB VRAM in use (Cursor, Firefox, LM Studio UI, etc.)

| Quant | Model VRAM | Total estimate | Headroom |
|-------|-----------|----------------|----------|
| Q4_K_M | ~15–16 GB | ~18–19 GB | ~5 GB ✅ |
| Q5_K_M | ~17–18 GB | ~20–21 GB | ~3 GB ⚠️ |
| Q8_0 | ~26 GB | Does not fit | ❌ |

**Operational rule:** Close LM Studio model loads before running DiffusionGemma. Do not run both simultaneously.

---

## Ednaficator-Specific Notes

Ednaficator-style pipelines (synthetic data, distillation, bulk transformation) are the **highest-value fleet use**:

- Output is consumed by downstream filters, not read by humans token-by-token.
- 200–400 tok/s vs 40–60 tok/s changes overnight batch jobs to lunch-break jobs.
- Quality gap vs Gemma 4 AR is acceptable when output is ranked, deduplicated, or used as seed data.
- Block-boundary artifacts (sentence splits mid-thought at 256-token seams) need a post-process join — trivial for JSON/structured output, annoying for prose.

---

## What We Are NOT Doing Yet

- [ ] Production deploy on Goliath
- [ ] `local-llm-mcp` provider plugin
- [ ] Benchmark suite (fleet-specific tasks)
- [ ] Fine-tune via Unsloth for fleet domain
- [ ] Replace any AR model in daily workflow

---

*See [WINDOWS_SCAFFOLD.md](./WINDOWS_SCAFFOLD.md) for install steps.*
