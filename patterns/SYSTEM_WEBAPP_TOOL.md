# System Webapp Tool Pattern

**Status**: SOTA Active
**Context**: MCP Server / Webapp Integration

## 1. The Problem
MCP servers often have associated dashboards (webapps) for visualization and control. However, these exist as separate processes (Next.js/React) that the user must manually launch via scripts (`start.ps1`). This creates friction and treats the interface as a "passive accessory" rather than an agent-managed resource.

## 2. The Solution: Self-Actuation
The "System Webapp Tool" pattern gives the MCP server a tool to launch its own dashboard. This allows the Agentic Layer to "open" the interface on demand, or checking if it's running.

## 3. Protocol Implementation

### A. The Underlying Script (`start.ps1`)
The MCP tool does **NOT** reimplement build/start logic. It relies entirely on the standardized `start.ps1` script (see [WEBAPP_PORTS](../operations/WEBAPP_PORTS.md)) which handles:
- Port clearing (Zombie suppression)
- `npm install` (Dependency management)
- Process orchestration (Backend + Frontend)

### B. The MCP Tool (`start_webapp`)
The tool is a simple trigger that executes the PowerShell script in a detached console.

```python
import subprocess
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Context

@mcp.tool()
async def start_webapp(ctx: Context) -> str:
    """
    Launch the associated dashboard webapp for this MCP server.
    
    Trigger:
    - User asks to "open the dashboard" or "show me the interface"
    - System setup verification
    
    Returns:
    - URL of the running webapp
    """
    # 1. Locate the definition - standard SOTA layout allows relative resolution
    # Assuming code is in src/package/server.py and webapp is in repo_root/webapp
    base_dir = Path(__file__).parent.parent.parent.parent # Adjust based on depth
    webapp_dir = base_dir / "webapp"
    script_path = webapp_dir / "start.ps1"

    if not script_path.exists():
        return f"Error: Webapp start script not found at {script_path}"

    try:
        # 2. Launch PowerShell script detached
        # creationflags=subprocess.CREATE_NEW_CONSOLE ensures it pops up independently
        subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script_path)],
            cwd=str(webapp_dir),
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            close_fds=True
        )
        
        # Ideally read port from config, but hardcoded fallback is acceptable for now
        return f"Webapp launching. Check console for details."

    except Exception as e:
        return f"Failed to launch webapp: {str(e)}"
```

## 4. Benefits
1.  **Agent Agency**: The agent controls its own interfaces.
2.  **Encapsulation**: Build complexity stays in `start.ps1`, not Python.
3.  **Resilience**: Reuses existing valid startup logic (zombie killing, etc.).
