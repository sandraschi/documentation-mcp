---
title: MCP Server First-Time Success Guarantee
status: active
last_updated: 2026-03-30
version: 13.1 (SOTA v13.1 Compliance)
---

# MCP Server First-Time Success Guarantee

> [!IMPORTANT]
> **SOTA v13.1 (2026-03-30)** — This is the authoritative standard for achieving a "Zero-Error First Connection" in the March 2026 fleet. All mentions of legacy FastMCP 2.x and Poetry have been purged.

## 🎯 Mission Statement

**Every MCP server MUST work perfectly on first connection to any MCP client (Claude Desktop, Cursor, Zed, etc.) without requiring any modifications, manual environment setup beyond `uv sync`, or LLM intervention.**

---

## 🚨 Guarantee Requirements

### 1. The "uv" Standard (Mandatory)
All Python fleet servers MUST use **uv** for dependency management. 
- **`pyproject.toml`** + committed **`uv.lock`** are required.
- **`justfile`** must contain a `dev` or `run` recipe that maps to `uv run python -m ...`.

### 2. FastMCP 3.1.1+ Baseline
Servers must target **FastMCP 3.1.1+** to ensure:
- Stable **Prefab UI** rendering (`app=True`).
- Correct **Discrete Tooling** discovery (no portmanteaus).
- Reliable **Async Sampling** (SEP-1577).

### 3. Immediate Success Path
- **✅ AUTO-SCAFFOLD**: `uv run` handles virtual environment creation implicitly.
- **✅ NO CONSTRUCTOR BLOAT**: Use `FastMCP(name="...", dependencies=[...])` carefully.
- **✅ LIFESPANS**: Resource initialization must be handled in `@mcp.lifespan`.

---

## 🔧 Implementation Framework

### 1. Robust Initialization
```python
from fastmcp import FastMCP
from contextlib import asynccontextmanager

@asynccontextmanager
async def server_lifespan(mcp: FastMCP):
    """Guaranteed startup validation."""
    try:
        # Check mandatory env vars
        if not os.getenv("REQUIRED_API_KEY"):
            logger.warning("⚠️ REQUIRED_API_KEY missing. Basic mode enabled.")
        yield
    finally:
        logger.info("Cleaning up resources...")

mcp = FastMCP(
    "My SOTA Server",
    lifespan=server_lifespan,
    dependencies=["httpx", "pydantic>=2.0"]
)
```

### 2. Discrete Tooling & Prefab UI
Abandon the "Universal Portmanteau" (v12 legacy). Use specialized tools with mandatory rich returns for visual data.

```python
from fastmcp import FastMCP
from fastmcp.prefab import PrefabApp
from mcp.types import ToolResult

@mcp.tool(app=True)
async def get_status() -> ToolResult:
    """Check server health and status. Returns a rich SOTA card."""
    data = {"status": "online", "uptime": "14d", "load": 0.15}
    
    return ToolResult(
        content=[{"type": "text", "text": f"Status: {data['status']} (Load: {data['load']})"}],
        structured_content=PrefabApp(
            type="status_card",
            title="System Health",
            data=data
        )
    )
```

### 3. The 3-4-100 Docstring Rule
To ensure agentic efficiency, all tool docstrings must be compact:
- **3-4 lines** of concise description.
- **100 characters** per line max.
- **No** redundant `@param` or `@return` tags (FastMCP handles schema generation).

---

## 📋 Implementation Checklist

### Phase 1: Environment (REQUIRED)
- [ ] Root `pyproject.toml` with `fastmcp>=3.1.1`.
- [ ] Root `justfile` with standard recipes.
- [ ] Root `llms.txt` and `llms-full.txt` (required pair).
- [ ] `manifest.json` + `assets/icon.png` for **MCPB** packaging.

### Phase 2: Logic (REQUIRED)
- [ ] Discrete tools for every feature (no "portmanteaus").
- [ ] `app=True` for any tool returning stats, images, or cards.
- [ ] Async-first implementation for all IO-bound tools.
- [ ] Proper error handling returning strings, not raising unhandled exceptions.

### Phase 3: Verification (REQUIRED)
- [ ] `uv run python -m ...` starts without tracebacks.
- [ ] `just mcpb-pack` builds a valid bundle in `dist/`.
- [ ] Prefab UI verified in Claude Desktop.

---

## 🔍 Validation Script (SOTA v13.1)

```powershell
# validate_sota.ps1
Write-Host "🔍 Validating FastMCP 3.1.1+ SOTA Compliance..."

# Check UV
if (!(Get-Command uv -ErrorAction SilentlyContinue)) { 
    Write-Error "❌ uv not found. Installation required."
}

# Check Version
$version = uv run python -c "import fastmcp; print(fastmcp.__version__)"
if ([version]$version -lt [version]"3.1.1") {
    Write-Error "❌ FastMCP version $version is too low. Must be 3.1.1+"
}

Write-Host "✅ SOTA v13.1 Baseline Verified."
```

---

**Last Updated:** 2026-03-30  
**Owner:** Sandra Schi  
**Compliance:** FastMCP 3.1.1+ / MCPB v0.2.0
