import pytest

from docs_mcp.server import persistence_recall, search_docs


@pytest.mark.asyncio
async def test_search_docs_tool(test_mode):
    """Verify the search_docs tool returns expected markdown."""
    # The tool uses get_store(), which we mock-injected in conftest.py
    query = "FastMCP"
    # search_docs in server.py is SYNC
    result_dict = search_docs(query=query)
    result = result_dict["result"]

    assert "Documentation Search" in result
    assert "FastMCP" in result
    if test_mode == "mock":
        assert "standards/AGENT_PROTOCOLS.md" in result


@pytest.mark.asyncio
async def test_persistence_recall_tool(test_mode):
    """Verify the persistence_recall tool returns expected formatted results."""
    namespace = "test-system"
    query = "memory"

    # persistence_recall is SYNC
    result_dict = persistence_recall(namespace=namespace, query=query)
    result = result_dict["result"]

    assert "Memory Recall" in result
    if test_mode == "mock":
        assert "Found persistent memory" in result


@pytest.mark.asyncio
async def test_search_docs_no_results(document_store, test_mode):
    """Test empty search handling."""
    if test_mode == "mock":
        document_store.search.return_value = []

    result_dict = search_docs(query="NonExistentTopic")
    result = result_dict["result"]
    assert "Found 0 relevant snippets" in result or "Error" in result
