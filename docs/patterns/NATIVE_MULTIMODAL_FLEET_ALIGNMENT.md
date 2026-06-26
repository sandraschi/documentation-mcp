# Pattern: Native Multimodal Fleet Alignment

**Status**: PROPOSED (April 2026)  
**Reference**: [Gemma 4 Technical Report](file:///C:/Users/sandr/.gemini/antigravity/brain/2d97e8d1-4089-4844-afbf-2fb404ac8568/gemma_4_analysis_report.md)

## 🎯 Context
Prior to 2026, agentic multimodal workflows relied on **Orchestral Patching**:
1. `User Audio` ──▶ `Whisper (STT)` ──▶ `LLM (Text)` ──▶ `Tool Call`
2. `Screenshot` ──▶ `Resizer` ──▶ `GPT-4o (Vision)` ──▶ `Analysis`

This pattern introduces cumulative latency (300ms–800ms per hop) and loses prosodic/spatial fidelity.

## 🏗️ The Native-First Pattern
With **Gemma 4**, the fleet standard shifts to **Native Grounding** — one model, multiple senses, no STT/CLIP sidecars:

| Tier | Hardware | Tags | Modalities |
| :--- | :--- | :--- | :--- |
| Desktop | RTX 4090 24 GB | `gemma4:12b` | Text + **image** (encoder-free; June 2026) |
| Edge | **Raspberry Pi 5 16 GB** | `gemma4:e4b`, `gemma4:e2b` | Text + **image** + **audio** |
| Heavy | Dedicated GPU | `gemma4:26b` | Agentic + partial multimodal |

See [open-source.md](../not-mcp-related/general-ai/models/open-source.md) and [LOCAL_LLM_STANDARDS.md](../standards/LOCAL_LLM_STANDARDS.md).

### 1. Zero-STT Audio Pipeline
Agents MUST prefer models with native audio encoders (Conformer-style) for voice interaction.
- **Goal**: Minimize the "Interaction Gap" to <200ms.
- **Fidelity**: Preserve prosody vectors (emotional markers) directly for the reasoning engine.

### 2. Variable Visual Grounding (The "Pixel Budget")
Fixed-size vision resizing is deprecated. Fleet-compliant vision agents MUST implement **Dynamic Visual Allocation**:

| Budget (Tokens) | Use Case | Result |
| :--- | :--- | :--- |
| **70** | "Glance" / Object Presence | Rapid detection for IoT triggers. |
| **320** | Component Layout | General UI analysis and navigation. |
| **1120** | Optical Context | OCR of dense logs, code screenshots, or complex architectural charts. |

> [!TIP]
> Use the **70-token budget** for continuous "Visual Watcher" agents to conserve GPU compute, only scaling to **1120** when the agent triggers a `detailed_observation` tool.

---

## 🚀 Implementation Standards

### 1. Tool Call Atomicity
Multimodal checks should be atomic. A single tool call should handle the sensory input and the reasoning step without intermediate text handoffs.

### 2. Resolution Preservation
Maintain aspect ratios. If a 21:9 monitor screenshot is provided, the fleet-compliant provider (e.g., `GemmaProvider`) MUST pass the geometry metadata to the inference engine to prevent artifacting.

---
**Standard Grade**: SOTA-2026-A  
**Fleet Target**: Antigravity, Speech MCP, World Labs integration.
