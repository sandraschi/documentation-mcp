import logging

from fastmcp import FastMCP

logger = logging.getLogger("docs_mcp.tools.prompts")

def register_tools(mcp: FastMCP):
    """Register MCP prompts."""

    @mcp.prompt(
        name="docs_expert",
        description="Documentation expert instructions.",
        tags={"docs", "expert", "search"},
    )
    def docs_expert(focus: str = "general") -> str:
        """Return system-style instructions for documentation expert behavior."""
        base = (
            "You are a documentation expert for the MCP ecosystem. Use search_docs, ask_docs, and get_document tools. "
            "Always cite sources from results."
        )
        if focus == "search": return base + "\nPrefer search_docs first."
        if focus == "sources": return base + "\nAlways return filenames."
        return base

    @mcp.prompt(
        name="research_workflow",
        description="Multi-step research guidance.",
        tags={"docs", "workflow", "research"},
    )
    def research_workflow() -> str:
        """Return guidance for using the agentic doc workflow."""
        return "To run research, use agentic_doc_workflow(workflow_prompt). Requires client sampling support."
