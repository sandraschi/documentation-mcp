# OpenClaw Alternatives - Sandbox & Supply-Chain Analysis

**Date noted:** 2026-09-26
**Sources:** GitHub live (openakita/openakita, HKUDS/nanobot, nanocoai/nanoclaw, elev8tion/zeroclaw), README fetch 2026-09-26
**Related:** openclaw, fleet-agent-mcp, security, MCP
**Original claim doc:** user-provided "alternatives to meta muse agent and openclaw" breakdown (PRC turnkey / minimal / isolation)

## TL;DR

* OpenClaw critique holds: ~500k LOC, 53 config files, 70+ deps (per nanoclaw README), single Node process, app-level allowlists only.
* `HKUDS/nanobot` (48,584 stars) is the most maintained alternative. `nanocoai/nanoclaw` (30,846 stars) is the strongest isolation story. `openakita/openakita` (1,992 stars) is best for Feishu/WeCom/DingTalk + DeepSeek/Qwen.
* Corrections: NanoClaw owner is `nanocoai`, not `gavrielc/nanoclaw` (does not exist). Nanobot is no longer 4k LOC. ZeroClaw canonical is tiny (24 stars) and fragmented.
* AutoGLM is a CUA/phone operator, not a drop-in OpenClaw replacement.

## 1. OpenAkita (openakita/openakita)

**Meta:** Python 3.11+, AGPL-3.0-only, 1,992 stars / 279 forks, updated 2026-09-25. Site openakita.ai, Desktop + pip + source.

**Why it beats OpenClaw:** GUI onboarding (5 min, zero CLI), QR scan-to-bind 30s for WeChat/Feishu/WeCom/DingTalk/QQ/OneBot/Telegram, 30+ LLM providers with failover (DeepSeek/Qwen/Kimi/MiniMax), 89+ tools, org orchestration (CEO/CTO roles, blackboard, deadlock detection), MCP client (stdio/HTTP/SSE).

**Verified 6-layer sandbox (from README):**

```
L1 Path Zoning        workspace / controlled / protected / forbidden
L2 Confirmation Gate  delete files, system commands require approval
L3 Command Intercept  regedit, format, rm -rf blocked outright
L4 File Snapshots     auto-checkpoint before writes, rollback
L5 Self-Protection    data/, src/, identity/ locked
L6 OS-Level Sandbox   Linux bwrap / macOS seatbelt / Windows MIC (HIGH-risk shell only)
```

Plus: `POLICIES.yaml` policy engine, resource budgets (token/cost/duration/iterations), runtime supervision (thrashing/loop detection), local-only memory/config, 3-tier plugin perms (Basic auto / Advanced confirm-on-install / System per-permission e.g. shell).

**Audit checklist:** default zone for new workspace? Is L6 default-deny or HIGH-only? Who classifies HIGH? Check POLICIES.yaml blocklist, mount scope for bwrap, snapshot retention.

**Caution:** QR relay path, update channel, AGPL obligations if forked into fleet.

## 2. Nanobot (HKUDS/nanobot)

**Meta:** Python, 48,584 stars / 8,582 forks, updated 2026-09-26. Largest claw-fork.

**Capabilities:** WebUI + terminal + chat apps (Telegram/Discord/Slack/WeChat/Email/Mattermost/Linear/Feishu), tools (files/shell/web/MCP/cron/image/subagents), Dream long-term memory, scheduled automations, Python SDK + OpenAI-compatible API, gateway mode (`nanobot gateway --background`).

**Security model (verified, no OS sandbox by default):**

* Workspace chooser + access mode in composer before project work
* First-run WebUI binds 127.0.0.1:8765 localhost-only, not LAN
* Local WebSocket channel enabled only after confirmation
* Apps catalog for MCP servers, `@` attach per-conversation, skills as reusable instructions
* Docker / Compose / systemd / LaunchAgent for deployment (opt-in isolation)
* Config docs cover providers, web search, MCP, runtime behavior

**Verdict:** Best auditable MCP-native base, but isolation = workspace scoping + localhost default + optional Docker. Do not assume container boundary unless you deploy it that way.

## 3. NanoClaw (nanocoai/nanoclaw) - CORRECTED OWNER

