# MCP Server Webapp Setup Guide

**Universal Quick Start Guide** - Build a FastAPI + Next.js webapp for any FastMCP-based MCP server without the debugging pain.

**Works for**: `plex-mcp`, `calibre-mcp`, `tailscale-mcp`, `virtualization-mcp`, and any other FastMCP 3.1.1++ server.

## Architecture Overview

**Recommended Structure** (use `webapp/` folder):

```
{mcp-server-repo}/
â”œâ”€â”€ src/                    # MCP server source (FastMCP tools)
â”œâ”€â”€ webapp/
â”‚   â”œâ”€â”€ backend/           # FastAPI HTTP wrapper
â”‚   â”‚   â”œâ”€â”€ app/
â”‚   â”‚   â”‚   â”œâ”€â”€ main.py    # FastAPI app + startup initialization
â”‚   â”‚   â”‚   â”œâ”€â”€ api/       # REST endpoints (one per MCP tool category)
â”‚   â”‚   â”‚   â”œâ”€â”€ mcp/
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ client.py  # MCP client wrapper
â”‚   â”‚   â”‚   â”œâ”€â”€ config.py  # Settings
â”‚   â”‚   â”‚   â””â”€â”€ utils/     # Error handling, etc.
â”‚   â”‚   â””â”€â”€ requirements.txt
â”‚   â””â”€â”€ frontend/          # Next.js 15 frontend
â”‚       â”œâ”€â”€ app/           # Next.js App Router pages
â”‚       â”œâ”€â”€ components/   # React components
â”‚       â””â”€â”€ package.json
```

**Legacy Structure** (some repos have `backend/` and `frontend/` in root - should be refactored):

```
{mcp-server-repo}/
â”œâ”€â”€ src/                    # MCP server source (FastMCP tools)
â”œâ”€â”€ backend/                # FastAPI HTTP wrapper (legacy - refactor to webapp/backend/)
â”‚   â””â”€â”€ ...                 # Same structure as webapp/backend/
â””â”€â”€ frontend/               # Next.js 15 frontend (legacy - refactor to webapp/frontend/)
    â””â”€â”€ ...                 # Same structure as webapp/frontend/
```

**Key Pattern**: Dual interface - FastMCP HTTP endpoints mounted at `/mcp` (stdio for MCP clients, HTTP for webapp).

**Note**: If your repo uses the legacy structure (`backend/` and `frontend/` in root), see the "Refactoring Legacy Structure" section below.

## Before You Start

**Replace these placeholders throughout this guide:**
- `{MCP_SERVER_NAME}` â†’ Your MCP server name (e.g., `plex_mcp`, `tailscale_mcp`, `virtualization_mcp`)
- `{mcp_server_module}` â†’ Your Python module name (e.g., `plex_mcp`, `tailscalemcp`, `virtualization_mcp`)
- `{PORT_BASE}` â†’ Base port number (e.g., `13100` for plex, `13200` for tailscale, `13300` for virtualization)
- `{REPO_PATH}` â†’ Full path to your repo (e.g., `d:\Dev\repos\plex-mcp`)
- `{WEBAPP_PATH}` â†’ Path to webapp folder: `webapp` (recommended) or empty string if using legacy `backend/` and `frontend/` in root

**Port Allocation Strategy:**
- `calibre-mcp`: 13000-13001
- `plex-mcp`: 13100-13101
- `tailscale-mcp`: 13200-13201
- `virtualization-mcp`: 13300-13301
- **Never use ports below 13000!**

**Folder Structure:**
- **Recommended**: Use `webapp/backend/` and `webapp/frontend/` (keeps webapp code organized)
- **Legacy**: Some repos have `backend/` and `frontend/` in root (should be refactored - see below)

## Critical Setup Steps (Do These First!)

### 1. Backend Setup

```powershell
cd webapp\backend

# Create venv
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# CRITICAL: Install {mcp_server_module} in editable mode
pip install -e ../../

# Verify import works
python -c "import {mcp_server_module}; print('SUCCESS')"
```

### 2. Path Configuration (CRITICAL!)

**Problem**: `uvicorn` reloader subprocesses don't inherit `sys.path` correctly.

