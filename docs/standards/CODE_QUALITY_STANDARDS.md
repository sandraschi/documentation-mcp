---
title: "Code Quality & Formatting"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-07-29
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Code Quality & Formatting

## 1. Python Standards (Ruff)

Ruff is MANDATORY for all Python-based MCP servers.

### 1.1. Configuration (`pyproject.toml`)
- `line-length = 100` (repo may use 120; keep consistent within repo)
- `target-version = "py311"` or `"py312"`
- **`select` is mandatory** — never rely on Ruff defaults. Ruff **0.16** expanded implicit defaults from ~59 to **413** rules when `select` is omitted.
- Fleet baseline: `select = ["E", "W", "F", "I", "B", "UP"]` (extend per repo as needed, e.g. `"S"`, `"RUF"`)
- To match pre-0.16 global defaults only: `select = ["E4", "E7", "E9", "F"]`
- **`E501`:** prefer wrapping long strings; for legacy repos with `"S"`/`"RUF"` in `select`, add `"E501"` to `ignore` manually in `pyproject.toml` if needed (do **not** use batch scripts that rewrite TOML without validation).
- **Legacy `S` / `RUF` repos:** use explicit `ignore` for noisy rules (`S106`, `S110`, `S112`, `S603`, `S607`, `S324`, `RUF012`, `E402`) rather than dropping `select`. Script: `mcp-central-docs/scripts/fix-fleet-ruff-sruf-ignores.ps1`.
- **Fleet lint repair:** `mcp-central-docs/scripts/fix-fleet-ruff-green.ps1` (explicit `select`, dev `ruff>=0.16`, `--unsafe-fixes`, format).
- **Ruff version:** dev/dependency-groups only — `"ruff>=0.16.0,<0.17"`. Never in `[project] dependencies`. CI **fails** if not 0.16.x or if `[tool.ruff.lint] select` is missing (Trap 7b).
- **Pre-commit pin:** `rev: v0.16.0` on [astral-sh/ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit) (must match pyproject major/minor).

### 1.2. Pre-commit hook (recommended)

