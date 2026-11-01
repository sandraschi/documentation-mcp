# Python in the Tout-Banc Fleet: Where It Wins After Rustification

**Version:** 3.12+ (fleet standard for remaining Python repos)
**Context:** ML/GPU worker, host-app scripting, wire-spec oracle - no longer the default for new MCP servers
**Architecture:** FastMCP for remaining Python servers / PyTorch + CUDA for Bucket D / thin in-host listeners for Bucket C
**Packaging:** `uv` (Rust-built, 10-100x faster than pip) | **Linting:** `ruff` (Rust-built)
**Sibling hub:** [Rust Hub](../rust/README.md) | **Regime rule:** [RUST_ARTCRAFT_STANDARD.md](../../../standards/RUST_ARTCRAFT_STANDARD.md)

> [!IMPORTANT]
> "Butter bei die Fische": this document is the Single Source of Truth for Python in this fleet AFTER the 2026-10-17 regime change. What changed: Python is no longer "primary language for 90% of the fleet". Buckets A (REST/Cloud/SQLite/System/CLI) and B (clean LAN hardware) convert to pure-Rust ArtCraft. Python keeps three jobs it does better than Rust: GPU/ML workloads (Bucket D), embedded scripting inside host binaries plus fast-moving reverse-engineered cloud crypto (Bucket C), and serving as the machine-readable wire specification that agents transpile into Rust (PyPI-as-oracle). Everything below assumes that framing.

---

## Table of Contents

