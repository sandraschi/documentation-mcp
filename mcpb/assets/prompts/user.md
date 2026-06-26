# documentation-mcp — User Guide

## Quick Start

### Prerequisites
- Python 3.10+ with uv
- A directory of documentation files (Markdown, text)

### Installation
```bash
git clone https://github.com/sandraschi/documentation-mcp
cd documentation-mcp
uv sync
```

### Start the Server
```bash
# MCP stdio mode (for Claude Desktop)
uv run python -m docs_mcp

# With custom docs root
set DOCS_ROOT=D:/Dev/repos/mcp-central-docs
uv run python -m docs_mcp

# Full webapp
.\web_sota\start.ps1
# Opens http://localhost:11032
```

### Register with Claude Desktop
```json
{
  "mcpServers": {
    "documentation-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "D:/Dev/repos/documentation-mcp", "python", "-m", "docs_mcp"],
      "env": { "DOCS_ROOT": "D:/Dev/repos/mcp-central-docs", "PYTHONPATH": "${workspaceFolder}/src" }
    }
  }
}
```

### First-Time Indexing
After starting the server, run a reindex to build the vector database:
```
reindex_docs()
```
This scans all documentation files, chunks them, generates embeddings, and populates the LanceDB index.

## Tutorials

### Tutorial 1: Check Server Status
Verify the server and index are healthy:
```
server_status()
```
Shows version, index health (chunk count, source count), and memory namespace stats.

### Tutorial 2: Semantic Search
Search for relevant documentation using natural language:
```
search_docs(query="How do I configure FastMCP portmanteau tools?", limit=5)
```
The search uses vector embeddings to find conceptually similar content, not just keyword matches. Results include similarity scores (0-1) and the source filename.

### Tutorial 3: Get Full Document Content
After finding a relevant file via search, retrieve the complete content:
```
get_document(relative_path="standards/TOOL_DESIGN_STANDARDS.md")
```
Returns the full file content, size, and last modified timestamp.

### Tutorial 4: Ask a Complex Question
Get an LLM-synthesized answer grounded in the documentation:
```
ask_docs(question="What is the portmanteau pattern and how do I implement it?")
```
The server retrieves the top 10 relevant chunks, then uses the host LLM (or local Ollama/LM Studio fallback) to synthesize an answer with source citations.

### Tutorial 5: Research a Topic Across Multiple Documents
```
ask_docs(question="Compare the different transport modes available for FastMCP servers (stdio, HTTP, SSE)")
```
Returns a synthesized comparison with citations to the relevant documentation files.

### Tutorial 6: Autonomous Research Workflow
For complex multi-step research:
```
agentic_doc_workflow(workflow_prompt="Research how to set up a new MCP server with FastMCP 3.2, including the directory structure, required files, and configuration. Generate a step-by-step guide.")
```
The LLM autonomously searches the documentation, synthesizes findings, and returns a structured report. Requires host sampling support.

### Tutorial 7: Reindex After Adding Documentation
After adding new files to the docs root:
```
reindex_docs()
```
This can take 10-60 seconds depending on the number of files. The old index is replaced atomically.

### Tutorial 8: Check Index Statistics
```
chunk_stats()
```
Returns the number of indexed sources and the embedding model in use.

### Tutorial 9: Use Persistent Memory
Store cross-session knowledge:
```
persistence_store_memory(namespace="email-mcp", content="The email-mcp server uses IMAP for inbox access. SMTP for outgoing. Supports auto-respond rules with optional AI generation.")
```
Recall it later:
```
persistence_recall(namespace="email-mcp", query="How does email sending work?")
```
Check memory usage:
```
persistence_compaction_status()
```

### Tutorial 10: Store and Recall Project Decisions
```
persistence_store_memory(namespace="project-x", content="Decided to use FastMCP 3.2 with portmanteau patterns. Using Starlette over FastAPI per fleet standards. Port 10812/10813.")
persistence_recall(namespace="project-x", query="What framework did we choose?")
```

