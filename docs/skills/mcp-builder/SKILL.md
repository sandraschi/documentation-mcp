# MCP Builder Skill — Goliath Fleet Standard
# FastMCP 3.2.4 | Starlette 1.0 | Sandra's Fleet | 2026-05-04
#
# INSTALLATION (Claude Desktop skills):
#   Copy this file to: C:\Users\sandr\AppData\Roaming\Claude\skills\mcp-builder\SKILL.md
#   OR place at: D:\Dev\repos\mcp-central-docs\skills\mcp-builder\SKILL.md
#   and symlink / reference from Claude Desktop skills config.
#
# This skill auto-loads when Claude detects MCP server build/scaffold/port tasks.

## TRIGGER CONDITIONS
Load this skill when the task involves any of:
- "create/scaffold/build a new MCP server"
- "add a tool/endpoint to [repo]-mcp"
- "what port should I use"
- "start.ps1 for new server"
- "FastMCP" appearing in a coding task
- "write a SKILL.md" or "create a skill"
- Dockerfile for a Python MCP container

---

## FLEET IDENTITY

- GitHub: sandraschi
- Repos root: `D:\Dev\repos\`
- Fleet hub (mcd): `D:\Dev\repos\mcp-central-docs\`
- Port registry: `D:\Dev\repos\mcp-central-docs\operations\WEBAPP_PORTS.md`
- Fleet index: `D:\Dev\repos\mcp-central-docs\projects\FLEET_INDEX.md`
- Standards: `D:\Dev\repos\mcp-central-docs\standards\`

**Before creating any new MCP server:** read WEBAPP_PORTS.md to find the next free port pair. Never guess. Never use 3000/5000/5173/8000/8080.

---

## FASTMCP 3.2.4 — CANONICAL PATTERNS

### SOTA as of 2026-05-04
```
fastmcp>=3.2.4
```

Key 3.2 additions over 3.1:
- `GenerativeUI` provider, `prefab-ui>=0.18.0`
- `@mcp.tool(app=True)` returns `PrefabApp` directly (not wrapped in `ToolResult`)
- `mcp.http_app(path="/")` replaces `mcp.sse_app()` for ASGI mounting
- `fastmcp dev apps` browser preview
- Security fixes: SSRF/path traversal (GHSA-vv7q-7jx5-f767), PyJWT CVE-2026-32597

Key 3.1 additions (still current):
- CodeMode (BM25 tool discovery) — `@mcp.tool()` with `description=` auto-indexes
- `@mcp.prompt()` for prompt templates
- `@mcp.resource()` for resource endpoints
- `ctx.sample()` for agentic sampling (SEP-1577)
- Prefab UI DSL (Python → React)
- `SearchTools` standalone transform
- Lazy imports

### Minimal server template

```python
"""[repo-name] MCP Server — [one line description]."""
from fastmcp import FastMCP, Context
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn

mcp = FastMCP("[ServerName]", version="0.1.0")

@mcp.tool()
async def my_tool(param: str, ctx: Context) -> dict:
    """Tool description — appears in CodeMode BM25 index."""
    return {"result": param}

# Mount MCP under /mcp on the Starlette app (Starlette 1.0 pattern)
app = Starlette(routes=[Mount("/mcp", mcp.http_app(path="/"))])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
```

### NEVER do this (anti-patterns)
```python
# WRONG — FastMCP 3.1 API, broken in 3.2
StreamingResponse(mcp.sse_app())

# WRONG — FastAPI/Pydantic (fleet standard is Starlette + plain dicts)
from fastapi import FastAPI
from pydantic import BaseModel

# WRONG — old decorator-call pattern (works but verbose)
mcp.tool()(my_function)

# WRONG — task=True on tool decorators (invalid, causes startup error)
@mcp.tool(task=True)
```

### Prefab UI (3.2)
```python
from fastmcp.contrib.prefab import PrefabApp, DataTable, Dashboard, Metric

@mcp.tool(app=True)
async def my_dashboard() -> PrefabApp:
    return Dashboard(title="Status", metrics=[
        Metric(label="Uptime", value="99.9%"),
    ])
```

---

## STARLETTE STANDARD (mandatory for new webapps)

All new MCP server webapps use **Starlette 1.0 + plain dicts**. No FastAPI. No Pydantic models.

```python
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "healthy", "version": "0.1.0"})

