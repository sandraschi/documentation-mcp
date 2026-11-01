---
title: "The Five Quality Gates — ruff, biome, pyright, tsc, pytest"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-08-01
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# The Five Quality Gates — ruff, biome, pyright, tsc, pytest

**Established**: 2026-08-01
**Scope**: What each tool catches, how they relate, and why you need all five.
**Related**: [VERIFICATION_STANDARDS.md](./VERIFICATION_STANDARDS.md) §3.4 (commands) · [CODE_QUALITY_STANDARDS.md](./CODE_QUALITY_STANDARDS.md) · [BIOME_STANDARDS.md](./BIOME_STANDARDS.md)

---

## 1. The One-Paragraph Answer

Five tools, three kinds of analysis. **ruff** and **biome** are style and
hygiene checkers (they look at the text). **pyright** and **tsc** are type
checkers (they look at the type graph — one per language). **pytest** is a
test runner (it executes the code). They are complementary, not alternatives —
each finds bugs the others cannot see.

| Tool | Language | Kind | Runs the code? | Catches |
|------|----------|------|----------------|---------|
| **ruff** | Python | Linter + formatter | No | Style, unused imports, syntax errors, import ordering |
| **biome** | JS/TS | Linter + formatter | No | Same for JavaScript/TypeScript (replaces ESLint + Prettier) |
| **pyright** | Python | Type checker | No | Type mismatches, `None` access, wrong args, bad imports |
| **tsc --noEmit** | JS/TS | Type checker | No | Type mismatches, wrong args, bad imports in TS/React |
| **pytest** | Python | Test runner | **Yes** | Behavioral bugs — wrong output, broken logic, regressions |

### 1.1 Three categories, five tools

Do not think "five kinds of analysis" — think **three categories**:

| Category | Python | JS/TS |
|----------|--------|-------|
| Style | ruff | biome |
| Types | pyright | tsc --noEmit |
| Behavior | pytest | (Vitest/Playwright for JS) |

pyright and tsc are the same category (types) applied per language — which is
why a repo with a webapp needs BOTH. Skipping tsc leaves TS type bugs that
ruff/biome cannot see; skipping pyright leaves Python type bugs that
ruff/pytest cannot see.

---

## 2. The Pipeline Analogy

```
source code
    │
    ▼
ruff / biome  →  "clean prose"       (style, structure, unused junk)
    │
    ▼
pyright / tsc →  "no contradictions" (types line up, nothing optional is None)
    │
    ▼
pytest        →  "behaves correctly" (executes and asserts real behavior)
```

Each stage is stricter than the last. You cannot reach a later stage with a
broken earlier one — or rather, you shouldn't, because the later stage's
failures will be confusingly noisy if the earlier stage was skipped.

---

## 3. What Each One Actually Sees

### 3.1 ruff (Python) / biome (JS/TS)

Think spellcheck + grammar. They do not need to understand what the code does:

- unused imports (`Div` imported but never used)
- unsorted import blocks
- line length, formatting drift
- syntax errors (malformed `def` etc.)

**Example from the field**: ruff caught `Div` imported but unused after a
refactor, and complained the import-sorting broke when `# pyright: ignore`
comments were appended to import lines.

### 3.2 pyright (Python types)

Think a proofreader who checks every claim against declared types. It builds
the full type graph, so it sees things ruff cannot:

- subscripting a possibly-`None` value (`job["status"]` when `job` is
  `dict | None`)
