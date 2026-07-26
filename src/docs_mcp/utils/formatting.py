import json
import logging

logger = logging.getLogger("docs_mcp.utils.formatting")


def _to_markdown(data: dict, operation: str) -> str:
    """Universal formatter to convert tool-specific dicts into high-fidelity Markdown."""
    if not data or not data.get("success"):
        return f"### ❌ Error: {data.get('message', 'Unknown error')}"

    lines = []
    if operation == "search_docs":
        query = data.get("query", "Search Results")
        results = data.get("data", [])
        lines.append(f"# 🔍 Documentation Search: {query}")
        lines.append(f"*Found {len(results)} relevant snippets*\n")
        for r in results:
            lines.append(f"### 📄 {r['filename']}")
            lines.append(f"- **Path**: `{r['relative_path']}`")
            lines.append(f"- **Relevance**: `{r['score']:.2f}`")
            lines.append(f"\n> {r['content'].strip()}\n")
            lines.append("---")
        if data.get("next_steps"):
            lines.append("\n**Next Steps**:")
            for step in data["next_steps"]:
                lines.append(f"- {step}")

    elif operation == "ask_docs":
        question = data.get("question", "Question")
        answer = data.get("data", {}).get("answer", "No answer synthesized.")
        sources = data.get("data", {}).get("sources", [])
        lines.append(f"# 🤖 AI Synthesis: {question}\n")
        lines.append(answer)
        if sources:
            lines.append("\n---")
            lines.append("### 📚 Sources")
            for s in sources:
                lines.append(f"- {s}")
        if data.get("next_steps"):
            lines.append("\n**Next Steps**:")
            for step in data["next_steps"]:
                lines.append(f"- {step}")

    elif operation == "chunk_stats":
        lines.append("# 📊 Documentation Index Statistics")
        lines.append(f"- **Total Sources**: {data['data']['source_count']}")
        lines.append(f"- **Embedding Model**: `{data['data']['embedding_model']}`")
        if data["data"].get("sources"):
            lines.append("\n### 📂 Indexed Sources (Sample)")
            for s in data["data"]["sources"][:10]:
                lines.append(f"- {s}")

    elif operation == "server_status":
        index = data.get("index", {})
        status = data.get("status", "unknown").upper()
        lines.append(f"# 🩺 Docs MCP Server Status: {status}")
        lines.append(f"- **Version**: `{data.get('version', '1.0.0')}`")
        lines.append(f"- **Chunks Indexed**: `{index.get('chunk_count', 0)}`")
        lines.append(f"- **Source Count**: `{index.get('source_count', 0)}`")
        if data.get("memory"):
            lines.append(f"- **Memory Entries**: `{data['memory'].get('total_entries', 0)}`")

    elif operation == "persistence_recall":
        namespace = data.get("namespace", "default")
        hits = data.get("data", [])
        lines.append(f"# 🧠 Memory Recall: {namespace}")
        lines.append(f"*Retrieved {len(hits)} relevant memory entries*\n")
        for h in hits:
            date_str = h.get("created_at", "unknown date")
            lines.append(f"#### 📅 {date_str} (Score: {h.get('score', 0):.2f})")
            lines.append(f"> {h.get('content', '').strip()}\n")
            lines.append("---")

    elif operation == "query_releasebot":
        product = data.get("product_slug", "Product")
        releases = data.get("releases", [])
        url = data.get("url", "")
        lines.append(f"# 🚀 Latest Releases: {product.title()}")
        if url:
            lines.append(f"[View Full Feed]({url})\n")
        if not releases:
            lines.append("*No recent releases found.*")
        for rel in releases:
            lines.append(f"- **{rel['date']}**: {rel['headline']}")

    elif operation == "reindex_docs":
        lines.append("# 🔄 Documentation synchronized")
        lines.append(f"- **Chunks Indexed**: `{data['data']['chunks']}`")
        if data.get("next_steps"):
            lines.append("\n**Next Steps**:")
            for step in data["next_steps"]:
                lines.append(f"- {step}")

    elif operation == "docs_help":
        lines.append("# 📖 Docs MCP Help")
        lines.append(f"{data['server']['description']}\n")
        lines.append("### 🛠️ Available Tools (by group)")
        for group, tools in data["tools_by_group"].items():
            lines.append(f"\n#### {group.replace('_', ' ').title()}")
            for t in tools:
                lines.append(f"- **{t['name']}**: {t['description']}")

        lines.append("\n### 📂 Documentation Index Summary")
        lines.append(f"- **Sources**: {data['index_summary']['source_count']}")
        lines.append(f"- **Total Chunks**: {data['index_summary']['chunk_count']}")

    else:
        # Generic fallback
        lines.append(f"# Output: {operation.replace('_', ' ').title()}")
        lines.append(data.get("message", ""))
        if "data" in data:
            lines.append(f"\n```json\n{json.dumps(data['data'], indent=2)}\n```")

    return "\n".join(lines)


def log_to_file(msg: str):
    """Fallback file logging for debug diagnostics."""
    try:
        with open("debug.log", "a") as f:
            f.write(msg + "\n")
    except Exception:  # noqa: S110
        pass
