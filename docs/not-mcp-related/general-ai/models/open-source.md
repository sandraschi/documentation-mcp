# Open Source / Open-Weight Models

**Status:** Thriving parallel ecosystem (updated 2026-06)  
**Fleet hardware reference:** NVIDIA RTX 4090 (24 GB) — see [LOCAL_LLM_STANDARDS.md](../../../standards/LOCAL_LLM_STANDARDS.md)

---

## 🔓 The 2026 landscape (fleet view)

Three buckets — not interchangeable:

| Bucket | Who | What you get | Fleet stance |
| :--- | :--- | :--- | :--- |
| **US open-weight** | **Google (Gemma)** | Downloadable weights, Apache 2.0, local + multimodal | **Default for US-sovereign + vision/audio** on 4090 and Pi 5 |
| **Chinese open-weight** | DeepSeek, Alibaba (Qwen), Moonshot (Kimi), … | Best-in-class **coding/math/agentic** weights; run locally via Ollama | **Default for raw codegen** on 4090 when text-only is enough |
| **US closed APIs** | OpenAI, Anthropic, (Google Gemini cloud) | Frontier quality, **per-token rent**, data leaves the machine | **Surgical use** (ULTRAPLAN, hard reasoning gaps) — not the default substrate |

**Reality check:** The “absolute ceiling” for capability still lives in **closed cloud APIs**. The **floor** that actually runs on your hardware is almost entirely **open-weight** — and in 2026 that floor is **mostly Chinese labs** for text/code, with **Google as the only major US corporation still shipping credible open weights** at scale.

**Meta / Llama:** Llama 3.x mattered; **Llama 4 landed as a fleet disappointment** (hype, weak adoption, unclear edge over Qwen/DeepSeek). Meta has effectively **ceded open-weight leadership** — community momentum and Ollama pulls moved on. Do not plan new fleet work around Llama 4 as the US alternative; plan around **Gemma 4** (US, multimodal) + **Qwen/DeepSeek** (Chinese, coding).

**OpenAI / Anthropic:** Strong products, **closed weights**, API economics built on ongoing token spend. Fine for IDE assist and one-shot frontier tasks; **poor fit as the primary agent substrate** when the fleet goal is sovereignty, zero marginal cost, and MCP loops that never stop. Use them where cloud is worth the invoice; run Gemma + Qwen locally everywhere else.

---

## 💰 Local vs cloud — why accountants (and valuations) should lose sleep

The fleet does not treat this as ideology; it is **unit economics**.

| Line item | Local open-weight (4090 + Ollama) | Closed cloud (Anthropic-class API) |
| :--- | :--- | :--- |
| **Upfront** | GPU already sunk (e.g. RTX 4090) | €0 hardware |
| **Recurring** | Power, occasional model pull | **€500–€1,000+/month** IDE/API bundles per power user |
| **Marginal cost per agent hour** | ~**zero** after weights load | Every MCP loop, every retry, every summarisation → **tokens** |
| **Multimodal** | **Gemma 4** 12B + E4B/E2B (FOSS, improving fast) | Bundled in cloud price — was the main moat |
| **Data** | Stays on machine | Crosses vendor boundary |
| **Switching cost** | Download different weights | Re-negotiate subscription / re-wire agents |

**The valuation tension:** Markets price **Anthropic, OpenAI, and peers** as if **recurring API rent** is permanent and expanding. That story assumes the **capability gap** to local inference stays wide forever. Historically the gap was **text reasoning** (Chinese FOSS already competitive) and **multimodal** (vision/audio still justified cloud). **Gemma 4 12B on a 4090** plus **Chinese open-weight** catching up on agents/code collapses the second pillar on the desktop; **E2B/E4B on Pi 5 16 GB** does the same at the edge.

