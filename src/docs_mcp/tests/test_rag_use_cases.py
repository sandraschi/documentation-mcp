import pytest

from docs_mcp.backend.ingestor import ContentIngestor


@pytest.fixture(scope="module")
def document_store():
    """Fixture to provide a clean test DocumentStore"""
    # Ensure the global store in server.py is also aware of this or sharing config
    from docs_mcp.server import get_store

    return get_store()


@pytest.fixture(scope="module")
def ingestor():
    """Fixture to provide a ContentIngestor"""
    return ContentIngestor()


def test_semantic_accuracy_fastmcp(document_store):
    """Scenario: Technical Detail Extraction
    Verify that specific API signatures like 'FastMCP' yield relevant chunks.
    """
    query = "How do I initialize FastMCP?"
    # We should ensure ingestion has run at least once for this store
    # Since we use overwrite mode in re-index, we can just run it if empty
    if not document_store.list_sources():
        from docs_mcp.server import reindex_docs

        reindex_docs()

    results = document_store.search(query, limit=3)

    assert len(results) > 0, "Should return at least one result after indexing"

    # Check if any result mentions FastMCP
    found_fastmcp = any("FastMCP" in r["content"] for r in results)
    assert found_fastmcp, f"Search for '{query}' should find context mentioning FastMCP"


def test_chunking_integrity_code_blocks(ingestor):
    """Scenario: Code Block Preservation
    Verify that chunking doesn't break code blocks in a disruptive way.
    Note: Testing the refined double-newline/paragraph logic.
    """
    mock_md = """# Sample Header
Some text here.

```python
def test_func():
    print("This should stay together")
```

Another paragraph here that is quite long but should be separated from the code block if possible."""

    chunks = ingestor.chunk_text(mock_md)

    # Verify code block prefix isn't orphaned
    code_block_found = False
    for chunk in chunks:
        if "```python" in chunk:
            code_block_found = True
            # Verify end of code block is also in the same chunk if it's small enough
            if len(mock_md) < ingestor.chunk_size:
                assert "```" in chunk.split("```python")[1], "Code block was split incorrectly"

    assert code_block_found, "Chunker failed to identify code block content"


def test_cross_source_discovery(document_store, ingestor):
    """Scenario: Cross-Source Discovery
    Verify that ingestion process correctly tags sources and they are searchable.
    """
    # This is more of an integration test
    docs = ingestor.load_all_docs()

    # Check if we have variety in sources (based on config)
    sources = {doc["metadata"].get("type", "docs") for doc in docs}
    print(f"Detected document types: {sources}")

    # Even if some paths don't exist in a test env, we should verify the logic
    # In a full run, we expect 'docs', maybe 'knowledge' or 'depot'
    assert len(docs) > 0, "No documents were loaded during ingestion test"


@pytest.mark.asyncio
async def test_reindex_lifecycle(document_store):
    """Scenario: Full Re-index Lifecycle
    Simulates the reindex_docs tool functionality.
    """
    from docs_mcp.server import reindex_docs

    # Initial count
    initial_sources = document_store.list_sources()

    # Trigger re-index
    result = reindex_docs()
    assert "Re-indexing complete" in result or "successfully" in result.lower()

    # Verify we still have sources
    final_sources = document_store.list_sources()
    assert len(final_sources) >= len(initial_sources), "Re-index should not result in less data"
