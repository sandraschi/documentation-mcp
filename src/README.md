# Backend Engine: Federated RAG

The `docs-mcp` backend is a Python-based FastMCP server that provides semantic search and intelligent document synthesis.

## Technical Architecture

### 1. Federated Ingestor
Located in `docs_mcp.backend.ingestor`, the engine implements a multi-root discovery logic:
- **Internal**: Scans the local `./docs` directory.
- **Federated**: Probes for sibling repositories (e.g., `advanced-memory-mcp`). If found, it automatically merges their `/knowledge` and `/notes` into the unified index.

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
- `DOCS_ROOT`: Primary document source.
- `ADVANCED_MEMORY_PATH`: Federated search root.

## Development
- **Dependencies**: Managed via `uv`.
- **Testing**: Run `uv run pytest` to execute the integration suite.
- **Port Management**: Backend **11033**, frontend **11032** (mcp-central-docs private hub: 10794/10795).
