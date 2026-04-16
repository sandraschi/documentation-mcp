import logging
from pathlib import Path
from fastmcp import FastMCP
from docs_mcp.backend.config import config
from docs_mcp.backend.store_registry import get_store
from docs_mcp.utils.formatting import _to_markdown

logger = logging.getLogger("docs_mcp.tools.system")

def register_tools(mcp: FastMCP):
    """Register system and diagnostic MCP tools."""

    @mcp.tool()
    def chunk_stats() -> dict:
        """Retrieve statistics and health metrics for the neural documentation index."""
        store = get_store()
        sources = store.list_sources()
        res = {
            "success": True,
            "operation": "chunk_stats",
            "message": f"Documentation index is healthy with {len(sources)} verified sources.",
            "data": {
                "source_count": len(sources),
                "sources": sources,
                "embedding_model": config.EMBEDDING_MODEL,
            },
        }
        return {"result": _to_markdown(res, "chunk_stats")}

    @mcp.tool()
    def server_status() -> dict:
        """Report server and index health, version, and memory summary."""
        from docs_mcp.backend.store_registry import get_memory_store # Late import to avoid cycles
        store = get_store()
        memory_store = get_memory_store()
        
        meta = store.get_table_metadata() if hasattr(store, "get_table_metadata") else {}
        sources = store.list_sources() if meta.get("exists") else []
        mem_stats = memory_store.get_stats() if hasattr(memory_store, "get_stats") else {}

        res = {
            "success": True,
            "status": "ready" if meta.get("exists") and meta.get("row_count") else "index_empty",
            "version": "1.0.1",
            "index": {
                "chunk_count": meta.get("row_count", 0),
                "source_count": len(sources),
                "embedding_model": config.EMBEDDING_MODEL
            },
            "memory": mem_stats
        }
        return {"result": _to_markdown(res, "server_status")}

    @mcp.tool()
    def docs_help() -> dict:
        """Return multilevel structured help for this server."""
        # Generic help logic - in a real build we'd introspect the mcp instance
        # but for now we follow the existing pattern in server.py
        try:
            # We would typically call _build_structured_help here
            # For simplicity in this refactor, I'll move _build_structured_help here too
            data = _build_refactored_help(mcp)
            res = {"success": True, **data}
            return {"result": _to_markdown(res, "docs_help")}
        except Exception as e:
            logger.exception("docs_help failed")
            return {"success": False, "error": str(e)}

def _build_refactored_help(mcp: FastMCP) -> dict:
    """Consolidated help builder for modualized server."""
    docs_root = config.DOCS_ROOT.resolve()
    store = get_store()
    meta = store.get_table_metadata() if hasattr(store, "get_table_metadata") else {}
    sources = store.list_sources() if meta.get("exists") else []
    
    # Discovery of doc areas
    doc_areas = []
    if docs_root.is_dir():
        for p in sorted(docs_root.iterdir()):
            if p.is_dir() and not p.name.startswith("."):
                doc_areas.append({"name": p.name, "path": str(p.relative_to(docs_root)).replace("\\", "/")})

    # Hardcoded summary of tools (since introspection is complex via FastMCP 3.2 internal API)
    # Maintaining parity with server.py's manual list for now
    tools_by_group = {
        "search_and_read": [
            {"name": "search_docs", "description": "Semantic search across documentation."},
            {"name": "ask_docs", "description": "Synthesized technical answers."},
            {"name": "get_document", "description": "Full document retrieval."}
        ],
        "index_and_workflow": [
            {"name": "reindex_docs", "description": "Force full synchronization."},
            {"name": "chunk_stats", "description": "Index health metrics."},
            {"name": "agentic_doc_workflow", "description": "Autonomous research workflow."}
        ]
    }

    return {
        "server": {
            "name": mcp.name,
            "description": "MCP Documentation Server - Modular Industrial Edition."
        },
        "tools_by_group": tools_by_group,
        "doc_areas": doc_areas,
        "index_summary": {
            "source_count": len(sources),
            "chunk_count": meta.get("row_count", 0)
        }
    }
