# Red-Green TDD for MCP Servers

**Related:** [Testing Standards](./testing.md) | [Code Quality Standards](./CODE_QUALITY_STANDARDS.md)

---

## What It Is

Red-Green TDD (Test-Driven Development) is a discipline where you write the test *before* the implementation. The cycle has three steps:

1. **Red** — write a test for functionality that does not exist yet. Run it. Watch it fail. This is intentional and required — a test that cannot fail is not a test.
2. **Green** — write the *minimum* code to make the test pass. No more. Resist the urge to generalize.
3. **Refactor** — clean up the implementation, knowing the test will catch regressions. Then repeat.

The color names come from pytest/unittest output: red for failing, green for passing. The discipline is strict: you are not allowed to write production code without a failing test first.

This is distinct from "write tests alongside code" (concurrent testing) or "write tests after code" (retroactive testing). Those have value too, but they are not TDD.

---

## Why It Works

The counterintuitive insight: writing the test first forces you to design the API before implementing it. You have to decide what the function signature looks like, what it returns, what errors it raises — before you write a single line of logic. This catches bad interfaces early when they are cheap to fix.

Secondary benefits:

- Tests are guaranteed to actually test something, because you saw them fail first
- Minimum-code discipline prevents over-engineering
- Refactoring becomes safe because the test suite is your regression net
- The test suite documents intent, not just behavior

---

## The Cycle in Practice

```python
# Step 1: RED — write the test first
# tests/test_validators.py

def test_validate_tool_input_rejects_empty_name():
    """Tool name cannot be empty string."""
    with pytest.raises(ValueError, match="name cannot be empty"):
        validate_tool_input(name="", timeout=30)

# Run: pytest tests/test_validators.py
# Result: FAILED — ImportError or NameError, validate_tool_input doesn't exist yet
# This is correct. Proceed to green.
```

```python
# Step 2: GREEN — minimum code to pass
# src/validators.py

def validate_tool_input(name: str, timeout: int) -> None:
    if not name:
        raise ValueError("name cannot be empty")

# Run: pytest tests/test_validators.py
# Result: PASSED
# Resist adding more logic. Next test drives next behavior.
```

```python
# Step 3: REFACTOR — clean up if needed, re-run to confirm green
# In this case nothing to refactor. Move to next test.

# Next RED:
def test_validate_tool_input_rejects_negative_timeout():
    with pytest.raises(ValueError, match="timeout must be positive"):
        validate_tool_input(name="my_tool", timeout=-1)

# GREEN:
def validate_tool_input(name: str, timeout: int) -> None:
    if not name:
        raise ValueError("name cannot be empty")
    if timeout < 1:
        raise ValueError("timeout must be positive")
```

Each test drives exactly one behavior. Never write more production code than the current failing test requires.

---

## Where to Use It in This Fleet

### Good fit — use TDD here

**Input validation and schema enforcement**

MCP tool handlers receive untyped dicts from the protocol. Validation logic is pure, has clear pass/fail semantics, and bugs here cause silent failures in clients. TDD is excellent.

```python
# RED
def test_parse_camera_config_requires_ip():
    with pytest.raises(ValueError, match="ip_address is required"):
        parse_camera_config({})

# RED
def test_parse_camera_config_validates_ip_format():
    with pytest.raises(ValueError, match="invalid IP format"):
        parse_camera_config({"ip_address": "not_an_ip"})

# RED
def test_parse_camera_config_accepts_valid_config():
    config = parse_camera_config({"ip_address": "192.168.1.100", "port": 554})
    assert config.ip_address == "192.168.1.100"
    assert config.port == 554
```

**Response formatters and transformers**

Pure functions that take data in and produce data out. Zero external dependencies. TDD shines here.

```python
# RED
def test_format_transport_departure_shows_minutes():
    departure = format_departure({"line": "U4", "seconds_until": 180})
    assert departure["minutes"] == 3
    assert departure["line"] == "U4"

# RED
def test_format_transport_departure_handles_zero_wait():
    departure = format_departure({"line": "U4", "seconds_until": 0})
    assert departure["minutes"] == 0
    assert departure.get("status") == "departing"
```

