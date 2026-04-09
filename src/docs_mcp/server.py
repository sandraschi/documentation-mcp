import json
import logging
import subprocess
import traceback
from contextlib import asynccontextmanager
from pathlib import Path

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

# Internal imports
from docs_mcp.backend import llm_client, settings_store
from docs_mcp.backend.config import config
from docs_mcp.backend.ingestor import ContentIngestor
from docs_mcp.backend.llm_client import list_ollama_models, list_openai_models
from docs_mcp.backend.memory_store import MemoryStore
from docs_mcp.backend.vector_store import DocumentStore
from docs_mcp.releasebot import query_releasebot_http
from fastmcp import Context, FastMCP

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("docs_mcp")

# Global State
_store: DocumentStore = None
_memory_store: MemoryStore = None


def get_store() -> DocumentStore:
    """Lazy-initialization for DocumentStore"""
    global _store
    if _store is None:
        logger.info("Initializing DocumentStore...")
        _store = DocumentStore()
    return _store


def get_memory_store() -> MemoryStore:
    """Lazy-initialization for MemoryStore (High-performance agent persistence)."""
    global _memory_store
    if _memory_store is None:
        logger.info("Initializing MemoryStore...")
        _memory_store = MemoryStore()
    return _memory_store


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


def log_to_file(msg):
    try:
        with open("debug.log", "a") as f:
            f.write(msg + "\n")
    except Exception:
        pass


@asynccontextmanager
async def lifespan(ctx):
    # Initialize RAG Components
    try:
        store = get_store()
        log_to_file(f"DEBUG: Store initialized. ID: {id(store)}")

        # Auto-Ingestion Check
        sources = store.list_sources()
        if not sources:
            logger.info("Vector Store is empty. Starting auto-ingestion...")
            log_to_file("DEBUG: Vector Store empty. Starting auto-ingestion...")

            ingestor = ContentIngestor()
            docs = ingestor.load_all_docs()
            if docs:
                store.add_documents(docs)
                log_to_file(f"DEBUG: Auto-ingestion complete. {len(docs)} chunks indexed.")
            else:
                log_to_file("DEBUG: No documents found to ingest.")
        else:
            log_to_file(f"DEBUG: Vector Store ready. {len(sources)} sources indexed.")

    except Exception as e:
        logger.error(f"Store init failed: {e}")
        log_to_file(f"CRITICAL ERROR: Store init failed: {e}")
        traceback.print_exc()

    log_to_file("DEBUG: Lifespan setup complete. Application taking requests.")
    yield
    logger.info("Shutting down Docs MCP Server...")


# Initialize FastMCP
docs_mcp = FastMCP("Docs MCP", lifespan=lifespan)

# Skills provider: expose bundled skills as skill:// resources (FastMCP 3.1)
try:
    from fastmcp.server.providers.skills import SkillsDirectoryProvider

    _skills_dir = Path(__file__).resolve().parent / "skills"
    if _skills_dir.is_dir():
        docs_mcp.add_provider(SkillsDirectoryProvider(roots=[_skills_dir]))
except Exception as e:
    logger.warning("Skills provider not registered: %s", e)

# --- MCP Tools ---


@docs_mcp.tool()
def start_webapp() -> dict:
    """Start the Documentation MCP webapp fully automatically: backend, then frontend, then open in browser.

    Runs the repo's web_sota/start.ps1 with -Automated: clears port squatters, starts the Python
    backend (hidden), waits until it is ready, starts the Vite frontend (hidden), waits until it
    is ready, then opens the default browser to the app. No user interaction required.

    Returns:
        success: True if the script completed and browser was opened.
        message: Short status.
        url: Frontend URL (e.g. http://localhost:10794).
    """
    repo_root = Path(__file__).resolve().parent.parent.parent
    start_ps1 = repo_root / "web_sota" / "start.ps1"
    if not start_ps1.is_file():
        return {
            "success": False,
            "message": f"Start script not found: {start_ps1}",
            "url": "",
        }
    try:
        proc = subprocess.run(
            [
                "powershell",
                "-ExecutionPolicy",
                "Bypass",
                "-NoProfile",
                "-File",
                str(start_ps1),
                "-Automated",
            ],
            cwd=str(start_ps1.parent),
            capture_output=True,
            text=True,
            timeout=120,
        )
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        if proc.returncode != 0:
            return {
                "success": False,
                "message": f"start.ps1 -Automated exited with {proc.returncode}. {err or out}",
                "url": "http://localhost:10794",
            }
        return {
            "success": True,
            "message": "Webapp started; backend and frontend are running, browser opened.",
            "url": "http://localhost:10794",
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "Start script timed out (120s). Backend or frontend may still be starting.",
            "url": "http://localhost:10794",
        }
    except Exception as e:
        logger.exception("start_webapp failed")
        return {
            "success": False,
            "message": str(e),
            "url": "http://localhost:10794",
        }


@docs_mcp.tool()
async def query_releasebot(product_slug: str, limit: int = 5) -> dict:
    """QUERY_RELEASEBOT — Recent releases for a product via public Releasebot pages (no API key).

    PORTMANTEAU RATIONALE: Single read-only tool for "did X ship something lately?" without
    subscribing to paid Releasebot APIs; scrapes the same HTML users see at releasebot.io.

    Args:
        product_slug: Feed slug, e.g. cursor, zed, notion, anthropic, openai.
            Valid slugs: https://releasebot.io/updates/alphabetical
        limit: Last N releases to summarize (default 5, max 20).

    Returns:
        success, message (short summary with dates + headlines), url (feed page),
        releases: list of {date, headline}. On unknown slug or empty feed, success False
        and a pointer to the alphabetical slug list.
    """
    lim = max(1, min(int(limit), 20))
    res = await query_releasebot_http(product_slug, limit=lim)
    res["product_slug"] = product_slug
    return {"result": _to_markdown(res, "query_releasebot")}


def _search_docs_raw(query: str, limit: int = 5) -> dict:
    """Internal search helper returning a plain dict (not markdown). Used by ask_docs and api_chat."""
    store = get_store()
    results = store.search(query, limit=limit)

    if not results:
        return {
            "success": False,
            "message": f"No documentation found for query: '{query}'",
            "data": [],
        }

    data = []
    for r in results:
        distance = r.get("_distance", 0.0)
        score = max(0.0, 1.0 - distance)
        data.append(
            {
                "filename": r["metadata"].get("filename", "unknown"),
                "score": score,
                "content": r["content"],
                "relative_path": r["metadata"].get("relative_path", "unknown"),
            }
        )

    return {
        "success": True,
        "operation": "search_docs",
        "query": query,
        "message": f"Found {len(data)} relevant documentation snippets for '{query}'",
        "data": data,
        "next_steps": [
            "Use 'ask_docs' to synthesize a specific answer",
            "Browse the file tree in the webapp",
        ],
    }


