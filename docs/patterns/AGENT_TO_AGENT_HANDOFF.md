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

---

## Session handoff (opencode file-based, Oct 2026)

Runtime handoff above assumes live agents. opencode sessions share no memory,
so session-to-session handoff is file-based: write a markdown handoff, `@` it
in the next session. `/share` makes a link for human eyes and gives the
receiving agent zero context - link for people, file for agents.

### Freshness guard (paste at the top of every handoff)

A handoff without a pinned state rots the moment either tree moves. The guard
names a checkable fact (commit hash + dirty count + real timestamp) so the
receiver has something to mismatch against. "Use current state" alone is not
checkable - the agent will reassess yesterday's tree and sound confident.

```
> FRESHNESS GUARD (receiving agent: run this first, before any assessment).
> This handoff is pinned to repo state at <YYYY-MM-DD HH:MM +ZZ:ZZ>, NOT to "latest".
> 1. Run: `git -C <repo> log --oneline -5` and `git status --porcelain | Measure-Object -Line`.
>    Pinned: HEAD `<hash subject>`, dirty = <N> paths (<describe: M files + untracked>).
> 2. If HEAD differs OR dirty count differs OR the user says work has landed: STOP.
>    Re-read the actual diff (`git diff`, new files) and state what moved before
>    reasoning. Treat every claim below about "current tree" as STALE until re-verified.
> 3. If verification is impossible (repo missing, git unavailable): say
>    `STATE UNKNOWN - cannot reassess` and ask. Never reassess from memory.
> 4. Temporal rule: never invent dates. Handoff claims expire at session end; re-stamp on use.
```

Notes:

- Unversioned dirs cannot be pinned by hash, only by "binary exists, built
  <date>". If a scratch dir stops being throwaway, `git init` + first commit
  (with `.gitignore` before first `git add`) so future handoffs pin it too.
- One guard per repo named in the handoff. Two dirty repos = two pinned blocks.
- Provenance: observed 2026-10-14 moving a Rust/WordCraft research handoff
  (`_exchange/rust-wordcraft-reversing-handoff-2026-10-14.md`) into a
  dirty-tree `reversing-mcp` reassessment.
- opencode invocation (share vs @file, snapshot format, HANDOVER.md,
  session-log): `opencode/SESSION_HANDOFF.md`. The template above is canonical;
  that page copies nothing, it points here.
