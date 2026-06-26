# LiveKit Documentation Hub

**Date:** 2026-04-06 (v2.0.0 Teams++)
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

- **[LIVEKIT_2_0_TEAMS_UPGRADE.md](LIVEKIT_2_0_TEAMS_UPGRADE.md)** - Upgrade guide for v2.0.0 (April 2026)
  - FastMCP 3.2+ async tool patterns
  - monorepo substrate split (Remoting/Conferencing)
  - uv dependency orchestration

- **[MCP_INTEGRATION.md](MCP_INTEGRATION.md)** - MCP server patterns for LiveKit projects
  - Recommended tools (get_dev_stats, livekit_room_list, etc.)
  - LiveKit HTTP API usage
  - FastMCP Python alternative
  - Cursor/Claude configuration

### Reference Implementation

- **myconf (Teams++)** - `d:/Dev/repos/myconf`
  - uv monorepo: Next.js UI + Python LiveKit agent + Remoting/Conferencing MCPs
  - Voice pipeline agent with Ollama (Gemma 3), Whisper, Piper, Silero
  - Native Input Injection (Remoting) and Meeting Intelligence (Conferencing)
  - **Completed (v2.0.0):** Teams++ architectural hardening and FastMCP 3.2+ sync
  - **Extensive project docs:** [docs/projects/myconf/](../../docs/projects/myconf/) (PRD, STATUS, STRUCTURE, ARCHITECTURE, INTEGRATION_GUIDE)

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
2. **Reference myconf**: Clone and run the reference implementation
3. **Configure MCP**: Add LiveKit-aware tools to your MCP server
4. **Deploy**: Use Docker Compose for full stack

---

**Status:** Active
**Last Updated:** 2025-01-28
**Related:** [TURBOREPO_MCP_MONOREPO_PATTERN.md](../../docs/patterns/TURBOREPO_MCP_MONOREPO_PATTERN.md)
