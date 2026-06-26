# Audiotool Nexus MCP (SOTA 14.1)

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://biomejs.dev"><img src="https://img.shields.io/badge/Linted_with-Biome-60a5fa?style=flat-square&logo=biome&logoColor=white" alt="Biome"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

![Audiotool Nexus Logo](file:///C:/Users/sandr/.gemini/antigravity/brain/97a950ab-822d-4106-b124-640a786adf30/nexus_logo_premium_1776123216232.png)

A high-performance **MCP Server** and **Industrial Dashboard** for the **[Audiotool NEXUS SDK](https://developer.audiotool.com)**. This node provides a bidirectional bridge between AI agents and the Audiotool modular DAW ecosystem.

---

## Quick Start

```powershell
git clone https://github.com/sandraschi/audiotool-nexus-mcp
cd audiotool-nexus-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:

## 📈 Dashboard Overview

The **Industrial Dashboard** provides real-time monitoring of project entities, device states, and connection health. It is designed for high-fidelity agentic orchestration.

- **Mixer View**: Real-time signal monitoring and channel strip oversight.
- **Sampler View**: Waveform visualization and parameter tracking.
- **Mastering View**: Spectral analysis and loudness monitoring.

> [!NOTE]
> The dashboard UI features decorative, "atmospheric" metering. For scientific audio measurement, always refer to the official Audiotool studio UI.

---

## 🛠️ Detailed Documentation

| Guide | Description |
| :--- | :--- |
| **[Installation & Setup](./docs/INSTALLATION.md)** | Step-by-step setup, `.env` config, and PAT authentication. |
| **[Architecture](./docs/ARCHITECTURE.md)** | Technical design, `NexusBridge` pattern, and quality stack. |
| **[Nexus Guide](./docs/NEXUS_GUIDE.md)** | Deep dive into the Audiotool ecosystem and SDK lifecycle. |
| **[Changelog](./CHANGELOG.md)** | Version history and SOTA 14.1 industrialization log. |

---

## 🚀 Quick Start (Production)

1.  **Deploy**: `npm install && npm run build`
2.  **Configure**: Set `AUDIOTOOL_PAT` in your `.env` or MCP environment.
3.  **Launch**: Port **10900** for the dashboard, **stdio** for the MCP server.

---

## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards:
- **Linting & Formatting**: [Biome](https://biomejs.dev/) (Rust-native, sub-millisecond execution).
- **Core Testing**: [Vitest](https://vitest.dev/) with comprehensive SDK mocking.
- **Task Orchestration**: [Justfile](./justfile) recipes for all fleet operations.