Use **[pre-commit](https://pre-commit.com/)** so **Ruff** (Python) and **Biome** (webapp / `web_sota`) run on **commit**, not only in CI.

**Canonical template:** `mcp-central-docs/templates/pre-commit-config.yaml.template`  
**Biome helper script:** `mcp-central-docs/templates/pre-commit-biome.ps1` → copy to `{repo}/scripts/pre-commit-biome.ps1`

**`.pre-commit-config.yaml`** (pin `rev` to a current [ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit) tag):

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: biome-web
        name: biome check (webapp)
        entry: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/pre-commit-biome.ps1
        language: system
        files: ^(webapp|web_sota)/(src/.*\.(ts|tsx|js|jsx|json)|biome\.json)$
        pass_filenames: false
        require_serial: true

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=5120]
```

**Setup:** `just bootstrap` (preferred) or `uv sync --extra dev` + `uv run pre-commit install` + `npm ci` in `webapp/` (or `web_sota/`).

**Agent / scaffold pitfall:** Adding `.pre-commit-config.yaml` (or documenting hooks) is **incomplete** without running `pre-commit install` in that repo. Prefer wiring `pre-commit install` and webapp `npm ci` into `just bootstrap` / `just install` so setup activates hooks automatically.

**CI parity:** Local pre-commit and `.github/workflows/ci.yml` MUST run the same gates on the **same paths** (Trap 7c — never narrow ruff `files:` in pre-commit alone):

| Step | Command | Blocking |
|------|---------|----------|
| Ruff version + explicit `select` | CI verify step | Yes |
| Ruff lint | `uv run ruff check src [tests]` (+ `scripts`, `mcpb`, … only if CI lists them) | Yes |
| Ruff format | `uv run ruff format --check src [tests]` (same path set as lint) | Yes |
| Pytest | `uv run python -m pytest tests/` | Yes (if `tests/` exists) |
| ty | `uv run ty check src` | No (`continue-on-error`) until fleet clean |
| pip-audit | `uv run pip-audit` | No (`continue-on-error`) until fleet clean |
| TS typecheck | `npm run check` | Yes (if frontend exists) |
| Biome | `npm run biome:ci` | Yes (if frontend exists) |
| Playwright | `npx playwright test` | Yes (if `playwright.config.*` exists) |

Template → `mcp-central-docs/templates/ci.yml.template`. Frontend detection: `webapp/` → `web_sota/` → `web-sota/`.

### 1.3. Manual / local (no hook)

```powershell
ruff check --fix .
ruff format .
```

### 1.4. **`ty`** (Astral type checker) — **non-blocking in CI by default**

- Add **`ty`** under **`[project.optional-dependencies] dev`** (or dev group), e.g. `ty>=0.0.24`.
- **CI:** run `uv run ty check src` (or project paths) in a step with **`continue-on-error: true`** until the codebase is clean — then remove `continue-on-error` and treat **`ty`** like Ruff.
- **Pre-commit:** optional local hook for `ty` once it is green; not required during the non-blocking phase.

**Reference:** [ty documentation](https://docs.astral.sh/ty/).

### 1.5. Recommended adjacent tooling (not duplicate linters)

The bar above is **Ruff + (eventually) `ty` + pytest**. These are **optional** layers that pay off on a **Python-heavy + Vite** fleet:

| Area | Tool | When to adopt |
|------|------|----------------|
| **Dependency CVEs** | **`pip-audit`** (or equivalent against your lockfile) | **Recommended** in CI: Ruff does not replace vulnerability scanning. |
| **HTTP-boundary tests** | **`respx`** or **`pytest-httpx`** | When MCP tools call **`httpx`** / external APIs: mock transport instead of hitting the network in unit tests. |
| **Web dashboard (Vite)** | **Biome** (`npm run lint` / `npm run format`) | **Mandatory** for repos with `webapp/`: ESLint+Prettier are retired. See [BIOME_STANDARDS.md](./BIOME_STANDARDS.md). |

Do **not** add container scanners (e.g. Trivy) by default unless the repo ships **images**.

### 1.6. Unicode safety (scripts - mandatory)

**EM DASH is never allowed anywhere in the fleet, any filetype** (broadened 2026-07-13 from the original script-only scope). See [patterns/unicode_safety.md](./patterns/unicode_safety.md).

```powershell
powershell.exe -NoProfile -File D:\Dev\repos\mcp-central-docs\scripts\check-unicode-safe.ps1 -RepoPath .
```

Recommended: local pre-commit hook (example in unicode_safety.md).

### 1.7. Style Requirements
- **Modern Types**: Use `dict` instead of `Dict`, `str | None` instead of `Optional[str]`.
- **Chained Exceptions**: Always use `raise ... from e`.
- **Unused Variables**: Prefix with `_` if intentional.

### 1.7. Windows Execution

On Windows systems where `ruff` is not on the global `PATH`, use the absolute path to the Python-managed executable:

- **Path**: `C:\Users\<user>\AppData\Local\Programs\Python\Python313\Scripts\ruff.exe`
- **Usage**: `& "C:\Users\<user>\AppData\Local\Programs\Python\Python313\Scripts\ruff.exe" check <path>`

## 2. TypeScript/JavaScript Standards (Biome)

**Biome** is the MANDATORY toolchain for linting and formatting in TypeScript-based MCP servers and webapps. It replaces ESLint + Prettier entirely. See [BIOME_STANDARDS.md](./BIOME_STANDARDS.md) for the full fleet standard including the canonical `biome.json`, migration notes, and the Ruff/Biome power couple rationale.

### 2.1. Configuration (`biome.json`)
See [BIOME_STANDARDS.md](./BIOME_STANDARDS.md) for mandated rules and configuration snippets.

### 2.2. Requirements
- **TypeScript**: Use for all new frontend/backend code.
- **Interfaces**: Define schemas for all API responses.
- **Accessibility**: ARIA labels and semantic HTML are mandatory.
- **React Hardening**: Use `useCallback` and Stable References for all effect dependencies. See [React Hardening Standards](./REACT_HARDENING.md).

## 3. Maintenance

Zero-tolerance for dead code. If it's not used, it must be removed. If it's complex and misunderstood, request clarification rather than modification.

## 4. Summary bar

| Layer | Tool | Blocking? |
|-------|------|-----------|
| Python lint + format | **Ruff** | Yes (local + CI + **pre-commit**) |
| Python types | **`ty`** | **No** in CI until clean, then yes |
| Dependency CVEs | **`pip-audit`** (or lockfile-aware audit) | Recommended in CI |
| HTTP tests (httpx) | **`respx`** / **pytest-httpx** | When tools call external HTTP |
| TS/JS lint + format | **Biome** | Yes (local **pre-commit** + CI) |
| LLM docs | **`llms.txt`** + **`llms-full.txt`** (both required) | N/A |

**Last updated:** 2026-07-28
