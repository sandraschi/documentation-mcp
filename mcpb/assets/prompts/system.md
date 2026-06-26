# documentation-mcp — MCP Server Capabilities

## Server Overview

Documentation MCP is a federated RAG (Retrieval-Augmented Generation) documentation server that provides semantic search, question answering, and autonomous research across a managed documentation corpus. It indexes local documentation files (Markdown, code comments, specification documents) into a LanceDB vector store with embeddings, then exposes tools for searching, retrieving full documents, asking complex questions with LLM-synthesized answers (using host sampling or local Ollama/LM Studio fallback), and executing autonomous multi-step research workflows. The server also maintains a persistent memory store for cross-session knowledge retention, a releasebot integration for querying recent product releases, and a webapp for file browsing.

The server is built on FastMCP with both stdio transport (for Claude Desktop) and a FastAPI HTTP control plane (for the web dashboard) running on ports 11032 (frontend) and 11033 (backend). It uses a modular architecture with separate tool registration for RAG operations, system diagnostics, workflow orchestration, prompt templates, and persistent memory. The documentation index supports multiple embedding models via FastEmbed, with the ability to reindex on demand.

## Tools

### Search and Retrieval

**search_docs** — Semantic search across all indexed documentation.
- Parameters: query (str, required) — Natural language search query. limit (int, optional, default 5) — Max snippets to return.
- Returns: {success, message, data: [{filename, score, content, relative_path}]}
- Uses LanceDB vector similarity search with BAAI/bge-small-en-v1.5 embeddings.

**ask_docs** — Ask a complex question and get an LLM-synthesized answer from the documentation.
- Parameters: question (str, required) — Technical question to answer.
- Returns: {success, message, data: {answer, sources: [filename]}}
- Fallback chain: host sampling (ctx.sample) > local Ollama > local LM Studio > clear error.
- Retrieves top 10 relevant chunks before synthesis.

**get_document** — Retrieve the full content of a documentation file by its relative path.
- Parameters: relative_path (str, required) — Path relative to docs root (e.g., "standards/AGENT_PROTOCOLS.md").
- Returns: {success, message, data: {content, path, size, modified}}
- Enforces path traversal protection — rejects paths that resolve outside the docs root.

**query_releasebot** — Query recent releases for a product via public Releasebot pages.
- Parameters: product_slug (str, required) — Feed slug (e.g., "cursor", "zed", "notion"). limit (int, optional, default 5).
- Returns: {success, message, url, releases: [{date, headline}]}
- Scrapes public releasebot.io HTML (no API key required).

### Index Management

**reindex_docs** — Force a full scan and re-indexing of all documentation sources.
- Parameters: None
- Returns: {success, message, data: {chunks: int}}
- Scans all files in the docs root and configured extra paths, chunks them, embeds, and replaces the index.

**chunk_stats** — Statistics and health metrics for the neural documentation index.
- Returns: {success, message, data: {source_count, sources, embedding_model}}
- Lists all indexed sources with their chunk counts.

**server_status** — Report server and index health, version, and memory summary.
- Returns: {status, version, index: {chunk_count, source_count, embedding_model}, memory: {namespaces, entries}}

**docs_help** — Multilevel structured help for this server.
- Returns: {server, tools_by_group, prompts, skills, doc_areas, index_summary}

### Persistent Memory

**persistence_store_memory** — Persist structured memory in a namespace for later semantic recall.
- Parameters: namespace (str, required) — Logical bucket (e.g., "email-mcp", "robofang"). content (str, required) — Text to store.
- Returns: {success, data: {id, namespace, created_at}}

**persistence_recall** — Semantic search over stored memory in a namespace.
- Parameters: namespace (str, required), query (str, required), limit (int, optional, default 10).
- Returns: {success, data: [{content, created_at, score, id}]}

**persistence_compaction_status** — Report memory density and per-namespace stats; suggests when to compact.
- Returns: {success, total_entries, namespaces, entries_per_namespace, suggestion}

### Agentic Workflow

**agentic_doc_workflow** — Execute autonomous documentation research and report generation.
- Parameters: workflow_prompt (str, required) — The research goal.
- Uses ctx.sample() to have the LLM autonomously search and synthesize documentation content.

**start_webapp** — Start the Documentation MCP webapp fully automatically.
- Returns: {success, message, url: "http://localhost:11032"}
- Runs web_sota/start.ps1 with -Automated flag.

### Prompts