**Solution**: Set up paths in `main.py` BEFORE any other imports:

```python
"""FastAPI application for {MCP_SERVER_NAME} webapp."""

import logging
import os
import sys
from pathlib import Path

# CRITICAL: Set up Python path BEFORE any other imports
# This ensures {mcp_server_module} is importable even in uvicorn reloader subprocesses
_current_file = Path(__file__).resolve()
# Path calculation: app/main.py -> app -> backend -> webapp -> repo_root (recommended)
# OR: app/main.py -> app -> backend -> repo_root (legacy)
# Go up enough levels to reach repo root
project_root = _current_file.parent.parent.parent.parent.parent  # For webapp/backend structure
# If using legacy backend/ structure, use: project_root = _current_file.parent.parent.parent.parent
src_path = project_root / "src"

if not src_path.exists():
    current = _current_file.parent
    while current != current.parent:
        if (current / "setup.py").exists() or (current / "pyproject.toml").exists():
            project_root = current
            src_path = project_root / "src"
            break
        current = current.parent

if src_path.exists():
    src_str = str(src_path)
    # CRITICAL: Set PYTHONPATH environment variable FIRST (for uvicorn subprocesses)
    os.environ["PYTHONPATH"] = src_str
    # Then ensure it's in sys.path
    if src_str not in sys.path:
        sys.path.insert(0, src_str)
    elif sys.path.index(src_str) != 0:
        sys.path.remove(src_str)
        sys.path.insert(0, src_str)

# NOW import FastAPI and other dependencies
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
```

### 3. Discover Your MCP Tools

**Before creating `client.py`, discover what tools your MCP server provides:**

```python
# Run this in your repo root to discover tools:
python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))
import {mcp_server_module}
# Check if tools are in a portmanteau directory or individual files
# Look for @mcp.tool() decorators or tool registration
"
```

**Common Tool Locations:**
- **Portmanteau tools**: `{mcp_server_module}.tools.portmanteau.*` (like plex-mcp)
- **Individual tools**: `{mcp_server_module}.tools.*` (like tailscale-mcp)
- **Single file**: `{mcp_server_module}.tools.portmanteau_tools` (some servers)

**Check your server's structure:**
```powershell
# List tool files
Get-ChildItem -Recurse -Path src\{mcp_server_module}\tools -Filter *.py | Select-Object FullName
```

### 4. MCP Client Setup

**Pattern**: Preload and cache tool functions to avoid import errors.

In `app/mcp/client.py`:

```python
"""MCP client wrapper for calling {MCP_SERVER_NAME} tools."""

import sys
import os
from pathlib import Path
from typing import Any, Dict
import httpx

# CRITICAL: Same path setup as main.py
_current_file = Path(__file__).resolve()
# Path calculation: app/mcp/client.py -> app -> backend -> webapp -> repo_root (recommended)
# OR: app/mcp/client.py -> app -> backend -> repo_root (legacy)
project_root = _current_file.parent.parent.parent.parent.parent  # For webapp/backend structure
# If using legacy backend/ structure, use: project_root = _current_file.parent.parent.parent.parent
src_path = project_root / "src"

if not src_path.exists():
    current = _current_file.parent
    while current != current.parent:
        if (current / "setup.py").exists() or (current / "pyproject.toml").exists():
            project_root = current
            src_path = project_root / "src"
            break
        current = current.parent

if src_path.exists():
    src_str = str(src_path)
    os.environ["PYTHONPATH"] = src_str
    if src_str not in sys.path:
        sys.path.insert(0, src_str)
    elif sys.path.index(src_str) != 0:
        sys.path.remove(src_str)
        sys.path.insert(0, src_str)

# Cache for preloaded tool functions
_tool_cache: Dict[str, Any] = {}

def _preload_tools():
    """Preload all MCP tool functions and cache them."""
    global _tool_cache
    
    # TODO: Replace with YOUR server's actual tool import paths
    # Discover tools by checking your server's structure (see Step 3)
    tool_modules = {
        # Example for portmanteau tools (like plex-mcp):
        # "tool_name": "{mcp_server_module}.tools.portmanteau.module.tool_name",
        
        # Example for individual tools (like tailscale-mcp):
        # "device_tool": "{mcp_server_module}.tools.device_tool",
        
        # Add ALL your MCP tools here with their import paths
    }
    
    for tool_name, module_path in tool_modules.items():
        try:
            module = __import__(module_path, fromlist=[tool_name])
            tool_func = getattr(module, tool_name)
            _tool_cache[tool_name] = tool_func
        except (ImportError, AttributeError) as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to preload tool {tool_name}: {e}")

# Preload tools at module import time
_preload_tools()

class MCPClient:
    """Wrapper for MCP client to call {MCP_SERVER_NAME} tools."""
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool by name."""
        # Check cache first (fast path)
        if tool_name in _tool_cache:
            tool_func = _tool_cache[tool_name]
            try:
                result = await tool_func(**arguments)
                return result if isinstance(result, dict) else {"success": True, "data": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        # Fallback: try HTTP (if FastMCP HTTP is mounted)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://127.0.0.1:{PORT_BASE}/mcp/call",
                    json={"tool": tool_name, "arguments": arguments},
                    timeout=30.0
                )
                return response.json()
        except Exception as e:
            return {"success": False, "error": f"Tool call failed: {e}"}

# Singleton instance
mcp_client = MCPClient()
```