**Meta:** TypeScript/Bun + Node host, 30,846 stars / 12,818 forks. Requires macOS/Linux/WSL2 + Node22 + pnpm10 + Docker + Claude Code. License check README before fleet use.

**Philosophy:** small enough to understand (one process + handful files), bespoke fork per user, customization = code changes, skills over features (channels/providers on `channels`/`providers` branches, `/add-telegram` etc copies only needed modules).

**Verified isolation (strongest of the three):**

* Per-agent-group Linux containers (Docker default, macOS/Linux/WSL2). Only explicitly mounted dirs visible.
* Flow: apps -> host router -> inbound.db -> container (Bun + Claude Agent SDK) -> outbound.db -> host delivery -> apps. Two SQLite files per session, single writer each, no shared memory.
* Per-group `CLAUDE.md`, memory, container, mounts. See `docs/isolation-model.md` (3-level), `docs/architecture.md`.
* Credential gateway: agents never hold raw keys. Outbound via OneCLI Agent Vault proxy with per-agent policies/rate limits.
* Multi-channel: WhatsApp/Telegram/Discord/Slack/Teams/iMessage/Matrix/GChat/Webex/Linear/GitHub/WeChat/email via Resend. Flexible isolation per channel.
* Scheduled tasks with script gates, agent templates (`ncl groups create --template`).

**Audit checklist:** list actual `-v/--mount` per group, confirm no `$HOME` full mount for convenience, confirm gateway policy file, review `src/container-runner.ts` + `container/agent-runner/`.

## 4. ZeroClaw (Rust)

**Meta:** Fragmented. `elev8tion/zeroclaw` 24 stars (2026-07-20). `Natfii/ZeroClaw-Android` 307 stars most active. Others: librefang (380), rayclaw (56), microclaw (740, Rust, nanoclaw-inspired).

**Claim:** single binary, no Node/Python venv, 15-30MB idle. Plausible for Rust but unverified here, and low adoption = no mass review, drift risk.

**Verdict:** Own-your-fork only. Consider microclaw/librefang if Rust is hard requirement, else prefer Nanobot/NanoClaw.

## 5. AutoGLM / GLM-Agent (Zhipu)

Phone/CUA GUI automation (visual grounding -> structured actions), GLM-4V optimized, single-script setup. Not a replacement for memory + chat hooks + cron + skills. Use alongside, not instead of. Locks to Zhipu weights.

## Comparison matrix

|  | OpenAkita | Nanobot | NanoClaw (nanocoai) | ZeroClaw |
|---|---|---|---|---|
| Lang | Python | Python | TS/Bun + Node host | Rust |
| Stars | 1,992 | 48,584 | 30,846 | 24 (canonical) |
| Channels CN | WeChat/Feishu/WeCom/DingTalk/QQ best | Feishu/WeChat + western | WeChat + western broad | varies |
| Models | 30+ incl DeepSeek/Qwen | OpenAI-compat + local | Claude SDK native, +Codex/OpenCode/Ollama | varies |
| Isolation | 6-layer, L6 bwrap/seatbelt/MIC HIGH-only | workspace + localhost + opt Docker | per-agent Docker, mount-scoped, cred gateway | binary, no runtime |
| Auditability | medium (89+ tools, org layer) | high (small core, readable) | high (small base, fork-per-user) | high but fragmented |
| Risk | QR relay, AGPL, HIGH classifier | over-mount, no default container | mount scope, Node host still TCB | maintainer bus factor |

## Recommendation for fleet

1. Lab/dev default: Nanobot. MCP-native, localhost-first, easiest to inspect.
2. Always-on chat gateway: nanocoai/nanoclaw in Docker, read-only mounts, gateway policy enforced. Verify `isolation-model.md` before prod.
3. CN chat + domestic weights: OpenAkita. Audit POLICIES.yaml + bwrap scope + egress first.
4. Rust daemon: only if you will own the fork; evaluate microclaw vs librefang.

## Next steps

1. Dump POLICIES.yaml + bwrap args from OpenAkita.
2. Dump default workspace/access-mode + Docker compose from Nanobot.
3. Dump container-runner mounts + isolation-model.md from NanoClaw.
4. Decide fleet pattern: gateway (NanoClaw) + lab (Nanobot) vs single stack.