**Feet-of-clay scenario (fleet wording):** If a developer stack of **~€60/month** for IDE subscriptions + **local inference** covers codegen, RAG, and multimodal screenshots, the incremental value of **~€1,000/month** for a single-vendor closed API becomes a **CFO question**, not a technology question. Trillion-dollar narratives built on “everyone must rent intelligence forever” look **fragile** when FOSS multimodal is “good enough” on hardware you already own.

**What closed cloud still buys (honest):**

- Frontier spikes (long CoT, rare model refresh, legal indemnity in enterprise contracts).
- Zero ops for individuals who will not run Ollama.
- Short-horizon lead before the next open-weight drop.

**Fleet policy:** Default **local** (Qwen/DeepSeek text, Gemma multimodal). Cloud APIs are **line items on a budget**, not the architecture. Revisit monthly: if local quality crossed your bar last month, **downgrade cloud seats** before the accountants ask why you are renting what you already run.

### Datacenter boom vs edge + FOSS (long view)

The **2023–2026 hyperscaler capex wave** (gigawatt clusters, “AI needs a datacenter for everything”) may read later as **supreme folly** if inference follows the same curve as mobile photography: **most work moves to the edge**, weights are **FOSS**, and the cloud is reserved for jobs nobody runs daily.

| Layer | Where it runs | What it does |
| :--- | :--- | :--- |
| **Daily AI (~99% of human use)** | **Phone NPU**, laptop, Pi, robot SoC | Dictation, search, photos, chat, home, commute, on-device vision/audio |
| **Power-user / fleet** | Desktop GPU (4090), homelab | Agents, MCP loops, codegen, RAG, robotics (Gemma + Qwen locally) |
| **Rare “dissertation tier”** | Cloud frontier (e.g. Claude Opus *n*, GPT *n*) | Novels, theses, litigation-grade drafts, one-off proofs — **not** the default substrate |

**LLM / LVM / LWM on edge:** Text models (**LLM**), on-device vision (**LVM** — scene, UI, camera), and lightweight world/action models (**LWM** — spatial, robotics, AR) are already shipping in **billions of NPUs**. Open-weight drops (Gemma E2B/E4B, Apple/Google on-device stacks, Chinese distillates) make **“call Virginia”** the exception, not the rule.

**iPhone thesis (fleet shorthand):** For most people, **the phone will do ~99% of the AI they actually notice** — faster, private, no per-token bill. Cloud frontier is for **the 1%** that is deliberately slow, expensive, and rare: *write my doctorate*, *ghost my novel*, *bet-the-company legal memo*. Use **whatever Opus/GPT number is current then** for that tier; do not architect the fleet or the household budget around it.

**Implication for builders:** Design agents and MCP for **edge-first + local FOSS**; treat datacenter APIs as **overflow**, not foundation. Capex-heavy “every prompt hits a GPU farm” product plans age badly if users expect **on-device** latency and zero marginal cost.

---

## Major Players (open-weight only)

### 1. Google (Gemma) — the US open-weight line

After Meta stepped back, **Google is the only US mega-corp still treating open-weight as a first-class product** (Gemma 4, Apache 2.0, Hugging Face/Kaggle/Ollama day-one). That matters for policy, multimodal edge (Pi + desktop), and “not everything in the stack is Beijing weights.” **Gemma 4** is the current generation; the full family ships under a true **[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)** license (OSI-approved), which matters for commercial reuse, fine-tuning, and fleet redistribution without Llama-style community-license friction.

| Model | Role | Ollama (typical) | Multimodal | Notes |
| :--- | :--- | :--- | :---: | :--- |
| **Gemma 4 12B** ⭐ | **4090 sweet spot** | `gemma4:12b` | **Yes** | Encoder-free: **text + images** in one forward pass (no separate CLIP/vision model). Closes quality gap under **26B** without VRAM tax. |
| Gemma 4 26B (MoE) | Max quality (heavy) | `gemma4:26b` | Partial | ~17 GB+ resident; dedicated GPU only on shared 4090. |
| **Gemma 4 E4B** | **Pi 5 16 GB** | `gemma4:e4b` | **Yes** | Vision + **audio** + tools on-device; ~5 GB at 4-bit fits **Raspberry Pi 5 16 GB** with ROS stack headroom. |
| **Gemma 4 E2B** | **Pi 5 light** | `gemma4:e2b` | **Yes** | Same multimodal stack, &lt;1.5 GB at 4-bit — validated for real-time edge loops (see edge doc below). |
| Gemma 4 31B dense | Leaderboard tier | Hugging Face / vLLM | Yes | Beyond comfortable single-GPU 4090 daily driver. |

