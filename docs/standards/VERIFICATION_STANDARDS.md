# Verification & Testing Standards

## 1. Visual Verification (SOTA)

All UI changes and bug fixes MUST be verified using browser automation tools
(see [rules/playwright_e2e_sota.md](./rules/playwright_e2e_sota.md) and
[rules/cua_nsis_smoke_testing.md](./rules/cua_nsis_smoke_testing.md)).

### 1.1. Evidence Requirements
- **Screenshots**: Mandatory "before" and "after" proof for all UI work.
- **Console Logs**: Capture `browser_console_messages()` to detect silent JS errors or network failures.
- **Log Tails**: For any system or server failure, a 20-line log tail MUST be captured and attached to the bug report.
- **Recordings**: Recommended for complex workflows or animations.

### 1.2. Verification Workflow
1.  **Launch**: Open the application in the browser tool.
2.  **Snapshot**: Use `browser_snapshot()` to get an accessible tree of the UI.
3.  **Interact**: Perform actions (click, type, navigate) to exercise the logic.
4.  **Confirm**: Inspect the DOM or capture console logs to verify the result.
5.  **Evidence**: Save a screenshot or recording to the artifacts directory.

---

## 2. Browser Interaction Safety (Anti-Loop Guards)

To prevent credit-wasting loops and subagent hangs (BUG-004), all browser interactions must follow these safety protocols.

### 2.1. DOM Availability Guard (The "Existence Check")
- **Mandatory Pre-check**: Before any `click` or `type` action, the agent MUST verify that the target element exists in the DOM.
- **Crashed State Detection**: If the subagent returns a "no DOM" or "empty page" state (e.g., after a crash), the agent MUST NOT attempt blind interactions.
- **Wait Policy**: Use explicit `wait_for_selector` with a maximum timeout of **5000ms**. If it fails, abort and report the crash rather than retrying indefinitely.

### 2.2. Interactive Debugging Consent
- **Autonomous Limit**: If a page crashes during verification, the agent is allowed **ONE** attempt to refresh the page.
- **Escalation**: If the refresh fails or the page is stuck in a "DOM-less" state, the agent MUST `notify_user` and request explicit permission before attempting complex interactive recovery (e.g., manually resetting state via console).
- **Stupid-Click Prohibition**: Never "click around" on an empty or error-marked page. If the UI is not rendered, diagnostic logging is the only acceptable action.

### 2.3. Timeout Policy
- **Maximum Duration**: No single browser subagent task should exceed **300 seconds**.
- **Iteration Limit**: Limit subagent steps to **10 iterations** per task. If unresolved, return to the user.

### 2.4. Desktop UI tools are not a substitute for browser verification

**Never** use **pywinauto-mcp** or other **OS-level** UI automation MCPs to verify a **webapp** when a **browser** tool (Playwright, MCP browser, CDP) is available. Desktop automation targets **native windows** and **global focus** — wrong window → loops, IDE takeover, unsafe cursor behavior.

Fleet policy: **remove pywinauto from default IDE MCP chains**; keep browser-scoped tools only. See [WEBAPP_STANDARDS.md §7](./WEBAPP_STANDARDS.md#7-mcp-capability-boundaries-web-vs-desktop-ui) and [FLEET_COMPUTER_USE_MCP.md](../patterns/FLEET_COMPUTER_USE_MCP.md).

---

## 3. Testing Coverage — Dual-Track Strategy

All fleet repos with a webapp MUST follow the **Playwright + CUA dual-testing model**:

| Track | Tool | Runs | What it catches |
|-------|------|------|----------------|
| **Dev loop** | Playwright (headless) | Every push/PR | Route errors, rendering, API integration, console errors |
| **Pre-release** | CUA (pywinauto) | Before each NSIS build | Install failures, CSP/CORS, timing races, registry cleanup |

### 3.1. Playwright E2E — Fleet Audit (Mandatory)

Every webapp MUST pass the minimum Fleet Audit suite from
[rules/playwright_e2e_sota.md](./rules/playwright_e2e_sota.md):

- Backend health endpoint returns 200
- Frontend SPA loads without crash
- No console errors (zero tolerance)
- No 404s on page navigation
- No hydration failures

Referenced implementation: `email-mcp/webapp/e2e/` (17 tests).

### 3.2. CUA-NSIS Smoke Test — Pre-Release Gate (Mandatory)

Every Tauri-wrapped repo MUST pass `just cua-nsis-test` before shipping
(see [rules/cua_nsis_smoke_testing.md](./rules/cua_nsis_smoke_testing.md)):

1. Kill stale processes
2. Silent install (`setup.exe /S`)
3. Launch operator
4. Health check (exponential backoff)
5. Window verify (pywinauto)
6. Screenshot capture
7. Diagnostics (`GET /api/v1/diagnostics`)
8. Silent uninstall

Referenced implementation: `pywinauto-mcp/scripts/cua-smoke.py` (9 phases).

### 3.3. Dashboard Requirements

To make verification reliable, every webapp dashboard MUST:

- Attach `data-testid` attributes on all KPIs and status badges
- Implement exponential backoff on health checks (1s, 2s, 4s, 8s, 16s)
- Listen for Tauri `backend-status` event for instant refresh
- Expose `GET /api/v1/diagnostics` endpoint (tools, Tesseract, window status)

### 3.4. Lint & Format Gates

All repos MUST pass these before any merge or build:

| Gate | Tool | Scope | Command |
|------|------|-------|---------|
| Python lint | `ruff` | `src/` + `tests/` | `ruff check src/ tests/` |
| Python format | `ruff format` | `src/` + `tests/` | `ruff format --check src/ tests/` |
| JS/TS lint | `biome` | `web_sota/src/` or `webapp/src/` | `biome ci .` (from webapp dir) |
| TypeScript | `tsc` | `web_sota/` or `webapp/` | `tsc --noEmit` (from webapp dir) |

`ruff` and `biome` are the **only** fleet linters. ESLint, Prettier, Flake8, Black are not used. Biome auto-fix with `biome check --write .` before commits.

### 3.5. API Resilience Pattern

Every HTTP endpoint that calls multiple downstream services (internal subprocesses, upstream MCP servers, databases) MUST wrap each call in its own try/except. A single failing sub-call MUST NOT cascade into a 500 error for the whole endpoint.

**Bad — one exception kills the response:**
```python
@app.get("/api/stats")
async def stats():
    notebooks = await nlm.notebook_list()  # if this raises, response is lost
    doctor = await nlm.doctor_text()
    return {"notebooks": notebooks["count"], "authenticated": doctor["authenticated"]}
```

**Correct — each call isolated:**
```python
@app.get("/api/stats")
async def stats():
    count = 0
    try:
        notebooks = await nlm.notebook_list()
        count = notebooks.get("count", 0)
    except NlmError:
        pass
    try:
        doctor = await nlm.doctor_text()
    except Exception:
        doctor = {"authenticated": False}
    return {
        "notebooks": count,
        "authenticated": doctor.get("authenticated", False),
    }
```

This applies to all `@router` and `@app` endpoint handlers, not just `/api/stats`. Aggressive isolation prevents one dead upstream from taking down the whole dashboard.

### 3.6. Unit & Integration Tests

- **Unit Tests**: 80% minimum coverage (Pytest or Vitest).
- **Integration Tests**: 70% minimum coverage for tool-to-application communication.

## 4. Manual Verification Fallback

If automated verification is impossible (e.g., hardware-specific), provide:
- Clear, step-by-step instructions for the user.
- Expected vs. actual outcomes.
- Request for user-provided screenshots as proof.