- passing the wrong type to a parameter (an `int` where `str` is declared)
- `proc.stdout` being `StreamReader | None`, not `StreamReader`
- dynamic-API mismatches (keyword args a stub doesn't declare)
- missing imports (a module that is not installed or not on the path)

**Example from the field**: pyright flagged `Row(label=..., value=...)` as
invalid because `prefab_ui.Row.__init__` accepts only `**kwargs`. Investigating
that surfaced a REAL runtime bug: `Div("text")` — `Div` is a container, text
belongs in `P()`, so the call crashed. pyright found a bug that would have
surfaced only when the Prefab card actually rendered.

### 3.3 tsc --noEmit (TypeScript types)

pyright's JS/TS sibling. Same category, different language. In a React/Vite
webapp it checks components, hooks, prop types, and API-client code — the
frontend half of the type gate:

- wrong prop types passed to a component
- `.map()` over a possibly-undefined array
- API response shapes that don't match the client interface
- unused imports flagged as errors (with `noUnusedLocals`)

**Example from the field**: tsc catches a `useState` typed as `string` being
assigned a number from a fetch, or a `data-testid` prop typo that biome's
style rules would never see.

### 3.4 pytest (execution)

The only one that actually runs the code. Catches what static analysis can
never see:

- a helper that calls itself recursively (type-valid, infinitely looping)
- wrong algorithm output, off-by-one pagination
- cascade deletes not firing (`PRAGMA foreign_keys` defaulting to OFF)
- regressions across refactors
- coverage measurement

**Example from the field**: after a batch `replaceAll` in a test file, pytest
immediately reported `RecursionError` — the helper `_job()` had been renamed
to call itself. pyright said nothing (the types were consistent); only
execution revealed the infinite loop.

---

## 4. Why All Five (not just two)

| Bug class | ruff/biome | pyright | tsc | pytest |
|-----------|:----------:|:-------:|:---:|:------:|
| Unused import, formatting | ✅ | — | — | — |
| `None` subscript, wrong arg type (Python) | — | ✅ | — | — |
| `undefined` access, wrong prop type (TS) | — | — | ✅ | — |
| Import typo / missing module | — | ✅ | ✅ | — |
| Logic error, wrong output | — | — | — | ✅ |
| Infinite recursion, deadlock | — | — | — | ✅ |
| Regression after refactor | — | — | — | ✅ |

The four static tools plus the dynamic one cover disjoint bug classes.
Skipping any one leaves a class of bug that reaches production:

- skip **ruff/biome** → messy diffs, unused imports, style drift (cheap, but
  pollutes every review)
- skip **pyright** → runtime `TypeError`s and `AttributeError`s in Python,
  plus silent dead exception handlers
- skip **tsc** → runtime type crashes in the React webapp that the backend
  gates never see
- skip **pytest** → logic bugs and regressions that no linter can dream of
  catching

---

## 5. Fleet Commands

| Tool | Command (repo root) | In CI? | Notes |
|------|---------------------|:------:|-------|
| ruff check | `uv run ruff check src/ tests/` | ✅ | `--fix` auto-fixes |
| ruff format | `uv run ruff format --check src/ tests/` | ✅ | `ruff format .` to apply |
| biome check | `cd web_sota && npx biome check src/` (or `biome ci .`) | ✅ | `biome check --write .` auto-fixes |
| pyright | `uv run pyright src/` (+ `api/` if present) | ✅ | CI scope: `src/` (+ `api/`). Local `just type-check` scans the whole repo including tests |
| tsc | `cd web_sota && npx tsc --noEmit` | ✅ | Runs from the webapp dir; gates the React/TS surface |
| pytest | `uv run pytest tests/` | ✅ | `--cov` for coverage (fleet floor: 30% suite, 80% unit per VERIFICATION_STANDARDS §3.6) |

The `just` recipes (`just check`, `just test`, `just type-check`) wrap these.

### 5.1 All five are CI gates

**All five must be green for CI to pass** — local and GitHub (see
[GITHUB_ACTIONS_NO_PRIVATE_CI.md](./GITHUB_ACTIONS_NO_PRIVATE_CI.md) mandatory
shape). ruff/biome for style, pyright + tsc for types (one per language),
pytest for behavior. A repo with a webapp needs BOTH type checkers: pyright
for `src/`, tsc for the webapp.

Pyright CI scope is deliberately `src/` (+ `api/`) — NOT `tests/`/`scripts/`/
`web_sota/` — because test files legitimately import optional deps (pywinauto,
PIL) and use `None`-assertions that aren't type-safe. The local `just
type-check` full-scan is stricter; fix everything it reports, but the CI step
stays scoped to keep the gate free of dep-noise. If your `tests/` are
pyright-clean, that's a bonus, not a requirement. tsc likewise runs only over
the webapp's `src/` (`tsc --noEmit` uses the project's `tsconfig.json`).

---

## 6. Interop Rules (learned the hard way)

1. **`# type: ignore` comments confuse ruff's import sorting.** Appending
   `# pyright: ignore[...]` to an import line can trigger ruff `I001`
   (un-sorted imports) because ruff wants multi-line form. Fix with
   `ruff check --fix`, or put the ignore where ruff won't reflow it.

2. **Optional dependencies need explicit ignores.** CUA smoke scripts import
   `pywinauto`, `pytesseract`, `PIL`, `pywinauto_mcp` — installed on demand,
   not in the project venv. Mark them
   `# pyright: ignore[reportMissingImports]` instead of installing heavy deps
   into every repo.

3. **pyright sees dynamic APIs as errors.** `Row(label=..., value=...)` on a
   `**kwargs` component looks invalid to pyright but works at runtime. Verify
   the runtime behavior first (`python -c "..."`), then suppress with a
   targeted `# type: ignore[reportCallIssue]` — never blanket-suppress a file.

4. **`PRAGMA foreign_keys = ON` is per-connection and defaults OFF in
   SQLite.** A test that relies on `ON DELETE CASCADE` must enable it on the
   write connection — the schema declares the FK but nothing fires without the
   pragma. pytest catches this; pyright cannot.

5. **Batch renames via replaceAll can silently rewrite helpers.** When using
   `replaceAll`, verify the helper you introduced wasn't caught in its own
   pattern (a helper calling itself is type-valid but infinitely recursive).
   pytest catches it instantly; pyright stays silent.

6. **Pre-existing gate failures are yours once you touch the repo.** If
   pyright reports 70 errors and 65 pre-date your change, fix all of them —
   a repo with a failing type gate cannot be verified. Scope: fix the error,
   not the architecture (`# pyright: ignore` for optional deps, real fixes
   for real bugs).

---

## 7. The Mental Model

> ruff/biome: "Would a careful reader stumble?" — style
> pyright/tsc: "Could this be a contradiction?" — types (per language)
> pytest: "Does it actually do the thing?" — behavior

All five must pass before a merge or build (`just check && just test && just
type-check`). The gates are cheap, fast, and disjoint. The cost of all five
running is minutes; the cost of shipping what one of them would have caught is
a production incident.
