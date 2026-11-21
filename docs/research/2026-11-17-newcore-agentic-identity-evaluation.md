# NewCore — Agentic Identity Platform Evaluation & FOSS Equivalents

**Date:** 2026-11-17 (Europe/Vienna) | **Status:** Evaluation note | **Location:** `mcp-central-docs/research/`
**Source:** `https://newcore.com/`

## 0. TL;DR + Verification Matrix

**NewCore** (`newcore.com`) is an enterprise **Agentic Identity & Security Platform (AISP)** built to unify human workforce IAM (SSO, MFA, directory, lifecycle) with Non-Human Identity (NHI) and AI agent governance. It treats AI agents as first-class identities—assigning human owners, replacing static API keys with short-lived task-scoped tokens, auditing agent actions, and shipping an "Agentic Skill" integration for coding agents (Claude Code, Cursor, Codex).

**Fleet verdict:** Useful for **mid-to-large enterprises** governing autonomous agents across corporate SaaS/cloud apps and replacing Okta/Ping gaps around agent identity. **Not usable / overkill** for our **local, single-operator `*-mcp` fleet**—there is no free self-serve tier, no open-source/self-hosted version, and pricing is custom enterprise-only (direct sales / AWS Marketplace). For our fleet, **lightweight FOSS secret brokering** (`agentsecrets` or `secr`) delivers the practical security win (keeping raw keys out of LLM contexts and logs) with near-zero operational overhead.

| Claim | Status (2026-11-17) | Source |
|---|---|---|
| NewCore provides unified IAM/governance for humans, machines, and AI agents | **VERIFIED** | `newcore.com`, `dealroom.co`, `picari.ai` |
| Replaces standing service-account/API credentials with short-lived, task-scoped tokens and enforces policies/audit trails | **VERIFIED** | `newcore.com`, `nhimg.org`, `picari.ai` |
| Offers "Agentic Skill" integration packages for Claude Code, Cursor, and Codex | **VERIFIED** | `newcore.com`, `msspalert.com` |
| Backed by $66M seed round (Cyberstarts, Index Ventures, Evolution Equity Partners); founded by former Dome9 / Check Point executives | **VERIFIED** | `prnewswire.com`, `dealroom.co` |
| No public self-serve pricing or free tier; sold via custom enterprise quotes and AWS Marketplace | **VERIFIED** | `newcore.com`, `amazon.com` (AWS Marketplace) |
| FOSS alternatives exist across secret brokering (`agentsecrets`, `secr`), agent IAM (`OpenA2A`, `ZeroID`), policy (`Cerbos`), and OAuth (`Casdoor`, `Ory`, `Zitadel`) | **VERIFIED** | `github.com`, `secr.dev`, `casdoor.com`, `cerbos.dev`, `ory.com` |

---

## 1. What NewCore Does

Legacy Identity Providers (Okta, Entra ID, Ping) were designed for humans logging into web apps, leaving AI agents and scripts to rely on long-lived API keys or over-privileged service accounts. NewCore targets that gap with:

1. **Unified Identity Graph & Discovery:** Maps human employees and AI agents across vendors into a single graph, tying every agent to an accountable human owner.
2. **Short-Lived, Task-Scoped NHI Credentials:** Eliminates standing credentials by issuing ephemeral, task-scoped tokens with separate lifecycle management and revocation.
3. **Agent Governance & Audit Trails:** Evaluates agent actions against corporate security policies and maintains a centralized audit log of what each agent accessed and did.
4. **Core Workforce IAM + Coding Agent Integration:** Includes SSO, MFA, phishing-resistant credentials, and "Agentic Skill" packages so coding assistants (Claude Code, Cursor, Codex) authenticate as managed enterprise identities rather than sharing a developer's raw tokens.

---

## 2. Pricing, Availability & Fleet Fit

### Cost & Procurement
* **Pricing model:** Custom enterprise quotes (no flat-rate or self-serve tier published on `newcore.com`), scaled by identity/seat count, managed apps/connectors, and agent identity volume.
* **Procurement:** Direct enterprise sales or **AWS Marketplace** private/enterprise billing.
* **Self-hosting / FOSS:** None. Proprietary enterprise platform.

