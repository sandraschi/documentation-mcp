---
name: Docs Research
description: Use MCP Central Docs server to search, ask, and retrieve documentation (FastMCP, standards, packaging).
---

# Docs Research Skill

**Description:** Fleet documentation research via MCP Central Docs server. Covers doc set indexing, semantic search across documentation repos, cross-repository queries, fleet standards navigation, and autonomous multi-doc research workflows.

## Trigger Phrases

- "Find docs about [topic]"
- "Search the fleet documentation for [concept]"
- "How do I [task] according to fleet standards?"
- "What does the standard say about [pattern]?"
- "Show me the documentation for [tool/system]"
- "Research best practices for [technology]"
- "Summarize all standards related to [topic]"
- "What changed in the latest version of [doc]?"

## Tools

- **`search_docs(query, limit)`** — Semantic search over indexed documentation. Use for "find docs about X", "where is Y documented". Returns ranked results with snippet and `relative_path`.
- **`ask_docs(question)`** — Get a synthesized answer from the docs (requires client sampling). Use for questions that need synthesis across multiple doc files.
- **`get_document(relative_path)`** — Fetch full file content after you have a path from `search_docs`. Always prefer this for reading entire standards or guides.
- **`agentic_doc_workflow(workflow_prompt)`** — Autonomous multi-step research. Pass a goal string like "Research all onboarding docs and create a summary". Chains search → get_document → ask_docs.
- **`reindex_docs()`** — Force re-indexing after doc changes. Run when new docs are added or existing docs are updated.
- **`chunk_stats()`** — Index health: total chunks, doc count, embedding model, last indexed timestamp.
- **`start_webapp()`** — Start the Docs webapp (backend + frontend + open browser).

## Workflow

1. **Search first**: Prefer `search_docs` with a clear, specific query. Use `limit` to control result breadth (default 10, increase for research surveys).
2. **Deep read**: Use `get_document(relative_path)` when a snippet isn't enough. Always include `filename` or `relative_path` from results for traceability.
3. **Synthesis**: Use `ask_docs` when the user wants a direct answer and the client supports sampling. Best for cross-document questions.
4. **Broad research**: Use `agentic_doc_workflow` or the `research_workflow` prompt for comprehensive multi-topic research tasks.
5. **Index maintenance**: Run `reindex_docs()` after any doc changes. Check `chunk_stats()` to verify index health.

## Citing Sources

Always include `filename` or `relative_path` from results so the user can open or re-fetch the doc. Format: `[filename](relative_path)` for clickable references.

## Indexed Content

The docs index covers: FastMCP standards, MCPB packaging, fleet workflow rules, SOTA patterns, port allocation registry, tool registration protocols, docstring standards, architectural guidelines, PowerShell conventions, and per-repo AGENTS.md files.

## Examples

- "Find the standard for MCP tool registration." → `search_docs(query="MCP tool registration", limit=5)` → `get_document(relative_path="standards/rules/mcp_registration.md")`
- "What are the fleet port allocation rules?" → `ask_docs(question="What port range is reserved for fleet webapps and which ports are forbidden?")`
- "Research all onboarding docs." → `agentic_doc_workflow(workflow_prompt="Find all onboarding and quickstart documents and create a summary guide")`
