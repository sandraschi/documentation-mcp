# Docs MCP – System Instructions

## Core capabilities

- **Semantic search**: Find documentation by meaning (FastMCP, MCPB, standards, patterns) via `search_docs(query, limit)`.
- **Synthesized answers**: Get direct answers from the knowledge base with `ask_docs(question)` when the client supports sampling.
- **Full documents**: Fetch complete file content with `get_document(relative_path)` after obtaining paths from search.
- **Agentic workflows**: Run multi-step research with `agentic_doc_workflow(workflow_prompt)`.
- **Webapp**: Launch the Docs webapp (dashboard, chat, settings) with `start_webapp()`.

## Usage patterns

1. **Find by topic**: `search_docs("FastMCP 3.1 prompts and skills", 5)` – use for "where is X documented", "find docs about Y".
2. **Get an answer**: `ask_docs("How do I add a prompt in FastMCP?")` – returns a synthesized answer (requires sampling).
3. **Read full file**: After search returns a `relative_path`, use `get_document(relative_path)`.
4. **Broad research**: `agentic_doc_workflow("Summarize MCPB packaging requirements")` – autonomous report.
5. **Open web UI**: `start_webapp()` – starts backend, frontend, and opens the browser.

## Response format

- Always cite **filename** or **relative_path** from results so the user can open or re-fetch.
- Prefer search first; use ask_docs when the user wants a single synthesized answer.

## Configuration

- No API keys required for local docs. Timeout is configurable in user_config (default 60s).
