import json
import logging
import subprocess
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request

from docs_mcp.backend.process_manager import process_manager

logger = logging.getLogger("docs_mcp.api.fleet")
router = APIRouter(prefix="/api")

@router.get("/apps")
async def api_apps():
    """List available local apps for the dashboard."""
    try:
        from docs_mcp.backend.apps_catalog import APPS_CATALOG
        return APPS_CATALOG
    except Exception as e:
        logger.error(f"Error in api_apps: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fleet-projects")
async def api_fleet_projects():
    """Serve the fleet-projects.json registry."""
    try:
        data_path = Path(__file__).parent.parent / "data" / "fleet-projects.json"
        if data_path.exists():
            with open(data_path, encoding="utf-8") as f:
                return json.load(f)
        raise HTTPException(status_code=404, detail="Fleet projects registry not found")
    except Exception as e:
        logger.error(f"Error in api_fleet_projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/launch")
async def api_launch_app(request: Request):
    """Launch a local app/service."""
    try:
        body = await request.json()
        cmd = body.get("command")
        id = body.get("id", "app")

        if not cmd:
            raise HTTPException(status_code=400, detail="No command provided")

        # SOTA v14.0 background launch pattern
        proc = subprocess.Popen(
            ["powershell.exe", "-Command", cmd],
            creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, "CREATE_NEW_CONSOLE") else 0
        )

        process_manager.register(id, proc)
        return {"success": True, "pid": proc.pid}
    except Exception as e:
        logger.error(f"Error launching app: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/processes")
async def api_processes():
    """List all active background processes tracked by the manager."""
    try:
        return {"processes": process_manager.list_active()}
    except Exception as e:
        logger.error(f"Error listing processes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/processes/stop")
async def api_stop_process(request: Request):
    """Stop a specific background process."""
    try:
        body = await request.json()
        pid = body.get("pid")
        proc_id = body.get("id")

        success = process_manager.stop_process(proc_id=proc_id, pid=pid)
        return {"success": success}
    except Exception as e:
        logger.error(f"Error stopping process: {e}")
        raise HTTPException(status_code=500, detail=str(e))
