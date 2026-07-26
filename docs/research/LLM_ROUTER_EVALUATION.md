# LLM Router Evaluation: Maestro vs LiteLLM

**Date:** 2026-06-25  
**Status:** Evaluated — pending decision  
**Sources:**  
- Maestro: https://github.com/walidboulanouar/maestro  
- LiteLLM: https://github.com/BerriAI/litellm  

---

## 1. What these tools do

Both sit between your app and LLM providers, but at very different scales:

| | Maestro | LiteLLM |
|---|---|---|
| **Category** | LLM Router (model selection + verify/escalate) | AI Gateway (auth, routing, spend, guardrails, MCP proxy) |
| **Stars** | 27 | 51.4k |
| **Language** | TypeScript (Node.js 20+, Hono) | Python (FastAPI + React UI) |
| **License** | MIT (core + all) | MIT (core proxy) + Commercial (enterprise features) |
| **Backing** | Solo dev (walidboulanouar) | YC W23 (BerriAI), production at Stripe/Netflix |
| **Dependencies** | 3 runtime (Hono, zod, @hono/node-server) | 15+ runtime (FastAPI, uvicorn, Redis, PostgreSQL, Prisma, etc.) |
| **Deploy** | `git clone && npm install && npm run serve` | `pip install 'litellm[proxy]'` or Docker Compose |
| **MCP support** | None | **Built-in MCP Gateway** — proxy any stdio/HTTP MCP server |
| **Dashboard** | Minimal HTML trace viewer | Full React admin dashboard |
| **Cost tracking** | Per-request breakdown in response | Per-key, per-team, per-user, all providers |

---

## 2. Maestro — detailed assessment

### What makes it interesting

Maestro's core loop — **classify → route → execute → verify → escalate** — is the only OSS implementation of the cheap-first-verify-escalate pattern (inspired by Sakana's TRINITY/Conductor papers). Key design wins:

- **Dual API compatibility** (OpenAI + Anthropic format) — works as a drop-in proxy for Claude Code, opencode, Cursor, any OpenAI SDK
- **Cost transparency** per response (`maestro` block with model, tokens, cost, savings_pct)
- **Deterministic offline benchmark** (`npm run eval`) — 25 fixtures, compares route quality vs oracle
- **Registry as data** — model specs in a dated JSON file, remappable without retraining
- **Ultra-lightweight** — 3 deps, no GPU, no DB, runs with zero config (mock provider)

### Concerns

- **27 stars, v0.1** — honest about being a ~5-hour build, not production-hardened. Risk of abandonment.
- **No Dockerfile shipped** (roadmap v0.2), no npm package, no CI/CD
- **Node.js** — not part of the current Python fleet stack. The MCP server would manage a Node.js subprocess.
- **"Free Fugu alternative" pitch** is weak if Fugu isn't a desired product
- **No MCP support** — adding MCP Gateway integration would be from scratch
- **Verifier is mock-only** — the real LLM-based verifier with rubric scoring is on the roadmap, not shipped. Without it, the "verify" step is a heuristic strength-vs-difficulty check, not an actual quality gate.
- **Classifier is regex/heuristic** — zero-cost but limited. No learned routing in this version.

### Fleet fit

| Need | Does it solve it? |
|---|---|
| Save API costs by routing simple queries to cheap models | Yes — that's the core value |
| Cost visibility per request | Yes — built-in |
| Drop-in for Claude Code / opencode | Yes — Anthropic-compatible endpoint |
| Centralized auth / spend control | No — too early |
| Replace meta-mcp for server discovery | No — not what it does |
| MCP Gateway (proxy our MCP servers) | No — would need to build |

---

## 3. LiteLLM — detailed assessment

### What makes it interesting

LiteLLM is the **de facto standard OSS AI Gateway**. It's not just a router — it's a full management plane for LLM infrastructure.

Key capabilities relevant to the fleet:

