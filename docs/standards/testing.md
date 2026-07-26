# Testing Standards

## Overview
Comprehensive testing standards for MCP servers, including unit tests, integration tests, end-to-end tests, and testing infrastructure.

## Testing Pyramid

### Test Categories
```
End-to-End Tests (E2E)     ── 10% (Slow, high confidence)
Integration Tests           ── 20% (Medium speed, medium confidence)
Unit Tests                  ── 70% (Fast, focused confidence)
```

## Unit Testing Standards

### Test Structure
```python
# tests/test_tool_name.py
import pytest
from unittest.mock import Mock, patch
from mcp_server.tools.tool_name import ToolClass


class TestToolName:
    """Test suite for tool_name functionality."""

    @pytest.fixture
    def tool_instance(self):
        """Fixture for tool instance."""
        return ToolClass()

    @pytest.fixture
    def mock_context(self):
        """Mock MCP context for testing."""
        context = Mock()
        context.logger = Mock()
        return context

    def test_successful_operation(self, tool_instance, mock_context):
        """Test successful tool operation."""
        # Arrange
        expected_result = {"status": "success", "data": "test"}

        # Act
        result = tool_instance.process_data(mock_context, "input_data")

        # Assert
        assert result["status"] == "success"
        assert "data" in result

    def test_error_handling(self, tool_instance, mock_context):
        """Test error handling."""
        # Arrange
        mock_context.logger.error = Mock()

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid input"):
            tool_instance.process_data(mock_context, None)

        # Verify error logging
        mock_context.logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_operation(self, tool_instance, mock_context):
        """Test asynchronous operations."""
        # Arrange
        async def mock_async_call():
            return "async_result"

        with patch.object(tool_instance, '_async_method', side_effect=mock_async_call):
            # Act
            result = await tool_instance.async_process(mock_context)

            # Assert
            assert result == "async_result"
```

### Test Coverage Requirements
```ini
# pyproject.toml coverage configuration
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/venv/*",
    "*/__pycache__/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "class .*\bProtocol\):",
    "@(abc\.)?abstractmethod"
]
```

### Minimum Coverage Targets
- **Unit Tests**: 80% coverage minimum
- **Integration Tests**: 70% coverage minimum
- **Critical Paths**: 95% coverage required

## Integration Testing

### MCP Server Integration Tests
```python
# tests/integration/test_mcp_server.py
import pytest
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp_server.server import app


@pytest.mark.asyncio
class TestMCPServerIntegration:
    """Integration tests for MCP server functionality."""

    async def setup_mcp_client(self):
        """Set up MCP client for testing."""
        # Create test server parameters
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "mcp_server.server"],
            env={}
        )

        # Connect client
        session = await ClientSession.connect(server_params)
        return session

    async def test_tool_listing(self):
        """Test that tools are properly listed."""
        session = await self.setup_mcp_client()

        try:
            # List available tools
            tools = await session.list_tools()

            # Verify expected tools are present
            tool_names = [tool.name for tool in tools]
            assert "example_tool" in tool_names
            assert "data_processor" in tool_names

        finally:
            await session.close()

    async def test_tool_execution(self):
        """Test tool execution through MCP protocol."""
        session = await self.setup_mcp_client()

        try:
            # Execute tool
            result = await session.call_tool(
                name="example_tool",
                arguments={"input": "test_data"}
            )

            # Verify result structure
            assert isinstance(result, dict)
            assert "status" in result
            assert result["status"] == "success"

        finally:
            await session.close()
```

### API Integration Tests
```python
# tests/integration/test_api.py
import pytest
from fastapi.testclient import TestClient
from mcp_server.api.main import app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


class TestAPIIntegration:
    """API integration tests."""

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_tool_execution_endpoint(self, client):
        """Test tool execution through REST API."""
        payload = {
            "tool_name": "example_tool",
            "arguments": {"input": "test"}
        }

        response = client.post("/api/tools/execute", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert "result" in data
        assert data["result"]["status"] == "success"

    def test_invalid_tool_request(self, client):
        """Test error handling for invalid requests."""
        payload = {
            "tool_name": "nonexistent_tool",
            "arguments": {}
        }

        response = client.post("/api/tools/execute", json=payload)
        assert response.status_code == 404

        data = response.json()
        assert "error" in data
        assert "not found" in data["error"].lower()
```

## End-to-End Testing — Dual-Track Strategy

The fleet uses two complementary E2E tracks (see [VERIFICATION_STANDARDS.md](./VERIFICATION_STANDARDS.md) §3):

| Track | Tool | When |
|-------|------|------|
| **Webapp E2E** | Playwright (headless) | Every push/PR |
| **Desktop certification** | CUA (pywinauto) | Before each NSIS build |

See:
- [rules/playwright_e2e_sota.md](./rules/playwright_e2e_sota.md) — Fleet Audit requirements, minimum test suite
- [rules/cua_nsis_smoke_testing.md](./rules/cua_nsis_smoke_testing.md) — Pre-release smoke test (install → launch → verify → uninstall)

