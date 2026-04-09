# Implementation Honesty Standard

## 1. Purpose

Prevent "fake-green" systems where tools appear to succeed but are not implemented.

This standard applies to:
- MCP tools and API routes
- background workers and plugin modules
- webapp UX states for unavailable capabilities

## 2. Lifecycle Policy

### 2.1 Prototype phase (allowed with controls)
- Placeholders are allowed only when explicitly tagged as temporary.
- Each placeholder MUST include owner, planned replacement, and expiration date.
- Responses MUST not claim completed work if logic is missing.

### 2.2 Pre-release and production (strict)
- No simulated success paths.
- No synthetic findings presented as real security/runtime output.
- No hardcoded "healthy" metrics in place of actual telemetry.
- Unimplemented paths MUST return explicit machine-readable errors:
  - `error_type: "not_implemented"` or equivalent
  - clear `message`
  - actionable `recovery_options` / `suggestions`

## 3. MCP Tool Contract Rules

- If integration/model/provider is unavailable, return a truthful failure contract.
- Never return `success: true` for placeholder logic.
- Destructive tools must keep guardrails even when not implemented (`confirm`, dry-run patterns).
- Docstrings must declare unavailable operations as `under construction` until complete.

## 4. Webapp UX Rules

- Any unavailable action must be visibly marked **Under construction**.
- Disable or guard non-functional controls when possible.
- Error banners must explain current limitation and next action.
- Do not silently no-op.

## 5. CI Enforcement

Repositories SHOULD include a policy check that fails CI on banned runtime patterns in `src/` and backend/webapp runtime code, while allowing tests/docs/examples.

Recommended banned indicators:
- `simulate`, `simulated` (runtime path)
- `placeholder` (runtime success path)
- `mock response` in production code
- hardcoded synthetic findings presented as real results

## 6. Accepted Exceptions

- Unit/integration tests, fixtures, and explicit demo/example modules.
- Migration adapters that throw explicit `not_implemented`.
- Compatibility wrappers that do not fabricate success.

## 7. Review Checklist

- Does every non-implemented path fail explicitly and truthfully?
- Is UI state explicit for unavailable functionality?
- Are any static/sample values emitted as if they were real?
- Is CI policy check active for PRs?
