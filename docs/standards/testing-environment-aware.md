# Environment-Aware Testing for Hardware MCP Servers

**Related:** [Testing Standards](./testing.md) | [Red-Green TDD](./testing-tdd-red-green.md)

**Applies to:** ocr-mcp (scanner), devices-mcp, robotics-mcp, yahboom-mcp, universal-actuator-mcp,
dreame-mcp, devices-mcp, any MCP server with physical hardware dependencies.

### Fleet adoption

**Implemented:** [**pywinauto-mcp**](https://github.com/sandraschi/pywinauto-mcp) ships this pattern: `tests/conftest_env.py`, markers (`requires_hardware`, `destructive`, …), `[tool.pytest.ini_options]` in `pyproject.toml`, and **`docs/TESTING.md`**. That repo adapts the **local Windows desktop + OpenCV / USB cameras** case (hardware-marked tests **skip in CI**; mocks and `TestClient` tests run in CI).

**Intended:** Apply the same **drop-in scaffold** across the rest of the fleet **wherever an MCP server touches hardware** — cameras (local UVC or IP), **robots**, **scanners**, **vacuums**, **smart home / IoT**, and any other **physical or LAN-attached** dependency — so each repo shares the **marker vocabulary** and **auto-skip hooks**, with **device-specific fixtures** (Tapo, Yahboom, WIA, etc.) layered on top.

---

## The Problem

Hardware MCP servers have tests that are fundamentally location-dependent:

- **GitHub Actions (CI):** No physical devices. Must mock everything. Scanner doesn't exist. Cameras unreachable. Robot not present.
- **Sandra's den (local + IoT):** Real scanner attached via USB. Tapo cameras on LAN. Dreame vacuum discoverable. Yahboom robot connected. Tests can hit actual hardware.
- **Local dev without IoT:** Goliath running, but hardware powered off or not connected. Needs mocks like CI, but `CI=true` is not set.

The naive approach — mock everything unconditionally — means you never test the real hardware path. The opposite — always hit hardware — breaks CI entirely.

The solution is **environment detection**: the test scaffold asks "where am I?" once at startup, then routes fixtures and skip-decisions automatically. Tests themselves are written once and work everywhere.

---

## How It Works

### Signal 1: `CI=true`

GitHub Actions sets this automatically. It is the canonical "I am not at a desk with hardware" signal. Never needs manual configuration.

### Signal 2: LAN probe

A `socket.create_connection()` call to a known device IP/port with a short timeout. If it succeeds, IoT hardware is reachable. If it times out, you are either in CI or the hardware is off. This catches the "local dev, hardware powered down" case that `CI=true` alone misses.

### Signal 3: Pytest markers

`requires_hardware`, `requires_network`, `ci_only` — applied to tests that cannot be meaningfully mocked. The `pytest_runtest_setup` hook reads the detected environment and auto-skips incompatible tests before they run.

### Signal 4: Smart fixtures

Fixtures detect the environment and return either a real implementation or a mock. The test body never needs `if CI` conditionals.

---

## The Drop-In conftest Template

This is the canonical template for hardware MCP servers. Copy `tests/conftest_env.py` into any
repo and import from it in the main `conftest.py`.

```python
# tests/conftest_env.py
"""
Environment-aware test scaffold for hardware MCP servers.
Detects CI vs local-no-iot vs local-with-iot automatically.

Usage:
    Copy this file to tests/conftest_env.py in any hardware MCP repo.
    In tests/conftest.py: from tests.conftest_env import *
    Configure IOT_PROBE_* env vars or .env for your specific hardware.
"""

from __future__ import annotations

import os
import socket
import pytest
from typing import Literal

# ---------------------------------------------------------------------------
# Environment detection — runs once at import time
# ---------------------------------------------------------------------------

EnvType = Literal["ci", "local_no_iot", "local_with_iot"]


def _detect_environment() -> EnvType:
    """
    Probe the environment once at session start.

    Priority:
      1. CI=true  →  "ci"  (GitHub Actions, no hardware, no LAN)
      2. LAN probe succeeds  →  "local_with_iot"
      3. Otherwise  →  "local_no_iot"

    Configure probe target via environment variables:
      IOT_PROBE_IP    default: 192.168.1.1  (router — always present if on LAN)
      IOT_PROBE_PORT  default: 80
      IOT_PROBE_TIMEOUT  default: 1.5  (seconds)

    For device-specific probes, set in .env or pyproject.toml [tool.pytest.ini_options]:
      SCANNER_IP, TAPO_IP, ROBOT_IP, DREAME_IP, etc.
    """
    if os.environ.get("CI", "").lower() in ("true", "1", "yes"):
        return "ci"

    probe_ip = os.environ.get("IOT_PROBE_IP", "192.168.1.1")
    probe_port = int(os.environ.get("IOT_PROBE_PORT", "80"))
    timeout = float(os.environ.get("IOT_PROBE_TIMEOUT", "1.5"))

    try:
        with socket.create_connection((probe_ip, probe_port), timeout=timeout):
            return "local_with_iot"
    except (OSError, ConnectionRefusedError, TimeoutError):
        return "local_no_iot"


def _probe_device(ip: str, port: int, timeout: float = 1.0) -> bool:
    """Check if a specific device is reachable on the LAN."""
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (OSError, ConnectionRefusedError, TimeoutError):
        return False


# Evaluate once per session — all tests share this result
ENV: EnvType = _detect_environment()


# ---------------------------------------------------------------------------
# Marker registration
# ---------------------------------------------------------------------------

def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "requires_hardware: test needs physical device on LAN — skipped unless local_with_iot",
    )
    config.addinivalue_line(
        "markers",
        "requires_network: test needs LAN access — skipped in CI",
    )
    config.addinivalue_line(
        "markers",
        "ci_only: mock-heavy contract test — skipped on local to avoid redundancy",
    )
    config.addinivalue_line(
        "markers",
        "slow: takes more than 5s — excluded from default run",
    )
    config.addinivalue_line(
        "markers",
        "destructive: modifies physical state (motor moves, relay trips) — use with caution",
    )


# ---------------------------------------------------------------------------
# Auto-skip hook
# ---------------------------------------------------------------------------

def pytest_runtest_setup(item: pytest.Item) -> None:
    """Skip tests automatically based on detected environment. No per-test if-blocks needed."""
    env = ENV

    if item.get_closest_marker("requires_hardware") and env != "local_with_iot":
        pytest.skip(
            f"requires_hardware: IoT not reachable (environment={env!r}). "
            "Run locally with devices powered on."
        )

    if item.get_closest_marker("requires_network") and env == "ci":
        pytest.skip("requires_network: no local network in CI")

    if item.get_closest_marker("ci_only") and env != "ci":
        pytest.skip("ci_only: skipping on local (set CI=true to force)")

    if item.get_closest_marker("destructive") and env != "local_with_iot":
        pytest.skip("destructive: only run with hardware present and operator watching")


# ---------------------------------------------------------------------------
# Session-scoped environment report
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def environment_report() -> None:
    """Print detected environment at session start. Helps debug unexpected skips."""
    env_labels = {
        "ci": "GitHub Actions / CI — all hardware tests skipped, mocks used",
        "local_no_iot": "Local dev — IoT not reachable, mocks used (hardware powered off?)",
        "local_with_iot": "Sandra's den — IoT reachable, hardware tests will run",
    }
    print(f"\n[test env] {ENV}: {env_labels[ENV]}")


# ---------------------------------------------------------------------------
# Helper for per-test device probing (optional, for fine-grained skipping)
# ---------------------------------------------------------------------------

def skip_if_device_unreachable(ip: str, port: int, label: str) -> None:
    """
    Call at the top of a test to skip if a specific device is not reachable.
    Use when a test depends on one specific device that might be off
    while others are on.

    Example:
        def test_scanner_adf(scanner_fixture):
            skip_if_device_unreachable("192.168.1.50", 9100, "HP scanner")
            ...
    """
    if not _probe_device(ip, port):
        pytest.skip(f"Device unreachable: {label} at {ip}:{port}")
```

---

## Per-Device Fixture Pattern

Each hardware MCP server adds its own device fixtures on top of the base scaffold.
The pattern is identical across all servers — only the real implementation differs.

### Scanner (ocr-mcp)

```python
# tests/conftest.py in ocr-mcp
from tests.conftest_env import ENV, skip_if_device_unreachable
from unittest.mock import MagicMock, AsyncMock
import pytest

SCANNER_IP = os.environ.get("SCANNER_IP", "192.168.1.50")
SCANNER_PORT = int(os.environ.get("SCANNER_PORT", "9100"))


@pytest.fixture
def scanner(tmp_path):
    """
    Real WIA scanner in local_with_iot, mock otherwise.
    Test body is identical in both environments.
    """
    if ENV == "local_with_iot":
        skip_if_device_unreachable(SCANNER_IP, SCANNER_PORT, "HP scanner")
        from ocr_mcp.scanner.wia_backend import WIAScanner
        s = WIAScanner(device_ip=SCANNER_IP)
        s.connect()
        yield s
        s.disconnect()
    else:
        mock = MagicMock()
        mock.is_connected.return_value = True
        mock.discover_devices.return_value = [
            {"id": "wia:mock_0", "name": "Mock Scanner", "max_dpi": 600}
        ]
        mock.scan.return_value = b"\x89PNG\r\n..."  # minimal PNG header
        mock.get_properties.return_value = {
            "supported_dpi": [150, 300, 600],
            "color_modes": ["Color", "Grayscale"],
        }
        yield mock


# Test using the fixture — works in CI and locally, unchanged:

def test_scanner_discovers_devices(scanner):
    devices = scanner.discover_devices()
    assert len(devices) > 0
    assert "id" in devices[0]


def test_scan_returns_bytes(scanner):
    result = scanner.scan(dpi=300, color_mode="Color")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.requires_hardware
def test_scanner_actual_dpi_range(scanner):
    """
    Verifies the real scanner reports sensible DPI values.
    Not meaningful to mock — skip in CI.
    """
    props = scanner.get_properties()
    assert 300 in props["supported_dpi"]
    assert max(props["supported_dpi"]) >= 600


@pytest.mark.requires_hardware
@pytest.mark.destructive
def test_adf_feeds_paper(scanner):
    """
    Physically feeds a page through ADF. Only run with paper loaded and watching.
    """
    result = scanner.scan(use_adf=True)
    assert isinstance(result, bytes)
```

### Tapo Camera (devices-mcp / devices-mcp)

```python
TAPO_IP = os.environ.get("TAPO_IP", "192.168.1.100")
TAPO_PORT = int(os.environ.get("TAPO_PORT", "554"))


@pytest.fixture
async def tapo_camera():
    if ENV == "local_with_iot":
        skip_if_device_unreachable(TAPO_IP, TAPO_PORT, "Tapo camera")
        from tapo_mcp.camera import TapoCamera
        cam = TapoCamera(ip=TAPO_IP)
        await cam.connect()
        yield cam
        await cam.disconnect()
    else:
        mock = AsyncMock()
        mock.get_snapshot.return_value = b"\xff\xd8\xff..."  # JPEG magic bytes
        mock.get_status.return_value = {"online": True, "ip": TAPO_IP}
        mock.ptz.return_value = {"success": True, "position": {"pan": 0, "tilt": 0}}
        yield mock


def test_snapshot_returns_jpeg(tapo_camera):
    result = await tapo_camera.get_snapshot()
    assert result[:3] == b"\xff\xd8\xff"  # JPEG magic


@pytest.mark.requires_hardware
@pytest.mark.destructive
async def test_ptz_pan_returns_to_home(tapo_camera):
    """Real motor movement. Only runs with hardware."""
    await tapo_camera.ptz(pan=10, tilt=0)
    await tapo_camera.ptz(pan=-10, tilt=0)  # return home
    status = await tapo_camera.get_status()
    assert status["online"]
```

### Robot (robotics-mcp / yahboom-mcp)

```python
ROBOT_IP = os.environ.get("ROBOT_IP", "192.168.1.200")
ROBOT_PORT = int(os.environ.get("ROBOT_PORT", "8080"))


@pytest.fixture
async def robot():
    if ENV == "local_with_iot":
        skip_if_device_unreachable(ROBOT_IP, ROBOT_PORT, "Yahboom robot")
        from robotics_mcp.robot import RobotController
        r = RobotController(ip=ROBOT_IP)
        await r.connect()
        yield r
        await r.stop_all()
        await r.disconnect()
    else:
        mock = AsyncMock()
        mock.get_status.return_value = {"connected": True, "battery": 85}
        mock.move.return_value = {"success": True}
        mock.get_sensor_readings.return_value = {
            "ultrasonic_cm": 42.0,
            "line_sensors": [0, 0, 1, 0, 0],
        }
        yield mock


def test_robot_status_has_battery(robot):
    status = await robot.get_status()
    assert "battery" in status
    assert 0 <= status["battery"] <= 100


@pytest.mark.requires_hardware
@pytest.mark.destructive
async def test_robot_moves_forward_briefly(robot):
    """Physically moves the robot. Needs clear floor space."""
    result = await robot.move(direction="forward", speed=20, duration_ms=200)
    assert result["success"]
    await robot.stop_all()


@pytest.mark.requires_hardware
async def test_ultrasonic_sensor_reads_reasonable_range(robot):
    """Reads real sensor. Not meaningful to mock."""
    readings = await robot.get_sensor_readings()
    assert 2.0 < readings["ultrasonic_cm"] < 400.0  # physical range of HC-SR04
```

### Dreame Vacuum (dreame-mcp)

```python
DREAME_IP = os.environ.get("DREAME_IP", "192.168.1.150")
DREAME_PORT = int(os.environ.get("DREAME_PORT", "54321"))


@pytest.fixture
async def dreame():
    if ENV == "local_with_iot":
        skip_if_device_unreachable(DREAME_IP, DREAME_PORT, "Dreame vacuum")
        from dreame_mcp.vacuum import DreameVacuum
        v = DreameVacuum(ip=DREAME_IP)
        await v.connect()
        yield v
        await v.disconnect()
    else:
        mock = AsyncMock()
        mock.get_state.return_value = {"state": "idle", "battery": 95, "error": 0}
        mock.start_cleaning.return_value = {"success": True}
        mock.get_map.return_value = {"rooms": [], "width": 0, "height": 0}
        yield mock
```

---

## GitHub Actions Workflow Integration

The environment detection is transparent in CI — `CI=true` is set by GitHub Actions automatically.
No workflow changes needed for the skip logic to work. The workflow still needs secrets for
device IPs if you ever run hardware tests remotely (not recommended).

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Run tests
        run: uv run pytest tests/ -v
        # CI=true is set automatically by GitHub Actions
        # requires_hardware tests are auto-skipped
        # All fixtures use mocks
        # No env vars needed

      - name: Lint (blocking)
        run: uv run ruff check src/

      - name: Format check (blocking)
        run: uv run ruff format --check src/

      - name: Type check pyright (blocking)
        run: uv run pyright src/

      - name: Type check ty (informational)
        run: uvx ty check src/
        continue-on-error: true
```

---

## pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
markers = [
    "requires_hardware: needs physical device on LAN",
    "requires_network: needs LAN access",
    "ci_only: only runs in GitHub Actions",
    "slow: takes more than 5 seconds",
    "destructive: modifies physical state — motor moves, relay trips, paper fed",
]
# Default run: everything except slow
addopts = "-v -m 'not slow'"

[tool.pytest.ini_options.env]
# Default probe target — override in .env for specific LAN
IOT_PROBE_IP = "192.168.1.1"
IOT_PROBE_PORT = "80"
```

`.env` (gitignored, per-machine):

```dotenv
# Device IPs — per machine, never committed
IOT_PROBE_IP=192.168.1.1
SCANNER_IP=192.168.1.50
TAPO_IP=192.168.1.100
ROBOT_IP=192.168.1.200
DREAME_IP=192.168.1.150

# Scanner-specific
SCANNER_PORT=9100
TAPO_PORT=554
ROBOT_PORT=8080
DREAME_PORT=54321
```

`.env.example` (committed, for reference):

```dotenv
# Copy to .env and fill in your device IPs
IOT_PROBE_IP=192.168.1.1      # Router — used to detect LAN presence
SCANNER_IP=192.168.1.50       # HP/Canon/Epson scanner
TAPO_IP=192.168.1.100         # Tapo camera
ROBOT_IP=192.168.1.200        # Yahboom / Unitree robot
DREAME_IP=192.168.1.150       # Dreame vacuum
```

---

## Run Commands

```bash
# Standard run — CI-equivalent (all hardware tests auto-skipped via mocks)
uv run pytest

# Force CI mode locally (same as GitHub Actions)
CI=true uv run pytest

# Full run including hardware (requires IoT on LAN)
uv run pytest -m ""

# Hardware tests only
uv run pytest -m requires_hardware

# Exclude destructive tests (read-only hardware access)
uv run pytest -m "requires_hardware and not destructive"

# Fast unit tests only
uv run pytest -m "not requires_hardware and not slow"

# Show what would be skipped without running
uv run pytest --collect-only -m requires_hardware
```

---

## What to Mock vs What to Skip

This is the critical design decision:

| Behavior | Approach | Reason |
|----------|----------|--------|
| Returns correct type (bytes, dict) | Smart fixture → mock in CI | Verifiable without hardware |
| Raises on bad input | Smart fixture → mock in CI | Pure logic, hardware irrelevant |
| Parses device response format | Smart fixture → mock in CI | Mock returns realistic response shape |
| Physical actuator moves | `requires_hardware` + `destructive` | Cannot mock a motor |
| Sensor reads real environment | `requires_hardware` | Mocked value has no signal |
| Network latency / timeout behavior | `requires_hardware` | Real timing, not simulatable |
| Firmware-specific quirks | `requires_hardware` | Mock can't know what firmware does |
| USB enumeration / WIA discovery | `requires_hardware` | OS-level, not mockable meaningfully |

**Rule:** mock the *interface contract*. Skip the *physical reality*. Never mock physical reality and claim the test passed — that is a false green.

---

## Implementation Status Per Repo

| Repo | Hardware | conftest_env.py | Markers | Smart Fixtures |
|------|----------|-----------------|---------|----------------|
| ocr-mcp | Scanner (WIA/USB) | ❌ not implemented | ❌ | ❌ all mocks unconditional |
| devices-mcp | Tapo, Ring, Netatmo, Dreame | ❌ not implemented | ❌ | ❌ all mocks unconditional |
| robotics-mcp | Various robots | ❌ not implemented | ❌ | ❌ |
| yahboom-mcp | Yahboom robot | ❌ not implemented | ❌ | ❌ |
| universal-actuator-mcp | Actuators | ❌ not implemented | ❌ | ❌ |
| dreame-mcp | Dreame vacuum | ❌ not implemented | ❌ | ❌ |

**Next step:** add `conftest_env.py` from this doc to each repo, then update each `conftest.py`
to import and extend it with device-specific fixtures.

---

## Adding to an Existing Repo (Checklist)

1. Copy `conftest_env.py` template into `tests/conftest_env.py`
2. Add `from tests.conftest_env import ENV, skip_if_device_unreachable, pytest_configure, pytest_runtest_setup` to `tests/conftest.py`  
   — or rename existing hooks and call both
3. Add device-specific fixtures using the smart fixture pattern
4. Add `.env.example` with device IP placeholders
5. Add `.env` to `.gitignore` (already there in fleet standard)
6. Add `IOT_PROBE_IP` etc. to your local `.env`
7. Update `pyproject.toml` markers section
8. Run `CI=true uv run pytest` — all hardware tests should skip, all mock tests should pass
9. Run `uv run pytest -m requires_hardware` locally — hardware tests should run

---

*Added: 2026-03-21 | Tags: testing, hardware, iot, environment-detection, ci-cd, conftest, scanner, robot, tapo, dreame*
