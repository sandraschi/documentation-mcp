"""Prefab UI card builders for documentation-mcp."""
import logging

from fastmcp import FastMCP
from prefab_ui.components import Card, CardContent, CardHeader, CardTitle, Metric, Text

logger = logging.getLogger("docs_mcp.prefab")


def register_prefab_cards(mcp: FastMCP):
    """Register app-enabled Prefab card tools for list/status surfaces."""

    @mcp.tool(app=True, annotations={"readonly": True}, version="1.0.0")
    async def show_server_status_card(ctx) -> dict:
        """Show server status as a rich Prefab card.

        ## Return Format
        ToolResult with structured PrefabApp showing server KPIs.
        """
        from docs_mcp.backend.store_registry import get_store

        store = get_store()
        meta = store.get_table_metadata() if hasattr(store, "get_table_metadata") else {}
        sources = store.list_sources() if meta.get("exists") else []
        chunk_count = meta.get("row_count", 0) if meta.get("exists") else 0

        with Card(css_class="max-w-lg") as card:
            with CardHeader():
                CardTitle("Server Status")
            with CardContent():
                Metric("Chunks Indexed", str(chunk_count), "Documentation chunks")
                Metric("Sources", str(len(sources)), "Verified sources")
                Metric("Status", "Active", "Backend operational")
                Text("LanceDB + FastEmbed (BAAI/bge-small-en-v1.5)")

        return {
            "content": f"Server healthy. {chunk_count} chunks from {len(sources)} sources.",
            "structured_content": card,
        }

    @mcp.tool(app=True, annotations={"readonly": True}, version="1.0.0")
    async def search_docs_card(query: str, limit: int = 5) -> dict:
        """Search documentation and show results as a Prefab card.

        ## Return Format
        ToolResult with structured PrefabApp showing search results.

        ## Examples
        - search_docs_card(query="Playwright e2e standards")
        - search_docs_card(query="portmanteau pattern", limit=3)
        """
        from docs_mcp.backend.store_registry import get_store

        store = get_store()
        results = store.search(query, limit=limit)

        items = []
        for r in results:
            distance = r.get("_distance", 0.0)
            score = max(0.0, 1.0 - distance)
            items.append({
                "title": r["metadata"].get("filename", "unknown"),
                "score": f"{score:.2f}",
                "path": r["metadata"].get("relative_path", ""),
                "snippet": r["content"][:300],
            })

        if not items:
            with Card(css_class="max-w-lg") as card:
                with CardHeader():
                    CardTitle("No Results")
                with CardContent():
                    Text(f"No documentation found for '{query}'.")
            return {
                "content": f"No results for '{query}'.",
                "structured_content": card,
            }

        with Card(css_class="max-w-lg") as card:
            with CardHeader():
                CardTitle(f"Search Results: {len(items)}")
            with CardContent():
                for item in items:
                    with Card(css_class="border-l-2 border-primary/30 pl-2 mb-2"):
                        with CardHeader():
                            CardTitle(item["title"])
                        Text(f"Score: {item['score']}  Path: {item['path']}")
                        Text(item["snippet"][:200])

        return {
            "content": f"Found {len(items)} results for '{query}'.",
            "structured_content": card,
        }
