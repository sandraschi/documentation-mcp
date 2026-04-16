import logging
from docs_mcp.backend.vector_store import DocumentStore
from docs_mcp.backend.memory_store import MemoryStore

logger = logging.getLogger("docs_mcp.backend.store_registry")

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

def close_stores():
    """Cleanup stores on shutdown."""
    global _store, _memory_store
    _store = None
    _memory_store = None
    logger.info("Stores closed.")
