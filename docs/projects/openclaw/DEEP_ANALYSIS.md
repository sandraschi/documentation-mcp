# Moltbot/OpenClaw Deep Analysis

**Timestamp**: 2026-02-08
**Scope**: D:\Dev\repos\external\moltbot (cloned from moltbot/moltbot)
**Version**: 2026.2.6-4 (package name: openclaw)

---

## 1. Identity and Naming

| Name | Role |
|------|------|
| **moltbot** | GitHub org/repo (moltbot/moltbot) |
| **openclaw** | Primary product brand, package name, openclaw.ai |
| **ClawdBot** | Original name (trademark conflict with Anthropic Claude) |
| **Clawd** | Original agent name |
| **Molty** | Agent name post-rebrand |

The repository at `moltbot/moltbot` is the canonical source. Package `openclaw`, CLI `openclaw`, config `~/.openclaw`. Docs: docs.openclaw.ai, docs.molt.bot (legacy).

---

## 2. General Functionality

**Core**: Local-first personal AI assistant. Single Gateway (WebSocket :18789) as control plane. Connects to messaging channels (WhatsApp, Telegram, Slack, Discord, Signal, iMessage, Teams, Matrix, Zalo, WebChat). Pi agent (RPC) for tool execution. Data stays on user hardware.

**Channels**: 12+ (Baileys, grammY, Bolt, discord.js, signal-cli, BlueBubbles, etc.). Extensions for MS Teams, Matrix, Zalo, Nostr, Feishu, Line, Twitch, Nextcloud Talk, Tlon.

**Tools**: Browser (CDP), Canvas/A2UI, bash, cron, webhooks, Gmail Pub/Sub, sessions (agent-to-agent). Skills (ClawHub, 565+).

**Platforms**: macOS menu bar, iOS/Android nodes (alpha), Voice Wake, Talk Mode, Live Canvas.

**Architecture**: Gateway + Pi agent + channels + skills. Multi-agent routing, DM pairing, sandboxing (Docker per-session), tool allow/deny.

---

## 3. Strong Points

- **Local-first**: Orchestration on user hardware; LLM calls are the only external dependency.
- **Security model**: DM pairing by default, allowlists, mention gating, sandboxing, `openclaw security audit` tool.
- **Comprehensive docs**: Security index, threat model, incident response, credential map.
- **Fixes post-breach**: Auth for canvas host, skill/plugin scanner, token redaction, gateway URL validation, trusted proxies.
- **Maturity**: 150k+ stars, active Discord, ClawHub skills registry, formal verification docs.
- **Extensibility**: Plugin SDK, extensions, skills watcher.

---

## 4. Weak Points and Possible Vulnerabilities

### Confirmed (Patched)

- **CVE-2026-25253** (CVSS 8.8): Control UI trusted `gatewayURL` query param; token exfiltration; one-click RCE. Fixed 2026.1.29.
- **Bitdefender (Jan 27, 2026)**: Hundreds of exposed control panels. Localhost trust + reverse proxy misconfig. Config/API keys/conversation leaks, unauthenticated exec in some cases. Deployment misconfiguration, not code bug.

### Opus 4.6 Audit (2026-02)

- **HIGH**: Default `--dangerously-skip-permissions`, auth bypass flags, no rate limiting.
- **MEDIUM**: Static tokens, unauthed Chrome ext, path traversal, JSON DoS.
- **LOW**: Env blocklist gaps, no CSRF.

### Opus vs Latest Release (2026.2.6-4)

| Opus Finding | Status | Notes |
|--------------|--------|-------|
| Token in URL query params (CVE-2026-25253) | Fixed | #9436 (2026.2.3): reject hook tokens in query; Control UI uses fragment |
| Auth for canvas host | Fixed | #9518 (2026.2.6) |
| Credentials in config.get | Fixed | #9806, #9858 (2026.2.6): redaction |
| `--dangerously-skip-permissions` default | **Open** | Still in `cli-backends.ts` and test defaults |
| `dangerouslyDisableDeviceAuth` | **Open** | Still configurable; no env override required |
| Gateway auth rate limiting | **Open** | No per-IP rate limit on auth attempts |
| Static tokens, Chrome ext, path traversal, JSON DoS | **Open** | P1 items not addressed |