**docs_expert** — System-style instructions for documentation expert behavior.
- Parameter: focus (str, optional) — "general", "search", or "sources".
- Returns: Context-aware instructions for the LLM agent.

**research_workflow** — Multi-step research guidance prompt.
- Returns: Instructions for using agentic_doc_workflow.

## Configuration

**Environment Variables:**
- DOCS_ROOT — Root directory for documentation content (default: repo's docs/ directory)
- DOCS_EXTRA_PATHS — Comma-separated additional paths to include in the index
- EMBEDDING_MODEL — FastEmbed model name (default: BAAI/bge-small-en-v1.5)
- OLLAMA_URL — Ollama server URL for fallback LLM (default: http://localhost:11434)
- LMSTUDIO_URL — LM Studio server URL (default: http://localhost:1234/v1)
- MCP_BRIDGE_URLS — Comma-separated URLs for MCP bridge proxy federation
- WEB_PORT, API_PORT — Web dashboard ports (defaults: 11032/11033)
- LOG_LEVEL — Logging verbosity (default: INFO)

**Data Directories:**
- LanceDB index: data/lancedb/
- Memory store: data/memory/
- Cache: data/cache/

## Data Sources

- **Local documentation files** — Markdown documents, code comments, specification files in the docs root
- **LanceDB vector store** — Embedded chunks for semantic similarity search
- **Memory store** — Persisted cross-session knowledge with namespaced semantic recall
- **Releasebot public pages** — Scraped release notes from releasebot.io
- **MCP bridge proxies** — Federated multi-server queries via MCP_BRIDGE_URLS

## Integration Points

- **FastMCP** — stdio (Claude Desktop) + FastAPI HTTP control plane
- **LanceDB** — Local vector database for semantic search
- **FastEmbed (BAAI/bge-small-en-v1.5)** — Embedding model for document chunks
- **Ollama / LM Studio** — Local LLM fallback for answer synthesis
- **Host Sampling (ctx.sample)** — Preferred LLM path when available
- **Web Dashboard** — FastAPI + React frontend on ports 11032/11033
- **Releasebot.io** — Public release tracking for software products

## Advanced RAG Architecture

### Indexing Pipeline
The documentation indexing pipeline transforms source files into searchable vector embeddings through a multi-stage process:

1. **File Discovery** — The ContentIngestor scans the configured DOCS_ROOT directory recursively for Markdown, text, and code files. Hidden files and binary formats are automatically excluded. Additional paths from DOCS_EXTRA_PATHS are merged into the discovery set.

2. **Content Chunking** — Each discovered file is split into overlapping chunks of approximately 512 tokens with 50-token overlap. Chunk boundaries respect markdown section headers (##, ###) and paragraph breaks to maintain semantic coherence. Large files (100+ KB) generate proportionally more chunks.

3. **Embedding Generation** — Each chunk is embedded using the configured FastEmbed model (default: BAAI/bge-small-en-v1.5, 384-dimensional vectors). The embedding model runs entirely locally using ONNX runtime — no external API calls or data leaving the machine. Chunks and their embeddings are stored in the LanceDB vector database.

4. **Index Storage** — LanceDB stores the vectors in a columnar format optimized for Approximate Nearest Neighbor (ANN) search. The index includes metadata for each chunk: source filename, relative path within the docs root, file modification timestamp, and chunk position. The index supports configurable distance metrics (cosine similarity by default) with automatic index optimization as data grows.

5. **Scheduled Reindexing** — The reindex_docs tool performs a full re-index from scratch, replacing the previous index atomically. The reindex operation is safe to run while other tools are being called — the old index remains available until the new one is fully constructed.

### Search Execution
When a search query arrives:
1. The query string is embedded using the same model as the index (BAAI/bge-small-en-v1.5)
2. LanceDB performs ANN search with configurable limit (default 5 results)
3. Results are scored by cosine distance (converted to a 0-1 similarity score where 1.0 = perfect match)
4. Each result includes the source filename, content snippet, similarity score, and relative path for direct file access
5. Results are returned sorted by score descending

### LLM Answer Synthesis
The ask_docs tool follows a fallback chain for LLM synthesis:
1. **Host Sampling (ctx.sample)** — Preferred path. Uses the MCP host's connected LLM (e.g., Claude in Claude Desktop) via the FastMCP sampling protocol. This provides the highest quality synthesis without additional configuration.
2. **Ollama (local)** — If host sampling is unavailable (returns a sampling error), the server auto-discovers Ollama at http://localhost:11434. It queries available models and selects one by priority: qwen2.5, llama3.2, phi4, gemma. The chosen model synthesizes the answer from the retrieved documentation context.
3. **LM Studio (local)** — If Ollama is not available, the server checks LM Studio at http://localhost:1234/v1. It uses the first available model via the OpenAI-compatible API endpoint.
4. **Clear Error** — If no LLM is available, returns the raw search results with a clear message explaining that synthesis requires a local LLM or host sampling support.

### Persistent Memory System
The memory system provides cross-session knowledge retention with the following architecture:
- **Namespaces** — Each memory entry belongs to a namespace, acting as a logical bucket for related content. Namespaces are created on first store and never need pre-registration. Example namespaces: "email-mcp", "project-x", "docker-mcp", "security-research", "fleet-notes".
- **Storage** — Memories are stored in a dedicated LanceDB table with the same embedding model as the documentation index. Each memory entry has: namespace, content, created_at timestamp, and embedding vector.
- **Recall** — The persistence_recall tool searches within a single namespace using semantic similarity. The query is embedded and compared against all entries in that namespace, returning the top matches with scores.
- **Compaction** — The persistence_compaction_status tool reports memory usage statistics per namespace, including entry count and density metrics. When a namespace has many entries, the tool suggests compaction through summarization.

### Releasebot Integration
The query_releasebot tool scrapes public Releasebot HTML pages (releasebot.io) to discover recent software releases without requiring any API key. Supported product slugs include:
- Development tools: cursor, zed, vscode, windsurf, claude, raycast, warp
- Platforms: notion, figma, docker, obsidian, linear
- AI companies: anthropic, openai

The scraper parses the Releasebot page for each product and returns the most recent N release entries with dates and headlines. If a slug is unknown, the tool returns a pointer to the alphabetical slug directory at https://releasebot.io/updates/alphabetical.

### Webapp Integration
The Documentation MCP webapp provides a graphical browser for the documentation corpus. The start_webapp tool automates launching it:
1. Finds web_sota/start.ps1 in the repo root
2. Executes it with -Automated flag in a new console window
3. The script clears zombie ports on 11032 (frontend) and 11033 (backend)
4. Starts the Python FastAPI backend and Vite React frontend
5. Opens the default browser to http://localhost:11032

The webapp features include documentation tree browsing, full-text search, file content viewer with syntax highlighting, and settings for configuring the documentation root and LLM providers.

### Fleet Discovery and Bridge Integration
The server supports MCP_BRIDGE_URLS for connecting to other MCP servers in the fleet. Configure comma-separated URLs and the server creates proxy providers that expose the bridged servers' tools through the same FastMCP instance. This enables multi-server documentation queries and cross-repository RAG.

## Error Handling

- Docs not found: `{"success": false, "error": "File not found"}`
- Path traversal attempt: `{"success": false, "error": "Access denied"}`
- Index empty: `{"status": "index_empty", "message": "No documents indexed yet"}`
- No results: `{"success": false, "message": "No documentation found for query"}`
- Sampling unavailable: Automatic fallback to Ollama, then LM Studio
- Workflow without sampling: `{"success": false, "message": "Sampling required"}`

## Index Time and File Processing

The documentation index processes all supported files in the configured DOCS_ROOT directory recursively. The following file types are supported: .md (Markdown, with section-header-aware chunking), .txt (plain text, chunked by paragraph breaks), .py (Python code, chunked by function and class boundaries), .js/ts (JavaScript/TypeScript code, chunked by function boundaries), .yaml/yml (YAML configuration files), .json (JSON configuration files), .cfg/.ini/.toml (configuration files), .html (HTML files, with tag-aware chunking), and .rst (reStructuredText files).

Files are excluded based on the following patterns: hidden files and directories (starting with .), binary files (detected by MIME type), files larger than 10MB, node_modules/, .venv/, __pycache__/, .git/, dist/, build/, .egg-info/, .mypy_cache/, .pytest_cache/, target/, .next/, and .cache/ directories. Additional exclusion patterns can be configured in the ContentIngestor.

The chunking algorithm produces overlapping chunks of approximately 512 tokens each, with 50 tokens of overlap between consecutive chunks to ensure context is not lost at chunk boundaries. Markdown files are split on ## and ### headings when possible, preserving the heading as the chunk title. Code files are split on function and class definitions. Plain text files are split on paragraph boundaries (double newlines).

## Memory Store Architecture

The persistence memory system uses a separate LanceDB table from the documentation index. Each memory entry is stored with its embedding vector, namespace string, content text, and creation timestamp. The namespace field enables logical isolation of memories for different projects or agents, while still using a single vector index for efficient cross-namespace queries if needed in the future.

The recall operation searches within a single namespace by embedding the query and computing cosine similarity against all entries in that namespace. Results are returned sorted by similarity score with the content, creation timestamp, and unique ID. The limit parameter controls the maximum number of results returned, with a default of 10 and a maximum of 50.

The compaction status tool reports the total number of entries across all namespaces, the list of active namespaces, the entry count per namespace, and a recommendation on whether compaction would be beneficial. Compaction is suggested when any namespace has more than 100 entries, as this may impact recall performance and memory usage.

## Webapp Architecture

The Documentation MCP webapp consists of a FastAPI backend running on port 11033 and a React SPA frontend running on port 11032. The backend serves REST API endpoints for documentation search, retrieval, memory operations, and reindexing. The frontend provides a documentation browser with tree view navigation, full-text search, content viewer with syntax highlighting, memory management interface, and settings page.

The webapp uses the same LanceDB index for search as the MCP tools, ensuring consistent results regardless of access method. The start_webapp tool launches both the backend and frontend using the web_sota/start.ps1 script, which handles port clearing, process startup, and browser opening.

## Tool Group Organization

All tools are organized into logical groups for discoverability: search_and_read group includes search_docs, ask_docs, and get_document for finding and consuming documentation content. The index_and_workflow group includes reindex_docs, chunk_stats, and agentic_doc_workflow for managing the index and running autonomous research. The memory group includes persistence_store_memory, persistence_recall, and persistence_compaction_status for cross-session knowledge retention. The system group includes server_status and docs_help for server introspection.

The docs_help tool provides a structured view of all tools by group, along with the list of indexed documentation areas and index health metrics. This is the recommended first call for new users to understand what tools are available and how they are organized.

## Content Ingestion Pipeline

The ContentIngestor is responsible for discovering, reading, chunking, and feeding documents to the embedding pipeline. The ingestion process begins with a filesystem scan of DOCS_ROOT and any configured DOCS_EXTRA_PATHS. Each discovered file is classified by extension into supported types (markdown, text, code, configuration, HTML, reStructuredText). Binary files, hidden files, and files matching exclusion patterns are skipped. Each supported file is read and split into overlapping chunks of approximately 512 tokens with 50 tokens overlap. Markdown files are chunked with awareness of section headers to maintain semantic boundaries.

Chunks are then embedded using the configured embedding model (BAAI/bge-small-en-v1.5 by default) running locally via ONNX runtime. The embedding vectors are stored in LanceDB along with chunk metadata including source file, relative path, and chunk position within the file. The completed index replaces the previous index atomically, ensuring that search operations never see a partially rebuilt index.

## Releasebot Integration Details

The query_releasebot tool scrapes releasebot.io HTML pages to extract software release information. For each product slug, the tool fetches the release page, parses the HTML to extract release entries with their dates and headlines, and returns the most recent entries up to the requested limit. The tool does not require any API key or authentication as it works with publicly available Releasebot pages.

If a product slug does not correspond to a known release page, the tool returns a helpful error message with a link to the Releasebot alphabetical directory for discovering valid slugs. The tool is designed for casual use to check for recent software updates without navigating to release pages manually. For production release monitoring, use the product's official API or RSS feeds instead.

## Documentation Index Structure

The LanceDB vector database stores all indexed chunks in a single table. Each row contains: the chunk text content, a 384-dimensional embedding vector (for the default BAAI/bge-small-en-v1.5 model), metadata fields for source filename, relative file path, file modification timestamp, chunk index within the file, and total chunks from the same file. The index uses HNSW (Hierarchical Navigable Small World) algorithm for efficient approximate nearest neighbor search, with configurable parameters for search quality and speed.

The index supports cosine similarity as the distance metric. Search returns results sorted by similarity score from 1.0 (exact semantic match) down to 0.0 (completely dissimilar). The score is calculated as 1.0 minus cosine distance, ensuring that higher scores indicate better matches. The index can be rebuilt at any time with reindex_docs, which atomically replaces the old index with a newly built one.

## Search Scoring and Ranking

Search results are ranked by cosine similarity between the query embedding and each chunk embedding. The cosine distance ranges from 0.0 (identical direction, perfect match) to 2.0 (opposite direction, completely unrelated). The score returned in search results is calculated as 1.0 minus distance, giving a score range from -1.0 to 1.0. In practice, good matches score above 0.7, decent matches score between 0.5 and 0.7, and poor matches score below 0.5. The limit parameter controls how many results are returned, not the scoring threshold.

The embedding model (BAAI/bge-small-en-v1.5) produces 384-dimensional vectors. This is a relatively small embedding size that provides good search quality while keeping memory usage low and search speed high. The model supports 100+ languages including English, German, French, Spanish, Chinese, Japanese, and Arabic. It is optimized for asymmetric search (short query + long document) which matches the documentation search use case.

## Memory Store Limitations

The persistent memory store has the following known limitations. Each memory entry is limited to approximately 10,000 characters. Entries beyond this limit are silently truncated. There is no built-in expiration or eviction policy. Memory entries accumulate until explicitly removed by clearing the data/memory/ directory. The recall operation searches within a single namespace only; cross-namespace queries are not supported. There is no update or delete operation for individual memory entries. For production use with high-volume memory storage, implement an external memory management strategy using the compaction status reports.

## Webapp Architecture Details

The webapp frontend is a React SPA built with Vite and styled with TailwindCSS. It communicates with the backend through REST API calls. The documentation tree view shows the DOCS_ROOT directory structure with expandable folders and file icons. Clicking a file displays its full content with syntax highlighting. The search panel shows search results with similarity scores and navigation links. The memory panel displays namespaces with their entry counts and recall query interface.

The backend serves both the REST API and static frontend files. In development mode, the Vite dev server proxies API calls to the backend. In production mode, the built frontend files are served directly by the backend. The start_webapp tool handles both modes appropriately.

## Document Chunking Strategy

The chunking algorithm is designed to maximize the semantic coherence of each chunk while maintaining compatibility with the embedding model's context window. Markdown files are the primary document type and receive specialized chunking treatment. Section headers (## and ###) are detected and used as natural chunk boundaries. Each chunk starts with the section header text to provide context. Sections longer than 512 tokens are split at paragraph boundaries with 50-token overlap. Sections shorter than 50 tokens are merged with adjacent sections to avoid undersized chunks.

Code files are chunked by function and class definitions. The chunk includes the function or class signature and docstring as context. Class methods are chunked individually with the class name included as context. Plain text files are chunked by paragraph breaks with a minimum chunk size of 100 tokens. Configuration files (YAML, JSON, INI) are chunked by top-level keys when the structure is hierarchical.

## Search Performance Benchmarks

On a modern laptop (2023 model with SSD and 16GB RAM), search performance benchmarks show approximately 10ms for exact match searches, 50ms for semantic searches on a 1,000-chunk index, 100ms on a 10,000-chunk index, and 200ms on a 100,000-chunk index. Reindex performance benchmarks show approximately 200 chunks per second with the default BAAI/bge-small-en-v1.5 model, meaning a 10,000-chunk index rebuilds in approximately 50 seconds. Memory usage scales approximately 16KB per chunk for the vector index, meaning a 10,000-chunk index requires approximately 160MB of RAM for the vector store.

## Federated Documentation Queries

When the server is configured with MCP_BRIDGE_URLS, documentation queries can be federated across multiple MCP servers. The search_docs tool searches the local index only. For federated search, configure the bridge URLs and call the remote server's search tools through their namespaced paths. The ask_docs tool works with local documentation only. Cross-server documentation queries require manual orchestration through the bridge mechanism. The agentic_doc_workflow tool operates on local documentation only but can be extended to incorporate remote server results through the sampling mechanism.

## Document Discovery Process

The ContentIngestor discovers documentation files by scanning the DOCS_ROOT directory and any configured DOCS_EXTRA_PATHS recursively. Each file is evaluated against inclusion and exclusion criteria. Included files are read, chunked, and queued for embedding. The ingestion process is single-threaded and processes files in filesystem order. For very large documentation sets (over 10,000 files), the ingestor batches file processing to manage memory usage. The reindex_docs tool initiates a full ingest cycle from scratch, replacing the previous index atomically upon completion.

## Search Query Expansion

The search_docs tool performs semantic search using embedding similarity. It does not perform query expansion or synonym matching beyond what the embedding model captures from the training data. For precise terminology searches, use the exact terms from the documentation. The BAAI/bge-small-en-v1.5 embedding model was trained on a diverse corpus including technical documentation, research papers, and web content. It captures semantic relationships like synonyms and related concepts within its embedding space, providing relevant results even when search terms differ from the exact documentation wording.
