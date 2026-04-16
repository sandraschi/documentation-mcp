# OpenClaw - Status Report

**Last Updated:** 2026-02-06
**Source Repo:** `D:\Dev\repos\external\moltbot` (moltbot/moltbot = openclaw product)
**Type:** Personal AI Assistant Platform (Gateway + CLI + Channels + Skills)

---

## Overview

OpenClaw (formerly ClawdBot, Moltbot) is a personal AI assistant platform. "The AI that actually does things." Inbox management, email sending, calendar control, flight check-in—all from WhatsApp, Telegram, Slack, Discord, or any chat app.

**Key Components:**
- **Gateway**: WebSocket control plane (port 18789), HTTP APIs, OpenAI Chat Completions proxy
- **Channels**: WhatsApp (Baileys), Telegram (grammY), Slack, Discord, Signal, iMessage, WebChat, etc.
- **Pi Agent**: RPC-mode coding agent from badlogic/pi-mono
- **Skills**: AgentSkills-compatible SKILL.md folders via ClawHub (565+ skills)

---

## Security Status (February 2026)

A comprehensive vulnerability scan was performed on 2026-02-06. See [SECURITY_VULN_SCAN_2026_02.md](./SECURITY_VULN_SCAN_2026_02.md) for full findings. Mitigation plan: `openclaw/docs/security/mitigation-plan-2026-02.md` in the OpenClaw repo.

| Severity | Count | Key Issues |
|----------|-------|------------|
| HIGH | 3 | Default skip-permissions, auth bypass flags, no rate limiting |
| MEDIUM | 6 | Static tokens, unauthed Chrome ext, path traversal, JSON DoS |
| LOW | 2 | Env blocklist gaps, no CSRF |

**Immediate Actions (P0):**
1. Remove `--dangerously-skip-permissions` from default CLI backend
2. Add rate limiting on gateway authentication
3. Harden `dangerouslyDisableDeviceAuth` / `allowInsecureAuth` (require env override)

---

## Integration with MCP Ecosystem

- OpenClaw is **not** an MCP server; it is a gateway/orchestration platform
- Can integrate with MCP servers via tools (e.g., web_fetch, custom tool plugins)
- Moltbot ecosystem (Clawd, Moltbook) uses OpenClaw as the control plane
- Advanced Memory MCP content includes [OpenClaw ADN notes](../../../advanced-memory-mcp/content/moltbot-ecosystem/)

---

## Documentation Links

- **Deep Analysis:** [DEEP_ANALYSIS.md](./DEEP_ANALYSIS.md) — Functionality, vulns, breach, FOSS competition, ecosystem
- **Dark Twin Honeytrap:** [docs/safety/dark-twin-honeytrap-pattern.md](../safety/dark-twin-honeytrap-pattern.md) — Safe/test install pattern for prompt injection detection
- **OpenClaw Docs:** https://docs.openclaw.ai
- **Security:** [Gateway Security](https://docs.openclaw.ai/gateway/security)
- **Vulnerability Scan:** [OpenClaw repo](/security/vulnerability-scan-2026-02/)
- **Mitigation Plan:** [OpenClaw repo](/security/mitigation-plan-2026-02/)