### 5. Startup Initialization Pattern

**Pattern**: Initialize state at startup, cache for fast access.

**Generic Template** (customize for your server):

In `app/main.py`:

```python
# Global cache for frequently accessed data
# TODO: Customize cache structure for YOUR server's needs
_server_cache: dict = {
    "initialized": False,
    "data": {},
    "loaded": False
}

@app.on_event("startup")
async def startup_event():
    """Initialize {MCP_SERVER_NAME} connection and cache data on startup."""
    import logging
    logger = logging.getLogger(__name__)
    
    # Re-check path on startup (uvicorn reloader may reset it)
    # ... (same path setup code as at module level)
    
    try:
        from .mcp.client import mcp_client
        
        # TODO: Add YOUR server-specific initialization here
        # Examples:
        # - Verify connection to external service
        # - Load initial data/state
        # - Cache frequently accessed information
        # - Initialize databases or connections
        
        logger.info("Initializing {MCP_SERVER_NAME}...")
        
        # Example: Test a simple tool call to verify connection
        # result = await mcp_client.call_tool("your_status_tool", {"operation": "status"})
        # if result.get("success"):
        #     _server_cache["initialized"] = True
        #     _server_cache["data"] = result.get("data", {})
        
        _server_cache["loaded"] = True
        logger.info("SUCCESS: {MCP_SERVER_NAME} initialized and ready")
        
    except Exception as e:
        logger.error(f"Failed to initialize {MCP_SERVER_NAME} on startup: {e}", exc_info=True)
        logger.warning("Server will start but operations may fail until manually initialized")

# Fast endpoint for cached data (customize for your needs)
@app.get("/api/status")
async def get_status():
    """Get cached status for dropdown/UI population."""
    global _server_cache
    return {
        "initialized": _server_cache.get("initialized", False),
        "loaded": _server_cache.get("loaded", False),
        "data": _server_cache.get("data", {})
    }
```

**Server-Specific Examples:**

**For Plex-MCP:**
```python
# Initialize Plex server connection, cache servers/libraries
servers_result = await mcp_client.call_tool("plex_server", {"operation": "status"})
```

**For Calibre-MCP:**
```python
# Initialize Calibre database, cache libraries list
libraries_result = await mcp_client.call_tool("manage_libraries", {"operation": "list"})
```

**For Tailscale-MCP:**
```python
# Verify Tailscale connection, cache device list
devices_result = await mcp_client.call_tool("device_tool", {"operation": "list"})
```

**For Virtualization-MCP:**
```python
# Initialize VM service, cache VM list
vms_result = await mcp_client.call_tool("vm_management", {"operation": "list"})
```

### 6. FastMCP HTTP Mount

**Pattern**: Mount FastMCP HTTP endpoints directly into FastAPI.