async def api_status(request: Request) -> JSONResponse:
    data = await request.json()
    return JSONResponse({"ok": True, "received": data})

app = Starlette(routes=[
    Route("/health", health),
    Route("/api/status", api_status, methods=["POST"]),
    Mount("/mcp", mcp.http_app(path="/")),
    Mount("/", StaticFiles(directory="dist", html=True), name="static"),
])
```

---

## PORT ALLOCATION

**Mandatory:** check `D:\Dev\repos\mcp-central-docs\operations\WEBAPP_PORTS.md` for next free pair.

Rules:
- Range: 10700–11000 only
- Frontend and backend ports MUST be adjacent (e.g., 10956/10957)
- Even-numbered preferred for backends
- After allocating: update WEBAPP_PORTS.md AND FLEET_INDEX.md

Current high-water mark (2026-05-04): **10963** (deepfang Grafana)
Next available pair: **10964/10965** — verify against registry before using.

---

## START.PS1 — NAKED-PC INSTALL STANDARD

Every new MCP server MUST have a `start.ps1` that works on a fresh Windows clone.

```powershell
<#
.SYNOPSIS
    Start [repo-name] MCP server — naked-PC compliant.
    Requires: uv, Node.js LTS, just (auto-installed via winget if missing)
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Require-Command {
    param([string]$cmd, [string]$wingetId = "")
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        if ($wingetId) {
            Write-Host "Installing $cmd via winget..."
            winget install --id $wingetId -e --accept-source-agreements --accept-package-agreements
            $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" +
                        [System.Environment]::GetEnvironmentVariable("PATH","User")
        } else {
            Write-Error "$cmd not found and no winget ID provided. Install manually."
            exit 1
        }
    }
}

Require-Command "uv"   "astral-sh.uv"
Require-Command "node" "OpenJS.NodeJS.LTS"
Require-Command "just" "Casey.Just"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Kill zombie processes on our ports
$BackendPort = 10964   # REPLACE with actual port
$FrontendPort = 10965  # REPLACE with actual port
@($BackendPort, $FrontendPort) | ForEach-Object {
    $conn = Get-NetTCPConnection -LocalPort $_ -ErrorAction SilentlyContinue
    if ($conn) { Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue }
}

# Install Python deps
& "C:\Users\sandr\.local\bin\uv.exe" sync

# Build frontend if dist missing
if (-not (Test-Path "webapp\dist\index.html")) {
    Write-Host "Building frontend..."
    Push-Location webapp
    npm ci
    npm run build
    Pop-Location
}

# Start backend
Start-Process -NoNewWindow "C:\Users\sandr\.local\bin\uv.exe" -ArgumentList "run", "python", "-m", "src.server"

# Wait for backend readiness
$timeout = 30
$elapsed = 0
while ($elapsed -lt $timeout) {
    try {
        $resp = Invoke-WebRequest "http://localhost:$BackendPort/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($resp.StatusCode -eq 200) { break }
    } catch {}
    Start-Sleep 1
    $elapsed++
}

Write-Host "Backend ready at http://localhost:$BackendPort"
Start-Process "http://localhost:$FrontendPort"
```

Also provide `start.bat`:
```bat
@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0start.ps1"
```

---

## UV + PYTHON — FULL PATHS

In subprocess/PowerShell context, `uv` is NOT on PATH. Always use full path:
```
C:\Users\sandr\.local\bin\uv.exe
```

Python:
```
C:\Users\sandr\AppData\Local\Programs\Python\Python313\python.exe
```

pyproject.toml minimum:
```toml
[project]
name = "repo-name-mcp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastmcp>=3.2.4",
    "starlette>=1.0.0",
    "uvicorn[standard]>=0.30.0",
    "httpx>=0.27.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## DOCKER / CONTAINERS

When writing Dockerfiles for MCP containers:

```dockerfile
FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir fastmcp>=3.2.4 starlette>=1.0.0 uvicorn[standard]>=0.30.0

# Non-root user (security standard — uid 65530+, one per container)
RUN adduser --disabled-password --gecos "" --uid 65530 mcp
USER mcp

EXPOSE 10964
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "10964"]
```

Non-root UIDs in use (deepfang):
- 65533 sanitizer
- 65532 worker
Next available: 65531, 65530, etc.

---