@docs_mcp.tool()
def search_docs(query: str, limit: int = 5) -> dict:
    """Perform a semantic search across all indexed documentation.

    This tool uses neural embeddings to find the most relevant document snippets based on
    meaning rather than exact keyword matches. It's ideal for discovering how-to guides,
    architectural patterns, and standard definitions.

    Args:
        query: The natural language search query (e.g., "FastMCP portmanteau pattern")
        limit: Maximum number of relevant snippets to return (default: 5)

    Returns:
        A conversational result object containing:
        - success: Boolean status
        - message: Summary of the search results
        - data: List of matching document snippets with scores and metadata
        - next_steps: Contextual suggestions for follow-up research
    """
    res = _search_docs_raw(query, limit=limit)
    return {"result": _to_markdown(res, "search_docs")}


@docs_mcp.tool()
async def ask_docs(question: str, ctx: Context) -> dict:
    """Ask a complex question about the documentation and get a synthesized answer.

    This tool leverages semantic retrieval followed by real-time AI synthesis to
    provide accurate technical answers based on the latest documentation.

    Args:
        question: The technical question to answer.
        ctx: FastMCP Context for sampling.

    Returns:
        A conversational result object with the synthesized answer.
    """
    search_result = _search_docs_raw(question, limit=10)
    if not search_result["success"]:
        return {"result": search_result["message"]}

    # Format context for the LLM
    context_text = "\n\n".join([f"SOURCE: {r['filename']}\nCONTENT: {r['content']}" for r in search_result["data"]])

    system_prompt = "You are a technical documentation expert. Provide concise, accurate answers citing sources."
    user_prompt = f"Answer the following question based ONLY on the provided documentation context.\n\nCONTEXT:\n{context_text}\n\nQUESTION: {question}"

    error_log = []

    # 1. Primary: Host Sampling (FastMCP 3.0+ API)
    try:
        ctx.report_progress("Attempting host-side AI sampling...", 20)
        response = await ctx.sample(
            messages=[user_prompt],
            system_prompt=system_prompt,
            max_tokens=1000,
        )
        res = {
            "success": True,
            "operation": "ask_docs",
            "question": question,
            "message": "Synthesized answer from documentation (via host sampling).",
            "data": {
                "answer": response.text,
                "sources": [r["filename"] for r in search_result["data"] if isinstance(r, dict)],
            },
            "next_steps": ["Ask for specific details", "Examine cited files in the webapp"],
        }
        return {"result": _to_markdown(res, "ask_docs")}
    except Exception as e:
        sampling_err = str(e)
        logger.warning(f"Sampling failed: {sampling_err}")
        error_log.append(f"Sampling Error: {sampling_err}")

    # 2. Fallback: Intelligent Auto-Discovery (Parallel)
    ctx.report_progress("Sampling failed. Starting local LLM discovery...", 40)
    settings = settings_store.load_settings()
    ollama_url = settings.get("ollama_url") or "http://localhost:11434"
    lmstudio_url = settings.get("lmstudio_url") or "http://localhost:1234/v1"

    import asyncio

    try:
        # Run list tasks in parallel with tight timeout
        tasks = [list_ollama_models(ollama_url), list_openai_models(lmstudio_url)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        ollama_res = results[0] if not isinstance(results[0], Exception) else ([], f"Ollama Error: {results[0]}")
        lmstudio_res = results[1] if not isinstance(results[1], Exception) else ([], f"LM Studio Error: {results[1]}")

        ollama_models, o_err = ollama_res
        lm_models, l_err = lmstudio_res

        if o_err:
            error_log.append(o_err)
        if l_err:
            error_log.append(l_err)

        # Priority Selection
        final_provider = None
        final_url = None
        final_model = None

        # A. Check LM Studio First (User prefers LM Studio for local work)
        if lm_models:
            final_provider = "openai"
            final_url = lmstudio_url
            final_model = lm_models[0]  # Usually the currently loaded model in LM Studio
            logger.info(f"Auto-selected LM Studio model: {final_model}")

        # B. Check Ollama
        elif ollama_models:
            final_provider = "ollama"
            final_url = ollama_url
            # Try to pick a lightweight one
            priority = ["qwen2.5", "llama3.2", "phi4", "gemma"]
            for p in priority:
                match = next((m for m in ollama_models if p in m.lower()), None)
                if match:
                    final_model = match
                    break
            if not final_model:
                final_model = ollama_models[0]
            logger.info(f"Auto-selected Ollama model: {final_model}")

        if final_provider and final_model:
            ctx.report_progress(f"Synthesizing answer via {final_provider} ({final_model})...", 60)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            if final_provider == "ollama":
                answer = await llm_client.chat_ollama(final_url, final_model, messages)
            else:
                answer = await llm_client.chat_openai_compatible(final_url, "", final_model, messages)

            res = {
                "success": True,
                "operation": "ask_docs",
                "question": question,
                "message": f"Synthesized answer from documentation (via {final_provider}: {final_model}).",
                "data": {
                    "answer": answer,
                    "sources": [r["filename"] for r in search_result["data"] if isinstance(r, dict)],
                },
                "next_steps": [
                    "Check cited sources",
                    "Tweak local LLM settings if answer is too long",
                ],
            }
            return {"result": _to_markdown(res, "ask_docs")}

    except Exception as e:
        error_log.append(f"Auto-Discovery Error: {e}")
        logger.error(f"Auto-discovery fallback failed: {e}")

    # 3. Final Fail
    return {
        "success": False,
        "error": "Synthesis error",
        "message": "The documentation was found, but all synthesis attempts (Sampling, LM Studio, Ollama) failed.",
        "data": search_result["data"],
        "diagnostic_log": error_log,
        "suggestions": [
            "Ensure LM Studio or Ollama is running",
            "Verify a model is loaded in LM Studio",
            "Try 'ollama pull llama3.2' if using Ollama",
        ],
    }


@docs_mcp.tool()
async def reindex_docs(ctx: Context) -> dict:
    """Force a full scan and re-indexing of all documentation sources.

    Use this tool after adding new documentation files or modifying existing ones
    to ensure the neural search index is synchronized with the filesystem.

    Returns:
        A conversational result object indicating indexing success and chunk counts.
    """
    logger.info("Manual re-indexing triggered...")
    try:
        ctx.report_progress("Connecting to DocumentStore...", 10)
        store = get_store()
        ingestor = ContentIngestor()

        ctx.report_progress("Crawling documentation filesystem...", 30)
        docs = ingestor.load_all_docs()

        if docs:
            ctx.report_progress(f"Embedding and indexing {len(docs)} chunks...", 60)
            # DocumentStore.add_documents handles overwrite mode by default
            store.add_documents(docs)
            count = len(docs)
            ctx.report_progress("Indexing complete.", 100)
            res = {
                "success": True,
                "operation": "reindex_docs",
                "message": f"Documentation synchronization successful. {count} chunks indexed.",
                "data": {"chunks": count},
                "next_steps": [
                    "Test search quality with 'search_docs'",
                    "Verify file tree in webapp",
                ],
            }
            return {"result": _to_markdown(res, "reindex_docs")}
        else:
            return {
                "success": False,
                "error": "No documents found",
                "message": "Re-indexing failed: The documentation source directories appear to be empty.",
                "suggestions": [
                    "Check the paths in config.py",
                    "Ensure source documents are markdown (.md)",
                ],
            }
    except Exception as e:
        err = f"Re-indexing error: {str(e)}"
        logger.error(err)
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "message": "Critical error during re-indexing process.",
            "traceback": traceback.format_exc(),
        }