```python
# Mount FastMCP HTTP endpoints BEFORE other routers
# FastMCP HTTP endpoints run on same port {PORT_BASE} - no port hopping!
# Dual interface: stdio for MCP clients, HTTP for webapp backend
logger = logging.getLogger(__name__)

try:
    # Most FastMCP servers expose the mcp instance via app.py or server.py
    # Check your server's structure to find the correct import path
    from {mcp_server_module}.app import mcp  # Common pattern
    # OR: from {mcp_server_module}.server import mcp  # Alternative pattern
    
    # FastMCP 3.1.1++ provides http_app() method directly
    mcp_app = mcp.http_app()
    if mcp_app:
        app.mount("/mcp", mcp_app)
        logger.info("FastMCP HTTP endpoints mounted at /mcp (dual interface: stdio + HTTP)")
except Exception as e:
    logger.warning(f"Could not mount FastMCP HTTP app: {e}")
    logger.warning("Falling back to direct import mode")
```

### 7. API Router Pattern

**Pattern**: One router file per MCP tool category.

**Create API routers for each tool category:**

Example: `app/api/example.py`

```python
"""Example API endpoints for {MCP_SERVER_NAME}."""

from fastapi import APIRouter, Query, Body
from typing import Optional

from ..mcp.client import mcp_client
from ..utils.errors import handle_mcp_error

router = APIRouter()

@router.get("/")
async def list_items():
    """List items (customize for your tool)."""
    try:
        # TODO: Replace with YOUR tool name and operation
        result = await mcp_client.call_tool(
            "your_tool_name",
            {"operation": "list"}  # Adjust if your tools don't use operation parameter
        )
        return result
    except Exception as e:
        raise handle_mcp_error(e)

@router.post("/action")
async def perform_action(data: dict = Body(...)):
    """Perform an action (customize for your tool)."""
    try:
        # TODO: Replace with YOUR tool name and parameters
        result = await mcp_client.call_tool(
            "your_tool_name",
            {
                "operation": "action",  # Adjust if needed
                **data  # Pass through user-provided parameters
            }
        )
        return result
    except Exception as e:
        raise handle_mcp_error(e)
```

In `main.py`:

```python
from .api import example  # ... all your routers

# Include routers
app.include_router(example.router, prefix="/api/example", tags=["example"])
```

### 8. Port Configuration

**CRITICAL**: Choose a unique port range for your server to avoid conflicts.

```python
# backend/app/config.py
class Settings:
    API_PORT: int = {PORT_BASE}  # e.g., 13100 for plex, 13200 for tailscale
    FRONTEND_PORT: int = {PORT_BASE + 1}  # e.g., 13101 for plex, 13201 for tailscale
```

```powershell
# Kill zombie processes before starting
Get-NetTCPConnection -LocalPort {PORT_BASE} -ErrorAction SilentlyContinue | 
    Select-Object -ExpandProperty OwningProcess | 
    ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }

# Start backend
uvicorn app.main:app --host 0.0.0.0 --port {PORT_BASE} --log-level info
```

### 9. Backend Requirements

Create `webapp/backend/requirements.txt`:

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
pydantic-settings>=2.0.0
httpx>=0.25.0
python-multipart>=0.0.6
python-dotenv>=1.0.1
```

### 10. Frontend Setup

```powershell
cd webapp\frontend
npm install

# Use Turbopack (faster than Webpack)
# In package.json:
# "dev": "next dev --turbo"
npm run dev
```

Frontend runs on http://localhost:{FRONTEND_PORT}

## Quick Scaffold Checklist

**Follow these steps in order to scaffold the entire webapp quickly.**

### Step 1: Create Directory Structure

**For recommended structure (`webapp/` folder):**
```powershell
cd {REPO_PATH}

# Create backend structure
New-Item -ItemType Directory -Force -Path webapp\backend\app
New-Item -ItemType Directory -Force -Path webapp\backend\app\api
New-Item -ItemType Directory -Force -Path webapp\backend\app\mcp
New-Item -ItemType Directory -Force -Path webapp\backend\app\utils

# Create frontend structure
New-Item -ItemType Directory -Force -Path webapp\frontend\app
New-Item -ItemType Directory -Force -Path webapp\frontend\components
```

**For legacy structure (`backend/` and `frontend/` in root):**
```powershell
cd {REPO_PATH}

