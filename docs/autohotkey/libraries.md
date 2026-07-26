# AHK v2 Libraries, Tools & Ecosystem

## Built-in (no #Include needed)

AHK v2 has no external library files — everything is compiled into `AutoHotkey64.exe`:

| Capability | Access | Notes |
|-----------|--------|-------|
| **GDI+** | `DllCall("gdiplus.dll\...")` | Full GDI+ via DllCall, no separate lib needed |
| **COM** | `ComObject()`, `ComValue()` | OLE/COM automation, ActiveX, ADO, etc. |
| **WinHTTP** | `ComObject("WinHttp.WinHttpRequest.5.1")` | HTTP requests |
| **ADO** | `ComObject("ADODB.Connection")` | SQL database access |
| **Speech** | `ComObject("SAPI.SpVoice")` | Text-to-speech |
| **Excel/Word** | `ComObject("Excel.Application")` | Office automation |
| **Internet Explorer** | `ComObject("InternetExplorer.Application")` | Web scraping (legacy) |
| **Crypto** | `DllCall("advapi32\...")` | CryptEncrypt, CryptHashData, etc. |
| **WinINet** | `DllCall("wininet.dll\...")` | FTP, HTTP (lower level) |
| **WinSock** | `DllCall("ws2_32.dll\...")` | TCP/UDP networking |
| **Window API** | `DllCall("user32.dll\...")` | Full Win32 API access |

## Bundled with AHK v2 Installation

| File | Location | Purpose |
|------|----------|---------|
| `WindowSpy.ahk` | `AutoHotkey\v2\WindowSpy\` | Identify window classes, controls, positions |
| `AutoHotkey64.exe` | `AutoHotkey\v2\` | The interpreter (32-bit also available) |
| `Ahk2Exe.exe` | `AutoHotkey\Compiler\` | Compile .ahk → .exe |

## Third-Party Libraries (thqby/ahk2_lib)

All MIT license from [github.com/thqby/ahk2_lib](https://github.com/thqby/ahk2_lib).
Bundled in `autohotkey-test/scriptlets/lib/`.

### Core Libraries

| Library | File | Lines | Purpose | Fleet Status |
|---------|------|-------|---------|-------------|
| **JSON** | `JSON.ahk` | 162 | JSON parse/stringify, `Load()`/`Dump()` aliases | ✅ In use |
| **Base64** | `Base64.ahk` | 31 | Base64 encode/decode via Crypt32 | ✅ Added |
| **Crypt** | `Crypt.ahk` | 60 | MD5, SHA-1/256, CRC32, AES-128/192/256 | ✅ Added |
| **YAML** | `YAML.ahk` | 389 | YAML parse/stringify | ✅ Added |

### Networking

| Library | File | Lines | Purpose | Fleet Status |
|---------|------|-------|---------|-------------|
| **Socket** | `Socket.ahk` | 360 | TCP/UDP sockets, client and server | ✅ Added |
| **WebSocket** | `WebSocket.ahk` | 320 | WebSocket client/server | ✅ Added |
| **HttpServer** | `HttpServer.ahk` | 589 | Pure AHK HTTP server (routes, middleware) | ✅ Added |
| **WinHttpRequest** | `WinHttpRequest.ahk` | 198 | HTTP client with async events, streaming | ✅ Added |
| **SMTPClient** | `SMTPClient.ahk` | — | Email sending | Not yet |

### GUI & Graphics

| Library | File | Lines | Purpose | Fleet Status |
|---------|------|-------|---------|-------------|
| **XCGUI** | `XCGUI/XCGUI.ahk` | 3302 | DirectX GUI framework — buttons, treeview, list, slider, etc. Requires separate XCGUI DLL | ✅ Added |
| **CGdip** | `CGdip.ahk` | 1178 | GDI+ wrapper: images, graphics, fonts, brushes | ✅ Added |
| **Direct2D** | `Direct2D.ahk` | — | Direct2D rendering | Not yet |

XCGUI is a full GUI framework using DirectUI technology — much richer than AHK's built-in `Gui()`. It provides professional-looking controls: tree views, list views, sliders, progress bars, tab controls, etc. Requires the `XCGUI.dll` from the [XCGUI project](https://github.com/twgh/xcgui).

### System & Automation

| Library | File | Lines | Purpose | Fleet Status |
|---------|------|-------|---------|-------------|
| **DirectoryWatcher** | `DirectoryWatcher.ahk` | 77 | Monitor file system changes (requires OVERLAPPED.ahk) | ✅ Added |
| **UIAutomation** | `UIAutomation.ahk` | 1991 | Windows MSAA/UIA automation — inspect, find, interact with controls | ✅ Added |
| **Monitor** | `Monitor.ahk` | 712 | Display info: resolutions, refresh rates, DPI, layout | ✅ Added |
| **Promise** | `Promise.ahk` | 242 | Async promise pattern for callbacks | ✅ Added |
| **OVERLAPPED** | `OVERLAPPED.ahk` | — | IO completion callbacks (dependency for DirectoryWatcher) | ✅ Added |

### Advanced

| Library | File | Purpose | Fleet Status |
|---------|------|---------|-------------|
| **CLR** | `CLR.ahk` | Host .NET CLR, call C#/VB.NET from AHK | Not yet |
| **Chrome** | `Chrome.ahk` | Chrome DevTools Protocol — control Chrome tabs | Not yet |
| **SQLite** | `Native/SQLite.ahk` | Native SQLite binding | Not yet |
| **Archive** | `archive.ahk` | ZIP compression | Not yet |
| **WinAPI** | `WinAPI/` | Comprehensive Win32 API wrappers | Not yet |

### Dependency Graph

```
DirectoryWatcher.ahk
  └── OVERLAPPED.ahk
