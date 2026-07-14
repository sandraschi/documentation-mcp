import logging
import time

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from docs_mcp.backend import settings_store
from docs_mcp.backend.chat_service import auto_discover, stream_chat
from docs_mcp.backend.log_buffer import get_log_buffer
from docs_mcp.backend.store_registry import get_memory_store, get_store
from docs_mcp.tools.rag import _search_docs_raw

logger = logging.getLogger("docs_mcp.api.interaction")
router = APIRouter(prefix="/api")
_SERVER_START = time.time()

@router.get("/v1/diagnostics")
async def api_v1_diagnostics(request: Request):
    """Diagnostics endpoint for CUA-NSIS smoke testing."""
    tool_count = 0
    if hasattr(request.app.state, "mcp"):
        try:
            tools = await request.app.state.mcp.list_tools()
            tool_count = len(tools)
        except Exception:
            logger.warning("Could not list tools for diagnostics")
    return {
        "status": "ok",
        "server": "Documentation MCP",
        "version": "1.0.1",
        "uptime_seconds": int(time.time() - _SERVER_START),
        "tool_count": tool_count,
        "tools": [{"name": t.name} for t in (await request.app.state.mcp.list_tools())] if tool_count else [],
        "system": {"windows": True},
        "errors": [],
    }

@router.get("/status")
async def api_status():
    """Industrial status endpoint for health monitoring."""
    try:
        from docs_mcp.backend.apps_catalog import APPS_CATALOG
        store = get_store()
        memory_store = get_memory_store()
        settings = settings_store.load_settings()

        meta = store.get_table_metadata() if hasattr(store, "get_table_metadata") else {}
        sources = store.list_sources() if meta.get("exists") else []

        return {
            "success": True,
            "chunk_count": meta.get("row_count", 0),
            "source_count": len(sources),
            "fleet_count": len(APPS_CATALOG),
            "provider": settings.get("provider", "none"),
            "model": settings.get("ollama_model") or settings.get("lmstudio_model"),
            "memory": memory_store.get_stats() if hasattr(memory_store, "get_stats") else {},
            "status": "ready" if meta.get("exists") and meta.get("row_count") else "index_empty",
        }
    except Exception as e:
        logger.error(f"Error in api_status: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/health")
async def api_health(request: Request = None):
    """Detailed health check for admin dashboard."""
    store = get_store()
    memory_store = get_memory_store()
    meta = store.get_table_metadata() if hasattr(store, "get_table_metadata") else {}
    sources = store.list_sources() if meta.get("exists") else []

    tool_count = 0
    if request and hasattr(request.app, "state") and hasattr(request.app.state, "mcp"):
        try:
            mcp = request.app.state.mcp
            tools = await mcp.list_tools()
            tool_count = len(tools)
        except Exception:
            logger.warning("Could not list tools for health")

    return {
        "status": "ok",
        "server": "Documentation MCP",
        "version": "1.0.1",
        "uptime_seconds": int(time.time() - _SERVER_START),
        "tool_count": tool_count,
        "providers": {
            "vector_db": {
            "status": "ok" if meta.get("exists") else "empty",
            "chunks": meta.get("row_count", 0),
            "sources": len(sources),
        },
            "memory_store": {"status": "ok" if hasattr(memory_store, "get_stats") else "unavailable"},
            "llm": {"provider": settings_store.load_settings().get("provider", "none")},
        },
    }

@router.post("/chat")
async def api_chat(request: Request):
    """Streaming conversational RAG endpoint (SSE)."""
    body = await request.json()
    question = (body.get("message") or "").strip()
    conversation_id = body.get("conversation_id")
    persona = body.get("persona", "default")
    provider = body.get("provider")
    model = body.get("model")
    api_key = body.get("api_key")
    api_url = body.get("api_url")
    system_prompt_override = body.get("system_prompt")

    if not question:
        raise HTTPException(status_code=400, detail="No message provided")

    s = settings_store.load_settings()

    async def event_stream():
        async for chunk in stream_chat(
            message=question,
            conversation_id=conversation_id,
            persona=persona or "default",
            provider=provider,
            model=model,
            api_key=api_key,
            api_url=api_url,
            system_prompt_override=system_prompt_override,
            search_fn=_search_docs_raw,
            settings=s,
        ):
            yield f"data: {chunk}\n\n"
        yield "data: {\"type\":\"stream_end\"}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@router.get("/auto-discover")
async def api_auto_discover():
    """Scan standard ports for running LLM engines."""
    result = await auto_discover()
    return result

@router.get("/logs")
async def api_logs(limit: int = 100):
    """Serve recent log entries from the in-memory ring buffer."""
    try:
        buf = get_log_buffer()
        if buf is None:
            return {"logs": ["Log buffer not initialized. Server may still be starting."], "source": "buffer"}
        lines = buf.get_logs(limit=limit)
        if not lines:
            return {
                "logs": ["No log entries captured yet. Activity will appear here as tools are called."],
                "source": "buffer",
            }
        return {"logs": lines, "source": "buffer"}
    except Exception as e:
        logger.error(f"Error serving logs: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/tools")
async def api_tools(request: Request):
    """List all registered MCP tools."""
    try:
        mcp = request.app.state.mcp
        tools = await mcp.list_tools()
        return {
            "tools": [{
                "name": t.name,
                "description": t.description or "",
                "parameters": t.parameters.get("properties", {}) if t.parameters else {}
            } for t in tools]
        }
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/execute")
async def api_execute_tool(request: Request):
    """Execute an MCP tool via REST API."""
    try:
        body = await request.json()
        tool_name = body.get("name")
        arguments = body.get("arguments", {})

        if not tool_name:
            raise HTTPException(status_code=400, detail="Tool name missing")

        mcp = request.app.state.mcp
        result = await mcp.call_tool(tool_name, arguments)
        return {"result": result}
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
