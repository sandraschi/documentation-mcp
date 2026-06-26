# Backend Engine: Documentation RAG

The `docs-mcp` backend is a Python-based FastMCP server that provides semantic search and intelligent document synthesis.

## Technical Architecture

### 1. Document Ingestor
Located in `docs_mcp.backend.ingestor`:
- **Primary**: Scans `documentation-mcp/docs` (override with `DOCS_ROOT` only when needed).
- **Optional**: `DOCS_FEDERATE_MEMORY=1` merges `advanced-memory-mcp/knowledge` and `notes`.
- **Optional**: `DOCS_EXTRA_PATHS` adds comma-separated extra markdown roots (not `mcp-central-docs` by default).

### 2. Vector Store
Uses **LanceDB** with **FastEmbed** for local, high-performance vector retrieval.
- **Default Model**: `BAAI/bge-small-en-v1.5`
- **Indexing**: Optimized for markdown chunking with frontmatter awareness.

### 3. Agentic Tools
Exposes several high-tier tools:
- `search_docs`: Core semantic retrieval.
- `ask_docs`: Multi-step synthesis using local LLM sampling (Ollama/LM Studio).
- `agentic_doc_workflow`: Autonomous research orchestration.

## Configuration
Settings are managed in `backend/config.py` and persisted in `backend/settings_store.py`. Key paths:
- `DOCS_ROOT`: Primary document source (defaults to repo `docs/`).
- `DOCS_FEDERATE_MEMORY`: Set to `1` to include Advanced Memory paths.
- `DOCS_EXTRA_PATHS`: Comma-separated extra markdown directories (merged with webapp Settings → Extra RAG paths).
- **Webapp Settings**: `rag_extra_paths` (one path per line) and `rag_federate_memory` checkbox.

## Development
- **Dependencies**: Managed via `uv`.
- **Testing**: Run `uv run pytest` to execute the integration suite.
- **Port Management**: Backend **11033**, frontend **11032** (mcp-central-docs private hub: 10794/10795).
