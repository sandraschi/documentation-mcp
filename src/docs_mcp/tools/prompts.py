"""MCP prompts and resources for documentation-mcp."""
import logging
from pathlib import Path

from fastmcp import FastMCP

logger = logging.getLogger("docs_mcp.tools.prompts")


def register_tools(mcp: FastMCP):
    """Register MCP prompts and resources."""

    # -- Prompts --

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
        if focus == "search":
            base += "\nPrefer search_docs first."
        if focus == "sources":
            base += "\nAlways return filenames."
        return base

    @mcp.prompt(
        name="research_workflow",
        description="Multi-step research guidance.",
        tags={"docs", "workflow", "research"},
    )
    def research_workflow() -> str:
        """Return guidance for using the agentic doc workflow."""
        return "To run research, use agentic_doc_workflow(workflow_prompt). Requires client sampling support."

    # -- Resources --

    @mcp.resource("resource://docs/capabilities")
    def resource_capabilities() -> str:
        """Overview of the Documentation MCP server capabilities."""
        return (
            "# Documentation MCP Capabilities\n\n"
            "## Tools\n"
            "- `search_docs` - semantic search across indexed docs\n"
            "- `ask_docs` - LLM-synthesized answers (sampling or local LLM)\n"
            "- `get_document` - retrieve full document content\n"
            "- `reindex_docs` - force full re-index\n"
            "- `chunk_stats` - index health metrics\n"
            "- `server_status` - server health + memory\n"
            "- `agentic_doc_workflow` - autonomous research (sampling)\n"
            "- `show_server_status_card` - Prefab status card\n"
            "- `search_docs_card` - Prefab search results\n\n"
            "## Prompts\n"
            "- `docs_expert` - expert documentation agent\n"
            "- `research_workflow` - multi-step research\n\n"
            "## Resources\n"
            "- `resource://docs/capabilities` - this document\n"
            "- `resource://docs/skills` - installed skills\n"
            "- `resource://docs/status` - live server status"
        )

    @mcp.resource("resource://docs/skills")
    def resource_skills() -> str:
        """List skills installed on this server."""
        skills_dir = Path(__file__).resolve().parent.parent / "skills"
        if not skills_dir.is_dir():
            return "No skills installed."

        lines = ["# Installed Skills\n"]
        for subdir in sorted(skills_dir.iterdir()):
            if not subdir.is_dir():
                continue
            skill_md = subdir / "SKILL.md"
            if not skill_md.is_file():
                continue
            name = subdir.name
            lines.append(f"- `skill://{name}/SKILL.md` — {name}")
            with open(skill_md, encoding="utf-8") as f:
                content = f.read()
            lines.append("")
            lines.append(content)
            lines.append("---")
        return "\n".join(lines)

    @mcp.resource("resource://docs/status")
    def resource_status() -> str:
        """Live server status."""
        from docs_mcp.backend.store_registry import get_store

        store = get_store()
        meta = store.get_table_metadata() if hasattr(store, "get_table_metadata") else {}
        sources = store.list_sources() if meta.get("exists") else []
        chunk_count = meta.get("row_count", 0) if meta.get("exists") else 0

        return (
            f"# Server Status\n\n"
            f"- **Status**: {'ready' if chunk_count > 0 else 'index_empty'}\n"
            f"- **Chunks**: {chunk_count}\n"
            f"- **Sources**: {len(sources)}\n"
            f"- **Embedding**: BAAI/bge-small-en-v1.5\n"
            f"- **Port**: 11033\n"
        )
