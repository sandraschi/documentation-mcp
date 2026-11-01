# LiveKit Documentation Hub

**Date:** 2026-09-06 (server v1.13.6, agents v1.8.0, client v2.22.2)
**Purpose:** Central documentation for LiveKit real-time communication and AI voice agent integration across MCP repositories

---

## Documentation Structure

This directory contains comprehensive LiveKit documentation for MCP projects:

### Core Documentation

- **[LIVEKIT_INTEGRATION_GUIDE.md](LIVEKIT_INTEGRATION_GUIDE.md)** - Complete integration guide
  - LiveKit architecture and components
  - WebRTC SFU infrastructure
  - AI Voice Agent patterns (VAD, STT, TTS, LLM)
  - MCP integration in LiveKit projects
  - Configuration, deployment, troubleshooting

- **[LIVEKIT_1_X_UPGRADE.md](LIVEKIT_1_X_UPGRADE.md)** - Upgrade guides (Agents 0.x -> 1.x, 1.5 -> 1.8; server 1.10 -> 1.13)
  - Unified `Agent`/`AgentSession` patterns, `LLMStream._run()`
  - TURN TTL enforcement, data tracks, Egress v2, `pID` -> `participantID`
  - FastMCP 3.2+ async tool patterns, monorepo substrate split (Remoting/Conferencing), uv orchestration

- **[MCP_INTEGRATION.md](MCP_INTEGRATION.md)** - MCP server patterns for LiveKit projects
  - Recommended tools (get_dev_stats, livekit_room_list, etc.)
  - LiveKit HTTP API usage
  - FastMCP Python alternative
  - Cursor/Claude configuration

### Reference Implementation

- **teleconference-mcp (Teams++)** - `D:\Dev\repos\teleconference-mcp`
  - uv monorepo: Next.js UI + Python LiveKit agent + Remoting/Conferencing MCPs
  - Voice pipeline agent with Ollama (Gemma 3), Whisper, Piper, Silero
  - Native Input Injection (Remoting) and Meeting Intelligence (Conferencing)
  - **Completed (v2.0.0):** Teams++ architectural hardening and FastMCP 3.2+ sync
  - **Extensive project docs:** [docs/projects/teleconference-mcp/](../../docs/projects/teleconference-mcp/) (PRD, STATUS, STRUCTURE, ARCHITECTURE, INTEGRATION_GUIDE)

---

## Purpose

This documentation hub serves as the central source of truth for:

- **LiveKit Infrastructure**: Server setup, room management, token generation
- **AI Voice Agents**: livekit-agents framework, pipeline architecture, plugin ecosystem
- **MCP Integration**: How to combine LiveKit conferencing with MCP tooling
- **Frontend Patterns**: LiveKit React components, room controls, device handling
- **Deployment**: Docker Compose, production considerations
- **Roadmap**: Full self-host calendaring & invitations (see integration guide)

---

## Quick Start

1. **Read Integration Guide**: Understand architecture and patterns
2. **Reference teleconference-mcp**: Clone and run the reference implementation
3. **Configure MCP**: Add LiveKit-aware tools to your MCP server
4. **Deploy**: Use the fleet Windows service `LiveKitSFU` (see below), or Docker Compose for non-Windows / dev machines

---

## Fleet deployment (Goliath)

> **2026-08-03: LiveKit now runs as a Windows service — not Docker.**

| Deployment | Command / status | Notes |
|-----------|------------------|-------|
| **Windows service (fleet)** | `Get-Service LiveKitSFU` | NSSM-wrapped native `livekit-server` 1.13.6 (upgraded 2026-09-06), config from `teleconference-mcp/livekit.yaml`, auto-start + crash-restart. Canonical on Goliath |
| Service logs | `Get-Content D:\Dev\repos\teleconference-mcp\logs\livekit.out.log -Tail 50` | Rotated by NSSM (`livekit.err.log` shows a benign Windows CPU-monitor notice) |
| Service reinstall/repair (elevated) | `powershell -File D:\Dev\repos\teleoperator-mcp\scripts\install-livekit-service.ps1` | UAC prompt |
| Docker alternative | `docker compose -f docker-compose.yaml up -d livekit` | Non-Windows / dev machines only |

**Consumers** (as of 2026-08): `teleoperator-mcp` (video return, port 15580, room `teleop-boomy`) and `teleconference-mcp` (conferencing stack). Key: `devkey`/`secret` in `livekit.yaml` must match consumer env vars.

**Status:** Active
**Last Updated:** 2026-09-06
**Related:** [TURBOREPO_MCP_MONOREPO_PATTERN.md](../../docs/patterns/TURBOREPO_MCP_MONOREPO_PATTERN.md)

---

## History

