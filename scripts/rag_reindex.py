"""Full documentation reindex — use with just rag / just rag-gpu (venv python, not uv run)."""

from __future__ import annotations

import sys


def main() -> int:
    from docs_mcp.backend.ingestor import ContentIngestor
    from docs_mcp.backend.rag_paths import effective_extra_paths
    from docs_mcp.backend.store_registry import get_store

    store = get_store()
    ingestor = ContentIngestor()
    extra = effective_extra_paths()
    docs = ingestor.load_all_docs(extra_paths=extra or None)
    if not docs:
        print("[rag] No documentation chunks found.")
        return 1

    device = getattr(store, "embed_device", "cpu")
    batch = getattr(store, "embed_batch_size", 64)
    print(f"[rag] Embed device: {device} (batch {batch})")
    print(f"[rag] Embedding {len(docs)} chunks...")

    def progress(done: int, total: int) -> None:
        pct = int(100 * done / total) if total else 0
        print(f"\r[rag:embed] {done}/{total} ({pct}%)", end="", flush=True)

    n = store.add_documents(docs, progress_callback=progress)
    print()
    print(f"[rag] Indexed {n} chunks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
