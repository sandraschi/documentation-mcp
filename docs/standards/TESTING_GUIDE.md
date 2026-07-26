# Testing Guide for AI-Assisted Development (SOTA 2026)

**Status:** Active
**Last updated:** 2026-07-12
**Related:** `rules/playwright_e2e_sota.md`, `rules/cua_nsis_smoke_testing.md`, `VERIFICATION_STANDARDS.md`, `FLEET_BUILD_TEST_PIPELINE.md`, `testing.md`, `testing-tdd-red-green.md`, `testing-environment-aware.md`

---

## The Honest Truth

Writing tests is the most unrewarding part of development. You grind for two days. You get no new UI, no new feature, no screenshot to show anyone. The only reward is that in six months, when you refactor something, the tests catch the three things you forgot.

**AI changes this.** The same LLM that wrote the feature code can write the tests in five minutes — if the tools, patterns, and scaffolding are in place. This guide exists to make that fast.

The goal is not 100% coverage. The goal is **the right 30% coverage** that catches real regressions and lets you ship with confidence.

---

## The Four Test Layers

```
Layer 4: CUA-NSIS Smoke     — install the real NSIS, launch, verify, uninstall
Layer 3: Playwright E2E      — webapp renders, navigates, fetches, no console errors
Layer 2: Integration         — tool talks to real/mocked ComfyUI, DB, API
Layer 1: Unit (pytest)       — pure logic, param transformation, edge cases
```

Every repo needs:
- **Layer 1** — always. This is where AI adds most value (fast, isolated, mocks)
- **Layer 3** — if the repo has a webapp. Catches the things unit tests can't (routing, rendering, API integration)
- **Layer 4** — if the repo ships a Tauri/NSIS installer. Mandatory before every release

Layer 2 is optional — you get most of the value from good Layer 1 tests with mocked external deps.

---

## Layer 1: Unit Tests (pytest) — Where AI Shines

### What to test

| What | Example | Priority |
|------|---------|----------|
| Pure logic functions | `_apply_params()`, `_gather_outputs()` | HIGH |
| Edge cases | Empty input, timeout, missing data | HIGH |
| Error paths | Invalid workflow ID, ComfyUI down | HIGH |
| State transitions | Queue → running → complete → fail | MEDIUM |
| Config loading | Env var parsing, defaults | MEDIUM |
| Model validation | Pydantic schemas, Literal enums | LOW (covered by type system) |

### What NOT to test

