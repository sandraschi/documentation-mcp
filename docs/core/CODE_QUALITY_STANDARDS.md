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

The bar above is **Ruff + (eventually) `ty` + pytest**. These are **optional** layers that pay off on a **Python-heavy + Vite** fleet without turning central docs into a stale “popular repos” list:

| Area | Tool | When to adopt |
|------|------|----------------|
| **Dependency CVEs** | **`pip-audit`** (or equivalent against your lockfile) | **Recommended** in CI: Ruff does not replace vulnerability scanning. |
| **HTTP-boundary tests** | **`respx`** or **`pytest-httpx`** | When MCP tools call **`httpx`** / external APIs: mock transport instead of hitting the network in unit tests. |
| **Web dashboard (Vite)** | **`npm run check`** using **Biome** *or* ESLint + Prettier | **Recommended** for repos with `webapp/`: one blocking CI script mirrors “Ruff for Python.” |

Do **not** add container scanners (e.g. Trivy) by default unless the repo ships **images**—see fleet guidance in conversations, not star counts.

### 1.6. Style Requirements
- **Modern Types**: Use `dict` instead of `Dict`, `str | None` instead of `Optional[str]`.
- **Chained Exceptions**: Always use `raise ... from e`.
- **Unused Variables**: Prefix with `_` if intentional.

### 1.7. Windows Execution

On Windows systems where `ruff` is not on the global `PATH`, use the absolute path to the Python-managed executable:

- **Path**: `C:\Users\sandr\AppData\Local\Programs\Python\Python313\Scripts\ruff.exe`
- **Usage**: `& "C:\Users\sandr\AppData\Local\Programs\Python\Python313\Scripts\ruff.exe" check <path>`

## 2. TypeScript/JavaScript Standards

- **TypeScript**: Use for all new frontend/backend code.
- **Interfaces**: Define schemas for all API responses.
- **Accessibility**: ARIA labels and semantic HTML are mandatory.
- **React Hardening**: Use `useCallback` and Stable References for all effect dependencies. See [React Hardening Standards](./REACT_HARDENING.md).

## 3. Maintenance

Zero-tolerance for dead code. If it's not used, it must be removed. If it's complex and misunderstood, request clarification rather than modification.

## 4. Summary bar (Python MCP)

| Layer | Tool | Blocking? |
|-------|------|-----------|
| Lint + format | **Ruff** | Yes (local + CI + **pre-commit**) |
| Types | **`ty`** | **No** in CI until clean, then yes |
| Dependency CVEs | **`pip-audit`** (or lockfile-aware audit) | Recommended in CI |
| HTTP tests (httpx) | **`respx`** / **pytest-httpx** | When tools call external HTTP |
| Vite / TS | **Biome** or ESLint+Prettier via **`npm run check`** | Recommended for `webapp/` repos |
| LLM docs | **`llms.txt`** + **`llms-full.txt`** (both required) | N/A |
