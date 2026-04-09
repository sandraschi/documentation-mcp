"""
Professional agent persistence store: persistent, namespace-scoped, semantic recall.
Uses the same LanceDB + BGE embedding stack as docs RAG. Table: persistence_memory.
"""

import logging
import time
import uuid
from typing import Any

from .config import config
from .rag_core import BaseVectorStore

logger = logging.getLogger(__name__)

MEMORY_TABLE = "persistence_memory"


class MemoryStore(BaseVectorStore):
    """Stores and recalls agent memory by namespace with semantic search."""

    def __init__(self):
        super().__init__(
            db_path=str(config.DB_PATH),
            embedding_model_name=config.EMBEDDING_MODEL,
            table_name=MEMORY_TABLE,
        )

    def store(self, namespace: str, content: str) -> dict[str, Any]:
        """Append one memory entry. Returns id and created_at."""
        if not namespace or not content or not content.strip():
            return {"success": False, "error": "namespace and content are required and non-empty"}
        namespace = namespace.strip()
        content = content.strip()
        entry_id = f"{namespace}_{uuid.uuid4().hex[:12]}"
        created_at = time.time()
        # Build doc in the shape add_documents expects; we need namespace/created_at as top-level for where()
        doc = {
            "id": entry_id,
            "content": content,
            "metadata": {"namespace": namespace, "created_at": created_at},
        }
        contents = [doc["content"]]
        embeddings = list(self.embedding_model.embed(contents))
        row = {
            "id": entry_id,
            "vector": embeddings[0].tolist(),
            "content": content,
            "namespace": namespace,
            "created_at": created_at,
        }
        if self.table_name not in self.db.list_tables():
            self.db.create_table(self.table_name, data=[row], mode="overwrite")
        else:
            tbl = self.db.open_table(self.table_name)
            tbl.add([row])
        logger.info("persistence_memory store: namespace=%s id=%s", namespace, entry_id)
        return {"success": True, "id": entry_id, "created_at": created_at, "namespace": namespace}

    def recall(self, namespace: str, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Semantic search within a namespace. Returns list of {content, created_at, score, id}."""
        if self.table_name not in self.db.list_tables():
            return []
        tbl = self.db.open_table(self.table_name)
        query_embedding = list(self.embedding_model.embed([query]))[0]
        # Restrict to namespace; escape single quotes in namespace for safety
        safe_ns = namespace.replace("'", "''") if namespace else ""
        where_expr = f"namespace = '{safe_ns}'" if safe_ns else None
        search_req = tbl.search(query_embedding).limit(limit)
        if where_expr:
            search_req = search_req.where(where_expr)
        rows = search_req.to_arrow().to_pylist()
        out = []
        for r in rows:
            dist = r.get("_distance", 0.0)
            score = max(0.0, 1.0 - dist)
            out.append(
                {
                    "content": r.get("content", ""),
                    "created_at": r.get("created_at"),
                    "id": r.get("id"),
                    "score": round(score, 4),
                }
            )
        return out

    def compaction_status(self) -> dict[str, Any]:
        """Return memory density and per-namespace stats; suggest compaction when useful."""
        if self.table_name not in self.db.list_tables():
            return {
                "success": True,
                "total_entries": 0,
                "namespaces": [],
                "entries_per_namespace": {},
                "suggestion": "No persistence stored yet. Use persistence_store_memory to add entries.",
            }
        tbl = self.db.open_table(self.table_name)
        rows = tbl.to_arrow().to_pylist()
        total = len(rows)
        by_ns: dict[str, int] = {}
        for r in rows:
            ns = r.get("namespace") or "_unknown"
            by_ns[ns] = by_ns.get(ns, 0) + 1
        namespaces = sorted(by_ns.keys())
        # Suggest compaction if any namespace has many entries (e.g. > 50)
        compact_threshold = 50
        needs_compact = [ns for ns, c in by_ns.items() if c >= compact_threshold]
        suggestion = (
            f"Consider compaction for namespaces with many entries: {needs_compact}."
            if needs_compact
            else "Memory density is fine; no compaction needed."
        )
        return {
            "success": True,
            "total_entries": total,
            "namespaces": namespaces,
            "entries_per_namespace": by_ns,
            "compaction_threshold": compact_threshold,
            "suggestion": suggestion,
        }
