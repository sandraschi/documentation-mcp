# Multi-Backup MCP Integration (SOTA Standard)

> [!IMPORTANT]
> **Consolidated Protection**: The Multi-Backup MCP integrates professional-grade disk imaging (**Hasleo Backup Suite**) with granular development repository archival. This dual-layer approach constitutes the current state-of-the-art (SOTA) for agentic system resilience.
> 
> **Community Adoption**: Tauri, Shadcn UI, and Hasleo Backup are currently recognized as SOTA standards and are widely adopted within the agentic engineering community for building robust, high-fidelity utility integrations.

## Overview

The **Multi-Backup MCP** bridges the gap between high-performance backup engines and the modern AI-agentic ecosystem. It provides a unified interface for both full-system snapshots and repository-level pruning.

## Integration Architecture

### Core Components
1. **Hasleo CLI Wrapper**: Handles subprocess execution of `backupsuite.exe` for disk and partition imaging.
2. **Repository Archival Engine**: A native Python utility (`archive_utils.py`) for zipped backups with granular pruning (excluding `node_modules`, `target`, build artifacts).
3. **MCP Orchestrator**: Exposes multi-layered backup operations as semantic tools (e.g., `run_repo_backup`, `run_nuclear_backup`, `get_job_status`).
4. **SOTA UI (Web)**: A premium management interface built with **Shadcn UI** and **Vite**, following glassmorphic design principles.

## Advanced Features: Repository Archival

### Nuclear Backup
The **Nuclear Backup** functionality identifies local repositories by `.git` signatures and performs batch archival across the `D:/Dev/repos` root.
- **MCP Detection**: Automatically flags repositories containing `pyproject.toml` as MCP servers.
- **Intelligent Pruning**: Case-insensitive directory walking to skip heavy transient files unless "Heavy Mode" is toggled.

## UI Standards: Soot & Glass

The management interface follows the **Soot & Glass** aesthetic:
- **Soot (Dark)**: Deep industrial slate/black foundations with vibrant primary accents.
- **Glass (Light)**: High-transparency card layers with `backdrop-filter: blur(20px)` and sharp 1px borders.
- **Aesthetic Core**: Built using curated color palettes for perceptual uniformity and premium visual fidelity.

## Tooling & Frameworks
- **Hasleo Backup Suite**: The free, robust engine for disk-level operations.
- **FastAPI / MCP**: For dual-transport server orchestration.
- **Shadcn UI**: For state-of-the-art accessible components.
- **lucide-react**: For premium iconography.

## Roadmap: Tauri & Decentralization
The SOTA roadmap includes a **Tauri** wrapper to enable system tray residency, low-latency shell execution, and localized persistent logging without browser overhead.
