import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session")
def test_mode():
    """Returns 'mock' or 'live' based on TEST_MODE env var."""
    return os.getenv("TEST_MODE", "mock").lower()


@pytest.fixture
def mock_document_store():
    """Mock implementation of the DocumentStore."""
    store = MagicMock()
    store.search.return_value = [
        {
            "content": "FastMCP is a high-performance framework for building MCP servers.",
            "metadata": {"filename": "AGENT_PROTOCOLS.md", "relative_path": "standards/AGENT_PROTOCOLS.md"},
            "_distance": 0.05,
        }
    ]
    store.list_sources.return_value = ["standards/AGENT_PROTOCOLS.md"]
    return store


@pytest.fixture
def mock_memory_store():
    """Mock implementation of the MemoryStore."""
    store = MagicMock()
    store.recall.return_value = [{"content": "Found persistent memory.", "score": 0.8}]
    return store


@pytest.fixture
def document_store(test_mode, mock_document_store, tmp_path_factory):
    """Fixture that provides the DocumentStore based on the test mode."""
    if test_mode == "live":
        from docs_mcp.backend.vector_store import DocumentStore
        test_db_dir = tmp_path_factory.mktemp("test_db")
        os.environ["LANCEDB_URI"] = str(test_db_dir)
        return DocumentStore()
    else:
        return mock_document_store


@pytest.fixture(autouse=True)
def inject_stores(document_store, mock_memory_store, test_mode):
    """Automatically inject stores into the store_registry for the duration of the test."""
    from docs_mcp.backend import store_registry

    orig_store = store_registry._store
    orig_memory = store_registry._memory_store

    store_registry._store = document_store
    if test_mode == "mock":
        store_registry._memory_store = mock_memory_store

    yield

    store_registry._store = orig_store
    store_registry._memory_store = orig_memory


@pytest.fixture
def ingestor(test_mode):
    """Fixture to provide a ContentIngestor (mocked logic if needed)."""
    from docs_mcp.backend.ingestor import ContentIngestor

    ing = ContentIngestor()
    if test_mode == "mock":
        ing.load_all_docs = MagicMock(
            return_value=[{"content": "Mock document content", "metadata": {"filename": "mock.md", "type": "docs"}}]
        )
    return ing
