# NVIDIA NemoClaw Integration

NVIDIA NemoClaw is an enterprise-grade AI agent platform built upon the open-source **OpenClaw** stack. Introduced at GTC 2026, it is designed to enhance the security, privacy, and scalability of autonomous AI agents by providing an isolated execution environment, robust memory management, and deep integration with NVIDIA's NeMo framework.

## Role in the Fleet (Robofang Memory Component)

Within the Antigravity fleet, NemoClaw serves as the secure **memory and state management component** for the `robofang` project (and other autonomous bots).

While OpenClaw manages agent memory through persistent on-disk Markdown files (allowing for contextual recall across sessions), NemoClaw introduces several critical enhancements:
- **NVIDIA OpenShell Sandbox**: A secure, isolated environment that ensures the agent cannot perform unauthorized system data access or destructive operations while recalling or modifying memories.
- **Privacy Router**: Manages data transmission when utilizing cloud-based frontier models alongside local Nemotron models, ensuring sensitive memory is kept private.
- **State Integrity**: Ensures that context compaction and semantic recall tools operate securely, maintaining the integrity of the agent's state across extended long-horizon tasks.

### Architecture

- **Hardware**: Hardware-agnostic at the agent layer, but highly optimized for RTX 4090 and DGX systems for running local language models (like `Llama 3.3 70B` or `Gemma 3 27B`) via the NeMo framework.
- **Persistent Storage**: Utilizes local file descriptors and vector storage to maintain context, decisions, and daily logs, which are securely sandboxed.
- **Orchestration**: Operates alongside `robofang` to enable a persistent "Robot Personality" (e.g., the autonomous coffee shop companion) that gracefully remembers previous interactions without compromising local host security.

## Using NemoClaw in MCP

**Implemented in Docs MCP** (functional stand-in using the same LanceDB + BGE stack as docs RAG):
- `nemoclaw_store_memory(namespace, content)`: Persists structured memory in a namespace; stored in table `nemoclaw_memory` for semantic recall.
- `nemoclaw_recall(namespace, query, limit)`: Semantic search over stored memory in that namespace.
- `nemoclaw_compaction_status()`: Returns total entries, per-namespace counts, and a compaction suggestion when namespaces exceed a threshold.

These tools are available via Docs MCP (Tools Hub, Memory page, and `POST /api/execute`). No OpenShell/Sandbox yet; persistence and semantic recall are fully functional.

---
*Status: Functional (Docs MCP); OpenShell/Sandbox and KVTC remain architecture / vendor roadmap*
*Tags: #robotics-mcp #robofang #nemoclaw #openclaw #memory*