**Error handling logic**

How your server decides to handle, wrap, and surface errors is critical and testable.

```python
# RED
def test_wrap_external_error_preserves_original_message():
    original = ConnectionError("refused")
    wrapped = wrap_tool_error(original, tool_name="get_camera_feed")
    assert "get_camera_feed" in str(wrapped)
    assert "refused" in str(wrapped)

# RED
def test_wrap_external_error_is_mcp_compatible_type():
    wrapped = wrap_tool_error(ValueError("bad input"), tool_name="test")
    assert isinstance(wrapped, MCPToolError)
```

**Regression fixes — always TDD**

When a bug is found in production, the workflow is:

1. Write a test that reproduces the bug (it will be RED)
2. Fix the bug (make it GREEN)
3. Never remove the test

This is the single highest-value use of TDD. The test is a permanent record that this specific failure mode was encountered and is now prevented.

```python
# Bug found: parse_duration crashed on "1h 30m" format, only handled "90m"
# RED — reproduce the bug first:
def test_parse_duration_handles_hours_and_minutes_format():
    assert parse_duration("1h 30m") == 90

# Now fix parse_duration. GREEN. Test stays forever.
```

---

### Poor fit — skip or defer TDD here

**Thin integration/glue code**

MCP servers that mostly wrap external APIs, call subprocesses, or talk to hardware end up mocking everything. The tests become tautological: "assert that mock was called with these args." They break whenever the external interface changes and provide little real confidence.

```python
# This kind of test is often not worth writing TDD-first:
def test_get_camera_snapshot_calls_rtsp():
    with patch("tapo_mcp.rtsp.connect") as mock_connect:
        get_snapshot(ip="192.168.1.1")
        mock_connect.assert_called_once_with("192.168.1.1")
# What does this actually test? That you called the mock. Thin value.
```

Better approach for glue code: integration tests against the real external system in a test environment, or a simple smoke test that confirms the tool is reachable.

**Exploratory/prototyping phase**

When the API shape is not yet clear, TDD forces premature decisions. Write exploratory code first, figure out the right shape, then add tests once the interface stabilizes. For AI-assisted development at this pace, the exploration phase is often 1-2 hours, not days.

**CLI entry points and server startup**

The `__main__` block, argparse setup, server initialization — not worth TDD-first. These are typically covered by the integration test suite.

**One-off scripts and tooling**

`sota-scripts/`, migration scripts, utility scripts in `scripts/` — not worth TDD unless they contain logic that will be reused.

---

## The Pragmatic Middle Ground

Strict TDD across an entire MCP server is overkill and fights the development pace. The practical approach:

| Code Type | TDD? | When to Write Tests |
|-----------|------|---------------------|
| Validators / parsers | ✅ Yes | Before implementation |
| Response formatters | ✅ Yes | Before implementation |
| Error handling logic | ✅ Yes | Before implementation |
| Bug fixes | ✅ Always | Before the fix |
| Core business logic | ✅ Yes | Before implementation |
| External API wrappers | ⚠️ Selective | After shape is clear |
| FastMCP tool handlers (pure) | ✅ Yes | Before implementation |
| FastMCP tool handlers (glue) | ⚠️ Selective | Integration test instead |
| Server startup / config loading | ❌ No | Smoke test only |
| CLI / argparse | ❌ No | Skip unless complex |
| Migration scripts | ❌ No | Skip |

The 80/20 rule: TDD the core logic layer aggressively. Test the integration layer with integration tests, not unit mocks.

---

## CI/CD Integration

Fits directly into the existing GitHub Actions pipeline from [testing.md](./testing.md). No special tooling needed.

