# Code Quality & Formatting

## 1. Python Standards (Ruff)

Ruff is MANDATORY for all Python-based MCP servers.

### 1.1. Configuration (`pyproject.toml`)
- `line-length = 100`
- `target-version = "py311"`
- `select = ["E", "W", "F", "I", "B", "UP"]`

### 1.2. Pre-commit hook (recommended)

Use **[pre-commit](https://pre-commit.com/)** so Ruff runs on **commit**, not only in CI.

**`.pre-commit-config.yaml`** (pin `rev` to a current [ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit) tag):

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

**Setup:** `pip install pre-commit` or `uv tool install pre-commit`, then `pre-commit install` in the repo root.

**CI:** Either run `pre-commit run --all-files` or keep explicit `ruff check` / `ruff format --check` — both align with the same rules.

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

**EM DASH is never allowed** in fleet script files (`start.ps1`, `justfile`, `src/`, `webapp/`, etc.). See [patterns/unicode_safety.md](./patterns/unicode_safety.md).

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

- **Path**: `C:\Users\sandr\AppData\Local\Programs\Python\Python313\Scripts\ruff.exe`
- **Usage**: `& "C:\Users\sandr\AppData\Local\Programs\Python\Python313\Scripts\ruff.exe" check <path>`

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
| TS/JS lint + format | **Biome** | Yes — ESLint+Prettier retired (SOTA 14.1+) |
| LLM docs | **`llms.txt`** + **`llms-full.txt`** (both required) | N/A |

**Last updated:** 2026-04-15
