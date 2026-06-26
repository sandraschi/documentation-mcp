# SOTA Local LLM Integration Guide for Cursor IDE (2026)

**Timestamp**: 2026-01-23  
**Status**: SOTA Standard  
**Target Hardware**: NVIDIA RTX 4090 (24GB VRAM)

## 🎯 Strategic Overview

**2026 truth table:**

1. **Chinese open-weight** (Qwen, DeepSeek, Kimi, …) — **dominates** local text/code/agentic throughput.
2. **Google Gemma 4** — **only major US corp** still shipping serious open weights (Apache 2.0, multimodal); Meta’s **Llama 4 cycle failed to hold the line**.
3. **OpenAI / Anthropic** — **closed** models; cloud **per-token APIs**. Use sparingly for frontier gaps, not as the fleet’s always-on brain.

The local stack is therefore a **two-pole open-weight** design: **Qwen/DeepSeek** for coding, **Gemma 4** for US-licensed multimodal (4090 + Pi 5). Closed APIs are a **paid overlay**, not the substrate.

**Economics:** Marginal cost of an agent hour is ~zero locally vs metered cloud tokens. As Chinese FOSS plus Gemma close **multimodal** gaps, standing subscriptions at **€500–€1,000+/month** per seat need a recurring business justification — see [open-source.md § Local vs cloud](../not-mcp-related/general-ai/models/open-source.md#-local-vs-cloud--why-accountants-and-valuations-should-lose-sleep).

**Long view:** Daily AI belongs on **edge NPUs** (phone, Pi, robot); cloud frontier is **dissertation tier** (novel, thesis, rare Opus-class jobs) — see [Datacenter boom vs edge + FOSS](../not-mcp-related/general-ai/models/open-source.md#datacenter-boom-vs-edge--foss-long-view).

**Fleet note (June 2026):** **Gemma 4 12B** (`gemma4:12b`) is the **multimodal** RTX 4090 daily driver (text + images, encoder-free). **E2B/E4B** are the **multimodal** pair for **Raspberry Pi 5 16 GB** (vision + audio on-device). **Gemma 4 26B** stays the text/agentic ceiling but is **too heavy** for a shared 4090; prefer 12B unless the GPU is dedicated.

| Tier | Hardware | Model | Multimodal |
| :--- | :--- | :--- | :---: |
| Desktop intel | RTX 4090 24 GB | `gemma4:12b` | Text + image |
| Edge brain | **Pi 5 16 GB** | `gemma4:e4b` or `gemma4:e2b` | Text + image + **audio** |
| Turbo / VRAM save | 4090 or Pi | `gemma4:e2b` | Same stack, smallest footprint |

---

## 🏗️ Technical Architecture: The "Fake OpenAI" Pattern
Cursor expects an OpenAI-compatible API. We provide this by running a local inference engine and tunneling it via **ngrok** to bypass localhost restrictions in Cursor's cloud-based indexing components.

```
[ Cursor Composer ] ──▶ [ ngrok Tunnel ] ──▶ [ Local Engine (11434) ] ──▶ [ GPU VRAM ]
```

---

## ⚙️ Inference Engine Comparison

| Feature | **Ollama** | **vLLM** | **LM Studio** |
| :--- | :--- | :--- | :--- |
| **Best For** | Daily Driver / Simplest | Raw Throughput / Speed | Visual Exploration / UI |
| **Quantization** | GGUF (Highly flexible) | AWQ / GPTQ / FP8 | GGUF |
| **Concurrency** | Good (Queued) | **Elite** (PagedAttention) | Single User |
| **Overhead** | Minimal | Moderate (Dedicated server) | High (Electron UI) |
| **SOTA Status** | Industry Standard | Enterprise Standard | Prosumer Tool |

---

## 🏆 Model Selection (The Chinese Coding Kings)

For a **4090 (24GB)**, avoid 70B models (too slow on CPU) and 7B models (too "dumb" for architecture). **32B is the Sweet Spot.**

### 1. Daily Driver: `Qwen2.5-Coder-32B`
*   **Intelligence**: Matches GPT-4o in coding benchmarks.
*   **Speed**: ~45 tokens/sec on 4090.
*   **VRAM**: ~18GB at Q4_K_M, leaving 6GB for context.

### 2. The Logic Specialist: `DeepSeek-R1-Distill-Qwen-32B`
*   **Intelligence**: Uses "Chain of Thought" (CoT) to solve complex bugs.
*   **Behavior**: It will "think" for 5-10 seconds before providing a perfect architectural solution.
*   **VRAM**: Similar to Qwen 32B.

### 3. Fleet daily driver (4090): `gemma4:12b` — Gemma 4 12B **multimodal** dense

*   **Release**: June 2026 — [Gemma 4 12B developer guide](https://developers.googleblog.com/gemma-4-12b-the-developer-guide/).
*   **License**: Apache 2.0 (true OSI open source; commercial fine-tune and redistribute).
*   **Multimodal (critical)**: Encoder-free — **text and images** in one model, one forward pass. Use for screenshots, dashboards, diagrams, UI captures, and doc photos without a separate vision API. Ollama accepts `images: [...]` on the message payload.
*   **VRAM**: ~8–14 GB quantized on Ollama depending on quant and context — leaves headroom on **24 GB** vs **26B**.
*   **Why fleet uses it**: Multimodal agentic work on desktop; closes quality gap under **26B** without cold-start pain when the 4090 is shared with the IDE.
*   **Pull**:

    ```powershell
    ollama pull gemma4:12b
    ```

*   **MCD tiers**: Prefer `gemma4:12b` for `ollama_model_intel` / `ollama_model_standard` when vision or quality matters; keep `gemma4:e2b` for turbo-only **text** paths.

### 4. Quality ceiling (dedicated GPU only): `gemma4:26b` — Gemma 4 26B MoE

*   **Intelligence**: Agentic workflows, function calling, multimodal (speech/vision on larger variants).
*   **Efficiency**: 26B total parameters, ~3.8B active per token (MoE).
*   **VRAM**: ~17 GB+ resident — **avoid as default** on a shared 4090; use when the machine is inference-focused.
*   **Speed**: High on a cold GPU; degrades sharply when VRAM is near full (see [STATUS.md](../STATUS.md)).

### 5. Edge / Pi 5 16 GB: `gemma4:e4b`, `gemma4:e2b` — **multimodal on the robot**

*   **Hardware**: **Raspberry Pi 5 with 16 GB RAM** (e.g. Yahboom Raspbot V2) — not theoretical; Google benchmarks and fleet tables target this class.
*   **Multimodal (critical)**: **Vision + audio + text** on-device (E2B/E4B). Local ASR, camera frames, OCR/UI understanding, tool calling — no cloud hop for perception loops.
*   **Memory (4-bit, fleet planning)**:

    | Tag | RAM (approx.) | Fits Pi 5 16 GB with ROS? |
    | :--- | :--- | :---: |
    | `gemma4:e2b` | &lt;1.5 GB | Yes — lightest multimodal brain |
    | `gemma4:e4b` | ~5 GB | Yes — better quality, still leaves headroom |

*   **Runtime on Pi**: Prefer **LiteRT-LM** (`pip install litert-lm`) for XNNPack CPU paths; **Ollama** works for simpler ops. See [GEMMA4_EDGE_ON_RASPBOT.md](../robotics/research/GEMMA4_EDGE_ON_RASPBOT.md).
*   **4090 fallback role**: `gemma4:e4b` also works as turbo tier when 12B is unloaded and desktop VRAM is tight (~9 GB on GPU).

---

## 🚨 GPU Optimization: The "Last Byte" Rule

### 1. The Saturation Penalty
**Never fill your VRAM to 100%.**
*   **Why?**: If your weights take 23.9GB of 24GB, the **KV Cache** (the "memory" of your current conversation) has no room to grow.
*   **Result**: Inference slows down by 90% as the system starts swapping data to system RAM (DDR5), which is 10x slower than VRAM.
*   **Standard**: Leave a **2GB buffer** for the KV Cache and Windows OS overhead.

### 2. Context Window Scaling
Context size is the #1 VRAM consumer after the model weights.
*   **4k Context**: ~500MB VRAM.
*   **32k Context**: ~4GB+ VRAM.
*   **Optimization**: Use `num_ctx 32768` for large codebase analysis, but drop to `8192` for simple chat to increase inference speed.

---

## 🧠 Intelligent Loading & Unloading

### Ollama Keep-Alive
Ollama unloads models after 5 minutes by default to free up the GPU for gaming/rendering. For a dedicated dev session, set this higher:
*   **Env Var**: `OLLAMA_KEEP_ALIVE=24h`
*   **Effect**: The model stays "hot" in VRAM all day for instant Cursor responses.

### Model Swapping
If you use both Qwen (for chat) and DeepSeek (for complex debugging):
*   **Ollama**: Swaps automatically. This takes ~2-4 seconds on a NVMe drive.
*   **vLLM**: Supports multi-lora but generally prefers one model at a time.

---

## 💡 Tips & Tricks for Cursor

1.  **System Prompting**: In Cursor settings, give your local model a "SOTA Personality":
    > "You are an expert software engineer running locally on a 4090. Be concise. Use modern ES2024+ or Python 3.12+ patterns. You have access to the full codebase."
2.  **Disable Web Search**: Local models cannot "browse" the live web unless you use a tool like `tavily`. Rely on your codebase indexing instead.
3.  **The "Live Video" Inspiration**: The Chinese breakthroughs in real-time video generation (e.g., Hailuo/MiniMax) use similar KV-cache optimizations we use for coding. High-speed inference is the 2026 competitive advantage.

---

## 🔍 Standard 4: Web-Native Dynamic Discovery
(Updated April 2026)

Static model lists in web applications are strictly deprecated. Fleet-compliant dashboards MUST implement **Proactive Elicitation**.

1. **Auto-Detection**: Scrape `localhost:11434` and `localhost:1234` recursively on dashboard mount.
2. **Persistence**: Store discovered model names in `localStorage` for cross-session continuity.
3. **Graceful Fallback**: Handle "Refused Connection" as a "Provider Offline" state rather than a system crash.

---

## 🏗️ Multi-IDE Configuration (2026 Standard)

While Cursor is the primary target, the same 4090 backend can power your entire IDE fleet.

### 1. Windsurf (Codeium) Setup
Windsurf currently handles local LLMs best via the **Continue** extension.
*   **Method**: Install `Continue` extension from the marketplace.
*   **Provider**: Select `Ollama`.
*   **URL**: `http://localhost:11434` (Windsurf runs mostly local, so ngrok is optional here unless using remote Cascades).
*   **Model**: `qwen2.5-coder:32b`.

### 2. Antigravity IDE (Gemini-based) Setup
Antigravity is Google's push into AI IDEs. Since it's built on the VS Code core:
*   **Override**: Look for **Settings** ──▶ **AI** ──▶ **OpenAI Compatibility**.
*   **Endpoint**: Use the ngrok URL (similar to Cursor) because Antigravity uses cloud-side reasoning.
*   **API Key**: `ollama`.

### 3. LM Studio (0.4.x) MCP
As of **LM Studio 0.4** (late January 2026), LM Studio supports MCP servers via a config file like other MCP clients. **Config**: Windows `%USERPROFILE%\.lmstudio\mcp.json` (e.g. `C:\Users\<user>\.lmstudio\mcp.json`); macOS/Linux `~/.lmstudio/mcp.json`. LM Studio uses Cursor-style `mcp.json` notation. See [integrations/lmstudio/README.md](../../integrations/lmstudio/README.md) and [lmstudio.ai/changelog](https://lmstudio.ai/changelog).

---

## 🛠️ Locking in SOTA: Custom Ollama Modelfile
To ensure your 4090 isn't restricted by default settings (like small 4k context windows), create a custom "Daily Driver" model.

1.  **Create a file** named `SOTA.Modelfile`:
    ```dockerfile
    FROM qwen2.5-coder:32b
    # Expand context to 32k (Uses ~4GB VRAM)
    PARAMETER num_ctx 32768
    # Ensure 100% of layers stay on your 4090
    PARAMETER num_gpu 99
    # Keep model hot in VRAM for instant responses
    PARAMETER keep_alive 24h
    # Professional System Prompt
    SYSTEM "You are a SOTA AI Engineer locally powered by an RTX 4090. Be precise, concise, and use modern 2026 patterns."
    ```
2.  **Build it**:
    ```powershell
    ollama create daily-driver -f SOTA.Modelfile
    ```
3.  **Use it**: In Cursor/Windsurf, select `daily-driver` as your model name.

---

## 🔒 Security Baseline (ngrok)
When exposing your model via ngrok, **protect your endpoint**.
```powershell
ngrok http 11434 --oauth=google --oauth-allow-email=your-email@gmail.com
```
*This ensures only YOU can hit your 4090 API from the Cursor cloud.*