#### Multimodal is the point (not an afterthought)

Unlike many **text-only** open-weight coding models (Qwen Coder, DeepSeek distill, etc.), **Gemma 4 is natively multimodal** across the sizes that matter to this fleet:

- **12B (desktop):** Encoder-free dense model — pass **images** directly to Ollama/API (screenshots, diagrams, Grafana panels, PDF crops) in the **same** session as code reasoning. No second vision API, no CLIP pre-stage.
- **E2B / E4B (edge):** Google validates **vision + audio input** on Pi-class hardware — ASR, OCR/UI understanding, bounding boxes for robotics, function calling, 128K context. This is what makes **yahboom-mcp** / on-robot cognition feasible without cloud round-trips.

Fleet rule: when the task involves **pixels or microphones**, default to Gemma 4 (12B on 4090, E4B/E2B on **Pi 5 16 GB**), not a text-only coder model.

#### Raspberry Pi 5 (16 GB RAM) — smaller Gemma 4 models

The **E2B** and **E4B** variants are explicitly aimed at edge devices. On a **Raspberry Pi 5 with 16 GB**:

| Variant | Typical 4-bit RAM | Multimodal | Fleet use |
| :--- | :--- | :---: | :--- |
| `gemma4:e2b` | &lt;1.5 GB | Vision + audio + text | Turbo parsing, always-on robot brain beside ROS |
| `gemma4:e4b` | ~5 GB | Vision + audio + text | Higher-quality on-Pi planning when 12B is on the desktop |

Run with **LiteRT-LM** (Google’s Pi-optimized path) or **Ollama** on the Pi. Full robotics breakdown: [GEMMA4_EDGE_ON_RASPBOT.md](../../../robotics/research/GEMMA4_EDGE_ON_RASPBOT.md).