### Structural

- **Power concentration**: Agent has shell, files, browser. Sandbox/guardrails target LLM manipulation, not external attackers.
- **Dangerous flags**: `dangerouslyDisableDeviceAuth`, `allowInsecureAuth`—break-glass only but easy to enable.
- **Deployment fragility**: Defaults assume localhost; exposing via proxy without `trustedProxies` and auth is risky.

---

## 5. FOSS Competition

| Project | Focus | Relation |
|---------|-------|----------|
| **Hugging Face Agents** | Cloud/API-centric | Different model; OpenClaw is local-first |
| **Ollama + local LLMs** | Inference only | OpenClaw can use Ollama; adds channels + tools |
| **n8n / Zapier** | Automation | No agentic loop; OpenClaw has full agent |
| **Moltworker** | OpenClaw on Cloudflare Workers | Alternative hosting; same stack |
| **Voice assistants (MyCroft, etc.)** | Voice-first | Narrower; OpenClaw is multi-channel |

OpenClaw is distinct: local-first + multi-channel + agentic + tools. No direct FOSS equivalent at same scope.

---

## 6. Ecosystem Relationship

### Moltbook (moltbook.com)

"Front page of the agent internet." Social network for agents: posts, comments, upvotes, DMs, submolts. Human verification via tweet. Heartbeat pattern for agent presence. **Relationship**: Separate project; OpenClaw skill (`clawhub install moltbook`). Moltbook gives agents social identity.

### Molt.church / Molt.art

Community/experimental domains in the Molt ecosystem. Exact relationship unclear from codebase; likely community sites or side projects. Not in core OpenClaw repo.

### OpenClaw

Runtime. Moltbook = social layer. ClawHub = skills registry. Steipete (Peter Steinberger) = creator/maintainer.

---

## 7. Last Week's Breach and Fix

### Bitdefender (Jan 27, 2026)

- **What**: Hundreds of internet-facing control panels. Config, API keys, conversation history exposed. Some unauthenticated command execution.
- **Cause**: Localhost trust + reverse proxy misconfig. Proxied connections treated as local, auto-approved.
- **Fix**: Deployment guidance. Not a code patch. Users must configure `gateway.trustedProxies`, auth, avoid exposing UI/WS without protection.

### CVE-2026-25253 (Disclosed Feb 3, 2026)

- **What**: Control UI trusted `gatewayURL` from query string. Auto-connect sent token to attacker server. One-click RCE via malicious link.
- **Fix**: 2026.1.29. Validate gateway URL; reject untrusted origins.
- **Impact**: Even loopback-only gateways affected (browser initiates outbound connection).

### Post-Breach Hardening (Changelog 2026.2.x)

- Require auth for Gateway canvas host and A2UI assets.
- Stop exposing auth tokens via URL query params; reject hook tokens in query.
- Add skill/plugin code safety scanner; redact credentials from config.get.
- Add node command allowlists (default-deny unknown node commands).
- Add non-root sandbox user to Dockerfiles.

---

## 8. Assessment Summary

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Functionality | Strong | Broad channels, tools, multi-agent |
| Security model | Good | Pairing, sandboxing, audit tool |
| Default safety | Weak | Dangerous flags, deployment fragility |
| Post-breach response | Good | Patches, hardening, docs |
| FOSS position | Unique | No direct equivalent |
| Build now? | **No** | Run security assessment first |

**Recommendation**: Clone-only until Opus-assisted security assessment passes. Do not build before assessment.

---

## References

- [Bitdefender Moltbot alert](https://www.bitdefender.com/blog/hotforsecurity/moltbot-security-alert-exposed-clawdbot-control-panels-risk-credential-leaks-and-account-takeovers/)
- [The Hacker News CVE-2026-25253](https://thehackernews.com/2026/02/openclaw-bug-enables-one-click-remote.html)
- [OpenClaw Security](https://docs.openclaw.ai/gateway/security)
- [mcp-central-docs openclaw STATUS](STATUS.md)
- [SECURITY_VULN_SCAN_2026_02](SECURITY_VULN_SCAN_2026_02.md)
