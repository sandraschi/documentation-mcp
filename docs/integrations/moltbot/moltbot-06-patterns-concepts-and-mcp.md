# Moltbot — Patterns, Concepts, and MCP Overlap

**Last updated:** 2025-01-28  
**See also:** [moltbot-00-overview](moltbot-00-overview.md) | [Architecture](moltbot-01-architecture-and-protocol.md)

---

## 1. "Clever Combo" — Pattern Breakdown

Moltbot is often described as a **clever combination of many not-so-difficult patterns, tools, and concepts**. The value is in **composition and product focus**, not in novel algorithms. Below we map each building block to familiar ideas.

---

## 2. Patterns and Building Blocks

### 2.1 Single WebSocket Control Plane

- **Pattern:** One long-lived Gateway daemon; all clients and nodes connect over WebSocket.
- **Concepts:** Central orchestration, request/response + server-push events, typed API.
- **Familiar:** Similar to a message broker or control-plane API (e.g. LSP, custom dashboards). Not novel; the discipline is **one gateway per host** and **one Baileys session**.

### 2.2 Channels as Adapters

- **Pattern:** Each messaging app is an adapter (Baileys, grammY, Bolt, discord.js, etc.) wired into the Gateway.
- **Concepts:** Normalize inbound/outbound messages; route to sessions; respect allowlists, DM policy, groups.
- **Familiar:** Adapter/plugin pattern. The work is **integration** and **routing**, not new protocol design.

### 2.3 Agent Loop and Tools

- **Pattern:** Pi agent in RPC mode; LLM receives context, calls tools, streams replies. Tools are JSON-schema described.
- **Concepts:** Tool use, streaming, chunking, idempotency for side effects.
- **Familiar:** Same family as OpenAI function-calling, MCP tools, dev Agent frameworks. No new inferencing trick.

### 2.4 Pairing and Device Identity

- **Pattern:** Device-based identity; new devices require approval; device tokens for reconnect.
- **Concepts:** Allowlist, challenge-response (sign nonce), scoped tokens.
- **Familiar:** Device auth patterns (e.g. 2FA devices, companion app pairing).

### 2.5 Sandbox and Tool Policy

- **Pattern:** Non-main sessions run in Docker; tool allow/deny lists.
- **Concepts:** Isolation, least privilege, policy as config.
- **Familiar:** Containerized execution, feature flags, RBAC-style tool access.

### 2.6 Skills and Workspace

- **Pattern:** `SKILL.md` in folders; load from bundled, managed, workspace; filter by bins/env/config/OS.
- **Concepts:** Declarative capability, gating, precedence (workspace > managed > bundled).
- **Familiar:** Plugin systems, env-based feature toggles, workspace-scoped config. AgentSkills-compatible.

### 2.7 Nodes as Capability Hosts

- **Pattern:** Devices connect with `role: node`, declare caps/commands; Gateway routes `node.invoke`.
- **Concepts:** Capability discovery, device-local execution, presence.
- **Familiar:** Smart home hubs, device SDKs, "node" as worker or peripheral.

### 2.8 Remote Access (Tailscale / SSH)

- **Pattern:** Gateway on loopback; Tailscale Serve/Funnel or SSH tunnel for remote clients.
- **Concepts:** No direct internet exposure; auth at tunnel or gateway token.
- **Familiar:** Standard secure remote access patterns.

---

## 3. Concepts Worth Reusing

| Concept | Reuse |
|--------|--------|
| **Single control plane** | One WS API for all clients and devices; single source of truth for sessions, channels, tools. |
| **Typed protocol (TypeBox)** | JSON Schema from TypeBox; codegen for Swift etc. Clear contracts, validation. |
| **Device pairing + tokens** | First-class device identity; approval flow; scoped tokens. |
| **Skills + gating** | SKILL.md + metadata (bins, env, config, OS); load-time filters. |
| **Sandbox + tool policy** | Separate *where* code runs (sandbox) from *what* tools are allowed (policy). |
| **Session snapshot** | Snapshot skills (and similar) at session start; reuse per turn; refresh on watcher or new session. |

---

## 4. Overlap with MCP

### 4.1 Similarities

- **Tools:** Both expose tools to an LLM (or agent). Moltbot tools are Gateway-owned; MCP tools are server-owned. Both use schemas (JSON / tool definitions).
- **Resources:** Moltbot has workspace files, skills, config; MCP has resources. Different shape, similar idea: structured data fed into context.
- **Protocol:** MCP uses JSON-RPC (stdio/SSE); Moltbot uses custom JSON-over-WebSocket. Both are request/response + events.
- **Extensibility:** MCP via servers and tools; Moltbot via skills, extensions, plugins.

### 4.2 Differences

- **Transport:** MCP typically stdio or SSE; Moltbot WebSocket. Moltbot also has a single Gateway that owns channels and nodes.
- **Scope:** MCP is tool/resource protocol for AI clients. Moltbot is a **full product**: channels, nodes, apps, skills, auth, sandbox.
- **Ownership:** Moltbot Gateway runs your assistant; MCP servers are often adjunct tool providers.

### 4.3 Integration Directions

- **MCP → Moltbot:** Expose MCP servers as **tools** or **skills** consumed by the Pi agent (e.g. bridge that translates MCP tools into Moltbot tool schemas and invokes MCP).
- **Moltbot → MCP:** Expose Moltbot’s agent or tools to **MCP clients** (e.g. Cursor, other IDEs). E.g. "Moltbot MCP server" that wraps `agent`, `send`, or specific tools.
- **Shared patterns:** Skills vs MCP tools; gating vs env-based server config; sandbox vs running MCP servers in containers.

---

## 5. Use and Extend (Summary)

### 5.1 Use

- **Personal assistant** over WhatsApp/Telegram/Slack/Discord without a new app.
- **Dev/automation** via bash, browser, cron, webhooks, skills.
- **Multi-device** with macOS app + iOS/Android nodes (voice, Canvas, camera).
- **Local-first** orchestration; only LLM calls leave the machine (or use local models).

### 5.2 Extend

- **MCP bridge:** Moltbot tools → MCP, or MCP tools → Moltbot skills/tools.
- **Knowledge/RAG:** `~/clawd` workspace + custom "knowledge" tool calling your graph/RAG (e.g. Advanced Memory).
- **Games-app / backends:** Webhooks, cron, or `moltbot agent --message "..."` calling your game APIs, stockfish, etc.
- **New channels:** Extensions under `extensions/` (e.g. internal comms, games lobby).
- **New skills:** ClawdHub or workspace skills that call your backends (e.g. chess, JLPT).
- **Ops:** Tailscale + password, `moltbot doctor`, sandbox non-main, monitor health/heartbeat.

---

## 6. References

- [moltbot-00-overview](moltbot-00-overview.md)
- [moltbot-01-architecture-and-protocol](moltbot-01-architecture-and-protocol.md)
- [moltbot-05-security-sandbox-and-ops](moltbot-05-security-sandbox-and-ops.md)
- [MCP Protocol Overview](../protocol/OVERVIEW.md) (if present in mcp-central-docs)
- [docs.molt.bot](https://docs.molt.bot)
