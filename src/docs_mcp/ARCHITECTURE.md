# MCD Integrated RAG Engine: Architecture

The MCP Central Docs (MCD) integrates a dedicated MCP server (`docs_mcp`) for high-performance documentation retrieval and semantic search across the entire repository. This engine leverages SOTA vector search patterns to minimize context-window noise and maximize LLM reasoning accuracy.

## ðŸ› ï¸ Tech Stack
- **Vector Database**: [LanceDB](https://lancedb.com/) (Serverless, disk-based vector storage).
- **Embeddings**: `BAAI/bge-small-en-v1.5` via [FastEmbed](https://github.com/qdrant/fastembed).
- **Orchestration**: FastMCP 3.1.1+.4+ (Python Substrate).
- **Logic Location**: `src/docs_mcp/backend/rag_core.py`.

## ðŸ§¬ Semantic Search Pipeline

### 1. Ingestion Phase (`ingestor.py`)
- **Parsing**: Markdown and code files are parsed, preserving hierarchy and metadata.
- **Chunking**: Overlapping semantic chunks ensure context preservation across boundaries.
- **Embedding**: Documents are converted into 384-dimensional vectors.
- **Persistence**: Vectors and metadata are stored in a specialized LanceDB table.

### 2. Retrieval Phase (`rag_core.py`)
- **Query Embedding**: The incoming natural language query is embedded using the same BGE model.
- **Vector Search**: LanceDB performs a high-speed cosine similarity search.
- **Pre-filtering**: Optional metadata filters (e.g., project scope, file type) are applied before vector retrieval to reduce the search space.

### 3. Synthesis (Client-side)
- The retrieved context chunks are returned to the calling LLM (Antigravity/Claude).
- The LLM synthesizes the final answer using the high-density documentation context.

## ðŸš€ Performance Features
- **Zero-Latency Search**: Sub-50ms retrieval on 10,000+ document chunks.
- **RTX 4090 Optimization**: GPU-accelerated embedding generation during ingestion.
- **Hybrid Ready**: Architected for future hybrid search (Keyword + Semantic) integration.

## ðŸŒ Web Stack (Docs MCP Webapp)
- **Frontend**: Vite/React in `web_sota/`; dev server on port **11032**.
- **Backend**: Starlette app in `src/docs_mcp/server.py`; uvicorn on port **11033** (`DOCS_MCP_PORT`).
- **Proxy**: Vite proxies `/api` → `http://127.0.0.1:11033`. Private mcp-central-docs uses **10794/10795**.

---
*Maintained by: Antigravity AI*
*Category: Architecture / Substrate*

