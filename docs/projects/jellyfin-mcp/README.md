# jellyfin-mcp — Project Overview

**Status:** Pre-Implementation | **Language:** Python 3.12+ | **Framework:** FastMCP 3.2+

---

## What

jellyfin-mcp is a FastMCP 3.2+ server + React webapp for Jellyfin Media Server. It fills the #1 priority gap in the fleet's media server tooling — a fully open-source, plugin-capable MCP server that exceeds Plex-mcp in every technical dimension: real-time WebSocket events, hardware transcoding (free), plugin management, Live TV, and complete air-gap capability.

## Why

Plex-mcp works, but Plex is a "weird hybrid" — 90%+ of users run it as private movie depots while Plex Inc. wraps it in commercial streaming content as a legal figleaf. The SCOTUS Cox ruling (2025) made this figleaf unnecessary: the Betamax doctrine protects tools with substantial non-infringing use regardless of whether they also host commercial content. Jellyfin is the pure expression of this doctrine — zero commercial content, zero telemetry, zero cloud dependency.

Jellyfin also beats Plex technically: free hardware transcoding, 100+ plugins (Plex deprecated theirs), real-time WebSocket API, full OpenAPI/Swagger docs, and fully local auth with no cloud account required.

## Fleet Context

| Document | Path |
|----------|------|
| Wrappee priority #1 | `docs-private/WRAPPEE_CANDIDATES_ANALYSIS.md` (5-star, "MUST-HAVE") |
| Connector taxonomy (backup) | `projects/robofang/connector_taxonomy.md.backup` (PLANNED status) |
| Plex-mcp reference | `projects/plexmcp/` (reference architecture) |

## Key Documents

| Document | Description |
|----------|-------------|
| [PRD.md](./PRD.md) | Product requirements: 22-tool surface, webapp pages, Jellyfin++ features, Plex comparison, politicolegal analysis |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System design: component breakdown, data flow, service layer, WebSocket bridge, comparison with plex-mcp |
| [Integrations Guide](../integrations/jellyfin-mcp.md) | User setup guide: API key, env vars, Claude Desktop config, webapp quickstart |

## Quick Comparison: plex-mcp vs jellyfin-mcp

| Aspect | plex-mcp (existing) | jellyfin-mcp (planned) |
|--------|---------------------|------------------------|
| Tools | 20 portmanteau | **22 portmanteau** |
| Real-time | None (polling) | **WebSocket event bus** |
| Plugins | N/A (Plex deprecated) | **First-class plugin management** |
| Live TV | N/A | **EPG grid + DVR management** |
| Hardware transcode | Plex Pass gated | **Free, GPU dashboard** |
| Auth | Cloud token (plex.tv) | **Local API key (air-gappable)** |
| API docs | Partial, manual | **Full OpenAPI/Swagger auto** |
| Ports | 10740/10741 | **10934/10935** |

## Timeline

| Phase | Content | Target |
|-------|---------|--------|
| 1 | Core MCP server (5 tools, STDIO) | Week 1 |
| 2 | Advanced tools (12 tools, WebSocket bridge) | Week 2 |
| 3 | Webapp (FastAPI + Next.js, 13 pages) | Week 3 |
| 4 | Polish (E2E tests, Tauri native, plugin catalog) | Week 4 |

---

*Last updated: 2026-05-21*
