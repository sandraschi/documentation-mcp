import logging
from fastmcp import FastMCP
from docs_mcp.backend.store_registry import get_memory_store
from docs_mcp.utils.formatting import _to_markdown

logger = logging.getLogger("docs_mcp.tools.memory")

def register_memory_tools(mcp: FastMCP):
    """Register persistent memory MCP tools."""

    @mcp.tool()
    def persistence_store_memory(namespace: str, content: str) -> dict:
        """Persist structured memory in a namespace for later semantic recall."""
        try:
            memory_store = get_memory_store()
            memory_id = memory_store.store(namespace, content)
            return {
                "success": True,
                "operation": "persistence_store_memory",
                "message": f"Memory stored in namespace '{namespace}'.",
                "data": {"id": memory_id, "namespace": namespace}
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    def persistence_recall(namespace: str, query: str, limit: int = 10) -> dict:
        """Semantic search over stored memory in a namespace."""
        try:
            memory_store = get_memory_store()
            hits = memory_store.recall(namespace, query, limit=limit)
            res = {
                "success": True,
                "operation": "persistence_recall",
                "namespace": namespace,
                "data": hits
            }
            return {"result": _to_markdown(res, "persistence_recall")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    def persistence_compaction_status() -> dict:
        """Report memory density and per-namespace stats."""
        try:
            memory_store = get_memory_store()
            stats = memory_store.get_stats()
            return {
                "success": True,
                "operation": "persistence_compaction_status",
                "data": stats
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