# Create backend structure
New-Item -ItemType Directory -Force -Path backend\app
New-Item -ItemType Directory -Force -Path backend\app\api
New-Item -ItemType Directory -Force -Path backend\app\mcp
New-Item -ItemType Directory -Force -Path backend\app\utils

# Create frontend structure
New-Item -ItemType Directory -Force -Path frontend\app
New-Item -ItemType Directory -Force -Path frontend\components
```

**Note**: If using legacy structure, update all path references in this guide:
- `webapp\backend\` â†’ `backend\`
- `webapp\frontend\` â†’ `frontend\`
- `../../` (for pip install) â†’ `../`

### Step 2: Backend Core Files

**2.1 Create `{WEBAPP_PATH}/backend/requirements.txt`:** (see Section 9)

**Note**: Replace `{WEBAPP_PATH}` with `webapp` (recommended) or empty string if using legacy structure.

**2.2 Create `webapp/backend/app/__init__.py`:**
```python
"""{MCP_SERVER_NAME} webapp backend package."""
```

**2.3 Create `{WEBAPP_PATH}/backend/app/config.py`:**
```python
"""Configuration for {MCP_SERVER_NAME} webapp backend."""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_TITLE: str = "{MCP_SERVER_NAME} Webapp API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "HTTP API wrapper for {MCP_SERVER_NAME} server"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = {PORT_BASE}  # Must be unique per server
    RELOAD: bool = True
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        f"http://localhost:{FRONTEND_PORT}",
        f"http://127.0.0.1:{FRONTEND_PORT}",
    ]
    
    # MCP Server configuration
    MCP_USE_HTTP: bool = os.getenv("MCP_USE_HTTP", "false").lower() == "true"
    BACKEND_URL: str = os.getenv("BACKEND_URL", f"http://127.0.0.1:{PORT_BASE}")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

**2.4 Create `webapp/backend/app/utils/__init__.py`:**
```python
"""Utility modules."""
```

**2.5 Create `{WEBAPP_PATH}/backend/app/utils/errors.py`:**
```python
"""Error handling utilities."""

from fastapi import HTTPException


class MCPError(Exception):
    """Base exception for MCP-related errors."""
    pass


def handle_mcp_error(error: Exception) -> HTTPException:
    """Convert MCP errors to HTTP exceptions."""
    if isinstance(error, MCPError):
        return HTTPException(status_code=500, detail=str(error))
    return HTTPException(status_code=500, detail=f"Internal server error: {str(error)}")
```

**2.6 Create `{WEBAPP_PATH}/backend/app/mcp/__init__.py`:**
```python
"""MCP client package."""
```

**2.7 Create `{WEBAPP_PATH}/backend/app/mcp/client.py`:** (see Section 4 - customize tool imports)

**2.8 Create `{WEBAPP_PATH}/backend/app/api/__init__.py`:**
```python
"""API routers package."""
```

**2.9 Create API routers:** (see Section 7 - create one per tool category)

**3.1.1+ Create `{WEBAPP_PATH}/backend/app/main.py`:** (combine Sections 2, 5, 6, 7)

**3.1.1+ Create `{WEBAPP_PATH}/backend/start_backend.ps1`:**
```powershell
# Kill zombies
Get-NetTCPConnection -LocalPort {PORT_BASE} -ErrorAction SilentlyContinue | 
    Select-Object -ExpandProperty OwningProcess | 
    ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }

Start-Sleep -Seconds 2

# Set environment
$env:PYTHONPATH = "{REPO_PATH}\src"
$env:MCP_USE_HTTP = "false"
# TODO: Add YOUR server-specific environment variables here
# Examples:
# $env:PLEX_TOKEN = "your-token"  # For plex-mcp
# $env:TAILSCALE_API_KEY = "your-key"  # For tailscale-mcp

# Start server
Set-Location $PSScriptRoot
python -m uvicorn app.main:app --host 0.0.0.0 --port {PORT_BASE} --log-level info
```

### Step 3: Test Backend

**For recommended structure:**
```powershell
cd webapp\backend

# Install dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -e ../../

# Test import
python -c "import {mcp_server_module}; print('SUCCESS')"

# Start backend
.\start_backend.ps1

# In another terminal, test endpoints
python -c "import httpx; r = httpx.get('http://127.0.0.1:{PORT_BASE}/api/status'); print(r.status_code, r.json())"
```