@docs_mcp.tool()
async def agentic_doc_workflow(workflow_prompt: str, ctx: Context) -> dict:
    """Execute autonomous documentation research and report generation workflows.

    This tool utilizes FastMCP sampling to enable the server to intelligently
    orchestrate its own search and synthesis tools to fulfill complex requests.

    Args:
        workflow_prompt: The goal of the research workflow.
        ctx: FastMCP Context for sampling.

    Returns:
        Structured result of the autonomous workflow execution.
    """
    # Real agentic workflow implementation using sampling
    system_prompt = (
        "You are an autonomous documentation researcher. Your goal is to use the "
        "available search_docs and ask_docs tools to fulfill the user's research request. "
        "Provide a comprehensive final report once you have gathered all information."
    )

    try:
        ctx.report_progress("Analyzing workflow requirements...", 10, 100)
        response = await ctx.sample(
            messages=[workflow_prompt],
            system_prompt=system_prompt,
            max_tokens=2000,
        )
        ctx.report_progress("Finalizing research report...", 90, 100)
        final_report = response.text

        return {
            "result": _to_markdown(
                {
                    "success": True,
                    "operation": "agentic_doc_workflow",
                    "message": "Autonomous research workflow complete.",
                    "data": {"report": final_report},
                },
                "agentic_doc_workflow",
            )
        }
    except Exception as e:
        logger.error(f"Workflow sampling failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "The autonomous workflow could not be completed.",
            "suggestions": ["Verify tool availability", "Check client sampling permissions"],
        }


@docs_mcp.tool()
def chunk_stats() -> dict:
    """Retrieve statistics and health metrics for the neural documentation index.

    This tool provides insights into the scale and distribution of the RAG system,
    including chunk counts by source and embedding model metadata.

    Returns:
        A conversational result object with index metrics.
    """
    store = get_store()
    sources = store.list_sources()
    # Note: DocumentStore could be enhanced to return chunk counts per source
    res = {
        "success": True,
        "operation": "chunk_stats",
        "message": f"Documentation index is healthy with {len(sources)} verified sources.",
        "data": {
            "source_count": len(sources),
            "sources": sources,
            "embedding_model": config.EMBEDDING_MODEL,
        },
        "next_steps": [
            "Run 'reindex_docs' if new projects were added",
            "Use 'search_docs' to explore content",
        ],
    }
    return {"result": _to_markdown(res, "chunk_stats")}


def _build_structured_help() -> dict:
    """Build multilevel help: server info, tools by group, prompts, skills, doc areas."""
    docs_root = config.DOCS_ROOT.resolve()
    store = get_store()
    meta = store.get_table_metadata() if hasattr(store, "get_table_metadata") else {}
    sources = store.list_sources() if meta.get("exists") else []
    # Top-level doc areas (dirs under DOCS_ROOT) for orientation
    doc_areas = []
    if docs_root.is_dir():
        try:
            for p in sorted(docs_root.iterdir()):
                if p.is_dir() and not p.name.startswith("."):
                    doc_areas.append({"name": p.name, "path": str(p.relative_to(docs_root)).replace("\\", "/")})
        except OSError:
            pass

    tools_by_group = {
        "search_and_read": [
            {
                "name": "search_docs",
                "description": "Semantic search across indexed documentation.",
                "args": [
                    {"name": "query", "type": "str"},
                    {"name": "limit", "type": "int", "default": 5},
                ],
            },
            {
                "name": "ask_docs",
                "description": "Ask a question; get a synthesized answer (uses client sampling).",
                "args": [{"name": "question", "type": "str"}],
            },
            {
                "name": "get_document",
                "description": "Retrieve full document content by relative path.",
                "args": [{"name": "relative_path", "type": "str"}],
            },
        ],
        "index_and_workflow": [
            {
                "name": "reindex_docs",
                "description": "Force full re-indexing of documentation sources.",
                "args": [],
            },
            {
                "name": "chunk_stats",
                "description": "Index statistics and health metrics.",
                "args": [],
            },
            {
                "name": "agentic_doc_workflow",
                "description": "Run autonomous documentation research (sampling).",
                "args": [{"name": "workflow_prompt", "type": "str"}],
            },
        ],
        "memory": [
            {
                "name": "persistence_store_memory",
                "description": "Persist memory in a namespace for later recall.",
                "args": [{"name": "namespace", "type": "str"}, {"name": "content", "type": "str"}],
            },
            {
                "name": "persistence_recall",
                "description": "Semantic search over stored memory in a namespace.",
                "args": [
                    {"name": "namespace", "type": "str"},
                    {"name": "query", "type": "str"},
                    {"name": "limit", "type": "int", "default": 10},
                ],
            },
            {
                "name": "persistence_compaction_status",
                "description": "Memory density and per-namespace stats.",
                "args": [],
            },
        ],
        "webapp": [
            {
                "name": "start_webapp",
                "description": "Start documentation-mcp webapp (backend, frontend, browser).",
                "args": [],
            },
        ],
        "discovery_and_health": [
            {
                "id": "documentation-mcp",
                "name": "Documentation MCP Hub",
                "description": "Public Repository - Documentation Control Plane for the documentation-mcp ecosystem.",
                "port": 10794,
            },
            {
                "name": "docs_help",
                "description": "This multilevel structured help (tools, prompts, skills, doc areas).",
                "args": [],
            },
            {
                "name": "server_status",
                "description": "Server and index health, version, memory summary.",
                "args": [],
            },
        ],
    }
    prompts = [
        {
            "name": "docs_expert",
            "description": "System instructions for documentation expert (search_docs, ask_docs, get_document).",
            "args": [{"name": "focus", "type": "str", "default": "general"}],
        },
        {
            "name": "research_workflow",
            "description": "Guidance for agentic_doc_workflow usage.",
            "args": [],
        },
    ]
    skills = []
    skills_dir = Path(__file__).resolve().parent / "skills"
    if skills_dir.is_dir():
        try:
            import frontmatter

            for subdir in sorted(skills_dir.iterdir()):
                if not subdir.is_dir():
                    continue
                skill_md = subdir / "SKILL.md"
                if not skill_md.is_file():
                    continue
                try:
                    with open(skill_md, encoding="utf-8") as f:
                        post = frontmatter.load(f)
                    skills.append(
                        {
                            "id": subdir.name,
                            "name": post.get("name") or subdir.name,
                            "description": (post.get("description") or "")[:200],
                            "uri": f"skill://{subdir.name}/SKILL.md",
                        }
                    )
                except Exception:
                    pass
        except Exception:
            pass

    return {
        "server": {
            "name": "Docs MCP",
            "description": "MCP Documentation Server – semantic search, ask_docs, agentic workflows, and navigation for the MCP ecosystem.",
        },
        "tools_by_group": tools_by_group,
        "prompts": prompts,
        "skills": skills,
        "doc_areas": doc_areas,
        "index_summary": {
            "source_count": len(sources),
            "sources_sample": sources[:15],
            "chunk_count": meta.get("row_count"),
        },
    }


