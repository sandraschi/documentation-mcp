# ⚓ Fleet Minesweeper (mcp-test-suite)

[![Python Version](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Tests - Pytest](https://img.shields.io/badge/Tests-Pytest-green?style=flat-square&logo=pytest&logoColor=white)](https://docs.pytest.org)
[![Linter - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

**Fleet minesweeper** — contract smoke tests and health auditing for the Sandra-class MCP task force under the P5 trust layer.

---

## 🚀 Overview

`mcp-test-suite` is the automated quality assurance scanner and validator for our fleet of Model Context Protocol (MCP) servers. It detects configuration anomalies, active port collisions, and missing launch scripts before deployments happen, ensuring agent capabilities remain robust and reliable.

---

## ⚡ Quick Start

```powershell
Set-Location D:\Dev\repos\mcp-test-suite
uv sync
uv run pytest -v
uv run fleet-smoke
```

## 🔍 Validation Tiers

| Tier | Check | Description |
|------|-------|-------------|
| **T0 (Registry)** | Golden Entry | Asserts server exists in `fleet-registry.json` |
| **T0 (Disk)** | Repo Presence | Verifies repository exists on disk at `repo_path` |
| **T0 (Files)** | Launch Ready | Checks for the presence of `pyproject.toml` and `start.ps1` |
| **T0 (Version)** | FastMCP Compatibility | Ensures the FastMCP dependency version is `>= 3.1.0` |
| **T0 (Global)** | Port Collision | Scans all active registry servers to ensure no port is double-assigned |
| **T1 (Probe)** | HTTP Health | Probes `http://127.0.0.1:{port}/health` (if port > 0) to assert `2xx` response |

## ⚙️ Configuration

| Env Var | Default | Description |
|---------|---------|-------------|
| `FLEET_OPS_ROOT` | `D:\Dev\repos\mcp-central-docs\operations` | Location of operations metadata |
| `FLEET_SMOKE_PROBE` | `1` | Set to `0` to skip live HTTP port probes |

## 🛡️ Golden Servers

Defined in [golden.py](file:///d:/Dev/repos/mcp-test-suite/src/mcp_test_suite/golden.py). The suite automatically audits these core fleet services.

## 🔗 Related

- [P5 Specification (Trust Layer)](file:///D:/Dev/repos/mcp-central-docs/operations/planning/specs/P5-fleet-trust-layer.md)
- `sync-fleet-registry.ps1` in `mcp-central-docs`
