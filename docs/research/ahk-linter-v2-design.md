# AHK Linter v2 — Design

## Decision: Standalone Repo

**Yes**, separate repo at `github.com/sandraschi/ahk-linter`.

Reasons:
- Independent installation (no need to clone the 80-script depot)
- CI with GitHub Actions
- GitHub Releases for versioned downloads
- Citeable in a paper
- The linter is the asset, the scriptlet depot is just its test suite

## Repo Layout

```
ahk-linter/
├── ahk_lint.py              # Main CLI (Python — robust parsing)
├── ahk_lint.ahk             # Fallback AHK runner (for self-hosted checks)
├── pyproject.toml           # Dependencies: lark-parser, click, json
├── grammar.lark             # Lark grammar for AHK v2
├── checks/                  # Check modules
│   ├── __init__.py
│   ├── v1_syntax.py         # 15 v1→v2 pattern checks
│   ├── style.py             # Naming, spacing, conventions
│   ├── safety.py            # Error handling, uninitialized vars
│   └── dead_code.py         # Unused variables, unreachable code
├── fixers/                  # Auto-fix generators
│   ├── __init__.py
│   └── v1_to_v2.py          # Mechanical v1→v2 transformations
├── config.py                # .ahklintrc loader (TOML)
├── reporter.py              # Output formatters (terminal, SARIF, JSON)
├── tests/
│   ├── fixtures/            # Test .ahk files (known-good, known-bad)
│   └── test_checks.py
├── .ahklintrc.example       # Example config
├── README.md
└── justfile
```

## Architecture

```
Source .ahk file
    │
    ▼
  Lexer + Parser (Lark grammar)
    │
    ▼
  AST (concrete + abstract)
    │
    ├──▶ V1 syntax checks    ──▶ Fix suggestions
    ├──▶ Style checks         ──▶ Warnings
    ├──▶ Safety checks        ──▶ Errors
    └──▶ Dead code analysis   ──▶ Warnings
    │
    ▼
  Reporter
    ├── Terminal (color, grouped by file)
    ├── SARIF (GitHub annotations)
    └── JSON (machine-readable)
```

## Key Design Decisions

### 1. Python-based, not AHK-based

| | AHK | Python |
|--|-----|--------|
| Parsing | Regex-only, fragile | Lark PEG parser — full grammar |
| Performance | Single-threaded, slow on 80+ files | Fast, parallel |
| Portability | Windows-only | Cross-platform |
| Ecosystem | No parser libraries | Lark, tree-sitter, pyparsing |

The AHK fallback runner (`ahk_lint.ahk`) still exists for when you want to lint without Python installed — it uses the current regex approach from v1. But the main linter is Python.

### 2. Lark PEG Grammar

A proper grammar in `grammar.lark`:

```lark
start: (statement | function_def | class_def)*

statement: assignment | if_stmt | loop_stmt | try_stmt | expression

assignment: variable ":=" expression -> assign_var
          | variable "." identifier ":=" expression -> assign_prop

function_def: "static"? identifier "(" param_list ")" block
class_def: "class" identifier ("extends" identifier)? "{" class_member* "}"
```

This enables:
- Scope tracking (local vs global vs static)
- Variable type inference
- Dead code detection
- Accurate expression boundaries

### 3. Config File: `.ahklintrc`

```toml
[checks]
v1_syntax = "error"
style = "warning"
safety = "error"
dead_code = "warning"

[suppressions]
"tests/" = ["style"]
"legacy/" = "all"

[fix]
enabled = true
backup = true
```

### 4. Per-Line Suppression

```autohotkey
; @ahk-lint-disable-next-line W001
Random, var, 1, 10  ; intentional v1 compat

; @ahk-lint-ignore W033: Known false positive with JSON library
JSON.Load(text)
```

### 5. SARIF Output

SARIF (Static Analysis Results Interchange Format) is the standard for GitHub code scanning:

```json
{
  "version": "2.1.0",
  "runs": [{
    "tool": { "name": "ahk-lint", "version": "2.0.0" },
    "results": [{
      "ruleId": "W001",
      "level": "error",
      "message": { "text": "Use var := Random(min, max) instead of Random, var" },
      "locations": [{
        "physicalLocation": {
          "artifactLocation": { "uri": "script.ahk" },
          "region": { "startLine": 42, "startColumn": 1 }
        }
      }]
    }]
  }]
}
```

## Check Categories (v2)

| ID | Check | Severity | Auto-fix | Description |
|----|-------|----------|----------|-------------|
| W001 | V1_Random | error | ✅ | `Random, var` → `var := Random()` |
| W002 | V1_StringSplit | error | ✅ | `StringSplit` → `StrSplit()` |
| W003 | V1_GuiCommand | error | ✅ | `Gui, Add` → `gui.Add()` |
| W004 | V1_IfEquals | error | ✅ | `IfEqual` → `if ( = )` |
| W005 | V1_FileRead | error | ✅ | `FileRead, var` → `var := FileRead()` |
| W006 | V1_FormatTime | error | ✅ | `FormatTime, var` → `var := FormatTime()` |
| W007 | V1_Gosub | warning | ❌ | `Gosub` → function call |
| W008 | V1_PercentDeref | error | ✅ | `%var%` → `var` |
| W009 | V1_MenuTray | error | ✅ | `Menu, Tray` → `A_TrayMenu` |
| W010 | V1_SetTimerLabel | warning | ✅ | `SetTimer, Label` → `SetTimer(Func)` |
| S001 | UnusedVariable | warning | ❌ | Variable assigned but never read |
| S002 | UnreachableCode | warning | ❌ | Code after return/throw |
| S003 | MissingErrorHandling | suggestion | ❌ | Function without try/catch for I/O |
| S004 | GlobalShadow | warning | ❌ | Local var shadows global |
| S005 | MissingDirectives | warning | ✅ | Missing `#Requires` or `#SingleInstance` |
| S006 | MixedCase | suggestion | ❌ | Inconsistent naming convention |

## CLI

```powershell
ahk-lint script.ahk                          # Lint single file
ahk-lint .\scriptlets\                        # Lint directory
ahk-lint . --fix                              # Auto-fix
ahk-lint . --format sarif > results.sarif     # SARIF output
ahk-lint . --config .ahklintrc                # Custom config
```

## Migration from v1 (current regex linter)

The v1 linter (`autohotkey-test/utils/linter_headless.ahk`) stays in place for self-hosted AHK-only linting. The v2 Python linter is the primary tool.

All 33 current checks map to the new system. The pass rate on the fleet's 80+ scripts must remain 100%.

## Development Phases

| Phase | Features | Effort |
|-------|----------|--------|
| **1** | Lark grammar (AHK v2 subset) + basic parsing | 2 days |
| **2** | 10 v1→v2 checks with auto-fix | 2 days |
| **3** | Config file + per-line suppression | 1 day |
| **4** | Safety checks (unused vars, globals, directives) | 1 day |
| **5** | SARIF + JSON output, CI | 1 day |
| **6** | Polish, README, paper draft | 2 days |

**Total:** ~9 days to a publishable v2.

## Status

✅ **Implemented** — see [github.com/sandraschi/ahk-linter](https://github.com/sandraschi/ahk-linter).
Phases 1-5 complete: Lark grammar, 10 v1→v2 checks with auto-fix, config file, per-line suppression, safety checks, SARIF/JSON output. Remaining: phase 6 (polish, paper draft).
