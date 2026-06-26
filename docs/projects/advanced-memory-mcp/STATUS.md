# Advanced Memory MCP (MemOps) -- Project Status

**Last Updated**: 2026-04-27
**Repo**: `D:\Dev\repos\advanced-memory-mcp` | [GitHub](https://github.com/sandraschi/advanced-memory-mcp)
**Version**: v1.9.0 (Industrial Portmanteau Standard)
**Python**: 3.12+ | **Node**: 18+ | **Build**: FastMCP / MCPB
**Status**: 💎 GOLD STANDARD (SOTA v14.2.0)

---

## What It Is

The flagship research-driven knowledge platform of the MCP ecosystem, colloquially known as **MemOps**. Optimized for **SOTA v14.1.0 (March 2026)**, it features a complete modular documentation suite and is anchored by **Benny (GSD)** for social/emotional grounding.

**Core Mission**: To provide a professional-grade, materialist knowledge substrate that bridges the gap between raw data and agentic intelligence.

---

## Architecture & Ecosystem

A massive, composite architecture designed for scalability and high-fidelity reasoning:
- **FastMCP 3.2 Core**: Native async orchestration with tool sampling and shadow unrolling.
- **RAG Engine**: LanceDB + FastEmbed (`BAAI/bge-small-en-v1.5`) for semantic vector search and hybrid retrieval.
- **Multi-Source Research**: Integrated trawlers for GitHub (code), arXiv (science), TV Tropes (narrative patterns), and the open web.
- **Zettelkasten System**: Bidirectional sync between SQLite and Markdown files with support for permanent notes and knowledge graphs.
- **Unified Skill Hub**: Automated discovery and management of Claude Skills across Cursor, Windsurf, and Antigravity.
- **Industrial Documentation**: Modular `docs/` suite covering Architecture, Usage, Fleet, and Compliance.
- **Social Anchor**: **Benny (GSD)** integrated as the manual override adjudicator for security and stability.
- **Standalone Web UI**: Premium React dashboard on port **10704** with real-time knowledge visualization.

---

## Technical Capabilities

| Feature Category | Implementation Status | Technical Component |
|------------------|-----------------------|---------------------|
| **Knowledge Graph** | 🟢 PRODUCTION | SQLAlchemy + SQLite + Whoosh/FTS5 Hybrid |
| **Document Ingest** | 🟢 PRODUCTION | PDF/EPUB processing via PyMuPDF/Pandoc |
| **Multi-IDE Skills** | 🟢 PRODUCTION | Automated cross-IDE discovery system |
| **Observability** | 🟢 PRODUCTION | Grafana + Prometheus + Loki Integration |
| **Semantic Search** | 🟢 PRODUCTION | LanceDB + FastEmbed RAG Implementation |
| **Voice Interfaces** | 🟢 PRODUCTION | GPU-accelerated STT/TTS (int8/float16) |
| **Industrial Testing** | 🟢 PRODUCTION | Prefab-based deterministic rehydration |
| **Arcade Compliance** | 🟢 PRODUCTION | Shadow Unrolling (Static Scanner Path) |
| **Industrial Portmanteau** | 🟢 PRODUCTION | Rationale-First + Discriminated Unions |

---

## SOTA 2026 Compliance

- **Distribution**: Fully packaged via `@anthropic-ai/mcpb` for one-click deployment.
- **Observability**: Real-time telemetry and structured logging (Loguru).
- **Security**: Aggressive Ruff linting and security scanning (Bandit/Safety).
- **Concurrency**: Asyncio/CTranslate2 for multi-threaded inference and I/O.

---

## Port Allocation

| Service | Port | Status |
|---------|------|--------|
| Webapp UI | 10704 | SOTA Standard (Static) |
| Bridge API | 10705 | SOTA Standard |
| Startup Svc | 8003 | Orchestrator |
| Metrics | 9090 | Prometheus Standard |

---

## MemOps Webapp (Port 10704)
The front-end interface for the MemOps ecosystem, providing a high-performance React dashboard for knowledge management.

- **Knowledge Graph**: Interactive visualization of Zettelkasten nodes.
- **Research Logs**: Persistent history of autonomous research missions.
- **Voice Workspace**: Integrated Kokoro/Whisper controls for auditory interaction.
- **Flash Attention Monitoring**: Real-time metrics for RTX 4090 Reranker performance.
