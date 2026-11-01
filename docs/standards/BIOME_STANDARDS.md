---
title: "Biome Code Quality Standard (v14.1 — June 2026 SOTA)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-08-02
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Biome Code Quality Standard (v14.1 — June 2026 SOTA)

**Standardization for Industrial-Grade MCP TypeScript/JavaScript Repositories**

## Version Floor & Known Pitfall (2026-08-01)

- **Version floor: Biome 2.x.** The fleet mandates `"@biomejs/biome": "^2.0.0"` as a webapp devDependency (§ Pre-commit hook), and canonical configs may use the `files.includes` key (Biome 2.x schema, e.g. `webapp/biome.json` in aiwatcher-mcp).
- **PITFALL — global Biome 1.9.x silently drops the config:** the globally installed `C:\Users\<user>\.local\bin\biome.exe` is **1.9.4** and **cannot parse the `files.includes` key** introduced in 2.x. Running `biome check` with such a config emits a `deserialize` error ("Found an unknown key `includes`"), the config is not applied, and results differ from CI (which uses the repo devDependency 2.x). Symptom: local `biome check` reports different error counts than `npm run biome:ci`.
- **Fix:** upgrade the global binary — `npm i -g @biomejs/biome` (verify `biome --version` ≥ 2.x). Until then, prefer running biome via the repo's devDependency (`npx biome` from the webapp dir) for results that match CI.

## Configuration Philosophy

To achieve "Ruff-speed" execution in the TypeScript ecosystem, all TS/JS repositories in the MCP fleet must align with the **Biome** toolchain. Biome replaces the fragmented ESLint/Prettier ecosystem with a high-performance Rust binary, ensuring sub-millisecond linting and formatting.

## Mandated `biome.json` Specification

All repositories with a `webapp/` or TS-native `src/` must include a `biome.json` at the root:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "style": {
        "noNonNullAssertion": "warn",
        "useImportType": "error"
      },
      "suspicious": {
        "noExplicitAny": "warn",
        "noConsoleLog": "off"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "trailingCommas": "all"
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "semicolons": "always",
      "arrowParentheses": "always"
    }
  }
}
```

## Implementation Recipes (`justfile`)

Consistent with [RUFF_STANDARDS](./RUFF_STANDARDS.md), Justfiles must implement the standard `lint` and `fix` recipes:

```bash
# Static analysis and style check (Biome)
lint:
    npm run lint

# Automated repair and formatting (Biome)
fix:
    npm run format
```

## Integration Goals

1. **Zero-Error State**: The `lint` recipe must return exit code 0 in CI.
2. **Deterministic Formatting**: All files must pass `biome format --check`.
3. **Speed**: Linter execution for a standard MCP node should not exceed 500ms.

## Pre-commit hook (mandatory when `webapp/` or `web_sota/` exists)

Repos with a Vite dashboard MUST wire **Biome** into **pre-commit** alongside Ruff — same bar as CI (`npm run biome:ci`).

1. Copy `mcp-central-docs/templates/pre-commit-biome.ps1` → `{repo}/scripts/pre-commit-biome.ps1`
2. Add the **`biome-web` local hook** from `mcp-central-docs/templates/pre-commit-config.yaml.template`
3. Ensure `webapp/package.json` (or `web_sota/package.json`) defines:
   - `"biome:ci": "biome check src"`
   - `"biome:fix": "biome check --write src"`
   - devDependency `"@biomejs/biome": "^2.0.0"`
4. `just bootstrap` runs `npm ci` in the web root so the hook can execute offline

The hook runs only when staged files match `webapp/` or `web_sota/` — Python-only commits stay fast.

See also [CODE_QUALITY_STANDARDS.md](./CODE_QUALITY_STANDARDS.md) §1.2 and [github-workflows.md](../operations/github-workflows.md).

## The Ruff/Biome Power Couple

The fleet standard is **Ruff for Python, Biome for TypeScript/JavaScript** — a matched pair of Rust-native, single-binary linters/formatters that replace entire legacy toolchains:

| Layer | Tool | Replaces |
|-------|------|----------|
| Python | Ruff | flake8 + isort + black + pyupgrade |
| TS/JS | Biome | ESLint + Prettier + import sorters |

Both share the same philosophy: fast, opinionated, zero plugin ecosystem to manage. The combined investment for a full fleet migration is a one-time cost; ongoing maintenance is negligible. See [RUFF_STANDARDS](./RUFF_STANDARDS.md) for the Python counterpart.

## Migration Notes (Fleet Experience, April 2026)

**The webapp-won't-start failure mode** is the most common migration surprise. Biome enforces rules that ESLint either missed or had disabled by default, surfacing real errors that had been silently accumulating. This is a good thing — treat it as free debt discovery, not breakage.

Common culprits on first migration:
- `useImportType` requires explicit `import type` for type-only imports (TS)
- `noNonNullAssertion` flags `!` operators that should be null-checked properly
- Import organisation rewrites can trigger HMR/Vite quirks on first run

**Mitigation pattern**: commit a clean state before running Biome fleet-wide in an agentic session. Any agent running Biome migrations should operate on one repo at a time with an explicit confirmation step between repos.

## Fleet Config Consistency

All repos must derive from the canonical `biome.json` in this document. Do not let per-repo configs drift — agents that auto-generate `biome.json` will produce subtly different rule sets. Recommended pattern: maintain the canonical config here, and include a note in the repo README pointing to this standard.

If a repo requires a rule override (e.g. a legacy codebase where `noExplicitAny` would produce hundreds of warnings), document the override inline in `biome.json` with a comment explaining the exception and a target date for remediation.

## Tone and Style
Documentation for these standards must remain **industrial, measured, and empirical**.
