import asyncio
import json
import logging
import time
import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request
from fastapi.responses import StreamingResponse

from docs_mcp.backend.config import config
from docs_mcp.backend.ingestor import ContentIngestor
from docs_mcp.backend.store_registry import get_store

logger = logging.getLogger("docs_mcp.api.docs")
router = APIRouter(prefix="/api")

_reindex_status: dict[str, str] = {}
_reindex_events: dict[str, list[str]] = {}


async def _run_reindex(job_id: str) -> None:
    try:
        _reindex_status[job_id] = "running"
        store = get_store()
        from docs_mcp.backend.rag_paths import effective_extra_paths

        ingestor = ContentIngestor()
        extra = effective_extra_paths()
        docs = ingestor.load_all_docs(extra_paths=extra or None)
        if docs:
            store.add_documents(docs)
            msg = f"complete:{len(docs)}"
            _reindex_status[job_id] = msg
            _reindex_events.setdefault(job_id, []).append(json.dumps({"type": "complete", "chunks": len(docs)}))
        else:
            _reindex_status[job_id] = "error:no docs found"
            _reindex_events.setdefault(job_id, []).append(json.dumps({"type": "error", "error": "No docs found"}))
    except Exception as e:
        logger.error(f"Reindex job {job_id} failed: {e}")
        _reindex_status[job_id] = f"error:{e}"
        _reindex_events.setdefault(job_id, []).append(json.dumps({"type": "error", "error": str(e)}))


@router.get("/search")
async def api_search(
    q: str = "",
    limit: int = Query(default=10, le=50),
    offset: int = Query(default=0, ge=0),
    source: str | None = Query(default=None),
    category: str | None = Query(default=None),
):
    """Semantic search with FTS5 fallback, filters, and pagination."""
    try:
        store = get_store()
        results = store.search(q, limit=limit, offset=offset, source=source)

        # If vector search returns 0, try FTS5 keyword fallback
        if not results and q.strip():
            results = _fts_fallback(q, limit, offset)

        data = []
        for r in results:
            distance = r.get("_distance", 0.0)
            score = max(0.0, 1.0 - distance) if "_distance" in r else 1.0
            item = {
                "id": r.get("id"),
                "filename": r.get("metadata", {}).get("filename", "unknown"),
                "relative_path": r.get("metadata", {}).get("relative_path", "unknown"),
                "score": score,
                "content": r.get("content", ""),
            }
            if "category" in r.get("metadata", {}):
                item["category"] = r["metadata"]["category"]
            data.append(item)

        # Client-side source/category filter
        if source:
            data = [d for d in data if source.lower() in d.get("filename", "").lower()]
        if category:
            data = [d for d in data if d.get("category", "").lower() == category.lower()]

        return {
            "results": data,
            "total": len(data),
            "limit": limit,
            "offset": offset,
            "has_more": len(data) >= limit,
        }
    except Exception as e:
        logger.error(f"Error in api_search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _fts_fallback(query: str, limit: int = 10, offset: int = 0) -> list[dict]:
    """Simple keyword fallback when vector search returns nothing."""
    query_lower = query.lower()
    store = get_store()
    meta = store.get_table_metadata() if hasattr(store, "get_table_metadata") else {}
    if not meta.get("exists"):
        return []
    # Get all docs and filter by keyword match (limited fallback for small corpuses)
    try:
        tbl = store.db.open_table(store.table_name)
        all_rows = tbl.to_arrow().to_pylist()
        matched = []
        for r in all_rows:
            content = (r.get("content") or "").lower()
            filename = (r.get("metadata") or {}).get("filename", "").lower()
            if query_lower in content or query_lower in filename:
                matched.append(r)
        return matched[offset:offset + limit]
    except Exception as e:
        logger.warning(f"FTS fallback failed: {e}")
        return []


@router.get("/search/sources")
async def api_search_sources():
    """List unique source filenames for the filter dropdown."""
    try:
        store = get_store()
        meta = store.get_table_metadata() if hasattr(store, "get_table_metadata") else {}
        if not meta.get("exists"):
            return {"sources": []}
        tbl = store.db.open_table(store.table_name)
        rows = tbl.to_arrow().to_pylist()
        sources = sorted(set(
            r.get("metadata", {}).get("filename", "unknown") for r in rows
        ))
        return {"sources": sources}
    except Exception as e:
        logger.error(f"Error listing sources: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tree")
async def api_tree():
    """Returns the documentation file tree for the browser."""
    try:
        docs_root = config.DOCS_ROOT.resolve()
        if not docs_root.exists():
            return []

        def build_file_tree(path: Path, root: Path) -> dict:
            item = {
                "id": str(path.relative_to(root)).replace("\\", "/"),
                "title": path.name,
                "type": "folder" if path.is_dir() else "file",
                "path": f"/api/content?path={path.relative_to(root)!s}" if path.is_file() else None,
            }
            if path.is_dir():
                children = []
                for child in sorted(path.iterdir()):
                    if child.name.startswith(".") or child.name == "__pycache__":
                        continue
                    children.append(build_file_tree(child, root))
                item["children"] = children
            return item

        tree = build_file_tree(docs_root, docs_root)
        return tree.get("children", [])
    except Exception as e:
        logger.error(f"Error in api_tree: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/content")
async def api_content(path: str):
    """Retrieve raw file content."""
    try:
        docs_root = config.DOCS_ROOT.resolve()
        target = (docs_root / path).resolve()
        if not target.is_relative_to(docs_root) or not target.is_file():
            raise HTTPException(status_code=403, detail="Access denied or file not found")

        with open(target, encoding="utf-8") as f:
            return {"content": f.read()}
    except Exception as e:
        logger.error(f"Error in api_content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reindex")
async def api_reindex(background_tasks: BackgroundTasks):
    """Trigger manual re-indexing in the background."""
    job_id = uuid.uuid4().hex[:12]
    _reindex_status[job_id] = "queued"
    background_tasks.add_task(_run_reindex, job_id)
    return {"success": True, "job_id": job_id, "message": "Reindex started in background."}

@router.get("/reindex/{job_id}")
async def api_reindex_status(job_id: str):
    """Poll reindex job status."""
    status = _reindex_status.get(job_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if status.startswith("complete:"):
        return {"success": True, "status": "complete", "chunks": int(status.split(":")[1])}
    if status.startswith("error:"):
        return {"success": False, "status": "error", "error": status.split(":", 1)[1]}
    return {"success": True, "status": status}

@router.get("/reindex/{job_id}/events")
async def api_reindex_events(job_id: str):
    """SSE stream for reindex job completion."""
    status = _reindex_status.get(job_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Job not found")

    async def event_stream():
        # Emit initial status
        if status.startswith("complete"):
            yield f"data: {json.dumps({'type': 'complete', 'chunks': int(status.split(':')[1])})}\n\n"
            return
        if status.startswith("error"):
            yield f"data: {json.dumps({'type': 'error', 'error': status.split(':', 1)[1]})}\n\n"
            return

        yield f"data: {json.dumps({'type': 'running'})}\n\n"

        # Wait for completion via event buffer
        for _ in range(300):  # 5 min timeout
            events = _reindex_events.get(job_id, [])
            if events:
                for ev in events:
                    yield f"data: {ev}\n\n"
                return
            await asyncio.sleep(1)

        yield f"data: {json.dumps({'type': 'timeout'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
