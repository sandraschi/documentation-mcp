# Fleet AHK v2 Linter

**Location:** `autohotkey-test/utils/linter_headless.ahk`  
**Status:** ✅ Production — used daily, 80+ scripts at zero errors

## Features

- 33+ AutoHotkey v2 compliance checks
- `--fix` mode for automatic v1→v2 mechanical fixes (with `.bak` backup)
- Known built-in variables/functions list — suppresses false positives
- Batch mode: scans all `.ahk` files, produces per-file report
- Exit code: 0 = clean, 1 = issues found

## Usage

```powershell
# From autohotkey-test/
just lint-ahk           # Lint all 80+ scriptlets
just lint-fix           # Auto-fix v1→v2 issues
just lint-one scriptlet # Lint single file

# Direct:
AutoHotkey64.exe utils/linter_headless.ahk path\to\script.ahk
AutoHotkey64.exe utils/linter_headless.ahk path\to\script.ahk --fix
```

## What It Catches

| Category | Checks | Example |
|----------|--------|---------|
| **v1→v2 syntax** | `Random(&var)`, `FormatTime`, `StringSplit`, `FileRead`, `Loop Files`, `SetTimer label` | `Random(&var)` → `var := Random()` |
| **Missing directives** | `#Requires`, `#SingleInstance` | Script without `#Requires AutoHotkey v2.0+` |
| **Runtime issues** | Unassigned variables, global shadowing | Local var with same name as global |
| **Error handling** | Missing `try/catch`, `OnError` | Uncaught exceptions |
| **GUI patterns** | v1 `Gui, New` → v2 `Gui()`, `GuiControl` → `.Value` | Legacy command-style GUI calls |

## False Positive Suppression

The linter maintains a list of known AHK v2 built-in variables and functions. This suppresses false warnings for:

- `A_` built-ins: `A_PID`, `A_Index`, `A_LoopField`, `A_Gui`, `A_Cursor`, `A_ProcessName`, etc.
- Built-in classes: `JSON`, `Map`, `Array`, `Error`, etc.
- Common functions: `TrayTip`, `InputBox`, `MsgBox`, `StrUpper`, `StrSplit`, etc.

To add a new entry, edit the `v2BuiltInFunctions` list in `linter_headless.ahk`.

## Publishing

The linter is currently bundled inside `autohotkey-test`. To publish as a standalone tool:

1. Extract `linter_headless.ahk` + `ScriptletErrorHandler.ahk` into a standalone repo
2. Add `--batch` mode for directory scanning
3. Package as MCPB for Claude Desktop
4. Add GitHub Actions for CI on pull requests
