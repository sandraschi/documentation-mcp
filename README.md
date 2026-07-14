# Documentation MCP

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://fastmcp.com"><img src="https://img.shields.io/badge/FastMCP-3.4-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>

Documentation server with semantic search, RAG, fleet registry, and a React dashboard.
Indexes `mcp-central-docs` and extra paths for cross-fleet document retrieval.

## Quick Start

```powershell
uv sync
cd web_sota && npm install && cd ..
./start.ps1
```

Opens at `http://localhost:11032` (frontend) with backend on port **11033**.

## Features

- **Semantic search** over indexed docs via LanceDB + FastEmbed (CPU/GPU)
- **RAG chat** with Ollama or OpenAI-compatible LLMs (auto-discovery)
- **Fleet registry** — discoverable apps catalog from `mcp-central-docs`
- **Persistence** — store/recall structured data across sessions (SQLite + LanceDB)
- **Tauri/NSIS desktop app** — embedded PyInstaller backend, single installer
- **MCPB bundle** — ready for Claude Desktop distribution
- **Zustand** state management, **Playwright** E2E tests, **pre-commit** hooks

## Ports

| Service | Port |
|---------|------|
| Frontend (Vite) | 11032 |
| Backend (FastAPI + MCP) | 11033 |

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastMCP 3.4.2, FastAPI, uvicorn, Starlette |
| Frontend | React 18, Vite 5, Tailwind 3, Radix, Zustand, Framer Motion |
| Vector DB | LanceDB + FastEmbed (CPU/GPU) |
| LLM | Ollama / OpenAI-compatible (auto-discovery) |
| Desktop | Tauri 2.0, NSIS installer, PyInstaller backend |
| CI | Ruff, Biome, tsc, pytest (GitHub Actions) |

## Session Context

The repo ships `.cursorrules` and `.claude-plugin/` for automatic tool-awareness prompt injection at session start — agents know about `search_docs`, `server_status`, and `reindex_docs` without being told.

## Repo Structure

```
src/docs_mcp/       Python backend (FastMCP server, RAG, API)
web_sota/           React frontend (Vite, Tailwind, Zustand)
native/             Tauri 2.0 desktop wrapper + NSIS build pipeline
mcpb/               MCPB bundle for Claude Desktop
scripts/            Fleet launcher, CUA-NSIS smoke test, MCPB pack
docs/               Documentation library (fleet standards)
```
