import logging

from fastmcp import Context, FastMCP

from docs_mcp.backend import llm_client, settings_store
from docs_mcp.backend.ingestor import ContentIngestor
from docs_mcp.backend.llm_client import list_ollama_models, list_openai_models
from docs_mcp.backend.store_registry import get_store
from docs_mcp.utils.formatting import _to_markdown

logger = logging.getLogger("docs_mcp.tools.rag")

def _search_docs_raw(query: str, limit: int = 5) -> dict:
    """Internal search helper returning a plain dict (not markdown)."""
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

def search_docs(query: str, limit: int = 5) -> dict:
    """Perform a semantic search across all indexed documentation."""
    res = _search_docs_raw(query, limit=limit)
    return {"result": _to_markdown(res, "search_docs")}


def register_tools(mcp: FastMCP):
    """Register RAG-related MCP tools."""

    mcp.tool()(search_docs)
    mcp.tool()(reindex_docs)
    mcp.tool()(get_document)

    @mcp.tool()
    async def ask_docs(question: str, ctx: Context) -> dict:
        """Ask a complex question about the documentation and get a synthesized answer."""
        search_result = _search_docs_raw(question, limit=10)
        if not search_result["success"]:
            return {"result": search_result["message"]}

        context_text = "\n\n".join([f"SOURCE: {r['filename']}\nCONTENT: {r['content']}" for r in search_result["data"]])
        system_prompt = "You are a technical documentation expert. Provide concise, accurate answers citing sources."
        user_prompt = f"Answer the following question based ONLY on the provided documentation context.\n\nCONTEXT:\n{context_text}\n\nQUESTION: {question}"

        error_log = []

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

        # Fallback to local LLM discovery
        ctx.report_progress("Sampling failed. Starting local LLM discovery...", 40)
        settings = settings_store.load_settings()
        ollama_url = settings.get("ollama_url") or "http://localhost:11434"
        lmstudio_url = settings.get("lmstudio_url") or "http://localhost:1234/v1"

        import asyncio
        try:
            tasks = [list_ollama_models(ollama_url), list_openai_models(lmstudio_url)]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            ollama_res = results[0] if not isinstance(results[0], Exception) else ([], f"Ollama Error: {results[0]}")
            lmstudio_res = results[1] if not isinstance(results[1], Exception) else ([], f"LM Studio Error: {results[1]}")

            ollama_models, o_err = ollama_res
            lm_models, l_err = lmstudio_res

            if o_err: error_log.append(o_err)
            if l_err: error_log.append(l_err)

            final_provider, final_url, final_model = None, None, None

            if lm_models:
                final_provider, final_url, final_model = "openai", lmstudio_url, lm_models[0]
            elif ollama_models:
                final_provider, final_url = "ollama", ollama_url
                priority = ["qwen2.5", "llama3.2", "phi4", "gemma"]
                for p in priority:
                    match = next((m for m in ollama_models if p in m.lower()), None)
                    if match:
                        final_model = match
                        break
                if not final_model: final_model = ollama_models[0]

            if final_provider and final_model:
                ctx.report_progress(f"Synthesizing answer via {final_provider} ({final_model})...", 60)
                messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]

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
                    "next_steps": ["Check cited sources", "Tweak local LLM settings"],
                }
                return {"result": _to_markdown(res, "ask_docs")}

        except Exception as e:
            error_log.append(f"Auto-Discovery Error: {e}")

        return {
            "success": False,
            "error": "Synthesis error",
            "message": "Documentation found, but synthesis failed.",
            "data": search_result["data"],
            "diagnostic_log": error_log,
        }


async def reindex_docs(ctx: Context) -> dict:
    """Force a full scan and re-indexing of all documentation sources."""
    try:
        ctx.report_progress("Connecting to DocumentStore...", 10)
        store = get_store()
        ingestor = ContentIngestor()
        from docs_mcp.backend.config import config as cfg
        extra = cfg.EXTRA_PATHS if cfg.EXTRA_PATHS else None
        docs = ingestor.load_all_docs(extra_paths=extra)

        if docs:
            ctx.report_progress(f"Embedding and indexing {len(docs)} chunks...", 60)
            store.add_documents(docs)
            res = {
                "success": True,
                "operation": "reindex_docs",
                "message": f"Documentation synchronized. {len(docs)} chunks indexed.",
                "data": {"chunks": len(docs)},
            }
            return {"result": _to_markdown(res, "reindex_docs")}
        return {"success": False, "message": "No docs found."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_document(relative_path: str) -> dict:
    """Retrieve the full content of a documentation file by its relative path."""
    try:
        from docs_mcp.backend.config import config
        docs_root = config.DOCS_ROOT.resolve()
        target_path = (docs_root / relative_path).resolve()

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
            }

        with open(target_path, encoding="utf-8") as f:
            content = f.read()

        import datetime
        stat = target_path.stat()
        res = {
            "success": True,
            "operation": "get_document",
            "message": f"Successfully retrieved '{relative_path}'.",
            "data": {
                "content": content,
                "path": str(target_path),
                "size": stat.st_size,
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            },
        }
        return {"result": _to_markdown(res, "get_document")}
    except Exception as e:
        return {"success": False, "error": str(e)}
