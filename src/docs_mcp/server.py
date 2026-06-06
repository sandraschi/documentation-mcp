import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastmcp import FastMCP
from fastmcp.server import create_proxy

from docs_mcp.api import docs, fleet, interaction, settings, skills
from docs_mcp.backend.process_manager import process_manager

# Modular Imports
from docs_mcp.backend.store_registry import close_stores, get_memory_store, get_store
from docs_mcp.tools import memory, prompts, rag, system, workflows

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("docs_mcp.server")

# 1. Initialize FastMCP
docs_mcp = FastMCP("Documentation MCP")

# MCP Bridge: ProxyProvider for multi-server federation
_bridge_urls = os.getenv("MCP_BRIDGE_URLS", "")
if _bridge_urls:
    for _url in _bridge_urls.split(","):
        _url = _url.strip()
        if _url:
            try:
                docs_mcp.add_provider(create_proxy(_url))
                logger.info("MCP bridge registered: %s", _url)
            except Exception as e:
                logger.warning("MCP bridge failed for %s: %s", _url, e)

# 2. Register Modular Components
rag.register_tools(docs_mcp)
system.register_tools(docs_mcp)
workflows.register_tools(docs_mcp)
prompts.register_tools(docs_mcp)
memory.register_tools(docs_mcp)

# 3. Lifespan Management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """SOTA v14.0 Lifespan: Init stores and ensure background process cleanup."""
    logger.info("🚀 docs-mcp starting up...")
    try:
        # Warm up stores
        get_store()
        get_memory_store()
    except Exception as e:
        logger.error(f"Failed to initialize stores: {e}")

    yield

    logger.info("🛑 docs-mcp shutting down...")
    # Cleanup background processes
    process_manager.cleanup_all()
    # Close stores
    close_stores()

# 4. Initialize FastAPI Application
app = FastAPI(title="Documentation MCP Control Plane", lifespan=lifespan)

# Store MCP instance in state for API handlers
app.state.mcp = docs_mcp

# Add CORS for cross-origin fleet interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Include Modular API Routers
app.include_router(docs.router)
app.include_router(fleet.router)
app.include_router(settings.router)
app.include_router(interaction.router)
app.include_router(skills.router)

# 6. SPA and Static Asset Handling
FRONTEND_DIST = Path(__file__).parent.parent.parent / "web_sota" / "dist"
ASSETS_DIR = FRONTEND_DIST / "assets"

if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

@app.get("/{path:path}")
async def serve_spa(path: str):
    """Catch-all for SPA routing."""
    # Check if requesting a file that exists (like robots.txt)
    requested_file = FRONTEND_DIST / path
    if requested_file.is_file():
        return FileResponse(requested_file)

    # Fallback to index.html for SPA routes
    index_path = FRONTEND_DIST / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return Response("Frontend not built. Run 'just build' in web_sota.", status_code=404)

def main():
    """Entry point for stdio transport."""
    docs_mcp.run(transport="stdio")

if __name__ == "__main__":
    import uvicorn
    # Public hub: frontend 11032, backend 11033 (mcp-central-docs keeps 10794/10795)
    port = int(os.getenv("DOCS_MCP_PORT", "11033"))
    uvicorn.run(app, host="0.0.0.0", port=port)