```yaml
# .github/workflows/test.yml (relevant section)
- name: Run tests with coverage
  run: |
    uv run pytest tests/ \
      --cov=src/ \
      --cov-report=term-missing \
      --cov-fail-under=80 \
      -v

# Type checking pipeline (see FASTMCP3_UPGRADE_STRATEGY.md)
- name: ruff lint (blocking)
  run: uv run ruff check src/

- name: ruff format check (blocking)
  run: uv run ruff format --check src/

- name: pyright type check (blocking)
  run: uv run pyright src/

- name: ty type check (non-blocking, informational)
  run: uvx ty check src/
  continue-on-error: true
```

The `--cov-fail-under=80` only makes sense if TDD is applied selectively to the testable core. If you apply it to everything including glue code, the 80% target becomes either impossible or meaningless.

---

## Tooling

No new dependencies beyond what's already in the fleet standard:

```toml
# pyproject.toml — already present in fleet SOTA
[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "pytest-cov>=6.0",
]
```

Run the cycle:

```bash
# Run specific test file during TDD cycle (fast feedback)
uv run pytest tests/test_validators.py -v

# Run with coverage after session
uv run pytest tests/ --cov=src/ --cov-report=term-missing

# Watch mode (if pytest-watch is installed)
uv run ptw tests/test_validators.py -- -v
```

For async MCP tool handlers, mark tests appropriately:

```python
import pytest

@pytest.mark.asyncio
async def test_async_tool_returns_success():
    result = await my_tool_handler({"input": "valid"})
    assert result["status"] == "success"
```

---

## Limitations

**TDD does not guarantee correctness.** It guarantees that the code matches the tests. If the tests encode wrong assumptions, the code will confidently implement the wrong behavior. Test your tests by seeing them fail first (the red step) — this is not optional ceremony.

**Coverage numbers lie.** 80% coverage with weak assertions is worse than 50% coverage with sharp assertions. A test that calls the function and asserts `result is not None` counts as coverage. It is useless. Assert the actual values.

**TDD slows down the first hour.** For any given feature, TDD is slower at the start and faster at the end (fewer debugging cycles, fewer regressions). At the AI-assisted development pace of this fleet, this tradeoff shifts: AI can generate both the test and the implementation fast, so the overhead is minimal. Use AI to generate the RED test, verify it actually fails, then generate the GREEN implementation.

**Mock hell.** If writing a test requires more than 2-3 `patch()` calls, stop. You are either testing the wrong thing or the code needs to be restructured so the pure logic is separable from the I/O. Extract the logic, test the logic, leave the I/O for integration tests.

---

## Summary

Red-Green TDD is a discipline, not a rule. Apply it where the code is pure and the behavior is well-defined. Skip it where you are integrating with external systems or exploring unknown territory. Always use it for bug fixes. The tests you write in the red phase are the most valuable tests you will ever write — because you know for certain that they test something real.

---

## Environment-Aware Testing: CI vs Local vs Sandra's Den

Testing IoT and hardware-dependent MCP servers requires tests that know where they are running. The core insight: **don't mock hardware in CI and pretend that's the same test** — instead, have the test scaffold detect the environment and decide what to run, mock, or skip entirely.

### Environment Detection

GitHub Actions always sets `CI=true`. That is the canonical signal. Everything builds on that.

```python
# tests/conftest.py
import os
import socket
import pytest


def is_ci() -> bool:
    """Running in GitHub Actions or any CI environment."""
    return os.environ.get("CI", "").lower() in ("true", "1", "yes")


def detect_environment() -> str:
    """
    Returns one of: 'ci', 'local_no_iot', 'local_with_iot'
    
    Probes the LAN for a known device to determine whether
    hardware is reachable, rather than just trusting CI flag.
    """
    if is_ci():
        return "ci"
    
    # Probe a device that only exists on the local LAN
    probe_ip = os.environ.get("IOT_PROBE_IP", "192.168.1.100")
    probe_port = int(os.environ.get("IOT_PROBE_PORT", "554"))
    try:
        sock = socket.create_connection((probe_ip, probe_port), timeout=1)
        sock.close()
        return "local_with_iot"
    except (OSError, ConnectionRefusedError, TimeoutError):
        return "local_no_iot"


# Evaluate once per session
ENV = detect_environment()
```

