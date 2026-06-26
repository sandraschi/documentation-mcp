# Windows Automation Approaches: AHK vs MCP

**Topic:** Comparative analysis of Windows desktop automation methods  
**Updated:** 2025-11-29

---

## Overview

Two primary approaches exist for Windows desktop automation in our ecosystem:

| Approach | Repository | Philosophy |
|----------|------------|------------|
| **AutoHotkey** | autohotkey-test | Scripted, shareable, lightweight |
| **PyWinAuto MCP** | pywinauto-mcp | AI-assisted, adaptive, integrated |

---

## Quick Comparison

| Aspect | AutoHotkey | PyWinAuto MCP |
|--------|------------|---------------|
| **Best For** | Shareable scripts, hotkeys | AI-driven automation |
| **Distribution** | Email .ahk/.exe | Requires MCP setup |
| **Target User** | Anyone (non-tech OK) | MCP developers |
| **Execution** | Deterministic | AI-adaptive |
| **Dependencies** | AHK runtime only | Python + MCP client |
| **Offline** | ✅ Yes | ❌ Needs Claude |

---

## The "Email to Steve" Test

**Scenario:** You want to share an automation with brother Steve who isn't technical.

### AutoHotkey ✅

```
1. Write clipboard_saver.ahk
2. Compile to clipboard_saver.exe
3. Email to Steve
4. Steve double-clicks → Works!
```

### PyWinAuto MCP ❌

```
1. Steve needs Python 3.10+
2. Steve needs pip knowledge
3. Steve needs Claude Desktop
4. Steve needs MCP configuration
5. Steve needs to restart Claude
6. Steve asks Claude "save my clipboard"
7. ...Steve calls you for help
```

**Conclusion:** For shareable tools, AHK wins decisively.

---

## The "Adaptive Automation" Test

**Scenario:** You need to fill a form that changes layout sometimes.

### AutoHotkey ⚠️

```ahk
; Script breaks if UI changes
ControlClick, Button1, MyApp
Sleep 100
ControlSetText, Edit1, MyText, MyApp
; If Edit1 moves → script fails
```

### PyWinAuto MCP ✅

```
User: "Fill out the name field in this form"

Claude: (analyzes UI, finds the right element regardless of exact ID)
        "Found the name field and filled it in."
```

**Conclusion:** For adaptive automation, PyWinAuto MCP wins.

---

## Use Case Matrix

### Use AutoHotkey When:

| Scenario | Example |
|----------|---------|
| Creating hotkey shortcuts | `^!n:: Run "notepad"` |
| Sharing with non-technical users | Compile to .exe, email |
| Building custom GUIs | Native AHK GUI toolkit |
| Offline operation required | No network dependencies |
| Deterministic, repeatable tasks | Same action every time |
| Low-level input needed | Game macros, key remapping |

**autohotkey-test examples:**
- `clipboard_manager.ahk` - Global clipboard history
- `window_snapping.ahk` - Custom window layouts  
- `chess_stockfish.ahk` - Full game with GUI
- `text_expander.ahk` - Text substitution

### Use PyWinAuto MCP When:

| Scenario | Example |
|----------|---------|
| AI should decide actions | "Find and click the save button" |
| Deep UI inspection needed | Accessibility tree analysis |
| OCR text extraction | Reading non-accessible dialogs |
| Face recognition security | Verify user before action |
| Complex cross-app workflows | AI orchestrates multiple apps |
| MCP ecosystem integration | Part of larger MCP system |

**pywinauto-mcp examples:**
- Desktop discovery ("What's open?")
- Form filling with element detection
- Error dialog text extraction
- Face-gated automation

---

## Feature Comparison

| Feature | AHK | PyWinAuto MCP |
|---------|-----|---------------|
| Hotkey binding | ✅ Native | ❌ N/A |
| Keyboard input | ✅ Send | ✅ automation_keyboard |
| Mouse control | ✅ Click, MouseMove | ✅ automation_mouse |
| Window ops | ✅ WinAPI | ✅ automation_windows |
| UI elements | ⚠️ Basic ControlClick | ✅ Deep UIA |
| GUI creation | ✅ Native | ❌ N/A |
| OCR | ❌ External | ✅ Built-in |
| Face recognition | ❌ N/A | ✅ Built-in |
| Compile to EXE | ✅ Ahk2Exe | ❌ N/A |

---

## Integration Pattern

For complex workflows, **use both**:

```
┌─────────────────┐     ┌──────────────────┐
│   AutoHotkey    │     │  PyWinAuto MCP   │
│                 │     │                  │
│  - Hotkeys      │────▶│  - AI analysis   │
│  - Quick GUIs   │     │  - Deep UI       │
│  - Local tasks  │◀────│  - OCR/Vision    │
└─────────────────┘     └──────────────────┘

User presses Ctrl+Alt+A → AHK triggers Claude → 
Claude uses pywinauto-mcp → Results back to user
```

---

## Decision Flowchart

```
Need Windows automation?
│
├── Share with non-tech users? → AutoHotkey (.exe)
│
├── Need hotkey shortcuts? → AutoHotkey
│
├── Building MCP system? → PyWinAuto MCP
│
├── Need AI adaptability? → PyWinAuto MCP
│
├── OCR/face recognition? → PyWinAuto MCP
│
├── Offline operation? → AutoHotkey
│
└── Simple repeatable task? → AutoHotkey
```

---

## Repository Links

- **autohotkey-test**: 75+ AHK scriptlets, games, productivity tools
- **pywinauto-mcp**: 8 portmanteau tools, AI-driven automation

---

## Summary

| Choose | When |
|--------|------|
| **AutoHotkey** | Sharing scripts, hotkeys, lightweight automation |
| **PyWinAuto MCP** | AI-driven, adaptive, MCP-integrated automation |
| **Both** | Complex workflows needing quick hotkeys + AI intelligence |

They're **complementary**, not competing. Use the right tool for each scenario.

