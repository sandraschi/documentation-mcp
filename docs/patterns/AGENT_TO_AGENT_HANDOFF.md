---
title: "Agent-to-Agent Handoff Patterns"
category: pattern
status: active
audience: mcp-dev
skill_candidate: false
related:
  - architecture/AGENTIC_MESH_ARCHITECTURE.md
  - architecture/AGENTIC_MESH_robofang_INTEGRATION.md
last_updated: 2025-12-31
---

# Agent-to-Agent Handoff Patterns

**Date**: 2025-12-31  
**Status**: SOTA Standard (Dec 2025)

---

## Overview

In the Dec 2025 SOTA landscape, the distinction between **Server Compositing** and **Agent-to-Agent Handoff** is critical for building scalable, secure, and maintainable AI ecosystems.

| Feature | Server Compositing | Agent-to-Agent Handoff |
|---------|-------------------------|---------------------------|
| **Nature** | Structural / Procedural | Behavioral / Agentic |
| **Visibility** | Hidden from the LLM | Explicit shift in LLM "Persona" |
| **Logic** | Code-driven (deterministic) | Model-driven (probabilistic) |
| **Context** | Shared process context | Transferred semantic context |
| **Example** | robotics-mcp calling unity-mcp | Generalist Agent → Robotics Agent |

---

## The Handoff Protocol (4 phases)

1. **Decision & Intent** — source agent determines specialist needed; calls `handoff_to_agent(target, context_summary, required_tools)`
2. **Context Serialization** — serialize relevant history and state; must not exceed target's context window
3. **Identity & Security Propagation** — sign a Handoff Token with user claims; mutual TLS or OIDC between endpoints
4. **Semantic Resume** — target agent initializes with transferred context: "Hello, I'm {Agent B}. I've reviewed your request..."

---

## Implementation (JSON-RPC)

```json
{
  "status": "HANDOFF_PENDING",
  "target_agent": "robotics-specialist-01",
  "handoff_context": {
    "summary": "User is troubleshooting Unitree Go2 motor calibration",
    "active_entities": ["memory://robotics/go2-unit-01"],
    "priority": "high"
  },
  "identity_token": "eyJhbGci...[SIGNED_JWT]",
  "next_steps": ["Verify motor wiring", "Check last calibration"]
}
```

## Security Rules

1. **Least Privilege** — only pass tools/resources strictly necessary for sub-task
2. **State Scrubbing** — remove PII before context transfer
3. **HITL** — for "Dangerous" agents (Financial, Deployment), require explicit `confirm_handoff()`

## Pydantic-AI Integration (2025 SOTA)

```python
@mcp.tool()
async def handoff_to_robotics(ctx: RunContext[MyDeps], reason: str):
    """Explicitly hands off to the Robotics Specialist."""
    return HandoffResult(agent="robotics", reason=reason)
```
