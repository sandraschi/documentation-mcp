import logging

from fastmcp import FastMCP

from docs_mcp.backend.store_registry import get_memory_store
from docs_mcp.utils.formatting import _to_markdown

logger = logging.getLogger("docs_mcp.tools.memory")

_READ_ONLY = {"readonly": True}
_MUTATING = {}


def persistence_store_memory(namespace: str, content: str) -> dict:
    """Persist structured memory in a namespace for later semantic recall.

    Stores content under a named namespace for retrieval via persistence_recall.

    ## Return Format
    {"success": bool, "operation": "persistence_store_memory", "message": str,
     "data": {"id": str, "namespace": str}}

    ## Examples
    - persistence_store_memory(namespace="project-alpha", content="Key findings from the MCP audit")
    """
    try:
        memory_store = get_memory_store()
        memory_id = memory_store.store(namespace, content)
        return {
            "success": True,
            "operation": "persistence_store_memory",
            "message": f"Memory stored in namespace '{namespace}'.",
            "data": {"id": memory_id, "namespace": namespace},
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def persistence_recall(namespace: str, query: str, limit: int = 10) -> dict:
    """Semantic search over stored memory in a namespace.

    Retrieves the most semantically relevant memories from the specified namespace.

    ## Return Format
    {"success": bool, "operation": "persistence_recall", "namespace": str,
     "data": list}

    ## Examples
    - persistence_recall(namespace="project-alpha", query="MCP audit findings", limit=5)
    """
    try:
        memory_store = get_memory_store()
        hits = memory_store.recall(namespace, query, limit=limit)
        res = {
            "success": True,
            "operation": "persistence_recall",
            "namespace": namespace,
            "data": hits,
        }
        return {"result": _to_markdown(res, "persistence_recall")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def persistence_compaction_status() -> dict:
    """Report memory density and per-namespace stats.

    Returns statistics about memory usage across all namespaces.

    ## Return Format
    {"success": bool, "operation": "persistence_compaction_status", "data": dict}

    ## Examples
    - persistence_compaction_status()
    """
    try:
        memory_store = get_memory_store()
        stats = memory_store.get_stats()
        return {
            "success": True,
            "operation": "persistence_compaction_status",
            "data": stats,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def register_tools(mcp: FastMCP):
    """Register persistent memory MCP tools."""
    mcp.tool(annotations=_MUTATING, version="1.0.1")(persistence_store_memory)
    mcp.tool(annotations=_READ_ONLY, version="1.0.1")(persistence_recall)
    mcp.tool(annotations=_READ_ONLY, version="1.0.1")(persistence_compaction_status)
