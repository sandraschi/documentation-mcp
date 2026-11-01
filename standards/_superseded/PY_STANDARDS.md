---
title: "Python Launcher (py) Standards (SOTA 2026)"
category: standards
status: active
audience: mcp-dev
last_updated: 2026-04-20
---

# Python Launcher (`py`) Standards

**Version**: 1.0  
**Status**: MANDATORY  
**Substrate**: Windows (Antigravity Fleet)

## 1. Overview
The Python Launcher for Windows (`py`) is the canonical entry point for all direct Python-based orchestration and server maintenance tasks within the Antigravity fleet.

## 2. Canonical Configuration
- **Absolute Path**: `C:\Windows\py.exe`
- **Installation**: Included with Python distributions on Windows.

## 3. Version Targeting
Always use the specific version flag to ensure compatibility with the fleet's SOTA 2026 stack (Python 3.13+):
- **Command**: `py -3.13 script.py`
- **MCP Verification**: `py -m package.mcp`

## 4. Rationale: Why `py`?
1. **Multi-version Safety**: Avoids the "First Python on PATH" ambiguity.
2. **Environment Discovery**: Automatically respects `#!` shebangs and `.python-version` files.
3. **Execution Reliable**: Unlike global `python.exe` which can be aliased to the Windows Store shim, `C:\Windows\py.exe` is a high-fidelity binary.

---
👉 [PowerShell SOTA](./rules/powershell-script-standards.md) | [uv Standards](./UV_STANDARDS.md)