1. [Executive summary: Python's three remaining jobs](#1-executive-summary-pythons-three-remaining-jobs)
2. [The remaining-Python standard (FastMCP, asyncio, pydantic)](#2-the-remaining-python-standard-fastmcp-asyncio-pydantic)
3. [Global context: Python's evolution](#3-global-context-pythons-evolution)
4. [Fleet integration patterns (uv, docker, PyO3, front-door)](#4-fleet-integration-patterns-uv-docker-pyo3-front-door)
5. [Advanced patterns (perf, security)](#5-advanced-patterns-perf-security)
6. [Reference material](#6-reference-material)

---

## 1. Executive summary: Python's three remaining jobs

In the tout-banc fleet, Python is a specialist, not the default. New Bucket A/B work goes to Rust (see Rust Hub). Python stays where the ecosystem moat is real:

- **Job 1 - GPU/ML worker (Bucket D).** PyTorch, Triton, Diffusers, Unsloth, IsaacLab, CUDA kernels, `.safetensors` loading. Rewriting this in Rust is a negative-ROI trap unless inference is pure ONNX (`ort`) or a local HTTP call to Ollama/vLLM. Pattern: Rust front door (CLI + MCP + GUI) with a Python GPU worker behind a local socket or HTTP loopback. Rust owns the agent contract; Python owns the tensors.
- **Job 2 - host-app embedded scripting + rotating cloud crypto (Bucket C).** Blender (`bpy`), FreeCAD, KiCad (`pcbnew`), LibreOffice, DaVinci Resolve run Python INSIDE the host binary - Rust cannot replace that interpreter. Likewise Xiaomi/Alexa-style cloud APIs with monthly reverse-engineered auth churn: keep the community `pysomething` package until the protocol stabilizes, then port. Pattern: Rust MCP server + Tauri/egui app talking over local TCP/pipe to a thin (~100-line) Python listener inside the host.
- **Job 3 - wire-spec oracle for Rust ports.** Almost every long-tail `pysomething` package is 85 percent ceremony around 15 percent wire essence (URLs, headers, OAuth quirks, framing). Agents read the Python source as an executable spec and emit a 150-300 line zero-unwrap Rust module (proven for Ring, Netatmo, Hue in rust-devices-mcp). Python's tests directory becomes the golden-fixture oracle for the Rust port. Full playbook in [Rust learning](../rust/learning/README.md).

Irony worth stating plainly: the two tools that make Python development fast in 2026 - `uv` and `ruff` - are themselves written in Rust (Astral). Wave 1 of rustification already happened inside Python's own toolchain.

**Why Python still, for these jobs?**

- **AI native:** every major inference engine and orchestration layer (PyTorch, JAX, LangChain, LlamaIndex) is Python-first with no Rust equivalent at parity.
- **Host lock-in:** `bpy`, `pcbnew`, and siblings only execute Python. No port is possible, only bridging.
- **Reverse-engineering velocity:** weekend contributors publish `pysomething` fixes in hours; hand-maintaining that churn in Rust wastes agent cycles until the protocol settles.
- **Type safety where it counts:** modern Python (3.12+) with Pydantic v2 plus `mypy`/`pyright` in CI gives validated boundaries, even though it cannot match the compiler-proven guarantees of `deny(unwrap_used)` Rust.

---

## 2. The remaining-Python standard (FastMCP, asyncio, pydantic)

This section applies to repos that STAY Python (Buckets C/D). New Bucket A/B servers must not use it; they follow the Rust ArtCraft pattern.

### FastMCP Architecture

FastMCP (decorators + type hints generating schemas automatically) remains the standard for remaining Python MCP servers.

#### The "Hello World" of the remaining fleet

```python
# src/server.py
from mcp.server.fastmcp import FastMCP
from pydantic import Field, BaseModel

# Initialize with metadata
mcp = FastMCP(
    "crypto-ticker",
    version="2.4.0",
    description="Real-time cryptocurrency market data"
)

class TickerData(BaseModel):
    symbol: str
    price: float
    volume_24h: float

@mcp.tool()
async def get_price(
    symbol: str = Field(..., description="Ticker symbol (e.g. BTC, ETH)", pattern="^[A-Z]{3,5}$"),
    currency: str = Field("USD", description="Quote currency")
) -> TickerData:
    """
    Fetch real-time price methodology.

    This docstring is automatically parsed into the MCP Tool Description.
    """
    # ... implementation using aiohttp ...
    return TickerData(symbol=symbol, price=98000.0, volume_24h=1.2e9)

if __name__ == "__main__":
    mcp.run()
```

### AsyncIO and Concurrency

**Synchronous I/O is BANNED** in production MCP servers. Blocking the main thread kills the agent's ability to multitask.

- **Network:** use `aiohttp` or `httpx` (async client).
- **File I/O:** use `aiofiles`.
- **Subprocesses:** use `asyncio.create_subprocess_exec`.

**Anti-Pattern (DO NOT DO THIS):**
```python
import requests
def fetch_data():
    return requests.get("https://api.example.com").json() # BLOCKS EVERYTHING
```

**SOTA Pattern:**
```python
import httpx
async def fetch_data():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com")
        return resp.json() # NON-BLOCKING
```

### Type Systems and Validation

We rely heavily on **type hints** and **Pydantic**.
- **Runtime enforcement:** Pydantic validates data entering and leaving the server.
- **Schema generation:** JSON Schemas for MCP tools are generated from these types.
- **IDE support:** robust autocompletion and error checking.

Honest caveat (post-Rustification): Pydantic validates at runtime what Rust proves at compile time. For agent-written code at 100+ tokens/sec, the Rust closed loop (rustc + clippy deny gates) catches hallucinated attributes before execution; Python catches them in production. That asymmetry is exactly why Buckets A/B moved. Inside Buckets C/D, Pydantic + mypy/pyright remains the best available net.

---

## 3. Global context: Python's evolution

*(Ingested from Wikipedia research, retained from the pre-conversion edition.)*

### History and Philosophy
Python was conceived in the late 1980s by **Guido van Rossum** at CWI in the Netherlands as a successor to the ABC language, targeting the Amoeba distributed OS with exception handling and system interfacing.

- **Python 2.0 (2000):** list comprehensions, reference-counted GC.
- **Python 3.0 (2008):** major cleanup, not backward-compatible; long transition period.
- **Python 3.12 (fleet SOTA):** improved error messages, low-impact monitoring, significant interpreter speedups.

**Philosophy (The Zen of Python, PEP 20):**
- *Beautiful is better than ugly.*
- *Explicit is better than implicit.*
- *Simple is better than complex.*
- *Complex is better than complicated.*
- *Readability counts.*

Fleet adherence: **"Explicit is better than implicit"** is enforced in both languages. Magic behavior is forbidden. In Rust repos the compiler enforces it; in Python repos reviewers and Pydantic must.

### Syntax and Semantics

Python is multi-paradigm: OOP and structured programming fully supported, functional and aspect-oriented (via decorators) available.

**Indentation:** whitespace delimits blocks (the "off-side rule"), not braces.

**Dynamic typing:** strict runtime enforcement via duck typing, plus static checking via the `typing` module (PEP 484) enforced with `mypy` and `pyright` in CI.

---

## 4. Fleet integration patterns (uv, docker, PyO3, front-door)

### Dependency Management (`uv`)
`pip` and `poetry` are retired. The standard is `uv` (by Astral, written in Rust, 10-100x faster).

**Standard `pyproject.toml` (remaining-Python server):**
```toml
[project]
name = "mcp-server-fleet-template"
version = "0.1.0"
description = "Standard template for fleet servers"
authors = [{ name = "Sandra S.", email = "sandra@wien.at" }]
dependencies = [
    "mcp[fastmcp]>=1.0.0",
    "pydantic>=2.0.0",
    "httpx>=0.25.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.0",
    "ruff>=0.1.0",
    "mypy>=1.6.0"
]
```

### Docker Containerization
Production Python servers (GPU workers especially need CUDA base images, not Alpine) run in containers. CPU-only template uses multi-stage slim builds:

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY src/ .
CMD ["python", "server.py"]
```

### Rust Extensions and PyO3 (the bridge direction that remains)

For CPU-bound hot paths inside Python repos, write the core in Rust and bind with `PyO3` (this is how `pydantic-core` itself works). The reverse direction - Python libraries absorbed INTO Rust - is the conversion playbook, not this section.

### Rust Front Door + Python GPU Worker (Bucket D canonical)

- Rust L1/L2 owns the agent contract: CLI `--json`, MCP stdio, egui controls, credential fence, Demo oracle for CI without GPUs.
- Python owns tensor execution behind a local socket/HTTP boundary with versioned JSON schemas shared from the Rust types.
- Neither side imports the other. The boundary is bytes on localhost, tested with golden fixtures on both sides.

### Thin In-Host Listener (Bucket C canonical)

- Rust MCP server + app talk over local TCP/pipe to a ~100-line Python listener inside Blender/FreeCAD/Resolve.
- The listener does no business logic beyond host-API calls and JSON marshal; all state machines live in Rust where the compiler checks them.

---

## 5. Advanced patterns (perf, security)

### Performance Optimization

1. **uvloop:** drop-in `asyncio` event loop replacement, 2-4x faster.
   ```python
   import uvloop
   import asyncio
   asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
   ```
2. **orjson:** fastest JSON library for high-throughput endpoints.
3. **Rust extensions via PyO3/maturin:** for CPU-bound tasks, port the hot function to Rust. This is Wave 1 history repeating at repo scale.

### Security Best Practices

1. **Input sanitization:** never trust tool inputs. Pydantic handles type validation; logic validation (path traversal, bounds) must be explicit.
2. **Environment variables:** secrets come from `os.environ`, never hardcoded.
   ```python
   API_KEY = os.environ.get("OPENAI_API_KEY")
   if not API_KEY:
       raise ValueError("OPENAI_API_KEY is not set")
   ```
3. **Least privilege:** run as non-root inside containers; GPU workers get device-scoped mounts only.

---

## 6. Reference material

- [Python 3.12 Documentation](https://docs.python.org/3.12/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/)
- [FastAPI / FastMCP Design Patterns](https://fastapi.tiangolo.com/)
- [uv: An extremely fast Python package installer](https://github.com/astral-sh/uv)
- [ruff: An extremely fast Python linter](https://github.com/astral-sh/ruff)
- [PyO3: Rust bindings for Python](https://pyo3.rs/)
- Sibling hub: [Rust Hub](../rust/README.md) - read before proposing any NEW Python MCP server.
- Conversion playbook: [Rust learning](../rust/learning/README.md) section 4 (for moving a Bucket A/B repo OUT of Python).

---

**Maintainer:** Sandra S.
**Last updated:** 2026-10-17 (tout-banc reframe; supersedes 2026-02-13 "Python for 90%" edition)
**Status:** SOTA 2026 compliant. ASCII-only by fleet hygiene rule.