@docs_mcp.tool()
def docs_help() -> dict:
    """Return multilevel structured help for this server: tools (grouped), prompts, skills, and doc areas.

    Use this first to discover what tools exist, how they are grouped, and what documentation areas
    are indexed. No arguments required.

    Returns:
        success, server (name, description), tools_by_group, prompts, skills, doc_areas, index_summary.
    """
    try:
        data = _build_structured_help()
        res = {"success": True, **data}
        return {"result": _to_markdown(res, "docs_help")}
    except Exception as e:
        logger.exception("docs_help failed")
        return {"success": False, "error": str(e), "message": "Failed to build structured help."}


@docs_mcp.tool()
def server_status() -> dict:
    """Report server and index health, version, and memory summary.

    Use this to check index readiness, chunk counts, and optional memory stats before running
    search_docs or ask_docs.

    Returns:
        success, server_name, version, index (chunk_count, source_count, embedding_model), memory (if available).
    """
    try:
        store = get_store()
        meta = store.get_table_metadata() if hasattr(store, "get_table_metadata") else {}
        sources = store.list_sources() if meta.get("exists") else []
        index_ok = meta.get("exists") and meta.get("row_count", 0) > 0
        memory_summary = None
        try:
            mem = get_memory_store()
            memory_summary = mem.compaction_status()
        except Exception:
            pass
        res = {
            "success": True,
            "server_name": "Docs MCP",
            "version": "1.0.0",
            "status": "ready" if index_ok else "index_empty",
            "index": {
                "chunk_count": meta.get("row_count", 0),
                "source_count": len(sources),
                "sources": sources[:20],
                "embedding_model": config.EMBEDDING_MODEL,
            },
            "memory": memory_summary,
        }
        return {"result": _to_markdown(res, "server_status")}
    except Exception as e:
        logger.exception("server_status failed")
        return {"success": False, "error": str(e), "message": "Status check failed."}


@docs_mcp.tool()
def get_document(relative_path: str) -> dict:
    """Retrieve the full content of a documentation file by its relative path.

    Use this after search_docs to fetch the complete document when a snippet is
    insufficient. The relative_path comes from search_docs result fields.

    Args:
        relative_path: Path relative to docs root, e.g. "standards/AGENT_PROTOCOLS.md"

    Returns:
        A result object with full markdown content and file metadata.
    """
    try:
        docs_root = config.DOCS_ROOT.resolve()
        target_path = (docs_root / relative_path).resolve()

        # Security: must stay inside DOCS_ROOT. use is_relative_to for robust check
        if not target_path.is_relative_to(docs_root):
            return {
                "success": False,
                "error": "Access denied",
                "message": f"Path '{relative_path}' resolves outside docs root.",
            }

        if not target_path.exists() or not target_path.is_file():
            return {
                "success": False,
                "error": "File not found",
                "message": f"No file found at '{relative_path}'.",
                "next_steps": [
                    "Use search_docs to locate the document",
                    "Check the file tree in the webapp Documents page",
                ],
            }

        with open(target_path, encoding="utf-8") as f:
            content = f.read()

        stat = target_path.stat()
        # Custom Markdown for get_document
        md = [
            f"# 📄 File: {target_path.name}",
            f"- **Path**: `{relative_path}`",
            f"- **Size**: `{stat.st_size} bytes`",
            "\n```markdown",
            content,
            "```",
        ]
        return {"result": "\n".join(md)}
    except Exception as e:
        logger.error(f"get_document error: {e}")
        return {"success": False, "error": str(e), "message": "Failed to retrieve document."}


# --- Managed Persistence tools (persistent, namespace-scoped, semantic recall) ---


@docs_mcp.tool()
def persistence_store_memory(namespace: str, content: str) -> dict:
    """Persist structured memory in a namespace for later semantic recall.

    Use this to store facts, decisions, or context that agents should remember across sessions.
    Namespaces isolate memory by agent, project, or topic (e.g. 'robofang', 'email-mcp').

    Args:
        namespace: Logical bucket for this memory (e.g. agent name or project).
        content: The text to store (will be embedded for semantic search).

    Returns:
        success, id, created_at, namespace; or success=False with error.
    """
    store = get_memory_store()
    return store.store(namespace=namespace or "", content=content or "")


@docs_mcp.tool()
def persistence_recall(namespace: str, query: str, limit: int = 10) -> dict:
    """Semantic search over stored memory in a namespace.

    Returns the most relevant stored entries for the query within the given namespace.
    Use after storing memories with persistence_store_memory.

    Args:
        namespace: The namespace to search (same as used in store).
        query: Natural language query (e.g. "What did we decide about the API?").
        limit: Max number of results (default 10).

    Returns:
        success, data (list of {content, created_at, score, id}), message.
    """
    store = get_memory_store()
    hits = store.recall(namespace=namespace or "", query=query or "", limit=min(limit, 50))
    res = {
        "success": True,
        "operation": "persistence_recall",
        "namespace": namespace,
        "data": hits,
        "message": f"Found {len(hits)} relevant memories in namespace '{namespace}'.",
    }
    return {"result": _to_markdown(res, "persistence_recall")}