- Trivial getters/setters
- Third-party library behavior (trust FastMCP's own tests)
- Complex mocking scenarios that break when the implementation changes slightly

### The AI Test Pattern

The fastest way to get good tests: give the AI the source file and the conftest fixtures, and ask for tests covering the function's contract, edge cases, and error paths. This is what produced the 125-test comfyops scaffold in under 5 minutes.

Key ingredients:
1. **A conftest.py with shared fixtures** — mock servers, temp directories, sample data. Write this once, the AI reuses it.
2. **Clean function signatures** — pure functions with no hidden state are trivially testable.
3. **`patch.object` for external deps** — mock the network boundary, test your logic.

### Fixture Pattern (from comfyops-mcp conftest.py)

```python
# tests/conftest.py
@pytest.fixture
def tmp_workflows_dir():
    """Create a temp workflows directory with a sample workflow."""
    with tempfile.TemporaryDirectory() as td:
        wf_dir = Path(td) / "workflows"
        wf_dir.mkdir()
        (wf_dir / "test.json").write_text(json.dumps(SAMPLE_WORKFLOW))
        yield str(wf_dir)

@pytest.fixture
def patch_config(tmp_workflows_dir, tmp_data_dir):
    """Point config at temp dirs."""
    with patch.multiple(cfg, WORKFLOWS_DIR=tmp_workflows_dir, DATA_DIR=tmp_data_dir):
        yield

@pytest_asyncio.fixture
async def mock_httpx_client():
    """Mock the HTTP client for ComfyUI API calls."""
    client = AsyncMock(spec=httpx.AsyncClient)
    client.get.return_value = MagicMock(status_code=200, json=lambda: HEALTH_RESPONSE)
    client.post.return_value = MagicMock(status_code=200, json=lambda: PROMPT_RESPONSE)
    with patch("mymodule.http_client._client", client):
        yield client
```

---

## Layer 2: Integration Tests

These test that your tool actually works against a real or realistically-mocked service. The pattern:

```python
class TestGenerateIntegration:
    async def test_happy_path(self, mock_httpx_client, patch_config):
        vram = await check_vram(4.0)
        assert vram["ok"] is True

        workflow = json.loads(Path(cfg.WORKFLOWS_DIR / "test.json").read_text())
        queue = await queue_prompt(workflow)
        assert queue["ok"] is True

        result = await wait_for_result(queue["prompt_id"])
        assert result["ok"] is True
        assert len(result["outputs"]) >= 1
```

The key: the fixtures handle the mocking. The test reads like a real usage flow.

---

## Layer 3: Playwright E2E

See `rules/playwright_e2e_sota.md` for the full standard. Minimum suite:

```typescript
test('Backend health', async ({ request }) => {
    const resp = await request.get(BE + '/health');
    expect(resp.status()).toBe(200);
});
test('Frontend loads', async ({ page }) => {
    await page.goto(FE);
    await expect(page.locator('#root')).toBeAttached();
    // Check no console errors
});
```

Every webapp MUST have these two tests. They catch:
- Backend not running on the expected port
- Frontend SPA fails to mount (missing dependencies, JS error)
- CORS/config issues that unit tests never touch

---

## Layer 4: CUA-NSIS Smoke

See `rules/cua_nsis_smoke_testing.md` for the full standard. This runs the actual NSIS installer in silent mode, launches the app, and verifies it works via pywinauto.

This is the slowest but most realistic test — it catches what nothing else can:
- PyInstaller frozen binary crashes
- WebView2 loading before backend is ready
- CSP/CORS misconfig blocking API calls
- Registry cleanup on uninstall

---

## What 30% Coverage Looks Like

Given 5 tools with 125 tests total (comfyops-mcp reference):

| Module | Tests | What they cover |
|--------|-------|-----------------|
| config | 11 | Default values, env var overrides |
| comfyui_manager | 20 | Health, VRAM, workflow depot, prompt queue, model listing |
| tools/generate | 18 | Param application, VRAM map, tool registration |
| tools/workflows | 20 | CRUD, search, discover, error handling |
| tools/models | 13 | List, VRAM, health, error handling |
| tools/library | 14 | Record, recent, search, edge cases |
| tools/agentic | 6 | Sampling with/without ctx, suggestions |

The **generate + workflows** tests (38 total) are the highest-value because they cover the two tools users interact with most.

---

## Making Tests Fast

| Technique | Speedup | How |
|-----------|---------|-----|
| `-q --tb=short` | Fast feedback | Run just failures quickly |
| `pytest --co` | Colored output | Easier to scan |
| `pytest -k "test_name"` | Targeted | Run one test while developing |
| `just test` | Convention | Fleet-wide consistent command |
| Module-level fixtures | Shared setup | `@pytest.fixture(scope="module")` for slow fixtures |

---

## The AI Test Prompt Template

When asking an AI to write tests for a module, give it:

1. The source file (so it knows the function signatures)
2. The conftest.py fixtures (so it knows what mocks are available)
3. A specific ask: "tests for function X covering normal case, edge case, and error case"

Example prompt:
```
Write tests for comfy_generate covering:
1. Normal case: valid workflow, VRAM ok, prompt succeeds, returns outputs
2. Edge case: missing workflow_id returns not_found error with suggestions
3. Error case: ComfyUI down returns vram/connection error
4. Param application: seed, prompt, size, negative_prompt all correctly injected

Use the mock_httpx_client and patch_config fixtures from conftest.py.
```

This produces ~20 tests in under 30 seconds.

---

## The Fleet Contribution: Scaffolding Over Generation

Research papers focus on test *generation* (the LLM writing assertions). Our fleet experience shows that **scaffolding is the bottleneck**, not generation. Give the AI good fixtures, and the test quality triples.

### The Scaffolding Pattern (from comfyops-mcp)

The conftest provides three things that make AI test generation fast:

1. **Temp directory fixtures** — `tmp_workflows_dir`, `tmp_models_dir`, `tmp_data_dir` point at isolated temp directories pre-populated with sample data. The AI doesn't need to think about filesystem state.
2. **Mock client fixtures** — `mock_httpx_client` returns predefined responses for every ComfyUI API call. The AI writes tests against a realistic API surface without needing ComfyUI running.
3. **Config patch fixtures** — `patch_config` and `patch_all` override all environment-dependent config with known temp paths in one line. The AI never needs to set env vars.

Without these, the AI writes tests that either (a) can't run because they depend on real infrastructure, or (b) are trivial because mocking takes too many lines.

### Default to Dialogic Error Returns on Failure

Every MCP tool should return clear, actionable error messages when the backend is unreachable — not timeouts or raw stack traces.

```python
# BAD — silent timeout, no info for the user
try:
    result = await call_backend()
except Exception:
    return {"success": False, "error": "An error occurred"}

# GOOD — tell the user what's wrong and what to do about it
try:
    result = await call_backend()
except httpx.ConnectError:
    return {
        "success": False,
        "error": "arxiv-mcp backend not reachable on port 10770",
        "error_type": "connection",
        "suggestions": [
            "Start the backend: `uv run python -m arxiv_mcp.__main__ --serve`",
            "Check ARXIV_MCP_HOST and ARXIV_MCP_PORT in .env",
        ],
    }
except Exception as e:
    return {"success": False, "error": str(e), "error_type": "general",
            "suggestions": ["Check the backend logs for details."]}
```

This is the fleet's dialogic returns pattern from `TOOL_DESIGN_STANDARDS.md` — every failure carries `suggestions` or `recovery_options` so the agent knows what to do next.

## Research References

arXiv papers on LLM-based test generation (when available):

| Paper | Focus | Key Insight |
|-------|-------|-------------|
| TestPilot (Microsoft, 2024) | Playwright test generation | LLM + page snapshot catches 2x more regressions than manual |
| CodaMosa (2024) | Test generation + search | LLMs miss edge cases; combine with search-based testing |
| Self-Refine for Tests (2024) | Iterative test repair | 3 cycles of generate → run → fix beats human assertion coverage |
| SWE-bench (2024) | Real bug fixes | ~70% of LLM fix failures are test-related (wrong assertions) |
| Codex Test Generation (OpenAI, 2023) | Unit test generation | ~70% pass rate but mostly trivial getter/setter coverage |

The gap the fleet fills: none of these papers address the **scaffolding problem** — giving the AI good fixtures, mocks, and config so the generated tests actually run. That's the fleet's contribution: conftest.py first, tests second.
