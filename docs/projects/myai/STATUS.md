# myai - Status Report

**Last Updated:** 2025-11-25  
**Status:** Production-Ready  
**Source Repo:** `D:\Dev\repos\myai`

---

## Overview

Dual-mode AI microservices platform with FastAPI dashboard, MCP server (11 tools), and 10 AI applications orchestrated via Docker.

---

## Health Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Dashboard | âœ… Healthy | Port 3060 |
| MCP Server | âœ… Healthy | 11 tools, FastMCP 3.1.1++ |
| Docker Stack | âœ… Healthy | 18+ services |
| Monitoring | âœ… Healthy | Prometheus/Grafana/Loki |
| GPU Services | âš ï¸ Conditional | Requires CUDA |

---

## Key Features

- **FastAPI Dashboard (3060)** - Service lifecycle, health probes, MCP orchestration
- **MCP Server** - 11 operational tools with comprehensive docstrings
- **10 AI Microservices** - LLM chat, document RAG, image gen, voice, etc.
- **Full Infrastructure** - Traefik, Prometheus, Grafana, Loki, Portainer

---

## Service Matrix

| Service | Port | Status | Notes |
|---------|------|--------|-------|
| Dashboard | 3060 | âœ… | MCP server + REST API |
| Bob & Alice | 5188 | âœ… | Multi-persona LLM chat |
| Character Conversation | 5190 | âœ… | Role-based ensemble |
| Document Viewer | 5192 | âœ… | RAG + Weaviate |
| Future You | 5194 | âœ… | Future self simulator |
| StableDiff Gradio | 5196 | âœ… (GPU) | Image generation |
| Talking Avatar | 5198 | âœ… (GPU) | Voice + animation |
| Teams Debate | 5200/5201 | âœ… | Multi-agent debate |
| **Gemini Tools** | 5206/3501 | âœ… | **Google Gemini multimodal** |
| Plex Plus | 3001/3020 | âœ… | Media AI extensions |
| Calibre Plus | 9000/8000 | âœ… | Ebook AI extensions |

---

## ðŸ¤– Gemini Tools - November 2025 Update

The `gemini_tools` service can leverage **Gemini 3** (released November 18, 2025):

- **SOTA performance** - 95% on AIME 2025, 91.9% on GPQA Diamond
- **Advanced reasoning** - Better problem-solving capabilities
- **Multimodal** - Text, image, audio, video understanding
- **Coding** - 76.2% on SWE-Bench

See `docs/google-ecosystem/gemini/gemini-3/` for full documentation.

---

## Recent Changes

- **MCP Orphan Guard** - Prevents zombie MCP servers (`mcp_orphan_guard.py`)
- **Docker Build Scripts** - 18-90x faster incremental builds
- **Polling Manager** - Centralized polling pattern (originated in devices-mcp)

---

## Integration Points

- **MCP Central Docs** - OrphanGuard pattern documented in `docs/patterns/`
- **devices-mcp** - PollingManager pattern cross-pollinated
- **Claude Desktop** - MCP server via stdio
- **Google AI** - Gemini Tools service connects to Google AI APIs

---

## Infrastructure Stack

| Component | Purpose | Port |
|-----------|---------|------|
| Traefik | Reverse proxy, load balancer | 80/8080 |
| Prometheus | Metrics collection | 9091 |
| Grafana | Dashboards | 3100 |
| Loki | Log aggregation | 3199 |
| Portainer | Container management | 9000 |
| PostgreSQL | Database | 5432 |
| Weaviate | Vector DB | 8081 |