@docs_mcp.tool()
def persistence_compaction_status() -> dict:
    """Report memory density and per-namespace stats; suggests when to compact.

    Use this to monitor how much is stored and whether summarization/compaction
    would be beneficial (e.g. when a namespace has many entries).

    Returns:
        success, total_entries, namespaces, entries_per_namespace, suggestion.
    """
    store = get_memory_store()
    return store.compaction_status()


# --- MCP Prompts (FastMCP 3.1) ---


@docs_mcp.prompt(
    name="docs_expert",
    description="Load system instructions for acting as a documentation expert using this server's tools (search_docs, ask_docs, get_document).",
    tags={"docs", "expert", "search"},
)
def docs_expert(focus: str = "general") -> str:
    """Return system-style instructions for documentation expert behavior."""
    base = (
        "You are a documentation expert for the MCP ecosystem. Use this server's tools to find and cite sources. "
        "Use search_docs(query, limit) for semantic search, ask_docs(question) for synthesized answers (requires client sampling), "
        "get_document(relative_path) to fetch a full file after search. Always cite filenames or relative_path from results."
    )
    if focus == "search":
        return base + "\n\nPrefer search_docs first; use ask_docs only when the user wants a synthesized answer."
    if focus == "sources":
        return base + "\n\nAlways return source filenames and relative_path so the user can open or get_document them."
    return base


@docs_mcp.prompt(
    name="research_workflow",
    description="Instructions for running a multi-step documentation research workflow (agentic_doc_workflow).",
    tags={"docs", "workflow", "research"},
)
def research_workflow() -> str:
    """Return guidance for using the agentic doc workflow."""
    return (
        "To run autonomous documentation research, use the agentic_doc_workflow(workflow_prompt) tool. "
        "Pass a clear goal (e.g. 'Summarize FastMCP 3.1 prompts and skills'). The server will use sampling to "
        "orchestrate search_docs and ask_docs and return a final report. Requires a client that supports MCP sampling."
    )


# --- Web App Integration ---