### Full Workflow Tests (legacy Docker-based E2E)
```python
# tests/e2e/test_full_workflow.py
import pytest
import docker
from mcp import ClientSession, StdioServerParameters


@pytest.mark.e2e
class TestFullWorkflow:
    """End-to-end workflow tests."""

    @pytest.fixture(scope="class")
    def docker_client(self):
        """Docker client for containerized testing."""
        return docker.from_env()

    def test_complete_mcp_workflow(self, docker_client):
        """Test complete MCP workflow from client to server."""
        # Start MCP server in container
        container = docker_client.containers.run(
            "mcp-server:latest",
            detach=True,
            ports={"8000/tcp": 8000}
        )

        try:
            # Wait for server to be ready
            import time
            time.sleep(10)

            # Connect MCP client
            session = self.connect_to_server()

            # Execute workflow
            result = self.execute_workflow(session)

            # Verify results
            assert result["workflow_status"] == "completed"
            assert len(result["steps"]) >= 3

        finally:
            container.stop()
            container.remove()

    def connect_to_server(self):
        """Connect to MCP server."""
        server_params = StdioServerParameters(
            command="python",
            args=["-c", "from mcp_server.server import app; import mcp.server.stdio; mcp.server.stdio.run_server(app.to_server())"],
            env={}
        )

        session = ClientSession.connect(server_params)
        return session

    def execute_workflow(self, session):
        """Execute a complete workflow."""
        results = []

        # Step 1: Initialize
        result1 = session.call_tool("initialize_workflow", {})
        results.append(result1)

        # Step 2: Process data
        result2 = session.call_tool("process_data", {"data": "test_input"})
        results.append(result2)

        # Step 3: Generate output
        result3 = session.call_tool("generate_output", {"format": "json"})
        results.append(result3)

        return {
            "workflow_status": "completed",
            "steps": results
        }
```

## Testing Infrastructure

### Test Configuration
```python
# tests/conftest.py
import pytest
import asyncio
from unittest.mock import Mock
from mcp_server.config import Settings


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = Mock(spec=Settings)
    settings.debug = True
    settings.database_url = "sqlite:///:memory:"
    return settings


@pytest.fixture
def mock_logger():
    """Mock logger for testing."""
    logger = Mock()
    logger.info = Mock()
    logger.error = Mock()
    logger.warning = Mock()
    return logger


@pytest.fixture(autouse=True)
def reset_mocks(mock_logger):
    """Reset mocks between tests."""
    mock_logger.reset_mock()
```

### Test Data Management
```python
# tests/fixtures/test_data.py
import pytest
from mcp_server.models import User, Document


@pytest.fixture
def sample_user():
    """Sample user for testing."""
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        is_active=True
    )


@pytest.fixture
def sample_document():
    """Sample document for testing."""
    return Document(
        id=1,
        title="Test Document",
        content="This is test content",
        author_id=1
    )


@pytest.fixture
def test_database():
    """In-memory test database."""
    # Setup test database
    # Return database session
    pass
```

## Performance Testing

### Load Testing
```python
# tests/performance/test_load.py
import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor


@pytest.mark.performance
class TestLoadPerformance:
    """Performance and load testing."""

    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        async def make_request(i):
            # Simulate MCP tool call
            await asyncio.sleep(0.1)  # Simulate processing time
            return f"result_{i}"

        # Test with 100 concurrent requests
        start_time = time.time()

        async def run_concurrent_test():
            tasks = [make_request(i) for i in range(100)]
            results = await asyncio.gather(*tasks)
            return results

        results = asyncio.run(run_concurrent_test())
        end_time = time.time()

        # Assertions
        assert len(results) == 100
        assert end_time - start_time < 15  # Should complete within 15 seconds

    def test_memory_usage(self):
        """Test memory usage under load."""
        # Monitor memory usage during test
        # Assert memory stays within bounds
        pass

    def test_response_times(self):
        """Test response time requirements."""
        # Measure response times
        # Assert they meet SLAs
        pass
```

## Test Automation

### CI/CD Integration
```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        pip install uv
        uv sync --group dev

    - name: Run unit tests
      run: uv run pytest tests/unit/ -v --cov=src/ --cov-report=xml

    - name: Run integration tests
      run: uv run pytest tests/integration/ -v --cov-append --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
```

### Test Reporting
```python
# tests/generate_report.py
import pytest
import json
from datetime import datetime


def generate_test_report():
    """Generate comprehensive test report."""
    # Run tests with JSON output
    pytest.main([
        "--json-report",
        "--json-report-file=test-results.json",
        "tests/"
    ])

    # Load results
    with open("test-results.json") as f:
        results = json.load(f)

    # Generate report
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": results["summary"],
        "tests": results["tests"],
        "coverage": calculate_coverage(),
        "performance": measure_performance()
    }

    with open("test-report.json", "w") as f:
        json.dump(report, f, indent=2)

    return report
```

## Next Steps
After testing implementation, proceed to:
1. [Error Handling Standards](./error-handling.md)
2. [Logging Standards](./logging.md)
3. [Monitoring Standards](./monitoring.md)
4. [Red-Green TDD Guide](./testing-tdd-red-green.md) — when and how to apply test-driven development to this fleet
5. [Environment-Aware Testing](./testing-environment-aware.md) — CI vs local vs hardware: automatic detection and skip logic for IoT/robot MCP servers (**pywinauto-mcp** implements the pattern; fleet intent: roll out to all hardware-connected repos — cameras, robots, IoT, etc.)
