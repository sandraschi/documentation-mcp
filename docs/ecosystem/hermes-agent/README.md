# Hermes Agent (NousResearch) — Ecosystem Notes

**Status:** No dedicated fleet write-up existed before this note (2026-08-29). Prior coverage was scattered — see "Existing scattered mentions" below. This consolidates a spike-planning session; nothing here has been installed yet.

> [!WARNING]
> **Name collision risk.** `operations/fleet-registry.json` already reserves the id `hermes-agent` (port 10972) for a **"Hermes WebUI (fleet conductor agent dashboard)"** at repo path `D:/Dev/repos/hermes-agent` — this repo **does not exist on disk**. It is unclear whether that registry entry refers to NousResearch's Hermes Agent (this doc) or an unrelated, unbuilt internal dashboard that happens to share the name. Resolve this before building anything under the `hermes-agent` name, or you'll get a fleet-registry collision the same way `agy-mcp` / `agy-fleet-mcp` did (see `ecosystem/antigravity/README.md`).

## What it is

Open-source, self-improving autonomous agent from Nous Research (MIT, github.com/NousResearch/hermes-agent). Not the Nous Hermes LLM line — same maker, different product. Architecture: SOUL.md (identity), MEMORY.md/USER.md (bounded persistent memory, ~2200/1375 char caps with auto-consolidation), autonomous skill creation and self-patching, crons, multi-channel gateway (Discord/Telegram/Slack/WhatsApp), `hermes mcp serve` (stdio; streamable HTTP is client-side only in the current release), and a **profiles** system for hard isolation between agent instances.

## Fleet relevance assessment (from this session)

Evaluated as a possible complement to Fritz (`fleet-agent-mcp`), **not a replacement**. Fritz is built around mechanical gates and a hard surveilability requirement (agent comms must be readable via visible channels — this was written in after unauthorized ad-hoc agent comms became a real problem). Hermes's core feature is autonomous self-modification — structurally the same pattern Fritz's design guards against. Verdict: worth running as a caged, isolated satellite for skill-mining and bounded research tasks; not worth merging into the fleet control plane.

## Existing scattered mentions (pre-dating this doc)

- `integrations/deepseek/awesome-deepseek-agent-overview.md`, item #13 — one-paragraph catalog entry, rated "Medium-High" fleet interest, notes the DeepSeek provider setup path (`hermes setup` → DeepSeek → `deepseek-v4-pro`)
- `integrations/deepseek/patterns-application-map.md` — cites Hermes's self-improving-loop pattern ("agent that writes its own tools")
- `integrations/agentmemory.md` — Hermes listed among agents that can share a memory server via MCP (Claude Code, Cursor, Gemini CLI, OpenCode, OpenClaw, Hermes, OpenManus)
- `integrations/unsloth/README.md` / `TECHNICAL.md` / `WORKFLOWS.md` — `unsloth start hermes` listed as a bridging/local-model-as-engine target

None of these constitute an install/config plan — they're catalog mentions, not operational docs. This file fills that gap.

## Install (Windows native, Goliath)

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```
Installs to `%LOCALAPPDATA%\hermes`. Pulls Python 3.11, Node 22, ripgrep, ffmpeg, portable Git Bash. Antivirus false-positive on `uv.exe` is known — whitelist, don't disable AV. Some release notes still flag native Windows as early-beta depending on version; WSL2 + Linux installer is the fallback if native misbehaves.

## Isolation plan (non-negotiable if built)

1. Dedicated profile (e.g. `hermes-sat`) — `hermes profile create hermes-sat` — own memory/SOUL/`.env`, no sharing with any other profile.
2. Own Discord bot application + own channel category (or separate guild), permission-scoped so it cannot see `#sfb-*` — enforced at the Discord permission level, not just `config.yaml`.
3. `allow_bots: none` confirmed (Hermes default) — no bot-to-bot crosstalk with Fritz's Discord presence.
4. No `hermes mcp serve` exposure to Fritz's control-plane tools at this stage.

## Local model backend

Requires tool-calling model, ≥64K context (Ollama defaults to 4096 — must be raised explicitly or tool calls silently degrade after 3-4 turns). Candidate: Qwen3.6-35B-A3B (Q4_K_M), already running on the 4090 for the OpenCode local-backend effort (see `ecosystem/opencode/local-backend-status.md`) — one tool-calling validation pass should cover both use cases rather than testing twice.

```powershell
hermes config set provider.base_url "http://localhost:11434/v1"
hermes config set provider.model "qwen3.6:35b-a3b"
```

## Discord setup sketch

```powershell
hermes gateway setup
hermes chat -q "reply with discord-provider-ok"
hermes gateway restart
hermes gateway status
```
`.env`: `DISCORD_BOT_TOKEN`, `DISCORD_ALLOWED_USERS`. `config.yaml`: `discord.allowed_channels` scoped to the new category, `allow_bots: none`, `allow_mentions.everyone/roles: false`.

## Acceptance test before any unattended run

Verify configured context length, run one observable tool-call task on the local model, compare against a known-good hosted route. Documented as the single most common local-setup failure — a model claiming a big context window but silently dropping tool calls after a few turns.

## Status — what's actually done

- Install: not run
- Profile: not created
- Discord bot/channels: not created
- Model backend config: not set
- Fleet-registry name collision: **not resolved**

Next session should either resolve the `hermes-agent` naming collision above or proceed with a different profile/repo name to sidestep it entirely.