### Tutorial 11: Query Product Release Notes
Check recent releases for any product tracked on Releasebot:
```
query_releasebot(product_slug="cursor", limit=5)
query_releasebot(product_slug="zed", limit=3)
query_releasebot(product_slug="anthropic", limit=10)
```
Useful for checking if a tool you depend on has shipped updates.

### Tutorial 12: Browse Documentation Areas
```
docs_help()
```
Returns a structured overview of all available tools grouped by category and lists all discoverable documentation areas.

### Tutorial 13: Use the Docs Expert Prompt
Load the documentation expert prompt:
```
docs_expert(focus="search")
```
Provides context-aware instructions for using the server's tools effectively.

### Tutorial 14: Start the Web Dashboard
```
start_webapp()
```
Automatically starts the backend and frontend, then opens the browser.

### Tutorial 15: Full Research Workflow Example
Combined workflow for investigating a topic:
```
# Step 1: Check index health
server_status()

# Step 2: Search for relevant docs
search_docs(query="MCP server security best practices", limit=5)

# Step 3: Read full documents
get_document(relative_path="standards/security-best-practices.md")

# Step 4: Ask a specific question
ask_docs(question="What are the recommended security practices for MCP servers handling API keys?")

# Step 5: Store the findings for later
persistence_store_memory(namespace="security-research", content="MCP security: [findings from research]")

# Step 6: Run an autonomous deep dive
agentic_doc_workflow(workflow_prompt="Research all security-related documentation and create a comprehensive security checklist for MCP server development.")
```

## API Reference

### REST Endpoints (FastAPI, port 11033)

**GET /health** — Server health check

**GET /api/status** — Full server status with index metrics

**POST /api/search** — Semantic search
Body: `{"query": "portmanteau pattern", "limit": 5}`

**POST /api/ask** — Ask a question
Body: `{"question": "What is FastMCP?"}`

**GET /api/document** — Get document by path
Query: `?relative_path=standards/TOOL_DESIGN_STANDARDS.md`

**POST /api/reindex** — Trigger reindex

**GET /api/stats** — Index statistics

**POST /api/memory** — Store memory
Body: `{"namespace": "my-app", "content": "key decision"}`

**GET /api/memory/{namespace}** — Recall memories
Query: `?query=decision&limit=5`

**GET /api/releasebot/{slug}** — Product release notes
Query: `?limit=5`

### MCP Tool Response Format
```json
{
  "success": true,
  "message": "Found 5 relevant snippets for 'portmanteau pattern'",
  "data": [
    {
      "filename": "TOOL_DESIGN_STANDARDS.md",
      "score": 0.89,
      "content": "...the Industrial Portmanteau pattern consolidates...",
      "relative_path": "standards/TOOL_DESIGN_STANDARDS.md"
    }
  ]
}
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Index empty | No docs indexed | Run reindex_docs() or set DOCS_ROOT |
| "No documentation found" | Query doesn't match docs | Try broader terms or check DOCS_ROOT |
| ask_docs fails | No LLM available | Install Ollama or add LM Studio |
| Host sampling not supported | Client doesn't support ctx.sample | Server falls back to local LLM automatically |
| Memory recall empty | No data in namespace | Use persistence_store_memory first |
| Path traversal error | Relative path contains ".." | Use paths starting with "standards/" not "../" |
| Reindex slow | Large documentation set | Expected for 1000+ files. Usually under 60s |
| Webapp won't start | Port conflict | Check :11032 and :11033 are free |
| Releasebot returns empty | Invalid slug | Check slug at https://releasebot.io/updates/alphabetical |

## FAQ

**Q: What file formats are supported?**
A: Markdown (.md), text (.txt), and any plain text files. Binary files are skipped.

**Q: How is the documentation indexed?**
A: Files are read, split into chunks, and embedded using FastEmbed (BAAI/bge-small-en-v1.5). Vectors are stored in LanceDB.

**Q: Can I add my own documentation?**
A: Yes. Set DOCS_ROOT to point at any directory of documentation files, or use DOCS_EXTRA_PATHS to add supplementary directories.

**Q: Does this work offline?**
A: Yes. Ollama provides local LLM inference. LanceDB and embeddings are entirely local.

**Q: What embeddings model is used?**
A: Default is BAAI/bge-small-en-v1.5, configurable via the EMBEDDING_MODEL environment variable.

**Q: How long does reindexing take?**
A: Depends on file count. ~10 seconds for 100 files, ~60 seconds for 1000+ files.

**Q: Can I have multiple documentation roots?**
A: Yes. Use DOCS_EXTRA_PATHS as a comma-separated list of additional directories.

**Q: Is the memory store persistent across restarts?**
A: Yes. Memory is stored in the data/memory/ directory and survives server restarts.

## Advanced Usage Guides

### Guide 1: Setting Up a Fleet Documentation Hub
Configure the server to serve your entire fleet's documentation:
```
# Step 1: Set DOCS_ROOT to the fleet standards directory
# DOCS_ROOT=D:/Dev/repos/mcp-central-docs