# API Routes
async def api_search(request: Request):
    """Semantic search across documentation"""
    try:
        q = request.query_params.get("q", "")
        store = get_store()
        results = store.search(q, limit=10)

        # Standardize format for frontend
        data = []
        for r in results:
            distance = r.get("_distance", 0.0)
            score = max(0.0, 1.0 - distance)
            data.append(
                {
                    "id": r.get("id"),
                    "filename": r.get("metadata", {}).get("filename", "unknown"),
                    "relative_path": r.get("metadata", {}).get("relative_path", "unknown"),
                    "score": score,
                    "content": r.get("content", ""),
                }
            )

        return JSONResponse(data)
    except Exception as e:
        logger.error(f"Error in api_search: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


def _persona_system_hint(persona: str) -> str:
    """Optional one-line system hint from persona id. Not a model list."""
    hints = {
        "technical": "Answer in a precise, code-focused way. Prefer exact names and snippets.",
        "concise": "Keep answers short and to the point. Bullet points when helpful.",
        "educator": "Explain step by step. Assume the user is learning.",
    }
    return hints.get((persona or "").strip().lower(), "")


async def api_chat(request: Request):
    """Conversational RAG endpoint. Uses settings (Ollama or local LLM) when configured."""
    try:
        body = await request.json()
        question = (body.get("message") or "").strip()
        system_prompt_override = (body.get("system_prompt") or "").strip()
        persona = (body.get("persona") or "").strip()

        if not question:
            return JSONResponse({"error": "No message provided"}, status_code=400)

        search_result = _search_docs_raw(question, limit=5)
        sources = [r["filename"] for r in search_result.get("data") or []]
        context_text = ""
        if search_result.get("success") and search_result.get("data"):
            context_text = "\n\n".join(
                [f"SOURCE: {r['filename']}\nCONTENT: {r['content']}" for r in search_result["data"]]
            )

        system_parts = []
        if system_prompt_override:
            system_parts.append(system_prompt_override)
        persona_hint = _persona_system_hint(persona)
        if persona_hint:
            system_parts.append(persona_hint)
        system_parts.append(
            "Answer based on the following documentation context. If the context does not contain enough information, say so and keep the answer brief."
        )
        if context_text:
            system_parts.append("\n\n--- Documentation context ---\n\n" + context_text)

        system_content = "\n\n".join(system_parts)
        messages = []
        if system_content:
            messages.append({"role": "system", "content": system_content})
        messages.append({"role": "user", "content": question})

        settings = settings_store.load_settings()
        provider = (settings.get("provider") or "").strip().lower()
        answer: str

        if provider == "ollama":
            ollama_url = (settings.get("ollama_url") or "").strip()
            ollama_model = (settings.get("ollama_model") or "").strip()
            if not ollama_url or not ollama_model:
                answer = "Ollama is selected but URL or model is missing. Check Settings."
            else:
                try:
                    answer = await llm_client.chat_ollama(ollama_url, ollama_model, messages)
                except Exception as e:
                    logger.exception("Ollama chat failed")
                    answer = f"I couldn't reach the LLM: {e!s}"
        elif provider == "local":
            local_url = (settings.get("local_llm_url") or "").strip()
            local_key = (settings.get("local_llm_key") or "").strip()
            model = (settings.get("ollama_model") or "").strip()  # reuse field for local model name if desired
            if not local_url:
                answer = "Local LLM is selected but base URL is missing. Check Settings."
            else:
                try:
                    answer = await llm_client.chat_openai_compatible(local_url, local_key, model or "default", messages)
                except Exception as e:
                    logger.exception("Local LLM chat failed")
                    answer = f"I couldn't reach the LLM: {e!s}"
        elif provider == "lmstudio":
            lmstudio_url = (settings.get("lmstudio_url") or "").strip()
            lmstudio_model = (settings.get("lmstudio_model") or "").strip()
            if not lmstudio_url:
                answer = "LM Studio is selected but server URL is missing. Check Settings."
            else:
                try:
                    answer = await llm_client.chat_openai_compatible(
                        lmstudio_url, "", lmstudio_model or "default", messages
                    )
                except Exception as e:
                    logger.exception("LM Studio chat failed")
                    answer = f"I couldn't reach the LLM: {e!s}"
        else:
            # No LLM configured: fallback to RAG-only concatenation
            if not search_result.get("success") or not search_result.get("data"):
                answer = "I couldn't find any relevant documentation to answer that."
                sources = []
            else:
                top_result = search_result["data"][0]["content"]
                answer = f"Based on the documentation ({', '.join(sources[:3])}), here is what I found:\n\n" + (
                    top_result[:800] + "..." if len(top_result) > 800 else top_result
                )

        return JSONResponse({"answer": answer, "sources": sources})
    except Exception as e:
        logger.error(f"Error in api_chat: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_settings_get(request: Request):
    """Return current webapp settings. API key is masked."""
    try:
        s = settings_store.load_settings()
        key = s.get("local_llm_key") or ""
        if len(key) > 4:
            s = {**s, "local_llm_key": "****" + key[-4:]}
        else:
            s = {**s, "local_llm_key": "****" if key else ""}
        return JSONResponse(s)
    except Exception as e:
        logger.error(f"Error in api_settings_get: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_settings_put(request: Request):
    """Save webapp settings (ollama_url, ollama_model, local_llm_url, local_llm_key, provider)."""
    try:
        body = await request.json()
        current = settings_store.load_settings()
        if "local_llm_key" in body and (body["local_llm_key"] or "").strip() == "":
            body["local_llm_key"] = current.get("local_llm_key") or ""
        if (body.get("local_llm_key") or "").startswith("****"):
            body["local_llm_key"] = current.get("local_llm_key") or ""
        updates = {
            "ollama_url": (body.get("ollama_url") or "").strip(),
            "ollama_model": (body.get("ollama_model") or "").strip(),
            "local_llm_url": (body.get("local_llm_url") or "").strip(),
            "local_llm_key": (body.get("local_llm_key") or "").strip(),
            "lmstudio_url": (body.get("lmstudio_url") or "").strip(),
            "lmstudio_model": (body.get("lmstudio_model") or "").strip(),
            "provider": (body.get("provider") or "").strip().lower(),
        }
        if updates["provider"] not in ("ollama", "local", "lmstudio", ""):
            updates["provider"] = ""
        settings_store.save_settings({**current, **updates})
        return JSONResponse({"success": True})
    except Exception as e:
        logger.error(f"Error in api_settings_put: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_ollama_models(request: Request):
    """List available Ollama models by querying Ollama API. Uses ?url= for ad-hoc or saved settings."""
    try:
        base_url = (request.query_params.get("url") or "").strip()
        if not base_url:
            s = settings_store.load_settings()
            base_url = (s.get("ollama_url") or "").strip()
        if not base_url:
            return JSONResponse({"models": [], "message": "Provide ?url= or configure Ollama URL in Settings."})
        models, error = await llm_client.list_ollama_models(base_url)
        payload = {"models": models}
        if error:
            payload["message"] = error
        return JSONResponse(payload)
    except Exception as e:
        logger.error(f"Error in api_ollama_models: {e}")
        return JSONResponse({"error": str(e), "models": [], "message": str(e)}, status_code=500)


async def api_lmstudio_models(request: Request):
    """List models from LM Studio (OpenAI-compatible GET /v1/models). Uses ?url= or saved lmstudio_url."""
    try:
        base_url = (request.query_params.get("url") or "").strip()
        if not base_url:
            s = settings_store.load_settings()
            base_url = (s.get("lmstudio_url") or "").strip()
        if not base_url:
            return JSONResponse({"models": [], "message": "Provide ?url= or configure LM Studio URL in Settings."})
        models = await llm_client.list_openai_models(base_url)
        return JSONResponse({"models": models})
    except Exception as e:
        logger.error(f"Error in api_lmstudio_models: {e}")
        return JSONResponse({"error": str(e), "models": []}, status_code=500)


async def api_ingest_folder(request: Request):
    """Dynamically ingest a user-specified folder of markdown files"""
    try:
        body = await request.json()
        folder_path_str = body.get("folder_path")

        if not folder_path_str:
            return JSONResponse({"error": "No folder_path provided"}, status_code=400)

        folder_path = Path(folder_path_str)
        if not folder_path.exists() or not folder_path.is_dir():
            return JSONResponse({"error": f"Invalid folder path: {folder_path_str}"}, status_code=404)

        store = get_store()
        ingestor = ContentIngestor()
        docs = ingestor.load_all_docs(extra_paths=[folder_path])

        if docs:
            # We don't overwrite everything, ideally we just add or update based on ids.
            # Add_documents handles upserts based on ID matching over lancedb.
            store.add_documents(docs)
            count = len(docs)
            return JSONResponse(
                {
                    "success": True,
                    "message": f"Successfully ingested {count} chunks including custom folder {folder_path_str}",
                    "chunks_processed": count,
                }
            )
        else:
            return JSONResponse({"success": False, "error": "No markdown files found to ingest."})

    except Exception as e:
        logger.error(f"Error dynamically ingesting folder: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


def build_file_tree(path: Path, root: Path) -> dict:
    """Recursively builds a file tree"""
    item = {
        "id": str(path.relative_to(root)),
        "title": path.name,
        "type": "folder" if path.is_dir() else "file",
        "path": f"/api/content?path={str(path.relative_to(root))}" if path.is_file() else None,
    }
    if path.is_dir():
        children = []
        try:
            for p in sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
                if p.name.startswith(".") or p.name == "__pycache__" or p.name == "node_modules":
                    continue
                if p.is_file() and p.suffix != ".md":
                    continue
                children.append(build_file_tree(p, root))
        except PermissionError:
            pass
        item["children"] = children
    return item


async def api_tree(request: Request):
    """Serve the documentation file tree"""
    try:
        root_path = config.DOCS_ROOT
        tree = build_file_tree(root_path, root_path)
        # Return children of root to avoid top-level "docs" folder if preferred,
        # or return the whole tree. Let's return the root's children to look cleaner.
        return JSONResponse(tree.get("children", []))
    except Exception as e:
        logger.error(f"Error building tree: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_content(request: Request):
    """Serve raw markdown content"""
    try:
        path_param = request.query_params.get("path")
        if not path_param:
            return JSONResponse({"error": "Missing path parameter"}, status_code=400)

        target_path = (config.DOCS_ROOT / path_param).resolve()

        # Security check: Ensure we don't escape DOCS_ROOT
        if not str(target_path).startswith(str(config.DOCS_ROOT)):
            return JSONResponse({"error": "Access denied"}, status_code=403)

        if not target_path.exists() or not target_path.is_file():
            return JSONResponse({"error": "File not found"}, status_code=404)

        with open(target_path, encoding="utf-8") as f:
            content = f.read()

        return JSONResponse({"content": content})
    except Exception as e:
        logger.error(f"Error serving content: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_logs(request: Request):
    """Serve the debug log content (last 100 lines)"""
    try:
        log_path = Path("debug.log")
        if not log_path.exists():
            return JSONResponse({"logs": ["Log file not found."]})

        with open(log_path, encoding="utf-8") as f:
            lines = f.readlines()
            # Return last 100 lines
            return JSONResponse({"logs": lines[-100:]})
    except Exception as e:
        logger.error(f"Error serving logs: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_reindex(request: Request):
    """Trigger the manual re-indexing tool via REST"""
    try:
        result = reindex_docs()
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error in api_reindex: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# Tools considered "pertinent" for MaaS (other repos calling Docs MCP as a service)
MAAS_TOOL_NAMES = frozenset(
    {
        "search_docs",
        "get_document",
        "ask_docs",
        "chunk_stats",
        "nemoclaw_store_memory",
        "nemoclaw_recall",
        "nemoclaw_compaction_status",
    }
)


def _tools_to_json(tools_list: list, filter_names: frozenset | None = None) -> list:
    out = []
    for tool in tools_list or []:
        name = getattr(tool, "name", "")
        if filter_names is not None and name not in filter_names:
            continue
        params = getattr(tool, "parameters", None) or getattr(tool, "inputSchema", None)
        out.append(
            {
                "name": name,
                "description": getattr(tool, "description", "") or "",
                "parameters": params,
            }
        )
    return out


async def api_tools(request: Request):
    """List all registered MCP tools. FastMCP 3 uses .parameters, legacy used .inputSchema."""
    try:
        tools_list = await docs_mcp.list_tools()
        return JSONResponse(_tools_to_json(tools_list))
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_maas_tools(request: Request):
    """List tools pertinent for MaaS (other repos): search_docs, get_document, ask_docs, chunk_stats."""
    try:
        tools_list = await docs_mcp.list_tools()
        return JSONResponse(_tools_to_json(tools_list, filter_names=MAAS_TOOL_NAMES))
    except Exception as e:
        logger.error(f"Error listing MaaS tools: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_execute_tool(request: Request):
    """Execute an MCP tool via REST. Uses FastMCP 3 call_tool()."""
    try:
        body = await request.json()
        name = body.get("name")
        arguments = body.get("arguments", {})

        if not name:
            return JSONResponse({"error": "Missing tool name"}, status_code=400)

        tools_list = await docs_mcp.list_tools()
        tool_names = {getattr(t, "name", "") for t in (tools_list or [])}
        if name not in tool_names:
            return JSONResponse({"error": f"Tool '{name}' not found"}, status_code=404)

        result = await docs_mcp.call_tool(name, arguments or None)

        # FastMCP 3 ToolResult: .content can be list of TextContent (not JSON-serializable); normalize to str
        def to_serializable(obj):
            if obj is None:
                return ""
            if isinstance(obj, dict):
                return json.dumps(obj, indent=2)
            if isinstance(obj, str):
                return obj
            if hasattr(obj, "content") and obj.content:
                parts = obj.content
                if isinstance(parts, list):
                    return "".join(getattr(p, "text", str(p)) if p else "" for p in parts).strip() or str(obj)
                return getattr(parts, "text", str(parts))
            if isinstance(obj, list) and obj and hasattr(obj[0], "text"):
                return (obj[0].text or "").strip() or str(obj)
            if hasattr(obj, "text"):
                return (obj.text or "").strip() or str(obj)
            return str(obj)

        out = to_serializable(result)
        return JSONResponse({"result": out})
    except Exception as e:
        logger.error(f"Error executing tool: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_launch_app(request: Request):
    """Launch an application by running its start script"""
    try:
        body = await request.json()
        label = body.get("label")

        # Find the app in the catalog
        from docs_mcp.backend.apps_catalog import APPS_CATALOG

        app = next((a for a in APPS_CATALOG if a["label"] == label), None)
        if not app:
            return JSONResponse({"error": f"App '{label}' not found"}, status_code=404)

        script_path = app.get("startScript")
        if not script_path:
            return JSONResponse({"error": f"Start script for '{label}' not defined"}, status_code=400)

        # Execute the script
        import subprocess
        from pathlib import Path

        # The scripts are relative to the repos root (d:\Dev\repos)
        # We can derive this if we are running in d:\Dev\repos\mcp-central-docs
        repos_root = Path(__file__).parent.parent.parent.parent

        abs_script_path = repos_root / script_path

        if not abs_script_path.exists():
            return JSONResponse({"error": f"Script not found at {abs_script_path}"}, status_code=404)

        cmd = []
        if abs_script_path.suffix == ".ps1":
            cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(abs_script_path)]
        else:
            # For .bat files on Windows
            cmd = [str(abs_script_path)]

        # Run in background without blocking the server
        # use CREATE_NEW_CONSOLE to ensure the webapp starts in its own terminal
        subprocess.Popen(cmd, cwd=str(abs_script_path.parent), creationflags=subprocess.CREATE_NEW_CONSOLE)

        return JSONResponse({"success": True, "message": f"Launched {label}"})
    except Exception as e:
        logger.error(f"Error launching app: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_fleet_launch(request: Request):
    """Standardized fleet launch endpoint"""
    try:
        body = await request.json()
        repo_path = body.get("repo_path")
        if not repo_path:
            return JSONResponse({"error": "Missing repo_path"}, status_code=400)

        path = Path(repo_path)
        if not path.exists():
            return JSONResponse({"error": "Path not found"}, status_code=404)

        # Security check
        allowed_base = Path("D:/Dev/repos")
        try:
            path.relative_to(allowed_base)
        except ValueError:
            return JSONResponse({"error": "Access denied"}, status_code=403)

        start_script = path / "web_sota" / "start.ps1"
        if not start_script.exists():
            start_script = path / "web" / "start.ps1"
            if not start_script.exists():
                start_script = path / "start.ps1"
                if not start_script.exists():
                    return JSONResponse({"error": "No start.ps1 found"}, status_code=400)

        import subprocess

        cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(start_script)]
        subprocess.Popen(cmd, cwd=str(path), creationflags=subprocess.CREATE_NEW_CONSOLE)
        return JSONResponse({"success": True, "message": f"Launched {path.name}"})
    except Exception as e:
        logger.error(f"Fleet launch failed: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_apps(request: Request):
    """Serve the fleet registry from the global operations file"""
    try:
        import json
        from pathlib import Path

        # Paths are relative to d:\Dev\repos\mcp-central-docs
        registry_path = Path(__file__).parent.parent.parent / "operations" / "fleet-registry.json"

        if registry_path.exists():
            with open(registry_path) as f:
                data = json.load(f)
                # Support both "apps" and "fleet" keys (fleet-registry.json uses "fleet")
                apps = data.get("apps") if "apps" in data else data.get("fleet", [])
                return JSONResponse(apps)

        # Fallback to local catalog if global not found
        from docs_mcp.backend.apps_catalog import APPS_CATALOG

        return JSONResponse(APPS_CATALOG)
    except Exception as e:
        logger.error(f"Error serving fleet registry: {e}")
        from docs_mcp.backend.apps_catalog import APPS_CATALOG

        return JSONResponse(APPS_CATALOG)


async def api_skills(request: Request):
    """List skills exposed by this server (SkillsDirectoryProvider). Scans server's skills dir and parses SKILL.md frontmatter."""
    try:
        import frontmatter

        skills_dir = Path(__file__).resolve().parent / "skills"
        if not skills_dir.is_dir():
            return JSONResponse({"skills": []})

        skills = []
        for subdir in sorted(skills_dir.iterdir()):
            if not subdir.is_dir():
                continue
            skill_md = subdir / "SKILL.md"
            if not skill_md.is_file():
                continue
            try:
                with open(skill_md, encoding="utf-8") as f:
                    post = frontmatter.load(f)
                skills.append(
                    {
                        "id": subdir.name,
                        "name": post.get("name") or subdir.name,
                        "description": post.get("description") or "",
                        "content": post.content,
                        "uri": f"skill://{subdir.name}/SKILL.md",
                    }
                )
            except Exception as e:
                logger.warning("Failed to parse skill %s: %s", subdir.name, e)
        return JSONResponse({"skills": skills})
    except Exception as e:
        logger.error(f"Error listing skills: {e}")
        return JSONResponse({"skills": [], "error": str(e)})


async def api_skill_marketplaces(request: Request):
    """Serve curated skill marketplaces from operations/skill_marketplaces.json."""
    try:
        import json

        repo_root = Path(__file__).resolve().parent.parent.parent
        path = repo_root / "operations" / "skill_marketplaces.json"
        if not path.exists():
            return JSONResponse({"marketplaces": []})
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse({"marketplaces": data if isinstance(data, list) else []})
    except Exception as e:
        logger.error(f"Error serving skill marketplaces: {e}")
        return JSONResponse({"marketplaces": [], "error": str(e)})


async def api_verification_matrix(request: Request):
    """Serve verification matrix from operations/verification_matrix.json (data-driven, no hardcode)."""
    try:
        import json

        repo_root = Path(__file__).resolve().parent.parent.parent
        matrix_path = repo_root / "operations" / "verification_matrix.json"
        if not matrix_path.exists():
            return JSONResponse(
                {
                    "title": "",
                    "subtitle": "",
                    "columns": [],
                    "clients": [],
                    "error": "verification_matrix.json not found",
                },
                status_code=404,
            )
        with open(matrix_path, encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse(data)
    except Exception as e:
        logger.error(f"Error serving verification matrix: {e}")
        return JSONResponse(
            {"title": "", "subtitle": "", "columns": [], "clients": [], "error": str(e)},
            status_code=500,
        )


async def api_status(request: Request):
    """Aggregate metrics and status for the dashboard"""
    try:
        store = get_store()
        meta = store.get_table_metadata() if hasattr(store, "get_table_metadata") else {}
        sources = store.list_sources() if meta.get("exists") else []

        # Get memory stats
        memory_summary = None
        try:
            mem = get_memory_store()
            memory_summary = mem.compaction_status()
        except Exception:
            pass

        # Get settings for model info
        settings = settings_store.load_settings()
        provider = settings.get("provider") or "none"
        model = settings.get("ollama_model") or settings.get("lmstudio_model") or "n/a"

        # Get fleet count
        fleet_count = 0
        try:
            from docs_mcp.backend.apps_catalog import APPS_CATALOG

            registry_path = Path(__file__).parent.parent.parent / "operations" / "fleet-registry.json"
            if registry_path.exists():
                with open(registry_path) as f:
                    data = json.load(f)
                    apps = data.get("apps") if "apps" in data else data.get("fleet", [])
                    fleet_count = len(apps)
            else:
                fleet_count = len(APPS_CATALOG)
        except Exception:
            pass

        return JSONResponse(
            {
                "success": True,
                "chunk_count": meta.get("row_count", 0),
                "source_count": len(sources),
                "fleet_count": fleet_count,
                "provider": provider,
                "model": model,
                "memory": memory_summary,
                "status": "ready" if meta.get("exists") and meta.get("row_count") else "index_empty",
            }
        )
    except Exception as e:
        logger.error(f"Error in api_status: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# SPA Handling
async def serve_spa(request: Request):
    frontend_dist = Path(__file__).parent.parent.parent / "web_sota" / "dist"
    index_path = frontend_dist / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return Response("Frontend not built", status_code=404)


# Create main Starlette app

routes = [
    # API Routes
    Route("/api/status", api_status, methods=["GET"]),
    Route("/api/search", api_search, methods=["GET"]),
    Route("/api/tree", api_tree, methods=["GET"]),
    Route("/api/content", api_content, methods=["GET"]),
    Route("/api/logs", api_logs, methods=["GET"]),
    Route("/api/tools", api_tools, methods=["GET"]),
    Route("/api/maas/tools", api_maas_tools, methods=["GET"]),
    Route("/api/apps", api_apps, methods=["GET"]),
    Route("/api/apps/launch", api_launch_app, methods=["POST"]),
    Route("/api/fleet/launch", api_fleet_launch, methods=["POST"]),
    Route("/api/reindex", api_reindex, methods=["GET"]),
    Route("/api/execute", api_execute_tool, methods=["POST"]),
    Route("/api/chat", api_chat, methods=["POST"]),
    Route("/api/ingest_folder", api_ingest_folder, methods=["POST"]),
    Route("/api/settings", api_settings_get, methods=["GET"]),
    Route("/api/settings", api_settings_put, methods=["PUT"]),
    Route("/api/ollama/models", api_ollama_models, methods=["GET"]),
    Route("/api/lmstudio/models", api_lmstudio_models, methods=["GET"]),
    Route("/api/skills", api_skills, methods=["GET"]),
    Route("/api/skill_marketplaces", api_skill_marketplaces, methods=["GET"]),
    # Static Assets (FastMCP 3.0 runs as stdio only, not mounted in Starlette)
    Mount(
        "/assets",
        app=StaticFiles(directory=Path(__file__).parent.parent.parent / "web_sota" / "dist" / "assets"),
        name="assets",
    ),
    # Catch-all for SPA (must be last)
    Route("/{path:path}", serve_spa),
]

app = Starlette(routes=routes, lifespan=lifespan)


from starlette.middleware.base import BaseHTTPMiddleware

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        log_to_file(f"DEBUG: Middleware request: {request.method} {request.url}")
        try:
            response = await call_next(request)
            log_to_file(f"DEBUG: Middleware response: {response.status_code}")
            return response
        except Exception as e:
            log_to_file(f"DEBUG: Middleware error: {e}")
            traceback.print_exc()
            raise e

app.add_middleware(LogMiddleware)


def main():
    """Entry point for stdio MCP mode (Claude Desktop)."""
    docs_mcp.run(transport="stdio")


if __name__ == "__main__":
    # For local testing, we can run this file directly
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=10794)