- **100+ provider adapters** — any model through one OpenAI-compatible endpoint
- **Built-in MCP Gateway** — register stdio/HTTP MCP servers, expose through `/mcp/` with per-key auth. This means we could register all fleet MCP servers in LiteLLM and access them through one gateway with auth tokens.
- **Virtual keys** — create scoped API keys per tool, per user, with budgets and rate limits
- **Cost tracking** — per model, key, team, user. Exports to Langfuse, Prometheus, Datadog.
- **Caching** — Redis response cache (dedup identical requests)
- **Guardrails** — PII masking, content filtering at proxy level
- **React admin dashboard** — live analytics, key management, MCP server management UI
- **Terraform modules** — AWS ECS + Aurora, GCP Cloud Run + Cloud SQL
- **Python** — matches fleet stack

### Concerns

- **Heavy architecture** — requires PostgreSQL + Redis for full functionality. This is a whole new infrastructure service to run.
- **Extra latency** — ~5-15ms P95 overhead per request (proxied mode). Marginal but real.
- **Enterprise creep** — some desirable features (SSO, advanced guardrails) are behind commercial license
- **Overkill for single-user** — the auth/budget/team features add complexity with no benefit when you're the only operator
- **1300+ open issues** — active project but also a lot of open surface area
- **Another service to maintain** — DB migrations, Redis config, proxy updates

### Fleet fit

| Need | Does it solve it? | Worth the complexity? |
|---|---|---|
| Centralized MCP server access with auth | Yes — MCP Gateway built-in | Maybe — meta-mcp already does discovery |
| Cost tracking across providers | Yes | Only if cost is a pain point |
| Virtual keys for sharing access | Yes — but single user | No — overkill |
| Rate limiting / guardrails | Yes | Not needed today |
| Provider fallback / failover | Yes | Marginal value in practice |
| Drop-in for Claude Code / opencode | Yes | LiteLLM is a proxy, not a router |

---

## 4. Honest assessment: do we need either?

### The question LiteLLM answers

> "I have a team of 10 engineers hitting 6 different LLM providers with shared API keys, and I need to track spend, set budgets, and rotate keys without redeploying."

We don't have this problem. Meta-mcp already handles fleet server discovery.

### The question Maestro answers

> "I want to automatically route simple queries to cheap models and only escalate to expensive frontier models when the cheap answer fails verification, saving 30-50% on API costs."

This is a real value proposition, but:
- The **classifier is heuristic** (not learned) — quality is capped
- The **verifier is mock-only** — not actually checking answer quality with an LLM yet
- For the fleet's typical usage (Claude Code coding sessions, individual tool calls), **the savings from routing are dwarfed by the cost of a wrong routing decision** that wastes developer time

### The real math

A typical deep research session costs ~$3-5 in API calls. A wrong routing decision that produces a bad answer costs ~15 minutes of debugging time — worth ~$15-30 at the user's hourly rate. The router has to save 5-10x its own failure rate just to break even.

**For a production API service at scale** (millions of requests/day), the 80/20 cheap/expensive split makes enormous sense. For a developer tool used by one person? The marginal savings don't justify the infra overhead.

---

## 5. Conclusion

| Tool | Verdict | Rationale |
|---|---|---|
| **Maestro** | **Skip** | 27 stars, v0.1, Node.js, no real verifier, "free Fugu" pitch irrelevant. Too early to bet on. |
| **LiteLLM** | **Skip for now** | Excellent project, wrong scale. The auth/budget/MCP-Gateway features solve team problems we don't have. Adding PostgreSQL+Redis for one dev is negative ROI. |
| **Neither** | **Stay course** | Current direct-to-provider setup works fine. Revisit if: (a) Maestro reaches 1k+ stars with a real verifier, or (b) the fleet grows to 5+ active developers sharing API keys. |

### Revisit triggers

- Maestro hits 500+ stars and ships a working LLM-based verifier
- LiteLLM publishes a lightweight single-binary mode (SQLite instead of Postgres, no Redis dependency)
- The fleet adds 3+ more active developers who need shared API key management
- API costs exceed $200/month and become a visible budget item
