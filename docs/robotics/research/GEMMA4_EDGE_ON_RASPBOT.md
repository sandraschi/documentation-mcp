# Gemma 4 Edge Models on Raspbot V2 (Pi 5 16GB)

**Date:** 2026-06-04 (edge section); Gemma 4 launch 2026-04-02  
**Tags:** [yahboom-mcp, raspbot, gemma4, on-device-llm, litert-lm, edge-ai, multimodal, research, medium]  
**Source:** Google DeepMind launch + [Gemma 4 12B developer guide](https://developers.googleblog.com/gemma-4-12b-the-developer-guide/) (June 2026)

---

## Summary

Google DeepMind released **Gemma 4** under Apache 2.0. For the **Raspbot / Pi 5 16 GB** fleet slice, the relevant models are **E2B** and **E4B** — **multimodal** (vision + audio + text) and small enough to run **on the robot** beside ROS. For the **desktop** slice, **Gemma 4 12B** (`gemma4:12b`) is the multimodal 4090 driver (see [open-source.md](../../not-mcp-related/general-ai/models/open-source.md)).

**Pi 5 16 GB is not a compromise tier** — it is the intended home for E2B/E4B. The 12B model is the step-up when you need denser reasoning on a GPU workstation.

---

## Why This Matters for the Raspbot

The Raspbot V2 runs a Raspberry Pi 5 with **16GB RAM**. This comfortably fits:

| Model | Memory (4-bit) | Memory (16-bit) | Fits on Pi 5 16GB? |
|-------|---------------|-----------------|---------------------|
| E2B   | <1.5GB        | ~5GB            | ✅ Easily           |
| E4B   | ~5GB          | ~15GB           | ✅ Comfortably (4-bit), tight at 16-bit |

Google officially benchmarks E2B on Pi 5:
- **133 tokens/s prefill**, **7.6 tokens/s decode** (CPU, 4 threads via XNNPack)

At 7.6 tok/s decode that's usable for real-time robot control loops — not fast for conversation,
but adequate for command parsing and agentic decision steps.

---

## The "E" Naming Explained

E2B and E4B use **Per-Layer Embeddings (PLE)** — a secondary embedding signal injected into every
decoder layer. A 5.1B-parameter model behaves with the memory footprint of a 2B model (E2B);
an 8B-parameter model behaves like 4B (E4B). This is the MatFormer/Matryoshka architecture
first previewed in Gemma 3n (March 2026).

---

## Capabilities Relevant to Robotics

Both E2B and E4B support natively (no fine-tuning required):

- **Audio input** — ASR and speech-to-translated-text (unique to edge models, not in 26B/31B)
- **Vision** — variable resolution image input, OCR, UI/screen understanding, object detection
  with bounding boxes (useful for navigation and manipulation)
- **Function calling** — native structured tool use, JSON output
- **Multi-step planning** — agentic workflows, configurable thinking/reasoning mode
- **128K context window**
- **140+ languages** (relevant for Japanese-language commands)
- **Offline** — no internet required after download

For the Raspbot specifically: local ASR + vision + tool calling + agentic planning, all in <2GB RAM
on the same Pi 5 that runs the robot stack. This was not feasible before this model family.

---

## Runtime: LiteRT-LM

Google's own edge runtime. Install:

```bash
pip install litert-lm
litert-lm --model gemma4-e2b-it
```

Also supports tool calling (same mechanism as Agent Skills in Google AI Edge Gallery).
CLI available on Linux, macOS, and Raspberry Pi.

Alternative runtimes with day-one support: llama.cpp, Ollama, Hugging Face Transformers,
LM Studio (not useful on Pi), vLLM (overkill for Pi).

For the Pi, **LiteRT-LM** is the recommended path — it's what Google uses internally for
Agent Skills and is optimized for XNNPack CPU acceleration.

Ollama is simpler but less optimized:
```bash
ollama run gemma4:e2b   # ~3-5GB download
ollama run gemma4:e4b   # recommended for 16GB+ RAM
```

---

## Potential Use Cases on Raspbot

1. **Local voice command parsing** — E2B has native audio input; combine with Yahboom mic
   hardware for fully offline voice control without cloud ASR.

2. **Visual scene understanding** — feed camera frames, get structured descriptions or
   bounding-box detections for navigation decisions.

3. **Agentic skill execution** — Google's Agent Skills framework maps directly to MCP tool
   calling; Raspbot skills (move, scan, avoid, report) could be LiteRT-LM "skills".

4. **Offline fallback brain** — when Goliath is unreachable (travel, network down), the Pi
   runs local inference for basic autonomous behaviour.

5. **Japanese-language commands** — native 140+ language support, no translation layer needed.

---

## Integration Path with yahboom-mcp

The existing yahboom-mcp architecture already has:
- ROS2 bridge on Pi 5
- FastMCP 3.x gateway forwarding tool calls from Goliath
- Sensor data (ultrasonic, camera, IMU) plumbed through MCP tools

Adding Gemma 4 E2B/E4B creates a second inference path: instead of every tool call being
forwarded to Goliath, the Pi can run a local LiteRT-LM instance that handles low-latency,
offline-capable decisions. Goliath remains the primary for complex reasoning.

**Full design documented in:**
- `yahboom-mcp/docs/BOOMY_AUTONOMOUS_INTELLIGENCE.md` — WIGO mode, scenarios, demo
- `yahboom-mcp/docs/BOOMY_COGNITIVE_ARCHITECTURE.md` — two-brain model, skill definitions
- `yahboom-mcp/docs/ARCHITECTURE_DECISION_ROS2_VS_LLM.md` — architecture decision

Rough architecture:
```
[Mic/Camera] → [LiteRT-LM E2B on Pi 5] → [ROS2 actions] → [Motors/Servos]
                        ↑
              [MCP tool definitions as LiteRT "skills"]
                        ↕  (when available)
              [Goliath Gemini/Claude via FastMCP gateway]
```

---

## Status / Next Steps

- [ ] Install LiteRT-LM on Pi 5, test E2B inference speed
- [ ] Test audio input with Raspbot mic hardware
- [ ] Benchmark E4B at 4-bit vs E2B for quality/speed tradeoff on Pi 5
- [ ] Prototype one Agent Skill (e.g., "navigate to wall and stop") using LiteRT-LM tool calling
- [ ] Evaluate whether LiteRT-LM skills can be wrapped as yahboom-mcp tools (bidirectional)

---

## References

- Google DeepMind Gemma 4 launch: https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
- Google AI Edge blog post: https://developers.googleblog.com/bring-state-of-the-art-agentic-skills-to-the-edge-with-gemma-4/
- LiteRT-LM docs: https://ai.google.dev/edge/litert/models/gemma
- HuggingFace E4B LiteRT: https://huggingface.co/litert-community/gemma-4-E4B-it-litert-lm
- Unsloth run guide: https://unsloth.ai/docs/models/gemma-4
- NVIDIA Jetson blog: https://developer.nvidia.com/blog/bringing-ai-closer-to-the-edge-and-on-device-with-gemma-4/