LiveKit began in 2021 as an open-source WebRTC SFU (Selective Forwarding Unit) founded by **Russ d'Sa (CEO)** and **David Zhao (CTO)** in San Francisco — "open infrastructure for the metaverse," i.e. a self-hostable alternative to Twilio/Agora for real-time audio/video. Early demand for a hosted version from companies such as Spotify, Oracle, and Reddit produced **LiveKit Cloud**. Shortly after ChatGPT launched, d'Sa demoed a LiveKit-powered voice interface, which led to a deal to run **ChatGPT's voice modes on LiveKit Cloud** — pivoting the project from conferencing plumbing to *the* infrastructure layer for voice AI. The stack grew accordingly: server SDKs, client SDKs, UI components, SIP/telephony, egress (recording), and the **Agents framework** (Python/Node.js workers that join rooms as participants). Funding: $7M seed (Redpoint, Dec 2021) + $8M (2022), $22M Series A (Altimeter, Jun 2024), $45M Series B (Altimeter, Apr 2025, $345M valuation), **$100M Series C (Index Ventures, Jan 2026, $1B valuation, $183M total raised)**. Backers/advisors include Jeff Dean, Elad Gil, Aravind Srinivas (Perplexity), Amjad Masad (Replit), Guillermo Rauch (Vercel), and Mati Staniszewski (ElevenLabs). Per the company: 300,000+ developers, `livekit/livekit` ~20.7k stars / 2.3k forks (Apache-2.0, Go), `livekit/agents` ~14k stars (Sep 2026).

---

## Who uses it (prominent products & repos)

| User | What runs on LiveKit |
|------|----------------------|
| **OpenAI ChatGPT voice modes** | Realtime voice conversation on LiveKit Cloud |
| **Apple FaceTime (iOS 18)** | LiveKit embedded for emergency calls |
| **France's Visio** | Government video-conferencing platform built on the OSS SFU |
| **Spotify / Oracle / Reddit / AT&T** | Early Cloud adopters (livestreaming, interactive audio) |
| **Salesforce, Meta** | Voice/video AI features (per company disclosures) |
| **911 emergency services (US)** | Real-time emergency-call media |
| **LiveKit Meet** (`livekit-examples/meet`, OSS) | Reference conferencing app — the template our `teleconference-mcp` web UI descends from |
| **Fleet (this repo)** | `teleconference-mcp` (AG-Visio conferencing + Visio voice agent) and `teleoperator-mcp` (robot video return, room `teleop-boomy`) on the `LiveKitSFU` service |

---

## Community

| Channel | Address |
|---------|---------|
| Docs (versioned, with `llms.txt`) | <https://docs.livekit.io> |
| GitHub org (server, agents, SDKs, components) | <https://github.com/livekit> |
| Community forum | <https://community.livekit.io> |
| Slack | <https://livekit.com/join-slack> |
| Blog (releases, architecture notes) | <https://livekit.io/blog> |
| YouTube (demos, talks) | <https://www.youtube.com/@livekit_io> |
| Coding-agent support (MCP) | <https://docs.livekit.io/mcp> |

---

## Bibliography

* LiveKit docs — <https://docs.livekit.io> (`/home`, `/agents`, `/deploy/*`, `/reference/*`); machine-readable `llms.txt` at <https://docs.livekit.io/llms.txt>
* `livekit/livekit` repo (Go SFU, Apache-2.0) — <https://github.com/livekit/livekit>; releases <https://github.com/livekit/livekit/releases>
* `livekit/agents` framework (Python/Node) — <https://github.com/livekit/agents>; releases <https://github.com/livekit/agents/releases>
* Client SDKs: `client-sdk-js`, `client-sdk-swift`, `client-sdk-android`, `client-sdk-flutter`; components: `components-js` (`@livekit/components-react`); server SDKs: `node-sdks`, `python-sdks`, `server-sdk-go`, `server-sdk-ruby` — all under <https://github.com/livekit>
* Wikipedia, "LiveKit" (history, funding, customers) — <https://en.wikipedia.org/wiki/LiveKit>
* Bass, D. (2026-01-22). "LiveKit, Seller of Voice Tools to OpenAI, Raises $100 Million." *Bloomberg* — <https://www.bloomberg.com/news/articles/2026-01-22/livekit-seller-of-voice-tools-to-openai-raises-100-million>
* Wiggers, K. (2025-04-10). "LiveKit's tools help power real-time communications." *TechCrunch* — <https://techcrunch.com/2025/04/10/livekits-tools-help-power-real-time-communications/>
* Shrivastava, R. (2024-06-04). "This $110 Million Startup Is Building A Nervous System For AI." *Forbes* — <https://www.forbes.com/sites/rashishrivastava/2024/06/04/this-110-million-startup-is-building-a-nervous-system-for-ai/>
* Bovenziner, N. (2026-02-11). "Inside the open source project powering France's video platform revolution." *The Stack* — <https://www.thestack.technology/inside-the-open-source-project-powering-frances-video-platform-revolution/>
* Makaryan, M. (2024-09-26). "5 Q's for Russell D'Sa." *Center for Data Innovation* — <https://datainnovation.org/2024/09/5-qs-for-russell-dsa-co-founder-and-ceo-of-livekit/>


