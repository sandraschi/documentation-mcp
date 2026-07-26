# AutoHotkey v2 Standard (SOTA 2026)

**Established**: 2026-07-05

## Rule

All AutoHotkey scripts in the fleet MUST use AHK v2 syntax and conventions. AHK v1 syntax is prohibited in new and modified scripts.

## Why

AHK v1 is EOL. The v2 rewrite introduced cleaner syntax, proper scoping, structured error handling (`try`/`catch`), and object-oriented features (classes, Maps, fat-arrow functions). Mixing v1 and v2 conventions in the same codebase creates silent bugs (especially around `%` dereferencing, `Send` syntax, and global variable scoping).

## Key v2 Conventions

### Variables & Scope
- Auto-execute section (top level) runs in global scope. `global var := val` at the top level makes `var` a super-global readable from all functions without explicit `global` declaration.
- Inside functions, use `global varName` to write to a global variable. Reading a super-global (declared with `global` at top level) does not require `global` inside the function.
- **NEVER** use `%var%` for dereferencing. Use `var` directly.

### Function Calls
- Use function-call syntax: `WinExist("A")`, NOT command syntax `WinExist, A`.
- Function names are case-insensitive but use PascalCase by convention: `WinGetTitle()`, `ControlSend()`, `Gui()`.

### Output Variables
- Use `&VarRef` for output parameters: `WinGetTitle(&title, "ahk_id " hwnd)`.
- When a global variable is used as an output parameter, do NOT also declare it as `global` in the same function — the `&` creates a VarRef that conflicts. Use the return value instead: `title := WinGetTitle("ahk_id " hwnd)`.

### Strings & Concatenation
- String concatenation uses whitespace: `"ahk_id " hwnd` (NOT `"ahk_id " . hwnd`).
- Use `Format()` for complex strings: `Format("x{1} y{2}", x, y)`.
- Substrings: `SubStr(str, start, length)`.

### GUI
- `Gui("+AlwaysOnTop +ToolWindow", "Title")` — options in quotes, comma-separated title.
- Button controls: `Gui.Add("Button", "x10 y10 w80 h30", "Text")`.
- Event binding: `btn.OnEvent("Click", HandlerFunction)`.

### Hotkeys
- `Hotkey("^!s", MyFunc)` — string hotkey, reference to function (NOT quoted function name).
- Hotkey functions receive a single `*` parameter: `MyFunc(*) { ... }`.

### ControlSend
- `ControlSend(Keys, Control, WinTitle)` — `Control` can be omitted (empty).
- Example: `ControlSend("{PgUp}", , "ahk_id " hwnd)`.

### Loops & Iteration
- `for index, value in array` — NOT `for index, value in array {` on same line.
- Use `_` for unused loop variables: `for _, item in list`.

### Error Handling
- `OnError(LogFunc)` with signature `LogFunc(exception, mode)`.
- Use `try`/`catch` for operations that may fail.

### File Headers
Every scriptlet MUST include the AHK v2 header:
```
#Requires AutoHotkey v2.0+
#SingleInstance Force
```
Optionally `#Warn` for stricter validation.

### Prohibited v1 Patterns
- **NO** command syntax (`WinActivate, ahk_id %hwnd%`)
- **NO** `%` dereferencing (`%var%`)
- **NO** `Gosub`/`Goto`
- **NO** legacy `IfEqual`/`IfExist`/`IfInString` — use `if (expr)` instead
- **NO** `StringSplit`/`StringReplace` — use `StrSplit()`/`StrReplace()`
- **NO** pseudo-arrays (`Array%i%`) — use `Array[i]`
- **NO** `SendInput`/`SendPlay`/`SendEvent` — use `Send()` with mode parameter or `SendMode`

## Reference

- Full migration guide: `not-mcp-related/autohotkey/AutoHotkey_v2_Syntax_Migration_Guide.md`
- Cheat sheet: `not-mcp-related/autohotkey/AUTO_HOTKEY_V2_CHEAT_SHEET.md`
- Common incompatibilities: `not-mcp-related/autohotkey/AutoHotkey_v2_Common_Incompatibilities.md`
