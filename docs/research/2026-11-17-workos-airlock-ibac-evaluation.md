# WorkOS Airlock — Intent-Based Access Control (IBAC) Evaluation

**Date:** 2026-11-17 (Europe/Vienna) | **Status:** Evaluation note | **Location:** `mcp-central-docs/research/`
**Source:** `https://workos.com/airlock` (via AlphaSignal Q4 2026)

## 0. TL;DR + Verification Matrix

WorkOS Airlock is a **hosted Intent-Based Access Control (IBAC) gateway** for AI agents. It sits between an agent (including MCP gateways and coding harnesses) and external APIs/credentials, evaluates every tool call against deterministic rules plus an LLM policy judge, and returns **allow**, **deny**, or **escalate to human** (e.g., Slack approval) while keeping raw OAuth tokens out of the agent's context.

**Fleet verdict:** Useful if shipping a **multi-user / B2B SaaS agent** that needs delegated OAuth, human-in-the-loop approvals, and compliance audit logs out of the box. **Not a good fit** for our **local, single-operator MCP fleet**—it is a proprietary cloud service with SaaS latency, cloud dependency, and no self-hosted deployment option.

| Claim | Status (2026-11-17) | Source |
|---|---|---|
| Airlock implements Intent-Based Access Control (IBAC) between agents and tools/APIs | **VERIFIED** | `workos.com/airlock` (via web search) |
| Integrates with WorkOS Pipes & MCP gateways; agent uses intent-bound tokens instead of raw OAuth credentials | **VERIFIED** | `workos.com`, `bytebytego.com`, `zhcinstitute.com` |
| Hybrid evaluation: deterministic rules (endpoints, HTTP methods, body values) + runtime LLM judge; outcomes are allow / deny / human approval (e.g., Slack) | **VERIFIED** | `workos.com`, `zhcinstitute.com` |
| Supports BYOK for governing inference (e.g., Fireworks AI) and full request/decision audit logging | **VERIFIED** | `workos.com` |
| Proprietary cloud service (early-access/preview pricing; no self-hosted or air-gapped deployment) | **VERIFIED** | `workos.com`, `sealgate.ai` |
| Open-source alternatives exist (`@waterlock/gateway`, `mcp-airlock`) | **VERIFIED** | `github.com`, `waterlock.cc` |

---

## 1. What WorkOS Airlock Does

Traditional authorization (RBAC, FGA) assumes permissions are static and known at compile time. AI agents discover and invoke tools dynamically at runtime, which makes static least-privilege scoping brittle.

Airlock addresses this with **Intent-Based Access Control (IBAC)**:

1. **Credential isolation:** Sits in front of downstream APIs (via WorkOS Pipes) and MCP gateways. The agent receives intent-bound tokens and never sees underlying OAuth tokens.
2. **Per-call policy evaluation:** Every intercepted tool/API call is checked against two layers:
   - **Deterministic rules:** Hard constraints on endpoints, HTTP methods, and restricted payload values.
   - **LLM policy judge:** A governing model evaluates the task context and stated intent against natural-language team policies (supports BYOK inference providers).
3. **Three-way enforcement:**
   - **Allow** — execute the call.
   - **Deny** — block the call.
   - **Human-in-the-loop** — pause and route to a teammate for approval (e.g., Slack).
4. **Auditability:** Logs every agentic request, context, and enforcement decision.

---

## 2. Fleet Fit Assessment

### Where Airlock *is* useful
- **Multi-user / B2B agent products:** Delegating per-user third-party OAuth safely without exposing tokens to the LLM or building a custom token-brokering + approval proxy.
- **High-impact external mutations:** Gating irreversible actions (financial transfers, external emails, production SaaS/API writes) where static role checks are too coarse.
- **Compliance-driven teams:** Out-of-the-box audit logs and human sign-off workflows.

### Where Airlock is *not* a good fit (especially for our fleet)
- **Local, single-operator MCP fleet (`*-mcp`):** Routing local MCP tool calls through a hosted cloud gateway introduces unnecessary network latency, external availability dependency, and vendor lock-in.
- **Self-hosted / local-only data requirements:** Airlock is a proprietary SaaS product; it cannot be self-hosted inside a local network or air-gapped environment.
- **Deterministic-only needs:** Running an LLM judge on every tool call adds latency and token cost. Where simple path/command/method allowlists suffice, deterministic local middleware is faster and more predictable.
- **Opaque / custom pricing:** Currently gated behind early-access / custom sales rollouts rather than transparent self-serve tiers.

---

## 3. Open-Source & Local Alternatives

If we want the **policy-gateway pattern** locally without WorkOS cloud lock-in:

| Capability | WorkOS Airlock | `@waterlock/gateway` | `mcp-airlock` |
|---|---|---|---|
| **License / Hosting** | Proprietary SaaS | MIT / Self-hosted (TS) | FOSS / Local binary (Go) |
| **Hides raw tokens from agent** | Yes (WorkOS Pipes) | Yes (session-scoped tokens) | Yes (OS keychain + DPoP) |
| **Deterministic parameter rules** | Yes | Yes (TypeScript functions) | No (auth/transport layer) |
| **LLM / natural-language policy** | Yes (BYOK) | Yes | No |
| **Human-in-the-loop (e.g. Slack)** | Yes (built-in) | DIY | No |
| **Primary target** | Multi-user SaaS agents & APIs | Self-hosted agents & APIs | `stdio` client → remote MCP |

### 3.1 `@waterlock/gateway` (`waterlock.cc`) — Details & Cons

`@waterlock/gateway` (`npm i @waterlock/gateway`, MIT) is the closest open-source equivalent to WorkOS Airlock. You run a trusted gateway holding real provider credentials (e.g., Gmail, Linear), issue short-lived session tokens to the agent, and enforce a **default-deny** policy using TypeScript functions and/or natural-language rules.

**Cons / Tradeoffs:**
- **Early ecosystem maturity:** Official provider wrappers are still expanding (REST first, GraphQL like Linear added later). Unwrapped APIs require writing custom provider definitions (e.g., `formatError` handlers).
- **SDK error-wrapping friction:** Because it proxies native third-party SDKs (like `@googleapis/gmail` or `@linear/sdk`), a gateway policy block can bubble up as a provider-formatted `403` error, requiring callers to inspect custom body fields (e.g., `reason` / `waterlock.cc` markers) to distinguish a policy block from an upstream API rejection.
- **TypeScript / Node-centric:** Fits TS/JS agent stacks cleanly, but adds a separate Node proxy hop if your fleet is Python-native (`FastMCP`).
- **Single-request evaluation scope:** Rules evaluate individual intercepted requests; multi-step stateful workflows across multiple apps are harder to express cleanly.
- **No turnkey HITL UI or OAuth broker:** Unlike WorkOS Airlock + Pipes, you own hosting, token storage, and any human-approval UX (e.g., Slack escalation).

### 3.2 `mcp-airlock` (GitHub / Go) — Details

Despite the similar name, `mcp-airlock` is **not** an LLM intent-judging policy engine. It is a local `stdio`-to-HTTPS security bridge for desktop/CLI clients (Claude Desktop, Cursor, Gemini CLI) connecting to **remote** MCP servers. It implements **FAPI 2.0 + DPoP** (sender-constrained, audience-restricted tokens) and stores credentials in the OS keychain, but does not inspect tool-call semantics or enforce parameter-level policies.

### 3.3 Fleet-native middleware

For our local Python `FastMCP` servers (`*-mcp`), deterministic tool-level allowlists and confirmation gates in-process avoid external proxy hops entirely.