### Why it is *not* a fit for our fleet
* **Single-operator local environment:** Our `*-mcp` servers and coding agents run locally for one operator, not across an org chart of employees, HR directories, and corporate SaaS tenants.
* **No immediate usability:** Cannot be installed locally, tested via a free tier, or integrated into our Python/FastMCP stack without enterprise procurement.
* **Heavy control-plane mismatch:** Standing up an enterprise IdP plane just to stop agents from seeing raw API keys is massive overkill.

---

## 3. FOSS Equivalents (Lightweight to Full IAM)

Depending on which problem you want to solve, open-source options split cleanly into four layers:

| Layer | Tool | License / Model | What It Solves | Best Fit |
|---|---|---|---|---|
| **1. Local Secret Proxy** | **`agentsecrets`** (`The-17/agentsecrets`) | MIT / Local proxy | Zero-knowledge proxy (`agentsecrets proxy`); injects bearer tokens/headers server-side so raw keys never enter LLM context or transcripts. Uses X25519 + AES-256-GCM. | **Best for solo / local MCP fleets** |
| **1. MCP Secret Gateway** | **`secr`** (`@secr/mcp`) | Open-source MCP gateway | Secret allowlists, log/transcript redaction hooks, and short-lived grants for Claude Code, Cursor, Continue, etc. | **Best for coding-agent harnesses** |
| **2. Agent IAM** | **OpenA2A** (`opena2a-org/agent-identity-management`) | Apache-2.0 | Ed25519 cryptographic identities for agents (replacing API keys), capability-based tool access, MCP server attestation, audit trails. | **Multi-agent / MCP attestation** |
| **2. Agent Delegation** | **ZeroID** | Open-source | RFC 8693 token exchange for multi-agent delegation chains (permissions attenuate down sub-agent trees) + OpenID SSF/CAEP revocation. | **Orchestrator → sub-agent trees** |
| **3. Tool Policy Engine** | **Cerbos** | Apache-2.0 | Stateless sub-millisecond YAML Policy-as-Code PDP to gate *which* MCP tools an agent can call in a given context. | **Fine-grained tool authorization** |
| **3. MCP OAuth 2.1** | **Casdoor** | Apache-2.0 | Implements MCP-required OAuth 2.1 specs (RFC 9728, RFC 7591, RFC 8707, DPoP-bound short-lived tokens, RFC 8693 token exchange). | **Remote / multi-user MCP servers** |
| **4. Full IAM / Secrets** | **Ory (`Kratos`/`Hydra`)**, **Zitadel**, **OpenBao**, **Infisical** | Open-source (self-hosted) | Full OAuth/OIDC, M2M tokens, and dynamic secret issuance. | **Production SaaS / infra teams** |

*(See also [2026-11-17-workos-airlock-ibac-evaluation.md](2026-11-17-workos-airlock-ibac-evaluation.md) for the complementary **tool-call policy / IBAC gateway** side—e.g. `@waterlock/gateway` and `mcp-airlock`.)*

---

## 4. Recommended First Lightweight Step for Our Fleet

**Start with a local zero-knowledge secret proxy (`agentsecrets` or `secr`) on a single high-risk API workflow—do not deploy an IAM server.**

### Why this first?
1. **Solves the #1 real local risk immediately:** In a local `*-mcp` + coding-agent fleet, the primary failure mode is not "who owns this corporate bot," it is **raw API keys/tokens leaking into LLM context windows, session transcripts, or debug logs** (or an agent reading `.env` files it shouldn't).
2. **Zero infra tax:** No database, no OAuth consent server, no IdP migration, and no external cloud dependency.
3. **Incremental adoption:** You can wrap a single sensitive integration (e.g., GitHub, cloud, or external REST APIs) first without touching the other 180+ local MCP servers.

### Concrete Pilot Plan
1. **Pick 1–2 sensitive external tokens** currently stored in `.env` or passed to an agent/MCP server (e.g., an external SaaS/cloud API token).
2. **Test `agentsecrets` (or `secr` if you want MCP-native allowlisting + log redaction):**
   * Store the real token in the local broker instead of exposing it in the agent's environment.
   * Route the tool/HTTP call through the local proxy so the agent only sees an abstract secret reference, never the raw value.
   * Verify that session transcripts/logs contain zero raw secret strings.
3. **Only graduate to Layer 2/3 (`Casdoor` + `Cerbos` or `OpenA2A`) if/when** we expose MCP servers over a network to multiple users or untrusted sub-agents that need attenuated OAuth 2.1 / DPoP tokens.