**For legacy structure:**
```powershell
cd backend

# Install dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -e ../

# Test import
python -c "import {mcp_server_module}; print('SUCCESS')"

# Start backend
.\start_backend.ps1

# In another terminal, test endpoints
python -c "import httpx; r = httpx.get('http://127.0.0.1:{PORT_BASE}/api/status'); print(r.status_code, r.json())"
```

### Step 4: Frontend Scaffold (Minimal)

**4.1 Create `{WEBAPP_PATH}/frontend/package.json`:**
```json
{
  "name": "{mcp-server-name}-webapp-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev --turbo -p {FRONTEND_PORT}",
    "build": "next build",
    "start": "next start -p {FRONTEND_PORT}"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "typescript": "^5.0.0"
  }
}
```

**4.2 Create `{WEBAPP_PATH}/frontend/tsconfig.json`:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{"name": "next"}],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**4.3 Create `{WEBAPP_PATH}/frontend/app/page.tsx`:**
```tsx
export default function Home() {
  return (
    <main>
      <h1>{MCP_SERVER_NAME} Webapp</h1>
      <p>Web interface for {MCP_SERVER_NAME}</p>
    </main>
  );
}
```

**4.4 Create `{WEBAPP_PATH}/frontend/app/layout.tsx`:**
```tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

### Step 5: Verify Complete Setup

**For recommended structure:**
```powershell
# Backend should start without errors
cd webapp\backend
.\start_backend.ps1
# Check logs for: "SUCCESS: {MCP_SERVER_NAME} initialized and ready"

# Frontend should start
cd ..\frontend
npm install
npm run dev
# Visit http://localhost:{FRONTEND_PORT} - should see "{MCP_SERVER_NAME} Webapp" page

# Test API from browser console (F12):
# fetch('http://127.0.0.1:{PORT_BASE}/api/status').then(r => r.json()).then(console.log)
```

**For legacy structure:**
```powershell
# Backend should start without errors
cd backend
.\start_backend.ps1
# Check logs for: "SUCCESS: {MCP_SERVER_NAME} initialized and ready"

# Frontend should start
cd ..\frontend
npm install
npm run dev
# Visit http://localhost:{FRONTEND_PORT} - should see "{MCP_SERVER_NAME} Webapp" page

# Test API from browser console (F12):
# fetch('http://127.0.0.1:{PORT_BASE}/api/status').then(r => r.json()).then(console.log)
```

### Step 6: Next Implementation Steps

1. **Discover all your tools** - Use Step 3 to find all available tools
2. **Create API routers** - One router per tool category (copy pattern from Section 7)
3. **Implement startup initialization** - Customize Section 5 for your server's needs
4. **Build UI components** - Use your API endpoints to create the interface
5. **Add server-specific features** - Customize for your domain (playback, VM management, etc.)

## Common Pitfalls & Solutions

### âŒ ImportError: No module named '{mcp_server_module}'

**Cause**: `uvicorn` reloader subprocesses don't inherit `sys.path`.

**Solution**: 
1. Set `PYTHONPATH` environment variable BEFORE starting uvicorn
2. Set paths in `main.py` BEFORE any imports
3. Install in editable mode: `pip install -e ../../`

```powershell
$env:PYTHONPATH="{REPO_PATH}\src"
uvicorn app.main:app --host 0.0.0.0 --port {PORT_BASE}
```

### âŒ Port Already in Use

**Cause**: Previous server instance not killed.

**Solution**: Always kill zombies first:

```powershell
Get-NetTCPConnection -LocalPort {PORT_BASE} -ErrorAction SilentlyContinue | 
    Select-Object -ExpandProperty OwningProcess | 
    ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
