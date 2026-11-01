# FastMCP 4 — Fleet Assessment (Revised Verdict)

**Date**: 2026-08-01
**Status**: BETA — FastMCP 4.0.0b1 is a prerelease. Do NOT adopt in production yet.
**Cross-ref**: [2026-07-28-spec-migration.md](2026-07-28-spec-migration.md) · [fleet-llm-post-sampling-design.md](../analysis/fleet-llm-post-sampling-design.md)

---

## 1. The Reframe

FastMCP 4 was never the problem. The problem was migrating to it **while still depending on `ctx.sample()`** — which is removed in v4.

If the fleet migrates to `fleet-llm` (server-side LLM: DeepSeek V4 Flash cloud tier + Ollama local tiers) **first**, the sampling removal stops hurting. We no longer need it. The two migrations are complementary:

```
Step 1: fleet-llm  → removes the ctx.sample() dependency (the blocker)
Step 2: FastMCP 4  → mechanical upgrade, no architectural pain
```

At that point FastMCP 4 is not just survivable — it's an improvement.

---

## 2. What FastMCP 4 Improves (with sampling out of the picture)

| Feature | What it gives |
|---------|---------------|
| **Multi-era serving** | One process serves old-protocol (Claude Desktop) and new-protocol clients simultaneously, negotiated per connection. No flag day, no fork. |
| **Server extensions API** | `mcp.add_extension()` — proper plugin surface. Tasks, auth, telemetry become opt-in extensions instead of core surgery. |
| **Snake_case protocol types** | `tool.input_schema`, `is_error`, `mime_type` — Pythonic typing, working autocomplete, happy type checkers. Wire format unchanged (camelCase aliases retained). |
| **Universal middleware** | `on_message` sees every message (notifications, validation failures, unknown methods), not just routable requests. Old selective dispatch was a source of silent bugs. |
| **Path security built-in** | Templated resources screen `..` traversal / absolute paths / null bytes at the read chokepoint before handlers run. Free hardening; per-param exemptions available. |
| **Deterministic tool ordering** | Stable `tools/list` order = better LLM prompt-cache hit rates = cheaper inference. |
| **Argument completion** | `@mcp.completion()` — autocomplete for prompt args and resource-template parameters. New capability, absent in v3. |
| **UserSession / SessionId** | Explicit server-minted state handles instead of fragile hidden session state. |
| **httpx2** | OS trust store TLS, same API surface, drop-in import swap. |
| **Spec-aligned error codes** | Resource-not-found moved to `-32602` (INVALID_PARAMS, SEP-2164). |
| **Cache hints** | Server-level cache hints (SEP-2549) — the fleet's own response caching can use them. |

---

## 3. The Proviso: Still Beta

FastMCP 4.0.0b1 is a **prerelease**. The release notes say it directly: *"This is a beta released for testing ahead of 4.0. Pin an exact version and expect sharp edges."*

- **Do NOT adopt in production yet.** No fleet server runs a beta framework on the critical path.
- **Pin the stable line while waiting**: `fastmcp>=3.4.5,<4.0.0` fleet-wide.
- **Watch for**: stable 4.0.0 release, FastMCP 4.x patch cadence, and the httpx2 fork's longevity (single-developer fork — the one genuine architectural risk).
- **Canary when stable ships**: convert a non-critical server (learnbot-mcp — zero sampling usage) first, run 2 weeks, then pilot, then roll.

---

## 4. Migration Costs (honest)

Even after fleet-llm removes the sampling dependency, the upgrade has busywork:

- ~28 moved imports (`fastmcp.server.proxy` → `fastmcp.server.providers.proxy`, `SkillsProvider` → `SkillsDirectoryProvider`, `Cachable*` → `Cacheable*`, etc.)
- `httpx` → `httpx2` in tool code (`except httpx.` handlers silently become dead code otherwise)
- `pydantic >= 2.12`, `FastAPI >= 0.133.0` (Starlette 1.x compat) dependency floors
- Tasks moved to `fastmcp[tasks]` extra + `TasksExtension()` registration
- camelCase bridge is temporary — migrate field reads to snake_case now to avoid the future hard break
- `ctx.elicit()` is era-gated — fleet tools that elicit need guard-pattern rewrite (separate audit)
- `Middleware.on_initialize` never fires on modern connections — auth gating must move to per-request checks

---

## 5. Recommended Sequence

| Order | Action | When |
|-------|--------|------|
| 1 | Pin `fastmcp>=3.4.5,<4.0.0` fleet-wide | Now |
| 2 | Build `fleet-llm` package (DeepSeek + Ollama, 3-tier) | Now — unblocks everything |
| 3 | Migrate sampling servers to `llm.ask()` / `llm.agent()` | As fleet-llm matures |
| 4 | Upgrade to FastMCP 4 **stable** (not beta) | When 4.0.0 final ships + canary passes |
| 5 | Convert the last sampling-era constructs (elicit, on_initialize) | During pilot |

---

## 6. Verdict

FastMCP 4 on its own merits: **7/10 for the fleet** — good engineering, real improvements, mechanical migration cost.

FastMCP 4 while still depending on `ctx.sample()`: **4/10** — removes more than it adds.

The pain was never the framework. It was the protocol change (sessionless 2026-07-28) removing the sampling subsidy with no replacement. DeepSeek V4 Flash **is** the replacement. Migrate fleet-llm first, FastMCP 4 second, and the fleet ends up protocol-independent, Anthropic-independent, and cheaper than the old $20/month Claude Pro was.
