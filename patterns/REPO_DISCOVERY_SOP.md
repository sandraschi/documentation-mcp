# REPO_DISCOVERY_SOP — Find Source Roots Reliably

**Established**: 2026-07-22
**Callers**: Any subagent or SOP that needs to find source files in a fleet repo.

## Problem

Two source layouts exist in the fleet:
- **Fleet standard**: `src/{package_name}/` (per AGENTS.md §6)
- **Legacy flat**: `{package_name}/` at repo root (pre-2026 convention)

A subagent checking only `src/` will report a flat-layout repo as "empty scaffold."

## Resolution Order

For any repo at `D:\Dev\repos\{repo}`:

```python
import os
from pathlib import Path

def find_package_root(repo_root: str, package_name: str = "") -> str | None:
    """Find the actual source root by trying all known layouts."""
    root = Path(repo_root)
    
    # 1. Fleet standard: src/{package_name}/
    candidates = list((root / "src").glob("*/")) if (root / "src").is_dir() else []
    if candidates:
        return str(candidates[0])
    
    # 2. Flat layout: {package_name}/ at root (name often matches repo minus -mcp)
    name = package_name or root.name.replace("-mcp", "").replace("-", "_")
    flat = root / name
    if flat.is_dir() and (flat / "__init__.py").exists():
        return str(flat)
    
    # 3. Try common package names
    for guess in [root.name.replace("-mcp", ""), root.name.replace("-", "_"),
                  root.name, f"{root.name.replace('-mcp', '').replace('-', '_')}_mcp"]:
        flat = root / guess
        if flat.is_dir() and (flat / "__init__.py").exists():
            return str(flat)
    
    # 4. Parse pyproject.toml for package find
    pip = root / "pyproject.toml"
    if pip.exists():
        import configparser
        # Check [tool.setuptools.packages.find]
        # Fallback: look for any directory with __init__.py at depth 1-2
        for path in root.iterdir():
            if path.is_dir() and not path.name.startswith((".", "_")) and path.name not in ("tests", "web_sota", "native", "scripts", "docs", "build"):
                init = path / "__init__.py"
                if init.exists():
                    return str(path)
    
    return None
```

## Also Check

Once you have the package root, look for:

| What | Where | Why |
|------|-------|-----|
| `pyproject.toml` | repo root | Dependencies, entry points, package name |
| `setup.py` or `setup.cfg` | repo root | Legacy package config |
| `server.py` | repo root | Some repos use root-level server entry (rare) |
| `run_server.py` | repo root | PyInstaller entry point |
| `justfile` | repo root | Available recipes |
| `{package}/__main__.py` | package root | CLI entry point |
| `{package}/server.py` | package root | MCP server definition |
| `{package}/tools/__init__.py` | package root | Tool registration |
| `{package}/portmanteau/` | package root | Portmanteau tools (legacy) |

## When to Run This SOP

Any subagent receiving an instruction to "explore repo X" MUST run this SOP first and report the discovered source root before listing files. Without this, the subagent's report is untrustworthy.
