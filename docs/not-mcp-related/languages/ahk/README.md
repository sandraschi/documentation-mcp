# AutoHotkey (AHK) for MCP Automation: The SOTA 2026 Standard

**Version**: 2.0+ (Mandatory)
**Context**: The "Nervous System" of Windows Automation
**Architecture**: Trigger & Delegate Pattern
**Integration**: Direct `mcp-cli` calls via `RunWait`
**Linting**: AHK v2 Language Support (VS Code)

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for AutoHotkey usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity AHK Standard](#the-antigravity-ahk-standard)
    *   [The Trigger & Delegate Pattern](#the-trigger--delegate-pattern)
    *   [Why AHK v2?](#why-ahk-v2)
    *   [JSON Handling in 2026](#json-handling-in-2026)
3.  [Global Context: AutoHotkey's Evolution](#global-context-autohotkeys-evolution)
    *   [History & Philosophy](#history--philosophy)
    *   [Features & Capabilities](#features--capabilities)
    *   [The v1 to v2 Transition](#the-v1-to-v2-transition)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [Calling MCP Tools](#calling-mcp-tools)
    *   [Handling Responses](#handling-responses)
    *   [The `mcp-cli` Wrapper](#the-mcp-cli-wrapper)
5.  [Advanced Patterns](#advanced-patterns)
    *   [Direct DllCall Integration](#direct-dllcall-integration)
    *   [COM Automation](#com-automation)
    *   [WebView2 GUIs](#webview2-guis)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, AutoHotkey plays a specific, critical role: **The Nervous System**.

While Python (via `windows-computer-use-mcp`) is the "Brain" that processes complex logic, Computer Vision, and AI reasoning, AutoHotkey is the "Reflex Arc". It sits at the very edge of the OS, intercepting user intent (keystrokes, mouse movements) with sub-millisecond latency.

**The Golden Rule of SOTA 2026 AHK:**
> *AutoHotkey should NEVER perform complex business logic. Its sole purpose is to detect intent and delegate execution to an MCP server.*

**Why AHK?**
-   **Latency**: Global system hooks in AHK are faster and more reliable than Python's `keyboard` or `mouse` libraries.
-   **Native UI**: Creating a simple input overlay (GUI) in AHK takes 3 lines of code. In Python (Qt/Tkinter), it takes 50.
-   **Stability**: The AHK runtime is a single, self-contained executable that rarely crashes.

---

## 2. The Antigravity AHK Standard

### The Trigger & Delegate Pattern

This is the fundamental architectural pattern for all AHK scripts in the fleet.

**1. Trigger**: AHK detects a Hotkey (`#c` for Win+C).
**2. Acknowledge**: AHK provides immediate visual feedback (Tooltip/sound).
**3. Delegate**: AHK calls `mcp-cli` to execute a tool on `windows-computer-use-mcp`.
**4. Feedback**: AHK displays the result via a Toast notification.

#### Code Example (SOTA 2026)

```autohotkey
; scripts/trigger_ocr.ahk
#Requires AutoHotkey v2.0
#SingleInstance Force

; Win+Shift+S: Capture Screen & OCR
#+s::
{
    ; 1. Trigger & Acknowledge
    Tooltip "📸 Capturing Screen..."
    SetSystemCursor("Wait")

    try {
        ; 2. Delegate to MCP
        ; We use 'RunWait' to block until the MCP tool returns
        ; The output is captured via stdout
        RunWait('mcp-cli call pywinauto automation_visual "{\"action\": \"ocr_screen\"}"', , "Hide")
        
        ; 3. Feedback
        TrayTip "OCR Complete", "Text copied to clipboard", "Mute"
    } catch as err {
        MsgBox "MCP Call Failed: " err.Message
    } finally {
        Tooltip
        SetSystemCursor("Arrow")
    }
}
```

### Why AHK v2?

We strictly mandate **AutoHotkey v2**.
-   **Syntax**: v2 uses true expressions and objects, eliminating the `command, param, %variable%` confusion of v1.
-   **Scoping**: Proper function scopes prevent global variable pollution.
-   **Error Handling**: v2 throws exceptions instead of setting `ErrorLevel`, allowing for `try/catch` blocks.

**Banned Legacy Syntax (v1):**
```autohotkey
; DO NOT USE THIS
MsgBox, Hello World
If Equal, var, value
```

**Required Modern Syntax (v2):**
```autohotkey
; USE THIS
MsgBox("Hello World")
if (var == "value")
```

### JSON Handling in 2026

Since MCP communicates via JSON, AHK must parse it. We use `cJson.ahk` (a machine-code compiled library) for high-performance JSON parsing.

```autohotkey
#Include <JSON>

response_str := '{"status": "success", "text": "Hello"}'
data := JSON.Load(response_str)
MsgBox data["text"]
```

---

## 3. Global Context: AutoHotkey's Evolution

*(Ingested from Wikipedia Research)*

### History & Philosophy

AutoHotkey (AHK) is a free and open-source custom scripting language for Microsoft Windows, initially aimed at providing easy keyboard shortcuts or hotkeys, fast macro-creation and software automation that allows users to automate repetitive tasks in any Windows application. It was originally a fork of AutoIt but evolved into a full-fledged language.

-   **Origins (2003)**: Created by Chris Mallett as a fork of AutoIt v2 to add hotkey support, which AutoIt v3 had dropped.
-   **The "IronAHK" Era**: Various attempts to cross-compile AHK to .NET/Mono failed, cementing it as a Windows-exclusive tool.
-   **AHK_L**: A major fork that added objects, classes, and Unicode support, eventually becoming the official v1.1.
-   **v2.0 (2023)**: The stable release of v2, breaking backward compatibility to clean up the syntax. This aligns perfectly with the **Antigravity SOTA 2026** initiative.

### Features & Capabilities

1.  **Remapping**: Remap keys (e.g., make CapsLock act as a specialized modifier).
2.  **Hotstrings**: Auto-replace text as you type (e.g., typing "btw" -> "by the way").
3.  **GUI Creation**: Create complex user interfaces with input fields, list views, and buttons.
4.  **System Hooks**: Low-level keyboard (`WH_KEYBOARD_LL`) and mouse hooks without needing C++.
5.  **dllCall**: Direct access to the Windows API (User32, Kernel32, GDI32).

### The v1 to v2 Transition

The transition from v1 to v2 was controversial but necessary.
-   **v1**: Command-syntax (literate) vs Expression-syntax mix. Confusing for developers.
-   **v2**: Pure expression syntax. Functions call functions. Strings are quoted.
    -   *Result*: AHK v2 feels like JavaScript or Python, making it acceptable for professional engineering.

---

## 4. Fleet Integration Patterns

### Calling MCP Tools

AHK does not have a native MCP SDK. We use the **CLI Bridge**.

The `mcp-cli` tool (part of the Antigravity fleet) exposes a command-line interface:
`mcp-cli call <server> <tool> <json-args>`

**Integration Wrapper Class:**

```autohotkey
class MCP {
    static Call(server, tool, args_obj) {
        json_args := JSON.Dump(args_obj)
        cmd := Format('mcp-cli call {} {} "{}"', server, tool, this.Escape(json_args))
        
        shell := ComObject("WScript.Shell")
        exec := shell.Exec(cmd)
        output := exec.StdOut.ReadAll()
        
        return JSON.Load(output)
    }
    
    static Escape(str) {
        return StrReplace(str, '"', '\"')
    }
}

; Usage
result := MCP.Call("pywinauto", "automation_elements", {action: "click", text: "Submit"})
```

### Handling Responses

All MCP tools return structured JSON.
-   **Success**: `{"content": [{"type": "text", "text": "result..."}]}`
-   **Error**: `{"isError": true, "content": ...}`

Your AHK scripts must parse this structure to determine if the action succeeded.

### The `mcp-cli` Wrapper

We provide a compiled `mcp-cli.exe` to avoid the startup cost of Python interpretation for every call. This wrapper keeps a persistent connection to the MCP servers in the background (via named pipes or HTTP), ensuring that the call from AHK returns in milliseconds, not seconds.

---

## 5. Advanced Patterns

### Direct DllCall Integration

For ultra-low latency inputs that even Python can't handle fast enough (e.g., game mechanic automation), we use AHK's `DllCall`.

```autohotkey
; Instant mouse move via user32.dll
DllCall("user32.dll\mouse_event", "UInt", 0x0001, "UInt", 100, "UInt", 100, "UInt", 0, "UPtr", 0)
```

However, per SOTA standards, request this via `windows-computer-use-mcp` first. Use local AHK DllCall only if latency requirements (<10ms) strictly demand it.

### COM Automation

AHK has native COM support (`ComObject`). This is useful for automating legacy Office applications (Excel, Word) where `pywinauto` UI automation is flaky.

```autohotkey
xl := ComObject("Excel.Application")
xl.Visible := true
xl.Workbooks.Add()
xl.Range("A1").Value := "Automated by AHK"
```

*Note: For complex Office automation, prefer the `excel-mcp` server (Python-based).*

### WebView2 GUIs

For complex UIs in AHK, we use the `WebView2` library to render HTML/JS/CSS interfaces. This allows us to share UI components with our web dashboards.

---

## 6. Security Best Practices

1.  **No Keyloggers**: AHK scripts must NEVER write keystrokes to disk or network unless explicitly authorized for a debugging session.
2.  **Admin Privileges**: Run AHK scripts with **User privileges** by default. Only elevate (`Run *RunAs`) if interacting with Admin-level windows (e.g., Task Manager).
3.  **Code Signing**: In production, compiled AHK scripts (`.exe`) should be signed to prevent AV false positives.

---

## 7. Reference Material

-   [AutoHotkey v2 Language Documentation](https://www.autohotkey.com/docs/v2/)
-   [JSON.ahk Library](https://github.com/thqby/ahk2_lib/blob/master/JSON.ahk)
-   [Win32 API Reference](https://docs.microsoft.com/en-us/windows/win32/)
-   [PyWinAuto-MCP Documentation](../../ecosystem/windows-computer-use-mcp/README.md)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
