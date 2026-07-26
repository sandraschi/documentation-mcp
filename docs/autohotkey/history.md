# AutoHotkey History

## Timeline

| Year | Event |
|------|-------|
| **2003** | Chris Mallett releases AutoHotkey v1.0. Inspired by AutoIt v2, designed to automate Windows GUI. |
| **2007** | AutoHotkey v1.0.48 — mature, stable. Scripts proliferate across forums. |
| **2009** | Chris Mallett steps away. Lexikos (Steve Gray) takes over development. |
| **2012** | AutoHotkey v1.1 (Lexikos fork) — major cleanup, bugfixes, Unicode support. |
| **2014** | AutoHotkey v2 alpha announced — breaking changes, object-oriented design, function-call syntax. |
| **2016** | v1.1.24 — last major v1 feature release. Development shifts to v2. |
| **2022-12** | AutoHotkey v2.0 stable released. v1 enters maintenance mode. |
| **2025** | v2.1 — continued improvements. v1 effectively EOL. |
| **2026** | Fleet standard: AHK v2 exclusively. v1 scripts migrated. |

## Why the Break (v1 → v2)

v1 grew organically over a decade. It had:

- **Two syntax systems** — command syntax (`MsgBox, Hello`) AND function syntax (`MsgBox("Hello")`) — both valid, causing confusion
- **Implicit output variables** — `StringSplit, OutputArray, input, ","` — the function name describes what it does, but the output goes to an unrelated variable
- **Legacy Win32 API patterns** — `Gui, Add, Button, x10 y10, OK` — command-style GUI that maps awkwardly to modern OOP
- **No structured types** — pseudo-arrays (`Array%i%`), no Map, no Error object
- **Inconsistent error handling** — some commands set `ErrorLevel`, others throw, most silently fail

v2 resolved these by:

- **One syntax** — functions only. `MsgBox("Hello")`, not `MsgBox, Hello`
- **Proper objects** — `Array`, `Map`, `Error`, `Buffer`, `Gui()` class, `Menu()` class
- **Output via return values** — `parts := StrSplit(input, ",")`, not `StringSplit, OutputArray, input, ","`
- **Structured error handling** — `try/catch` everywhere, `Error` object with `.Message`, `.Line`, `.Stack`
- **Consistent GUI** — `myGui := Gui()`, `myGui.Add("Button", "x10 y10", "OK")`

## Migration Stats (Fleet)

As of 2026-06, the fleet's `autohotkey-test` depot migrated 77 scripts from v1 to v2:

| Metric | v1 (2025) | v2 (2026) |
|--------|-----------|-----------|
| Scripts | 77 | 77 |
| Lint errors | 300+ | 0 |
| v1 syntax patterns | 200+ | 0 |
| Failed runtime | 38/75 (51%) | 0/80 (0%) |

## Key Architectural Changes

### Variables
```autohotkey
; v1
var = value         ; global by default
StringSplit, out, input, ","
arr%i% := "item"

; v2
var := "value"      ; local by default in functions
out := StrSplit(input, ",")
arr[i] := "item"
```

### GUI
```autohotkey
; v1
Gui, New, +Resize, MyWindow
Gui, Add, Text, x10 y10 w100, Hello
Gui, Show

; v2
myGui := Gui("+Resize", "MyWindow")
myGui.Add("Text", "x10 y10 w100", "Hello")
myGui.Show()
```

### Error handling
```autohotkey
; v1
FileRead, content, C:\file.txt
if ErrorLevel {
    MsgBox, Failed
}

; v2
try {
    content := FileRead("C:\file.txt")
} catch as e {
    MsgBox("Failed: " . e.Message)
}
```

## References

- Original AutoHotkey: [autohotkey.com](https://www.autohotkey.com/)
- v2 documentation: [lexikos.github.io/v2/docs](https://lexikos.github.io/v2/docs/)
- v1→v2 migration guide: [autohotkey.com/v2/v2-changes.htm](https://www.autohotkey.com/v2/v2-changes.htm)
- Community: [reddit.com/r/AutoHotkey](https://reddit.com/r/AutoHotkey)
- GitHub: [github.com/AutoHotkey/AutoHotkey](https://github.com/AutoHotkey/AutoHotkey)
