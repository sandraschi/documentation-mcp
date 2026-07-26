# Biome Code Quality Standard (v14.1 — June 2026 SOTA)

**Standardization for Industrial-Grade MCP TypeScript/JavaScript Repositories**

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