```

### âŒ Server Not Initialized

**Cause**: Startup event not completing before requests arrive, or missing environment variables.

**Solution**: 
1. Set required environment variables (check your MCP server's docs)
2. Use `startup_event` to verify connection and cache initial state
3. Provide fast cached endpoints for UI
4. Log initialization success/failure clearly

### âŒ Slow API Responses

**Cause**: Every request calls MCP tool directly.

**Solution**: 
1. Cache frequently accessed data at startup
2. Provide fast cached endpoints (e.g., `/api/status`)
3. Use direct Python imports (cached) instead of HTTP when possible

### âŒ Unicode Emoji Errors

**Cause**: Emojis break encoding in terminals/logs.

**Solution**: NEVER use Unicode emojis in code/logs. Use text markers:
- `[ERROR]`, `[SUCCESS]`, `[INFO]` instead of emojis

## File Structure Checklist

**Recommended structure (`webapp/` folder):**
```
webapp/
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ app/
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ main.py              # FastAPI app + startup
â”‚   â”‚   â”œâ”€â”€ config.py            # Settings
â”‚   â”‚   â”œâ”€â”€ api/
â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”œâ”€â”€ example.py       # One router per MCP tool category
â”‚   â”‚   â”‚   â””â”€â”€ ...              # Add more routers as needed
â”‚   â”‚   â”œâ”€â”€ mcp/
â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â””â”€â”€ client.py        # MCP client wrapper
â”‚   â”‚   â””â”€â”€ utils/
â”‚   â”‚       â”œâ”€â”€ __init__.py
â”‚   â”‚       â””â”€â”€ errors.py         # Error handling
â”‚   â”œâ”€â”€ requirements.txt
â”‚   â”œâ”€â”€ README.md
â”‚   â””â”€â”€ start_backend.ps1        # Startup script
â””â”€â”€ frontend/
    â”œâ”€â”€ app/                      # Next.js App Router
    â”œâ”€â”€ components/
    â”œâ”€â”€ package.json
    â””â”€â”€ README.md
```

**Legacy structure (should be refactored):**
```
backend/                          # Same as webapp/backend/
â””â”€â”€ ...
frontend/                         # Same as webapp/frontend/
â””â”€â”€ ...
```

## Testing Checklist

1. **Backend starts without errors**
   ```powershell
   # For recommended structure:
   cd webapp\backend
   # OR for legacy structure:
   # cd backend
   
   # Set required environment variables first
   uvicorn app.main:app --host 0.0.0.0 --port {PORT_BASE}
   # Check logs for: "SUCCESS: {MCP_SERVER_NAME} initialized and ready"
   ```

2. **Imports work**
   ```powershell
   python -c "import {mcp_server_module}; print('SUCCESS')"
   ```

3. **API endpoints respond**
   ```powershell
   python -c "import httpx; r = httpx.get('http://127.0.0.1:{PORT_BASE}/api/status'); print(r.status_code, r.json())"
   ```

4. **Frontend connects to backend**
   - Visit http://localhost:{FRONTEND_PORT}
   - Check browser console for API errors
   - Verify dropdowns populate from cached endpoints

## Refactoring Legacy Structure

**If your repo has `backend/` and `frontend/` in root, refactor to `webapp/` structure:**

```powershell
cd {REPO_PATH}

# Create webapp directory
New-Item -ItemType Directory -Force -Path webapp

# Move backend and frontend into webapp
Move-Item -Path backend -Destination webapp\backend
Move-Item -Path frontend -Destination webapp\frontend