```

### Usage

```autohotkey
; Add to top of your script:
#Include %A_ScriptDir%\lib\JSON.ahk
#Include %A_ScriptDir%\lib\Socket.ahk
#Include %A_ScriptDir%\lib\XCGUI\XCGUI.ahk

; Base64
encoded := Base64.Encode(myBuffer)
decoded := Base64.Decode(encodedString)

; Crypt
hash := MD5(dataBuffer)
hash := Crypt_Hash(dataBuffer, , "SHA256")
encryptedSize := Crypt_AES(pData, nSize, "password", 256, true)

; Socket
sock := Socket("TCP")
sock.Bind("127.0.0.1", 8080)
sock.Listen()
client := sock.Accept()

; WinHttpRequest
http := WinHttpRequest()
response := http.request("https://api.example.com/data")

; HttpServer — route-based HTTP server
server := HttpServer()

; XCGUI — professional DirectX GUI (requires XCGUI.dll)
import xcgui
xcgui.XInitXCGUI()
hWindow := xcgui.XWnd_Create(0, 0, 400, 300, "My App")
xcgui.XBtn_Create(20, 40, 100, 30, "OK", hWindow)
xcgui.XRunXCGUI()
```

## Other Notable Libraries

| Library | Author | Purpose | Link |
|---------|--------|---------|------|
| **Gdip_All.ahk** | mmikeww | Full GDI+ wrapper — images, fonts, transforms. V2 port of the classic v1 Gdip library. | [GitHub](https://github.com/mmikeww/AHKv2-Gdip) |
| **AHK-Rare** | Ixiko | Collection of 600+ rare/advanced functions | [GitHub](https://github.com/Ixiko/AHK-Rare) |
| **AHK-Object-Oriented-GUIs** | Run1e | OOP GUI framework for AHK v2 | [GitHub](https://github.com/Run1e/AHK-Object-Oriented-GUIs) |

## CLI Tools

| Tool | Purpose |
|------|---------|
| `AutoHotkey64.exe` script.ahk | Run script directly |
| `Ahk2Exe.exe /in script.ahk` | Compile to standalone .exe |
| `just lint-ahk` (fleet) | Lint all scripts |
| `just lint-fix` (fleet) | Auto-fix v1→v2 syntax |

## MCP Servers (Fleet)

| Server | Port | Purpose |
|--------|------|---------|
| **autohotkey-mcp** | 10746 | FastMCP 3.4 — list/run/stop scriptlets, generate AI scripts, help system |
| **ScriptletCOMBridge** | 10744 | HTTP bridge — `/scriptlets`, `/run/:name`, `/stop/:name`, `/dashboard` |

## Fleet Tools

| Tool | Location | Purpose |
|------|----------|---------|
| **Linter** | `utils/linter_headless.ahk` | 33+ v2 compliance checks, `--fix` mode |
| **Batch debugger** | `utils/batch_debugger.ps1` | PowerShell batch syntax checker |
| **Compatibility scanner** | `utils/compatibility_scanner.ahk` | v1→v2 migration scanner |
| **GdipHelper** | `scriptlets/lib/GdipHelper.ahk` | Minimal GDI+ wrapper for game rendering (fleet) |
| **ScriptletErrorHandler** | `scriptlets/lib/ScriptletErrorHandler.ahk` | Self-registering OnError handler |

## Other Projects

| Project | Description | Link |
|---------|-------------|------|
| **AHK-Studio** | Modern AHK IDE with debugging | [GitHub](https://github.com/maestrith/AHK-Studio) |
| **AutoGUI** | Visual GUI designer for AHK | [GitHub](https://github.com/samfisherirl/AutoGUI) |
| **VS Code extension** | AHK language support for VS Code | Marketplace: `mark-wiemer.vscode-autohotkey-plus-plus` |
