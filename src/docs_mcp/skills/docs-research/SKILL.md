---
name: Docs Research
description: Use MCP Central Docs server to search, ask, and retrieve documentation (FastMCP, standards, packaging).
---

# Docs Research Skill

Use this skill when you need to search or navigate the MCP Central Docs knowledge base (FastMCP, MCPB, standards, patterns).

## Tools to use

- **search_docs(query, limit)** – Semantic search. Use for "find docs about X", "where is Y documented".
- **ask_docs(question)** – Get a synthesized answer from the docs (requires client sampling).
- **get_document(relative_path)** – Fetch full file content after you have a path from search.
- **agentic_doc_workflow(workflow_prompt)** – Autonomous multi-step research; pass a goal string.
- **reindex_docs()** – Force re-indexing after doc changes.
- **chunk_stats()** – Index health and chunk counts.
- **start_webapp()** – Start the Docs webapp (backend + frontend + browser).

## Workflow

1. Prefer **search_docs** first with a clear query.
2. Use **get_document** when a snippet isn’t enough and you have the `relative_path`.
3. Use **ask_docs** when the user wants a direct answer and the client supports sampling.
4. Use **research_workflow** prompt or **agentic_doc_workflow** for broad research tasks.

## Citing sources

Always include `filename` or `relative_path` from results so the user can open or re-fetch the doc.
