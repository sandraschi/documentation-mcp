# Windows Operations MCP -- Project Status

**Last Updated**: 2026-04-16
**Repo**: `D:\Dev\repos\windows-operations-mcp` | [GitHub](https://github.com/sandraschi/windows-operations-mcp)
**Version**: 14.2.0 (runtime `__version__`; FastMCP 3.2)
**Python**: 3.12+ | **Build**: uv / hatchling / MCPB
**Status**: Production ready (SOTA 2026)

---

## What It Is

A comprehensive system operations server for Windows. Implements the **Portmanteau Pattern** to surgically manage OS-level entities like services, event logs, and performance counters.

**Distinction**: Fully compliant with 2026 SOTA standards (FastMCP 3.2), using MCPB workflow for zero-friction distribution via `.mcpb` bundles.

---

## Architecture

Consolidates many Windows operations into **portmanteau** tools (registry, network, environment, apps, services, event logs, performance, accounts, permissions, automation, archives, JSON, commands, file ops, etc.):
- **Services**: `list_windows_services`, `start`, `stop`, `restart`.
- **Logs**: `query_windows_event_log`, `export`, `clear`, `monitor`.
- **Performance**: `get_performance_counters`, `monitor_performance`.
- **Permissions**: `get_file_permissions`, `set`, `analyze`.
- **Execution**: `run_powershell_tool`, `run_cmd_tool`.
- **Packages**: Automated `.mcpb` packaging scripts for distribution.

---

## Current State

| Feature | Status | Notes |
|---------|--------|-------|
| PowerShell Bridge | Working | Reliable execution with error capture |
| Service Manager | Working | Real-time service state control |
| Event Log Query | Working | High-performance WMI/COM integration |
| MCPB Packaging | Working | Official v1.18.1 bundle compliance |
| Test Suite | Working | 160+ industrial-grade tests |

---

## Port Allocation

| Service | Port | Status |
|---------|------|--------|
| Backend | 10748 | Reserved |
| Frontend | 10749 | Reserved |

