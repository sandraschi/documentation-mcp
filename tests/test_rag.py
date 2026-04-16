import pytest


def test_semantic_accuracy(document_store, test_mode):
    """Scenario: Technical Detail Extraction
    Verify that specific API signatures like 'FastMCP' yield relevant chunks.
    """
    query = "How do I initialize FastMCP?"

    # In live mode, we might need a real index. In mock mode, the fixture handles it.
    if test_mode == "live" and not document_store.list_sources():
        from docs_mcp.server import reindex_docs

        reindex_docs()

    results = document_store.search(query, limit=3)

    assert len(results) > 0, "Should return at least one result"

    if test_mode == "mock":
        # Check against our mock data in conftest.py
        assert any("FastMCP" in r["content"] for r in results)
    else:
        # In live mode, we just check if it found *something*
        assert len(results) > 0


def test_chunking_integrity_code_blocks(ingestor):
    """Scenario: Code Block Preservation
    Verify that chunking doesn't break code blocks.
    """
    mock_md = """# Sample Header
Some text here.

```python
def test_func():
    print("This should stay together")
```

Another paragraph here."""

    chunks = ingestor.chunk_text(mock_md)

    code_block_found = False
    for chunk in chunks:
        if "```python" in chunk:
            code_block_found = True
            # Verify end of code block is also in the same chunk
            assert "```" in chunk.split("```python")[1], "Code block was split incorrectly"

    assert code_block_found, "Chunker failed to identify code block content"


def test_source_tagging(ingestor, test_mode):
    """Scenario: Metadata Tagging
    Verify that ingestion process correctly tags sources.
    """
    docs = ingestor.load_all_docs()
    assert len(docs) > 0

    # Check if we have variety in sources
    for doc in docs:
        assert "filename" in doc["metadata"]
        assert "type" in doc["metadata"]


@pytest.mark.asyncio
async def test_reindex_lifecycle(test_mode):
    """Scenario: Full Re-index Lifecycle
    Simulates the reindex_docs tool functionality.
    """
    from unittest.mock import MagicMock

    from docs_mcp.server import reindex_docs

    # reindex_docs is ASYNC and expects ctx: Context
    ctx = MagicMock()
    result_dict = await reindex_docs(ctx=ctx)
    result = result_dict["result"]
    assert "synchronized" in result.lower() or "successfully" in result.lower()
