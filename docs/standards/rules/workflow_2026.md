# SOTA 2026 Agentic Workflow

This workflow is the "Biggest Unlock" for high-leverage development. It front-loads thinking and maintains context hygiene.

## The 4-Phase Loop

1. **EXPLORE (Read-Only)**
   - Research the codebase, understand patterns, and identify dependencies.
   - Use "Plan Mode" (or equivalent) to prevent accidental edits.
   - Ask deep questions ("Spec-First Interview") to build a `SPEC.md` if the task is complex.

2. **PLAN (Architectural Alignment)**
   - Create a structured `implementation_plan.md`.
   - The plan MUST be the source of truth that survives context resets.
   - Challenge assumptions and edge cases before starting execution.

3. **IMPLEMENT (Execution)**
   - Switch to "Normal" or "Auto-Accept" mode.
   - Execute the approved plan phase-by-phase.
   - Clear context between unrelated phases to prevent "Context Drift."

4. **COMMIT & VERIFY**
   - Run automated tests and verify logic.
   - Run Playwright e2e tests for webapp repos (see `playwright_e2e_sota.md`).
   - Create conventional commits and PRs.

## Context Hygiene
- **Proactive Compaction**: Run `/compact` at ~75% token capacity.
- **Session Focus**: One clear scope per session. Start fresh (`/clear`) when switching tasks.
- **Spec-First Interview**: For significant features, interview the user using the `AskUserQuestion` tool to lock the requirements.

---

## Phase 5: PLAYWRIGHT-AIDED WEBAPP IMPROVEMENT (Headless Iteration)

Trigger: "improve the webapp of repo X" or "fix dashboard bugs in repo X".

The agent runs headless Playwright (isolated Chromium, no desktop interference) to
visually and structurally audit the webapp, then iterates autonomously.

### Loop

1. **START** — Launch webapp via `just dev` / `start.ps1` if not running. Clear port
   zombies first (Get-NetTCPConnection → Stop-Process). Wait for HTTP 200 on backend
   and frontend ports before proceeding.

2. **PROBE** — Headless Playwright:
   - `browser_navigate` to frontend URL
   - `browser_snapshot` (accessibility tree, not raw HTML — richer structure)
   - `browser_take_screenshot` full page
   - `browser_console_messages` capture errors/warnings

3. **AUDIT** — Scan for:
   - 404s, broken links, failed API calls (console errors + network check)
   - Missing elements (empty content areas, placeholder text, lorem ipsum)
   - Layout breaks (overlapping text, clipped elements from screenshot)
   - Console errors (React warnings, uncaught exceptions, CORS)
   - MCP tool discovery failures (hardcoded tool lists instead of dynamic fetch)

4. **FIX** — Read relevant source files, edit, save. Do NOT restart the dev server
   (Vite/FastAPI hot reload handles it).

5. **RE-AUDIT** — `browser_navigate` (fresh load), re-run all checks from step 3.
   Confirm each issue is resolved. Check for regressions.

6. **LOOP** — Repeat steps 4-5 until all identified issues are clean or blocked
   by something requiring user input.

### Rules

- **Headless only.** No `browser_click`, `browser_type`, etc. against the live app
  outside snapshot/inspection — read-only audit. User interacts with the actual app.
- **Hot reload is your friend.** No server restarts between edits. Just re-navigate.
- **Console errors are high signal.** Always check after each change.
- **Report.** After the loop, show: what was found, what was fixed, what remains.
- **If the app won't start**, report the build/serve error and stop.
