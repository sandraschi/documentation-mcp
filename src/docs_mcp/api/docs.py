import logging
from pathlib import Path
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from docs_mcp.backend.store_registry import get_store
from docs_mcp.backend.ingestor import ContentIngestor
from docs_mcp.backend.config import config

logger = logging.getLogger("docs_mcp.api.docs")
router = APIRouter(prefix="/api")

@router.get("/search")
async def api_search(q: str = ""):
    """Semantic search across documentation."""
    try:
        store = get_store()
        results = store.search(q, limit=10)
        data = []
        for r in results:
            distance = r.get("_distance", 0.0)
            score = max(0.0, 1.0 - distance)
            data.append({
                "id": r.get("id"),
                "filename": r.get("metadata", {}).get("filename", "unknown"),
                "relative_path": r.get("metadata", {}).get("relative_path", "unknown"),
                "score": score,
                "content": r.get("content", ""),
            })
        return data
    except Exception as e:
        logger.error(f"Error in api_search: {e}")
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
async def api_reindex():
    """Trigger manual re-indexing."""
    try:
        store = get_store()
        ingestor = ContentIngestor()
        docs = ingestor.load_all_docs()
        if docs:
            store.add_documents(docs)
            return {"success": True, "chunks": len(docs)}
        return {"success": False, "error": "No docs found"}
    except Exception as e:
        logger.error(f"Error in api_reindex: {e}")
        raise HTTPException(status_code=500, detail=str(e))