# Update path references in scripts:
# - start_backend.ps1: Change `cd backend` to `cd webapp\backend`
# - package.json scripts: Update paths if needed
# - Any CI/CD workflows: Update paths
# - README.md: Update installation instructions
```

**After refactoring:**
- Update `pip install -e ../` â†’ `pip install -e ../../`
- Update path calculations in `main.py` and `client.py`:
  - Change `project_root = _current_file.parent.parent.parent.parent` (legacy)
  - To `project_root = _current_file.parent.parent.parent.parent.parent` (webapp structure)
- Update `start_backend.ps1`: Verify `$env:PYTHONPATH = "{REPO_PATH}\src"` is correct
- Update any documentation referencing paths
- Update CI/CD workflows if they reference `backend/` or `frontend/` paths
- Test that imports still work: `python -c "import {mcp_server_module}; print('SUCCESS')"`

**Why refactor?**
- Keeps webapp code organized in one place
- Consistent structure across all MCP server repos
- Easier to ignore webapp files in `.gitignore` patterns
- Better separation of concerns (MCP server vs webapp)

## Key Takeaways

1. **Path setup FIRST** - Always set `PYTHONPATH` and `sys.path` before imports
2. **Preload tools** - Cache tool functions to avoid import errors
3. **Startup initialization** - Cache frequently accessed data at startup
4. **Fast cached endpoints** - Provide `/api/status` for UI dropdowns
5. **Dual interface** - Mount FastMCP HTTP at `/mcp` for webapp, stdio for MCP clients
6. **Unique ports** - Never use ports below 13000, allocate unique ranges per server
7. **Kill zombies** - Always kill existing processes before starting
8. **No emojis** - Use text markers `[ERROR]`, `[SUCCESS]` instead
9. **Discover tools first** - Use Step 3 to find all your server's tools before scaffolding
10. **Use webapp/ folder** - Prefer `webapp/backend/` and `webapp/frontend/` over root-level folders

## Reference Implementations

See these complete working examples:
- **`calibre-mcp/webapp/`** - Book/library management (ports 13000-13001)
  - See `calibre-mcp/WEBAPP_SETUP_GUIDE.md` for Plex-specific details
- **`plex-mcp/webapp/`** - Media playback (ports 13100-13101)
  - See `plex-mcp/WEBAPP_SETUP_GUIDE.md` for Plex-specific details

Both include:
- `backend/app/main.py` - FastAPI app with startup initialization
- `backend/app/mcp/client.py` - MCP client with tool caching
- `backend/app/api/` - API routers for all MCP tools
- `backend/ENDPOINTS.md` - Complete API documentation

**To adapt for your server:**
1. Copy this generalized guide to your repo root as `WEBAPP_SETUP_GUIDE.md`
2. Replace all `{PLACEHOLDERS}` with your server-specific values
3. Discover your tools using Method 1-3 in Section 3
4. Customize startup initialization (Section 5) for your domain
5. Create API routers (Section 7) for each tool category
6. Choose a unique port range (Section 8)

## Server-Specific Customization Guide

### Quick Reference Table

| Server Type | Port Range | Startup Action | Key Environment Vars | Example Tools |
|------------|------------|----------------|---------------------|---------------|
| **Media Servers** (Plex, Jellyfin) | 13100+ | Connect to server, cache libraries/clients | `PLEX_TOKEN`, `PLEX_SERVER_URL` | `plex_streaming`, `plex_media`, `plex_library` |
| **Infrastructure** (Tailscale) | 13200+ | Verify API connection, cache devices | `TAILSCALE_API_KEY` | `device_tool`, `network_tool`, `monitor_tool` |
| **Virtualization** (Hyper-V, VirtualBox) | 13300+ | Initialize VM service, cache VM list | `HYPERV_ENABLED`, `VBOX_PATH` | `vm_management`, `snapshot_management`, `network_management` |
| **Content Management** (Calibre) | 13000+ | Initialize database, cache libraries | `CALIBRE_LIBRARY_PATH` | `manage_libraries`, `query_books`, `manage_viewer` |
| **Development Tools** | 13400+ | Verify tool availability | Varies by tool | Project management, build operations |

### Detailed Customization

#### For Media Servers (Plex, Jellyfin, etc.)
- **Startup**: Connect to media server, cache libraries/clients
- **UI**: Media browser, playback controls, client selector
- **Key Tools**: Streaming, media browsing, library management
- **Example**: `plex-mcp/webapp/`

#### For Infrastructure (Tailscale, Virtualization, etc.)
- **Startup**: Verify service connection, cache device/VM lists
- **UI**: Device/VM management, network visualization, status dashboards
- **Key Tools**: Device management, network operations, monitoring
- **Example**: `tailscale-mcp/` (no webapp yet - use this guide!)

#### For Content Management (Calibre, etc.)
- **Startup**: Initialize database, cache library list
- **UI**: Book browser, reader integration, metadata management
- **Key Tools**: Library management, search, viewer operations
- **Example**: `calibre-mcp/webapp/`

#### For Development Tools
- **Startup**: Verify tool availability, cache project lists
- **UI**: Project browser, operation panels, status indicators
- **Key Tools**: Project management, build operations, deployment

**Customize the startup initialization (Section 5) and API routers (Section 7) based on your server's domain.**