### Markers and Auto-Skip

```python
# tests/conftest.py (continued)

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "requires_hardware: needs physical IoT devices — skipped unless local_with_iot"
    )
    config.addinivalue_line(
        "markers", "requires_network: needs LAN access — skipped in CI"
    )
    config.addinivalue_line(
        "markers", "ci_only: mock-heavy contract tests — skipped on local"
    )


def pytest_runtest_setup(item):
    """Auto-skip based on detected environment. No manual intervention needed."""
    env = ENV  # already evaluated

    if item.get_closest_marker("requires_hardware") and env != "local_with_iot":
        pytest.skip(f"hardware not reachable (environment: {env})")

    if item.get_closest_marker("requires_network") and env == "ci":
        pytest.skip("no local network in CI")

    if item.get_closest_marker("ci_only") and env != "ci":
        pytest.skip("ci_only test, skipping on local")
```

### Smart Fixtures: Real or Mock, Automatically

The fixture provides the real implementation locally and a mock in CI. Tests themselves don't change.

```python
# tests/conftest.py (continued)
from unittest.mock import AsyncMock


@pytest.fixture
async def tapo_camera():
    """
    Real TapoCamera when IoT is reachable, mock otherwise.
    Tests are written once and work in both environments.
    """
    if ENV == "local_with_iot":
        from tapo_mcp.camera import TapoCamera
        ip = os.environ.get("TAPO_TEST_IP", "192.168.1.100")
        cam = TapoCamera(ip=ip)
        await cam.connect()
        yield cam
        await cam.disconnect()
    else:
        mock_cam = AsyncMock()
        mock_cam.get_snapshot.return_value = b"fake_jpeg_bytes"
        mock_cam.get_status.return_value = {"online": True, "ip": "192.168.1.100"}
        mock_cam.ptz.return_value = {"success": True}
        yield mock_cam
```

Test is environment-agnostic:

```python
# tests/test_camera_tools.py

@pytest.mark.asyncio
async def test_snapshot_returns_bytes(tapo_camera):
    """Runs everywhere — mock in CI, real camera locally."""
    result = await tapo_camera.get_snapshot()
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
@pytest.mark.requires_hardware
async def test_ptz_actually_moves_camera(tapo_camera):
    """
    Only runs when hardware is reachable.
    Skipped in CI and local_no_iot — not mocked.
    Some things cannot be meaningfully mocked (physical motor movement).
    """
    result = await tapo_camera.ptz(pan=10, tilt=0)
    assert result["success"] is True
```

The key decision: tests that verify *behavior* (returns bytes, parses status) use the smart fixture and run everywhere. Tests that verify *physical reality* (camera actually pans) are marked `requires_hardware` and skipped rather than mocked.

### pyproject.toml

```toml
[tool.pytest.ini_options]
markers = [
    "requires_hardware: needs physical IoT devices",
    "requires_network: needs LAN access",
    "ci_only: only runs in GitHub Actions",
    "slow: takes more than 5 seconds",
]
addopts = "-v -m 'not slow'"
```

### Run Commands

```bash
# CI (automatic via ENV detection):
# CI=true uv run pytest
# Hardware tests auto-skipped, mocks used

# Local, all tests including hardware:
uv run pytest -m ""

# Simulate CI locally (no hardware):
CI=true uv run pytest

# Only hardware tests (requires IoT reachable):
uv run pytest -m requires_hardware

# Fast unit tests only:
uv run pytest -m "not requires_hardware and not slow"
```

### What Not to Mock

Some hardware behavior cannot be meaningfully mocked and should simply be skipped in CI rather than faked:

- Physical actuators (PTZ, relays, motors)
- Sensor readings that depend on environmental conditions
- Network latency and timeout behavior of real devices
- Authentication handshakes with specific firmware versions

Mock the *interface contract* (returns bytes, raises on error). Skip the *physical reality* tests. Never mock physical reality and claim the test passed.

---

*Added: 2026-03-21 | Tags: testing, tdd, python, quality, ci-cd, iot, hardware, environment-detection*
