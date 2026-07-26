# Competitive Analysis

> RoboFang vs OpenClaw vs OpenFang vs OpenManus — different solutions for different problems.

**Canonical deep dive (RoboFang repo):** `D:\Dev\repos\robofang\docs\COMPETITIVE_LANDSCAPE.md`  
**Chat-first UX:** `D:\Dev\repos\robofang\docs\CHAT_UX.md`  
**Backlog:** `D:\Dev\repos\robofang\docs\NEXT_PRIORITIES.md`

---

## TL;DR

| | **RoboFang** | **OpenClaw** | **OpenFang** | **OpenManus** |
|---|:---:|:---:|:---:|:---:|
| **What it is** | Fleet + embodiment hub | Messaging-first agent | Security-first agent OS | CLI general agent |
| **Wins at** | Robotics + MCP fleet | Channels + community | WASM + A2A/OFP | Browser/code loop |
| **Language** | Python 3.12+ | Node.js 22+ | Rust | Python 3.12 |
| **Stars (order of mag.)** | Niche infra | **~200k–300k+** | Low–mid | Mid (FOSS) |
| **Cost model** | Local-first default | Often cloud API | Cloud or local | Local optional |

Star counts change daily; they measure **distribution**, not robotics fitness.

---

## Feature Matrix

| Capability | **RoboFang** | **OpenClaw** | **OpenFang** | **OpenManus** |
|-----------|:-:|:-:|:-:|:-:|
| **Chat-first UX** | 🔄 Hub SPA (chat thread) | ✅ Native channels | ⚠️ Desktop | ⚠️ CLI |
| **Local Inference** | ✅ Primary | ⚠️ Secondary | ⚠️ Supported | ✅ Ollama in config |
| **Multi-Agent Debate** | ✅ Council | ⚠️ Sub-agents | ❌ Fan-out | ❌ Single loop |
| **MCP Federation Hub** | ✅ 30+ servers | ⚠️ Via MCP server | ⚠️ Client+server | ✅ MCP client |
| **Messaging Channels** | ⚠️ Some | ✅ 20+ | ✅ Many adapters | ❌ |
| **Physical Robotics** | ✅ | ❌ | ❌ | ❌ |
| **Virtual Embodiment** | ✅ Resonite/VRChat | ❌ | ❌ | ❌ |
| **Security Sandbox** | ⚠️ Logical + planned | ⚠️ Allowlists | ✅ WASM | ⚠️ Docker optional |
| **A2A / OFP** | ❌ Not yet | ❌ | ✅ | ❌ |
| **Browser automation** | Via fleet MCP | Plugins | Tools | ✅ Built-in |

---

## Where RoboFang Wins

1. **Embodiment** — physical + VR as first-class.
2. **MCP fleet hub** — thin control plane, no monorepo duplication.
3. **Council of Dozens** — adversarial synthesis vs single-agent loops.
4. **Local economics** — council at electricity cost.

## Where Others Win

- **OpenClaw:** channels, ClawHub, mobile chat familiarity, stars/community.
- **OpenFang:** security depth, A2A/OFP, Rust performance.
- **OpenManus:** turnkey Manus-class agent; fleet integrates via **openmanus-mcp**.

---

## Recommended next (RoboFang)

1. **Chat-first hub** — bubble UI, Council/RAG toggles (shipping).
2. **Starter fleet packs** + one-command onboarding doc.
3. **Telegram** (or Signal) hand — channel gap vs OpenClaw.
4. **Streaming ask** + session persistence.
5. **OpenManus** as peer node, not merged source.

See RoboFang `docs/NEXT_PRIORITIES.md`.

---

## Integration Opportunities

| Opportunity | Approach | Effort |
|------------|---------|--------|
| **OpenFang Hands** | `openfang_adapter.py` | ✅ Done |
| **OpenManus tasks** | `openmanus-mcp` fleet node | ✅ Scaffold |
| **A2A Protocol** | Read-only bridge first | Medium |
| **ClawHub plugins** | Manifest → hand adapter | Medium |
| **DefenseClaw / OpenShell / Bastio** | Evaluate; see SECURITY_INTEGRATIONS | Planned |

---

## Change log

- **2026-03-28:** Added OpenManus column; updated stars; chat-first priority; links to RoboFang COMPETITIVE_LANDSCAPE.md.
