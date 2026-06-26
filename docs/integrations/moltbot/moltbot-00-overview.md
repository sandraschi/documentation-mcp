# Moltbot (ClawdBot) — Overview and Index

**Last updated:** 2025-01-28  
**Repo:** [moltbot/moltbot](https://github.com/moltbot/moltbot)  
**Docs:** [docs.molt.bot](https://docs.molt.bot)  
**Author:** Peter Steinberger (Vienna-based; PSPDFKit founder, exited to Insight Partners)

---

## What Moltbot Is

Moltbot (formerly ClawdBot) is an **open-source, local-first personal AI assistant**. You run a **Gateway**—a WebSocket control plane, typically on `127.0.0.1:18789`—that owns all messaging surfaces and talks to a **Pi agent** (RPC-style loop with tools). All orchestration and tool execution stay on your hardware; you bring your own LLM (Anthropic, OpenAI, local models, etc.). Data privacy is preserved by design for everything except the provider API calls you choose to make.

The project is widely described as a "clever combo" of familiar patterns: a single gateway, existing channel SDKs, a standard agent loop with tools, pairing/sandboxing, and a skills system. None of the building blocks are novel in isolation; the leverage comes from **composition** and **product focus**: local-first, multi-channel, bring-your-own-LLM, and extensibility via skills and extensions.

---

## Stack and Surfaces

| Layer | Technology |
|-------|------------|
| Runtime | Node 22+ |
| Language | TypeScript (ESM) |
| Package manager | pnpm (Bun optional for scripts) |
| Tests | Vitest |
| CLI | `moltbot` (legacy shim: `clawdbot`) |
| Config | `~/.clawdbot/moltbot.json`, `~/.clawdbot/credentials/` |
| Workspace | `~/clawd` (configurable via `agents.defaults.workspace`) |

**Channels:** WhatsApp (Baileys), Telegram (grammY), Slack (Bolt), Discord (discord.js), Google Chat, Signal (signal-cli), iMessage, BlueBubbles, Microsoft Teams, Matrix, Zalo, Zalo Personal, WebChat.

**Optional apps:** macOS menu bar app, iOS node, Android node. Voice Wake, Talk Mode, Canvas (A2UI), camera, screen recording.

**Tools:** Bash (exec), browser (CDP), Canvas, cron, webhooks, Gmail Pub/Sub, skills (ClawdHub), session tools (agent-to-agent).

---

## Document Series (Integrations)

This series lives under **MCP Central Docs → Integrations** and provides detailed references for architecture, protocol, channels, tools, skills, nodes, security, and pattern analysis. Use it to integrate Moltbot with MCP-based tooling, design bridges, or reuse patterns.

| Doc | Content |
|-----|---------|
| [moltbot-00-overview](moltbot-00-overview.md) | This overview and index. |
| [moltbot-01-architecture-and-protocol](moltbot-01-architecture-and-protocol.md) | Gateway, WebSocket protocol, handshake, framing, roles, pairing, remote access. |
| [moltbot-02-channels-and-messaging](moltbot-02-channels-and-messaging.md) | Channels, routing, groups, DM policy, allowlists, extensions. |
| [moltbot-03-tools-and-skills](moltbot-03-tools-and-skills.md) | Tools (exec, browser, canvas, cron, webhooks, sessions), skills, ClawdHub, workspace. |
| [moltbot-04-nodes-devices-and-apps](moltbot-04-nodes-devices-and-apps.md) | Nodes (macOS/iOS/Android), `role: node`, device commands, macOS app, Voice Wake, Talk, Canvas. |
| [moltbot-05-security-sandbox-and-ops](moltbot-05-security-sandbox-and-ops.md) | Security model, sandbox, pairing, deployment pitfalls, Tailscale, doctor, hardening. |
| [moltbot-06-patterns-concepts-and-mcp](moltbot-06-patterns-concepts-and-mcp.md) | Pattern breakdown, concepts, overlap with MCP, use and extend. |
| [moltbot-07-academic-ecosystem-and-zoo-integration](moltbot-07-academic-ecosystem-and-zoo-integration.md) | Academic background, predecessors, FOSS competitors, arXiv; extension ideas; combining with MCP zoo. |

---

## Quick Start

```powershell
# Clone (e.g. into D:\Dev\repos\coolstuff)
git -c core.longpaths=true clone --depth 1 https://github.com/moltbot/moltbot.git moltbot
cd moltbot

# Install and build
pnpm install
pnpm ui:build
pnpm build

# Onboard and run gateway
moltbot onboard --install-daemon
moltbot gateway --port 18789 --verbose
```

**Upstream:** [Getting started](https://docs.molt.bot/start/getting-started), [Wizard](https://docs.molt.bot/start/wizard), [Security](https://docs.molt.bot/gateway/security).

---

## References

- [moltbot/moltbot](https://github.com/moltbot/moltbot)
- [docs.molt.bot](https://docs.molt.bot)
- [Architecture](https://docs.molt.bot/concepts/architecture)
- [Gateway protocol](https://docs.molt.bot/gateway/protocol)
- [ClawdHub](https://clawdhub.com) (skills registry)
