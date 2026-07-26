# AutoHotkey Syntax: v1 vs v2

## Quick Reference Table

| Feature | v1 (legacy) | v2 (current) |
|---------|-------------|--------------|
| Assignment | `var = value` | `var := value` |
| Number comparison | `if var > 5` | `if (var > 5)` |
| String comparison | `if var = hello` | `if (var = "hello")` |
| Function call | `MsgBox, Hello` | `MsgBox("Hello")` |
| Object creation | `obj := Object()` | `obj := Map()`, `obj := {}` |
| GUI | `Gui, Add, Text,, Hello` | `gui.Add("Text", , "Hello")` |
| Array | `arr%i%` (pseudo) | `arr[i]` (real) |
| Error handling | `ErrorLevel` | `try/catch as e` |
| Output params | `StringSplit, Out, In, ","` | `out := StrSplit(In, ",")` |
| Random | `Random, var, 1, 10` | `var := Random(1, 10)` |
| Loop files | `Loop, Files, *.txt` | `Loop Files "*.txt"` |
| Include | `#Include file.ahk` | `#Include file.ahk` (same) |
| Hotkey | `a::` | `Hotkey("a", Callback)` or `a::` |
| Class | — | `class MyClass {}` |
| Ternary | `var := var ? 1 : 0` | `var := var ? 1 : 0` (same) |
| String concat | `"hello " . var` | `"hello " . var` or `"hello " var` |

## Detailed Comparison

### Variables and Assignment

```autohotkey
; === v1 ===
MyVar = Hello          ; global by default (unless declared local)
Global MyVar := 0       ; explicit global
Local x = 5             ; local
StringSplit, Parts, InputString, `,
Array%Index% := Value

; === v2 ===
MyVar := "Hello"        ; local in function, global at top-level
global MyVar := 0        ; explicit global
local x := 5             ; explicit local
Parts := StrSplit(InputString, ",")
Array[Index] := Value
```

### Control Flow

```autohotkey
; === v1 ===
If var > 5
    MsgBox, Greater
Else If var = 3
    MsgBox, Three
Else
    MsgBox, Other

; === v2 ===
if (var > 5)
    MsgBox("Greater")
else if (var = 3)
    MsgBox("Three")
else
    MsgBox("Other")
```

### Loops

```autohotkey
; === v1 ===
Loop, 5
    MsgBox, % A_Index

Loop, Files, *.txt, R
    MsgBox, % A_LoopFileName

For key, value in Object
    MsgBox, %key% = %value%

; === v2 ===
Loop 5
    MsgBox(A_Index)

Loop Files "*.txt", "R"
    MsgBox(A_LoopFileName)

for key, value in MyMap
    MsgBox(key " = " value)
```

### Functions

```autohotkey
; === v1 ===
MyFunction(param1, param2) {
    global SharedVar
    local temp
    temp := param1 + param2
    Return temp
}

; === v2 ===
MyFunction(param1, param2) {
    ; Variables are local by default
    temp := param1 + param2
    return temp
}
```

### Objects and Classes

```autohotkey
; === v1 (no native classes) ===
obj := {}
obj.key := "value"

; === v2 ===
class Counter {
    static count := 0
    
    __New() {
        this.count := 0
    }
    
    Increment() {
        this.count++
        return this.count
    }
    
    static Reset() {
        this.count := 0
    }
}

c := Counter()
c.Increment()
Counter.Reset()
```

### Error Handling

```autohotkey
; === v1 ===
FileRead, content, C:\file.txt
if ErrorLevel {
    MsgBox, 16, Error, Failed to read file
}

; === v2 ===
try {
    content := FileRead("C:\file.txt")
} catch as e {
    MsgBox("Failed: " . e.Message, "Error", "Iconx")
}
```

### GUI

```autohotkey
; === v1 ===
Gui, New, +Resize +MinSize400x300, MyWindow
Gui, Add, Text, x10 y10 w200, Enter name:
Gui, Add, Edit, x10 y30 w200 vName
Gui, Add, Button, x10 y60 w100 gSubmit, OK
Gui, Show

Submit:
Gui, Submit, NoHide
MsgBox, Hello, %Name%

; === v2 ===
myGui := Gui("+Resize +MinSize400x300", "MyWindow")
myGui.Add("Text", "x10 y10 w200", "Enter name:")
nameEdit := myGui.Add("Edit", "x10 y30 w200")
submitBtn := myGui.Add("Button", "x10 y60 w100", "OK")
submitBtn.OnEvent("Click", (*) => ProcessSubmit(nameEdit.Value))
myGui.Show()

ProcessSubmit(name) {
    MsgBox("Hello " . name)
}
```

### Hotkeys

```autohotkey
; === v1 ===
^!p::
    MsgBox, Ctrl+Alt+P pressed
Return

; === v2 ===
Hotkey("^!p", (*) => MsgBox("Ctrl+Alt+P pressed"))
; OR label-style (still valid in v2):
^!p::MsgBox("Ctrl+Alt+P pressed")
```

## Prohibited v1 Patterns (Fleet Standard)

These v1 patterns cause runtime errors or silent failures in v2:

| Pattern | Problem |
|---------|---------|
| `%var%` dereferencing | Should be `var` directly |
| `StringSplit` | Use `StrSplit()` |
| `StringReplace` | Use `StrReplace()` |
| `Random, var, min, max` | Use `var := Random(min, max)` |
| `FormatTime, var` | Use `var := FormatTime()` |
| `Gui, New` | Use `Gui()` constructor |
| `GuiControl, , ctrl, value` | Use `ctrl.Value := value` or `ctrl.Text := value` |
| `IfEqual, a, b` | Use `if (a = b)` |
| `Gosub`/`Goto` | Use functions |
| `#Persistent` | Implicit in v2 |
| `Menu, Tray` | Use `A_TrayMenu` |
| `SetTimer, Label` | Use `SetTimer(Func)` with function reference |
| `OnExit, Label` | Use `OnExit(Func)` with function reference |
