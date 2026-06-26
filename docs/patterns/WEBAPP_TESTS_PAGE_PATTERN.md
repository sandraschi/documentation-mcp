# Webapp Tests Page Pattern

**Last Updated:** 2026-03-05  
**Status:** Optional, recommended for SOTA/local-first webapps  
**Reference implementation:** [advanced-memory-mcp](https://github.com/sandraschi/advanced-memory-mcp) (Tests page, `tests_router.py`, `Tests.tsx`)

---

## Overview

A **Tests page** in the webapp lets users run the project test suite (pytest, npm test, etc.) from the browser and see pass/fail, duration, and raw output. The backend exposes a single guarded endpoint; the frontend provides a Run button and results area.

**When to use:** Repo has a test suite and you want to run it from the UI during local dev or demos.  
**When to skip:** No meaningful tests to run from the UI, or production-only app where a test-runner endpoint is undesirable.

---

## Architecture

- **Backend:** `POST /tests/run` (or under your API prefix). Runs the test runner in a subprocess with a timeout. **Must be guarded** by an env flag (e.g. `ENABLE_WEBAPP_TESTS=1`); return 403 if not set.
- **Frontend:** "Tests" nav item and page: Run button, optional target/args input, display of exit code, duration, stdout/stderr (and optionally structured report).

---

## Implementation checklist

### Backend

1. Add route `POST /tests/run`. Require env guard; return 403 when disabled.
2. Resolve repo/project root (from `__file__` or env).
3. Run test command (e.g. `python -m pytest <target>` or `npm run test`) via subprocess with configurable timeout.
4. Return JSON: `{ success, exit_code, stdout, stderr, duration_seconds }`. Optionally add structured report (e.g. pytest-json-report) for richer UI.

### Frontend

1. API client: `runTests({ target?, timeout_seconds?, extra_args? })`.
2. Tests page: Run button, target input, results (summary + raw log). Optionally per-test list with expandable failures if backend returns structured report.
3. Nav: "Tests" entry (e.g. flask/beaker icon).

### Docs

- Webapp README: Note that the Tests page exists and that the backend must be started with the feature flag. Do not enable in production.

---

## Security

- Never enable the test runner in production. Rely on the env flag; document that it must not be set in prod.
- Optional: restrict by IP or auth if the webapp is exposed beyond localhost.

---

## Variations

- **Node/Express backend:** Same idea; run `npm run test` or `npx jest` in repo root.
- **Frontend-only webapp:** No backend endpoint; run tests via CI or a separate script, or add a minimal server just for this endpoint.
- **Structured results:** Use a reporter (e.g. pytest-json-report, jest JSON output) and return structured pass/fail per test for expandable failure UI.

---

## Cross-references

- **Advanced Memory pattern doc:** `advanced-memory-mcp/docs/WEBAPP_TESTS_PATTERN.md`
- **MemOps note (knowledge graph):** `advanced-memory-mcp/docs/notes/webapp-tests-page-pattern.md` (entity-style note for ADN/MemOps)
- **Ports and webapp ops:** [operations/WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md)