## TOOL DESIGN PATTERNS

### Portmanteau (preferred for dense tool sets)
Single tool with `op` parameter instead of explosion of separate tools:

```python
@mcp.tool()
async def my_ops(op: str, path: str = "", content: str = "") -> dict:
    """
    Unified file operations.
    op: read | write | list | delete
    """
    if op == "read": ...
    elif op == "write": ...
    raise ValueError(f"Unknown op: {op}")
```

### Agentic workflow (SEP-1577)
```python
@mcp.tool()
async def my_agentic_workflow(goal: str, ctx: Context) -> str:
    """Multi-step workflow via FastMCP 3.2 sampling."""
    result = await ctx.sample(
        messages=goal,
        system_prompt="You are a [domain] specialist...",
        temperature=0.2,
        max_tokens=1024,
    )
    return result.text
```

### Safe-fail defaults
All tools that call external services must fail safely:
```python
try:
    resp = await client.get(url, timeout=10.0)
except Exception as e:
    return {"success": False, "error": str(e)}
```

---

## CLAUDE DESKTOP MCP CONFIG

Path: `C:\Users\sandr\AppData\Roaming\Claude\claude_desktop_config.json`

New stdio server entry:
```json
"repo-name-mcp": {
    "command": "C:\\Users\\sandr\\.local\\bin\\uv.exe",
    "args": ["run", "--directory", "D:\\Dev\\repos\\repo-name-mcp", "python", "-m", "src.server"],
    "env": {
        "SOME_VAR": "value"
    }
}
```

New HTTP/SSE server entry (for FastMCP 3.2 http_app):
```json
"repo-name-mcp": {
    "type": "sse",
    "url": "http://localhost:10964/mcp/sse"
}
```

MCP logs: `C:\Users\sandr\AppData\Roaming\Claude\logs\mcp-server-{name}.log`

---

## GIT OPERATIONS IN POWERSHELL

`git -C <path>` via splatting fails. Always use:
```powershell
Push-Location "D:\Dev\repos\repo-name"
& "C:\Program Files\Git\cmd\git.exe" add .
& "C:\Program Files\Git\cmd\git.exe" commit -m "message"
Pop-Location
```

Never use `&&` in PowerShell — use semicolons or separate statements.

---

## FLEET INDEX + PORT REGISTRY UPDATES

After creating any new server, update both:

1. `D:\Dev\repos\mcp-central-docs\projects\FLEET_INDEX.md` — add row to table
2. `D:\Dev\repos\mcp-central-docs\operations\WEBAPP_PORTS.md` — add port rows

Fleet index row format:
```
| [repo-name](file:///D:/Dev/repos/repo-name) | MCP Server | Active | **Description (v0.1.0)** — FastMCP 3.2.4; N tools; brief feature list. Backend **XXXXX**, frontend **XXXXX**. |
```

---

## MCPB PACKAGING

Fleet uses source-code-only packaging via Anthropic mcpb CLI:
```powershell
mcpb validate   # validate manifest
mcpb pack       # create package
# Never use: mcpb init, mcpb publish
```

No bundled deps in packages. `pyproject.toml` is the dependency manifest.

---

## ADVANCED MEMORY NOTES

After significant work on any MCP server, write a note:
```
memops:adn_notes(operation="write",
    title="repo-name-YYYY-MM-DD-session",
    folder="projects",
    tags=["repo-name", "fastmcp", "mcp", "status", "priority"],
    content="..."
)
```

Tag ALL notes: [project-name, technology, status, priority]

---

## COMMON MISTAKES TO AVOID

| Mistake | Correct |
|---------|---------|
| `mcp.sse_app()` | `mcp.http_app(path="/")` |
| `@mcp.tool(task=True)` | `@mcp.tool()` |
| `from fastapi import FastAPI` | `from starlette.applications import Starlette` |
| `where uv` in subprocess | `C:\Users\sandr\.local\bin\uv.exe` |
| `git -C path` splatting | `Push-Location path; git ...` |
| `&&` in PowerShell | `;` or separate statements |
| Guessing port numbers | Read WEBAPP_PORTS.md first |
| `mkdir` in PowerShell | `New-Item -ItemType Directory` |
| Mixing `\` and `/` in Windows paths | Always `\` for Windows paths |
| Not adding to FLEET_INDEX | Always update after creating server |