# Step 2: Start the server with the fleet docs
# uv run python -m docs_mcp

# Step 3: Reindex to build the vector database
reindex_docs()

# Step 4: Verify the index
chunk_stats()
server_status()

# Step 5: Configure extra paths for repository-specific docs
# Set DOCS_EXTRA_PATHS=D:/Dev/repos/devices-mcp/docs,D:/Dev/repos/docker-mcp/docs

# Step 6: Reindex with extra paths
reindex_docs()
```

### Guide 2: Cross-Session Project Memory
Maintain a persistent knowledge base for a long-running project:
```
# Session 1: Store key decisions
persistence_store_memory(namespace="project-alpha", content="Architecture: FastAPI backend with React SPA frontend. Port 10812/10813. TailwindCSS dark theme.")

persistence_store_memory(namespace="project-alpha", content="Database: SQLite via SQLAlchemy async. Migration tool: Alembic. Stored in data/project-alpha.db.")

persistence_store_memory(namespace="project-alpha", content="Testing: pytest with pytest-asyncio. Playwright e2e for frontend. Coverage target: 80%.")

# Session 2 (later): Recall decisions
persistence_recall(namespace="project-alpha", query="What database are we using?", limit=5)

# Session 2: Add more knowledge
persistence_store_memory(namespace="project-alpha", content="Deploy: NSIS installer via Tauri. PyInstaller for backend. CI: GitHub Actions on tag push.")

# Check memory health
persistence_compaction_status()
```

### Guide 3: Multi-Repository Documentation Research
Research a topic across multiple documentation sources:
```
# Step 1: Search the main docs
search_docs(query="MCP tool registration and FastMCP patterns", limit=5)

# Step 2: Get relevant full documents
get_document(relative_path="standards/rules/mcp_registration.md")

# Step 3: Ask for synthesis
ask_docs(question="What are the complete steps for registering a new MCP tool with FastMCP?")

# Step 4: Search for related patterns
search_docs(query="portmanteau tool pattern implementation", limit=5)
search_docs(query="tool annotations READ_ONLY MUTATING DESTRUCTIVE", limit=5)

# Step 5: Get the full standards document
get_document(relative_path="standards/TOOL_DESIGN_STANDARDS.md")

# Step 6: Run autonomous deep research
agentic_doc_workflow(workflow_prompt="Research all standards related to tool implementation and create a concise implementation guide for a new MCP tool following fleet standards.")
```

### Guide 4: Automated Release Monitoring
Track releases across your toolchain:
```
# Check multiple tools with one call each
query_releasebot(product_slug="cursor", limit=3)
query_releasebot(product_slug="docker", limit=3)
query_releasebot(product_slug="claude", limit=3)
query_releasebot(product_slug="zed", limit=3)
query_releasebot(product_slug="openai", limit=5)

