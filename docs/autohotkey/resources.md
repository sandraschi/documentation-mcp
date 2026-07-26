# AutoHotkey Resources & Bibliography

## Official

| Resource | Link |
|----------|------|
| AutoHotkey v2 download | [autohotkey.com](https://www.autohotkey.com/) |
| v2 documentation | [lexikos.github.io/v2/docs](https://lexikos.github.io/v2/docs/) |
| v1→v2 changes | [autohotkey.com/v2/v2-changes.htm](https://www.autohotkey.com/v2/v2-changes.htm) |
| GitHub repository | [github.com/AutoHotkey/AutoHotkey](https://github.com/AutoHotkey/AutoHotkey) |
| v2.0 release notes | [autohotkey.com/v2/whatsnew-v2.htm](https://www.autohotkey.com/v2/whatsnew-v2.htm) |

## Libraries & Tools

| Name | Description | Link |
|------|-------------|------|
| **thqby/ahk2_lib** | Comprehensive AHK v2 library pack (JSON, Socket, Crypt, WebSocket, UIA, GDI+) | [GitHub](https://github.com/thqby/ahk2_lib) |
| **Gdip_All.ahk** | GDI+ graphics library (v2 compatible fork) | [GitHub](https://github.com/mmikeww/AHKv2-Gdip) |
| **AHK v2 Linter** | Fleet's custom linter — 33+ checks, --fix mode | `autohotkey-test/utils/linter_headless.ahk` |
| **JSON.ahk** | JSON parser/serializer (MIT, bundled in fleet) | [thqby](https://github.com/thqby/ahk2_lib) |
| **Socket.ahk** | TCP/UDP networking (bundled in fleet) | [thqby](https://github.com/thqby/ahk2_lib) |
| **UIAutomation.ahk** | Windows UI automation via MSAA/UIA (bundled) | [thqby](https://github.com/thqby/ahk2_lib) |
| **Ahk2Exe** | Compile .ahk to .exe | [GitHub](https://github.com/AutoHotkey/Ahk2Exe) |

## Community

| Platform | Link |
|----------|------|
| r/AutoHotkey | [reddit.com/r/AutoHotkey](https://reddit.com/r/AutoHotkey) |
| AHK Discord | [discord.gg/autohotkey](https://discord.gg/autohotkey) |
| AHK Scripts & Functions | [autohotkey.com/boards](https://www.autohotkey.com/boards/) |
| Stack Overflow (AHK) | [stackoverflow.com/questions/tagged/autohotkey](https://stackoverflow.com/questions/tagged/autohotkey) |

## Learning

| Resource | Type | Description |
|----------|------|-------------|
| AHK v2 Tutorial | Official | [lexikos.github.io/v2/docs/Tutorial.htm](https://lexikos.github.io/v2/docs/Tutorial.htm) |
| The Bored Chat Tutorial | Community | [autohotkey.com/boards/viewtopic.php?t=94199](https://www.autohotkey.com/boards/viewtopic.php?t=94199) |
| AHK v2 Concepts | Guide | [lexikos.github.io/v2/docs/concepts.htm](https://lexikos.github.io/v2/docs/concepts.htm) |
| v2 Scripting Language | Reference | [lexikos.github.io/v2/docs/Scripts.htm](https://lexikos.github.io/v2/docs/Scripts.htm) |
| Learn AHK in 15 Minutes | Tutorial | [autohotkey.com/docs/Tutorial.htm](https://autohotkey.com/docs/Tutorial.htm) |

## Related Tools

| Tool | Purpose |
|------|---------|
| **WindowSpy.ahk** (ships with AHK) | Identify window class, controls, position for automation |
| **Ahk2Exe** | Compile scripts into standalone .exe files |
| **Run Script** (fleet) | `autohotkey-test/scriptlet_launcher_v2.ahk` — native GUI launcher |
| **ScriptletCOMBridge** (fleet) | HTTP bridge on port 10744 — remote list/run/stop |
| **autohotkey-mcp** (fleet) | FastMCP 3.4 server for AI-agent AHK usage |

## Fleet Publications

| Document | Location |
|----------|----------|
| Fleet AHK v2 Standard | `standards/rules/autohotkey_v2_standard.md` |
| AHK v2 Syntax Guide | `autohotkey/syntax.md` |
| AHK History | `autohotkey/history.md` |
| Library Reference | `autohotkey/libraries.md` |
| Linter Docs | `autohotkey/linter.md` |
| v1→v2 Migration Guide | `autohotkey-test/docs/AutoHotkey_v2_Syntax_Migration_Guide.md` |
| Error Handling Guide | `autohotkey-test/docs/AutoHotkey_v2_Error_Handling_and_Debugging.md` |
| Common Incompatibilities | `autohotkey-test/docs/AutoHotkey_v2_Common_Incompatibilities.md` |
| GDI+ Fixes | `autohotkey-test/docs/AutoHotkey_v2_GUI_Fixes.md` |

## Bibliography

### Language History
- Mallett, C. (2003). AutoHotkey v1.0 release. *First public release of the Windows automation tool.*
- Gray, S. (Lexikos). (2012). AutoHotkey v1.1 fork. *Major cleanup and Unicode support.*
- Gray, S. (Lexikos). (2022). AutoHotkey v2.0 stable release. *Complete rewrite with OOP, proper types, function-only syntax.* [autohotkey.com](https://www.autohotkey.com/)

### Related Work
- AutoIt v2/v3. The original automation tool that inspired AutoHotkey. AHK was created when Chris Mallett was prohibited from distributing AutoIt patches. [autoitscript.com](https://www.autoitscript.com/)
- Windows Script Host (WSH). Microsoft's VBScript/JScript automation — AHK's predecessor for desktop automation. [Microsoft](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc737847(v=ws.10))
- PowerShell. Microsoft's task automation framework. Fleet uses PowerShell alongside AHK for system-level tasks. AHK handles GUI/input automation, PowerShell handles system administration.

### Computer Science Foundations
- Gamma et al., *Design Patterns: Elements of Reusable Object-Oriented Software* (1994). The observer pattern (AHK's event system), command pattern (hotkey binding).
- Hunt & Thomas, *The Pragmatic Programmer* (1999). "Don't Repeat Yourself" — AHK scripts reduce repetitive Windows tasks.
- Spolsky, *The Best Software Writing I* (2005). Essays on usability that apply to AHK's philosophy: automate everything, reduce friction.

### Windows Internals
- Richter, *Windows via C/C++* (2007). Window messaging, subclassing, and hook techniques that underpin AHK's `OnMessage`, `SetWindowsHookEx`.
- Russinovich & Solomon, *Windows Internals* (ongoing). Process/thread management, UI automation, window station concepts.
- Petzold, *Programming Windows* (1998). Win32 API patterns that AHK wraps: window classes, messages, controls.