**Why Gemma 4 12B matters (June 2026):** [Gemma 4 12B developer guide](https://developers.googleblog.com/gemma-4-12b-the-developer-guide/) — **multimodal** dense weights for laptop/4090, 256K context class, Ollama / Hugging Face / LiteRT-LM. Fleet observation: on RTX 4090 it **runs great** for agentic + vision workloads; **26B remains too big** for a shared dev desktop.

```powershell
# Desktop (4090) — multimodal 12B
ollama pull gemma4:12b
ollama run gemma4:12b

# Pi 5 16 GB — multimodal edge (pick one)
ollama pull gemma4:e4b
# or: litert-lm with gemma4-e2b-it on the robot (see edge doc)
```

**Policy contrast:** Gemma 4 ships **OSI Apache 2.0**, not a community license with revenue caps. For EU/public-sector and on-prem MCP fleets, that is the workable **US-origin weights** story in 2026.

---

### 2. Chinese labs — dominating open-weight **text & code**

This is where **most of the field actually moved** while US labs monetize APIs:

| Lab | Flagship (fleet) | Strength | Typical local tags |
| :--- | :--- | :--- | :--- |
| **Alibaba** | Qwen 2.5 / 3.x Coder | Agentic coding, throughput on 4090 | `qwen2.5-coder:32b`, `qwen3.5:*` |
| **DeepSeek** | R1 / V3 distillates | Math, logic, CoT debugging | `deepseek-r1:32b`, DeepSeek-V3 family |
| **Moonshot** | Kimi K2 Thinking | Large MoE agentic reasoning | HF / vLLM pulls |

**Fleet split:** Chinese open-weight for **text-only** heavy lifting (refactors, codegen, RAG synthesis); **Gemma 4** when the task is **multimodal** or you need a **US-licensed** weight file.

---

### 3. Meta (Llama) — legacy, not 2026 default

- **Llama 3.x:** Still in registries; fine for experiments.
- **Llama 4:** **Fleet assessment: dud cycle** — disappointing quality/adoption vs Qwen/DeepSeek/Gemma 4; Meta no longer drives the open-weight narrative.
- **License:** Llama Community License is **not** Apache/MIT — another reason the fleet standardized on **Gemma** for US open-weight.

*Historical note only; do not greenfield on Llama 4.*

---

### 4. US closed cloud (not open-weight — listed for contrast)

| Vendor | Model lines | Model |
| :--- | :--- | :--- |
| **OpenAI** | GPT-4.x / o-series | Closed weights, API-only |
| **Anthropic** | Claude 4.x | Closed weights, API-only |
| **Google** | Gemini (cloud) | Closed frontier; separate from **Gemma weights** |

Use when the task justifies **rented intelligence** (long-horizon planning, rare frontier capability). Do **not** confuse Gemini **API** with Gemma **weights** — the fleet’s local US story is **Gemma files on disk**, not Google Cloud tokens.

Economics: see [Local vs cloud — why accountants should lose sleep](#-local-vs-cloud--why-accountants-and-valuations-should-lose-sleep) above.

---

## 🛠️ Tools & Libraries

### Gradio (Hugging Face)
- **Status:** The standard UI for ML demos and internal tools.
- **2025 Updates:** Faster latency, native streaming support, "agent" UI components.

### Local Inference Stack

Running open-weight models locally requires inference infrastructure. Three
tools dominate, serving different needs:

#### Ollama
- **What it is:** Local LLM runner with CLI and GUI
- **Key feature:** Dead simple. `ollama run llama3` just works
- **Target user:** Developers, hobbyists, anyone wanting local LLMs
- **How it works:** Wraps llama.cpp, handles model downloads from its registry
- **2025 Update:** Now includes a native GUI alongside the CLI
- **Strengths:** 
  - One-command setup (CLI) or click-to-run (GUI)
  - Automatic quantization selection based on your hardware
  - Built-in model library (Llama, Mistral, Gemma, etc.)
  - REST API for integration
  - Cross-platform (macOS, Windows, Linux)
- **Limitations:** Single-user, not optimized for high-throughput serving

#### LM Studio
- **What it is:** Desktop GUI application for running local LLMs
- **Target user:** Non-technical users, people who want a ChatGPT-like interface locally
- **Key feature:** Visual model browser, download manager, chat interface
- **How it works:** Electron app wrapping llama.cpp with nice UI
- **Strengths:**
  - No command line needed
  - Drag-and-drop GGUF model loading
  - Built-in prompt templates per model
  - Local server mode for API access
- **Limitations:** Heavier than Ollama, less scriptable

#### vLLM
- **What it is:** High-performance inference engine for production serving
- **Target user:** Companies deploying LLMs at scale
- **Key feature:** PagedAttention for efficient memory management
- **How it works:** Optimized CUDA kernels, continuous batching, tensor parallelism
- **Strengths:**
  - 2-4x higher throughput than naive implementations
  - Multi-GPU support
  - OpenAI-compatible API server
  - Production-grade reliability
- **Limitations:** Requires more setup, needs decent GPU(s)

**The Stack in Practice:**
- **Hobbyist/Dev:** Ollama or LM Studio on MacBook/gaming PC
- **Startup:** vLLM on cloud GPUs (Lambda, RunPod, etc.)
- **Enterprise:** vLLM cluster behind load balancer, or managed service (Anyscale, Together AI)

---

## 📉 The "Open Washing" Debate
- **True Open Source:** OSI-approved licenses (Apache 2.0, MIT).
- **Open Weights:** "Look but don't touch" (Llama Community License).
- **Trend:** More "Open Weights" releases, fewer "Open Training Data" releases.