# Store notable releases in memory
persistence_store_memory(namespace="release-monitor", content="cursor released v0.45 with MCP improvements on 2025-06-15")
```

### Guide 5: Troubleshooting Documentation Workflows
Common research scenarios and how to handle them:

**Scenario: Searching for a Standard You Know Exists**
If search_docs returns no results, try:
1. Verify DOCS_ROOT is set correctly with `server_status()`
2. Check index health with `chunk_stats()` — if 0 chunks, run `reindex_docs()`
3. Try broader search terms
4. Use `docs_help()` to discover available documentation areas
5. Browse the webapp at http://localhost:11032 to find files manually

**Scenario: Ask_Docs Returns Raw Search Instead of Answer**
This means no LLM is available. To fix:
1. Install Ollama (ollama.ai) and pull a model: `ollama pull qwen2.5:7b`
2. Or install LM Studio and load a model on port 1234
3. The server auto-discovers these on the next ask_docs call

**Scenario: Memory Recall Returns Incomplete Results**
Memories are searched by semantic similarity, not keyword match. Try:
1. Rephrase your query to match the semantic content of what you stored
2. Check the namespace has entries: `persistence_compaction_status()`
3. Use broader query terms

## Reference

### All Tool Parameters Reference

| Tool | Required Params | Optional Params | Returns |
|------|----------------|-----------------|---------|
| search_docs | query | limit (5) | Scored snippets |
| ask_docs | question | — | Synthesized answer |
| get_document | relative_path | — | Full file content |
| reindex_docs | — | — | Chunk count |
| chunk_stats | — | — | Source list |
| server_status | — | — | Health + index + memory |
| docs_help | — | — | Structured help |
| agentic_doc_workflow | workflow_prompt | — | Research report |
| start_webapp | — | — | Launch status |
| persistence_store_memory | namespace, content | — | Memory ID |
| persistence_recall | namespace, query | limit (10) | Memories |
| persistence_compaction_status | — | — | Namespace stats |
| query_releasebot | product_slug | limit (5) | Release entries |

### Embedding Model Details
- **Default model**: BAAI/bge-small-en-v1.5
- **Vector dimensions**: 384
- **Max tokens per chunk**: 512
- **Chunk overlap**: 50 tokens
- **Similarity metric**: Cosine distance (converted to 0-1 score)
- **Search algorithm**: Approximate Nearest Neighbor (ANN) via LanceDB
- **Performance**: ~100ms per search on a 10,000-chunk index
- **Memory**: ~150MB for a 10,000-chunk index
- **Reindex speed**: ~200 chunks/second on CPU (modern laptop)

### LanceDB Configuration
The vector database is stored at data/lancedb/ relative to the server root. The database uses HNSW (Hierarchical Navigable Small World) index structure with the following defaults:
- M (max connections per node): 16
- ef_construction (index build quality): 200
- ef_search (search quality): 100
- Distance metric: cosine

These can be tuned for larger indexes or faster search by modifying the LanceDB configuration in store_registry.py.

### Releasebot Slug Reference
| Product | Slug | Notes |
|---------|------|-------|
| Cursor Editor | cursor | AI code editor |
| Zed Editor | zed | Rust-based editor |
| Claude Desktop | claude | Anthropic's desktop app |
| VS Code | vscode | Microsoft editor |
| Windsurf | windsurf | AI IDE |
| Docker Desktop | docker | Container platform |
| Obsidian | obsidian | Knowledge base |
| Notion | notion | Docs & wiki |
| Figma | figma | Design tool |
| Raycast | raycast | macOS launcher |
| Linear | linear | Issue tracking |
| Warp | warp | Terminal emulator |
| OpenAI | openai | AI platform |
| Anthropic | anthropic | AI safety company |

## Performance Optimization Guide

Search performance depends on the index size and hardware. For indexes under 10,000 chunks, searches complete in under 100ms. For indexes over 100,000 chunks, search time increases to 200-500ms. Reindexing speed is approximately 200 chunks per second on modern laptop hardware with SSD storage. For large documentation sets, plan for 5-10 minutes per 100,000 chunks during reindexing.

The ask_docs tool adds LLM synthesis time on top of search time. Host sampling (ctx.sample) completes in 2-5 seconds. Local LLM (Ollama) synthesis completes in 5-30 seconds depending on model size and hardware. GPU-accelerated local models (via Ollama with CUDA) reduce synthesis time by 50-70%.

## Embedding Model Comparison

BAAI/bge-small-en-v1.5 (default) provides the best balance of speed and accuracy for general documentation search. It generates 384-dimensional vectors, requires approximately 150MB of memory for 10,000 chunks, and provides strong multilingual support including German. Alternative models can be configured via the EMBEDDING_MODEL environment variable, but may require different chunk sizes and overlap settings.

For specialized English-only documentation, sentence-transformers/all-MiniLM-L6-v2 provides slightly better accuracy at the same vector dimensions. For multilingual corpora with strong non-English content, BAAI/bge-m3 provides multilingual support with 1024-dimensional vectors (requires more memory and storage).

## Releasebot Data Freshness

Releasebot data is scraped live on each query_releasebot call and is not cached server-side. This means every call fetches the latest data from releasebot.io. The response time depends on the releasebot.io server responsiveness and typically completes in 1-3 seconds. If a product slug is invalid, the tool returns a clear error message with a link to the alphabetical slug directory for discovering valid slugs.

## Advanced Use Cases

### Use Case: Server Onboarding Documentation Hub
When onboarding new developers, configure the Documentation MCP server with docs_root pointing to your team's documentation repository. Reindex to build the vector database. Team members can then search for onboarding guides, coding standards, architecture documents, and API references using natural language queries. The ask_docs tool synthesizes answers from the relevant documentation, providing context-specific guidance without requiring the developer to manually search through dozens of files.

### Use Case: Code Review Reference System
During code reviews, use the server to quickly reference relevant standards and best practices. Search for specific patterns like batch mutation safety or NSIS kill hooks. Retrieve full documents for detailed reference. Ask synthesis questions about complex topics. Store review findings in persistent memory for future reference. The documentation server becomes a real-time reference system integrated into the review workflow.

### Use Case: Fleet Standard Compliance Audit
Run a comprehensive audit of a codebase against fleet standards using the documentation server. Search for each standard topic and retrieve the full document. Compare the retrieved requirements against the codebase implementation. Store audit findings in memory for tracking compliance over time. The agentic_doc_workflow tool can automate the research phase of this audit, searching across multiple documentation areas and synthesizing findings into a structured report.

### Use Case: Release Note Generation
When preparing a release, use query_releasebot to check for new versions of all dependencies. Search for relevant changelog entries and migration guides. Synthesize findings into comprehensive release notes. Store the generated notes in persistent memory for future reference. The server helps automate the research-heavy parts of release management while keeping a historical record of findings.

### Use Case: Cross-Project Knowledge Sharing
Teams working on different projects can share knowledge through the memory system. Each project uses its own namespace for structured storage of architecture decisions, API designs, deployment configurations, and lessons learned. Other teams can recall relevant memories from other projects' namespaces when facing similar design decisions. The persistence_recall tool makes cross-project knowledge discovery as simple as asking a natural language question.

### Use Case: Technical Debt Tracking
Use the memory system to track technical debt items across projects. Each item includes the affected component, the nature of the debt, the recommended fix, and the estimated effort. Recall items by querying for specific patterns like performance or security. The compaction status helps identify namespaces with accumulating entries that need review. This creates a lightweight, searchable technical debt register integrated into the development workflow.

## LLM Provider Configuration Guide

The ask_docs tool uses a priority-based LLM selection algorithm to ensure maximum availability. Host sampling via ctx.sample is always preferred when available as it uses the client's connected LLM (e.g., Claude in Claude Desktop). If host sampling fails, the server falls back to locally available LLMs.

For Ollama configuration, ensure the Ollama service is running on the default port 11434 or configure a custom URL in the settings. The server auto-discovers available models and selects one based on a priority list: qwen2.5 at the top, followed by llama3.2, phi4, and gemma. The selected model must be pulled before use: ollama pull qwen2.5:7b. Models with 7B parameters or fewer provide good balance of speed and quality for documentation synthesis. Larger models (13B, 30B) provide higher quality answers at the cost of slower response times.

For LM Studio configuration, ensure the LM Studio application is running with the local API server enabled on port 1234. Load a model in LM Studio's model hub tab, then enable the local inference server in the settings. The server uses the first available model from LM Studio's loaded models list. LM Studio supports the same model formats as Ollama but provides additional GPU acceleration configuration options through its UI.

When both Ollama and LM Studio are available, LM Studio is preferred for its typically faster response times due to better GPU utilization. When only one is available, the server uses whichever is accessible. When neither is available, ask_docs returns the raw search results with a clear explanation that synthesis requires a local LLM.

## Documentation File Organization Best Practices

For optimal indexing results, organize documentation files with clear hierarchical structure using directory names as categories. Use descriptive filenames that indicate the content area. Include section headers (## and ###) in Markdown files for better chunking. Keep individual files reasonably sized (under 100KB) to enable complete document retrieval without truncation. Use consistent formatting across files for uniform chunk quality.

The ContentIngestor processes files in alphabetical order within each directory. The first time a file is indexed, all its chunks are added to the vector store. When reindexing, the entire store is rebuilt from scratch. The chunking algorithm respects code blocks in Markdown (fenced with backticks) and preserves them as complete units.

## Index Performance Factors

Index size grows linearly with the number of files and their sizes. A typical 1MB Markdown file generates approximately 20-30 chunks. A 10MB codebase generates approximately 200-300 chunks. Search performance degrades gracefully with index size: doubling the index size increases search time by approximately 20% due to the ANN algorithm's logarithmic complexity profile.

Reindex time depends primarily on file count and the embedding model. BAAI/bge-small-en-v1.5 processes approximately 200 chunks per second on a modern CPU. A documentation set of 1000 files averaging 500KB each generates approximately 3,000-5,000 chunks, requiring 15-25 seconds for a full reindex. GPU acceleration can increase throughput by 3-5x but requires CUDA-compatible hardware and ONNX runtime with CUDA execution provider.

## FAQ Additional Questions

Q: Can I search code files, not just documentation?
A: Yes. Code files (.py, .js, .ts) in the DOCS_ROOT are indexed and searchable. The chunker respects code structure by splitting at function and class boundaries.

Q: How do I add new documentation without restarting the server?
A: Add the new files to the DOCS_ROOT directory, then call reindex_docs(). The server does not need a restart.

Q: What happens to the old index during reindexing?
A: The old index remains available for queries until the new index is fully built and atomically replaces it.

Q: Can I search specific file types only?
A: Not directly. The search is across all indexed files. Use precise queries to narrow results to your area of interest.

Q: How do I delete memories?
A: There is no direct delete API. Delete the data/memory/ directory while the server is stopped to clear all memories.

Q: Can I use multiple embedding models simultaneously?
A: No, a single embedding model is used for the entire index. Change the EMBEDDING_MODEL environment variable and reindex.

Q: Does the server support Chinese, Japanese, or Korean text?
A: The default embedding model (BAAI/bge-small-en-v1.5) supports CJK text. The chunker handles Unicode correctly.

Q: How do I contribute documentation files?
A: Add Markdown files to the DOCS_ROOT directory. Follow the existing file organization structure. Run reindex_docs to index them.

## Troubleshooting Common Index Issues

If search returns no results or poor results, check chunk_stats to verify the index has documents. If chunk_stats shows 0 sources, run reindex_docs. If the index has sources but search returns nothing relevant, try broader search terms or check that the embedding model matches what you used when the index was built. If the index was built with a different EMBEDDING_MODEL than the current setting, rebuild the index with the current model.

If ask_docs consistently fails with sampling errors, check that your MCP client supports sampling (required for ctx.sample) or that a local LLM (Ollama or LM Studio) is running and accessible. The server logs diagnostic information about LLM discovery attempts to help identify configuration issues.

If the webapp does not start with start_webapp, manually check port availability for ports 11032 and 11033, verify that web_sota/start.ps1 exists in the repository root, and check that Node.js and npm/bun are installed for the Vite frontend build.

## Integrating with CI/CD Pipelines

The Documentation MCP server can be integrated into CI/CD pipelines for automated documentation validation. Add a CI step that starts the server, runs reindex_docs to load the latest documentation, executes specific search_docs or ask_docs queries to verify content accuracy, checks that critical documents are indexed with expected chunk counts, and shuts down the server. This ensures that documentation changes are properly indexed and searchable before deployment.

## Advanced Research Workflow Examples

### Research Flow: Compliance Audit
Run a compliance audit against fleet standards: start with search_docs for each standard category (security, documentation, testing, packaging). Use get_document to read each relevant standard in full. Use ask_docs to synthesize requirements across multiple standards. Store findings in the memory system under a compliance namespace. Run agentic_doc_workflow for a cross-cutting research task covering multiple standards. Export the audit results for reporting.

### Research Flow: Tool Implementation Guide
When implementing a new MCP tool, search for tool design patterns, docstring standards, annotation guidelines, and return format requirements. Read the full relevant standards documents. Ask synthesis questions about edge cases and best practices. Store implementation decisions in the memory system for future reference. Use agentic_doc_workflow to research how similar tools are implemented across the fleet.

### Research Flow: Technology Evaluation
For evaluating a new technology against fleet standards, search for relevant integration patterns and compatibility requirements. Ask specific questions about deployment, security, and maintenance implications. Cross-reference with existing technology decisions stored in the memory system. The research workflow provides comprehensive context for informed technology decisions.

## Compatibility and Extensions

The documentation server's LanceDB index is compatible with standard vector database operations. The embedding model can be changed by setting the EMBEDDING_MODEL environment variable to any model supported by FastEmbed. The chunking parameters can be adjusted by modifying the ContentIngestor configuration. The webapp can be customized by modifying the React frontend source in the web_sota directory. The REST API provides a standard HTTP interface for integration with external tools and automation systems. The MCP bridge system enables federation with other MCP servers in the fleet for combined documentation queries.

## Documentation Index Maintenance Schedule

Recommended maintenance schedule for the documentation index: reindex weekly for actively changing documentation sets, or reindex after every significant documentation update. Monitor index health with server_status after each reindex. Check memory compaction status monthly for active memory namespaces. Review and prune stale memories quarterly. Export logs periodically for audit purposes. The reindex operation is safe to run during active use as the old index remains available until the new index is complete.

## Conclusion

The documentation-mcp server provides comprehensive semantic search and retrieval capabilities for technical documentation. Its local-first architecture ensures privacy and offline operation. The LLM-powered answer synthesis provides context-aware responses grounded in the documentation. The persistent memory system enables cross-session knowledge retention. The releasebot integration provides convenient release monitoring. Together, these capabilities make the server an essential tool for fleet documentation management and developer productivity.

## Releasebot Data Structure

Each release entry from query_releasebot contains the release date in ISO format (YYYY-MM-DD) and the headline describing the release. The entries are ordered from newest to oldest. The tool returns the most recent releases up to the requested limit. Release pages may include additional details not captured by the headline, such as version numbers, change notes, and download links. For complete release information, visit the product's official website or release notes page. The Releasebot service aggregates release information from multiple sources and may not include all releases for all products.

## Webapp Feature Reference

The Documentation MCP webapp provides the following features accessible through the browser interface. The Documentation Tree panel shows the DOCS_ROOT directory structure with expandable folders and clickable file links. The Search panel provides a text input for semantic search with clickable result snippets. The File Viewer displays document content with Markdown rendering and syntax highlighting for code blocks. The Memory panel shows namespaces with entry counts and provides the recall query interface. The Settings page configures DOCS_ROOT path, DOCS_EXTRA_PATHS, embedding model, and LLM provider URLs. The Server Status panel displays index health, chunk counts, memory stats, and server version.

## Performance and Scalability

The documentation server scales well with documentation size. Indexes of up to 100,000 chunks perform within acceptable response times. Beyond 100,000 chunks, consider splitting the documentation into multiple DOCS_ROOT directories and running separate server instances for each documentation domain. The memory store scales independently of the documentation index and supports up to 10,000 entries per namespace before compaction is recommended.

## Extending the Server

The server's modular architecture allows easy extension with new tools. Add new tools by creating functions in the appropriate tool module (rag.py, system.py, memory.py, workflows.py) and registering them in the register_tools function. New documentation sources can be added by configuring DOCS_EXTRA_PATHS. New embedding models can be configured via the EMBEDDING_MODEL environment variable. The server's REST API provides a stable interface for integration with external tools and automation systems.

## Summary

The documentation-mcp server provides a complete solution for managing, searching, and synthesizing technical documentation with local LLM integration and persistent memory capabilities.
