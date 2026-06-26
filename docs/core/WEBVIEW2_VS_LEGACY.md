# WebView2 vs Legacy Windows Web Rendering Engines

## Historical Context

Windows has shipped three web rendering engines for native apps. Understanding the lineage
explains why the fleet standardized on Tauri 2.0 + WebView2 and why the older options are
unusable for modern webapps.

| Era | Engine | Control / API | Ship vehicle | Status |
|-----|--------|---------------|--------------|--------|
| **1997–2020** | Trident (MSHTML) | `WebBrowser` / `IWebBrowser2` | Internet Explorer | **Deprecated** — IE11 retired Jun 2022 |
| **2015–2021** | EdgeHTML + Chakra | UWP `WebView` | Edge Legacy | **Deprecated** — Edge Legacy EOL Mar 2021 |
| **2021–present** | Chromium Blink + V8 | WebView2 COM/WinRT | Edge Chromium | **Active** — evergreen via Windows Update |

---

## 1. Engine & Standards Support

| Feature | Trident (IE WebBrowser) | EdgeHTML (UWP WebView) | WebView2 (Edge Chromium) |
|---------|------------------------|------------------------|--------------------------|
| **JS engine** | Chakra (old) / JScript | Chakra (modern) | V8 |
| **ES6+ support** | No (ES5 max) | Partial (ES2015–ES2018) | **Full ES2023+** |
| **CSS Grid** | No | Partial (EdgeHTML 16+) | Full |
| **CSS `:has()`** | No | No | Yes |
| **CSS container queries** | No | No | Yes |
| **CSS `backdrop-filter`** | No | EdgeHTML 18+ | Yes |
| **CSS custom properties** | No | Yes | Yes |
| **WebAssembly** | No | Yes (EdgeHTML 17+) | Full WASM + SIMD |
| **WebGPU** | No | No | Yes |
| **WebCodecs** | No | No | Yes |
| **AV1 video** | No | No | Yes (hardware on supported GPUs) |
| **HTTP/2, HTTP/3** | No | HTTP/2 only | HTTP/2 + HTTP/3 (QUIC) |
| **WebRTC** | No | Yes | Full (including data channels) |
| **Service Workers** | No | No (EdgeHTML support was removed) | Yes |
| **WebSocket** | No | Yes | Yes + WebSocket over HTTP/2 |

**Practical impact:** A React app built with TailwindCSS + Framer Motion + TypeScript that
works in Chrome will work identically in WebView2. In EdgeHTML, it would fail on CSS
grid layout alone. In Trident, it wouldn't even load the bundle (ES module syntax,
arrow functions, template literals all fail).

---

## 2. Developer Experience

| Capability | Trident | EdgeHTML | WebView2 |
|------------|---------|----------|----------|
| **DevTools** | None (`IWebBrowser2` has no debugger) | Limited (EdgeHTML via `Debug` menu, but must be enabled for the process) | **Full Chromium DevTools** (`Ctrl+Shift+I`, elements, console, network, sources, performance, memory, application, recoder, lighthouse) |
| **`console.log` output** | Not captured | Captured via `ScriptNotify` | Captured via DevTools Protocol or `CoreWebView2.WebMessageReceived` |
| **Source maps** | No | Partial | Full |
| **Remote debugging** | No | Via `msedge.exe --devtools` deprecation flags | Via DevTools Protocol on any port (`--remote-debugging-port=9222`) |
| **Network inspection** | None | EdgeHTML F12 tools | Full (request blocking, throttling, HAR export, waterfall) |
| **Programmatic script injection** | `IHTMLWindow2.execScript()` (limited) | `InvokeScriptAsync()` (async only) | `CoreWebView2.ExecuteScriptAsync()` (full modern JS) |
| **CSP enforcement** | No (ActiveX can still load) | Yes (original WebView) | Yes, with strict `Content-Security-Policy` |
| **Error messages** | Inscrutable COM HRESULTs | Better but truncated | Full stack traces, Chromium crash reports, minidump generation |

---

## 3. Process Architecture & Reliability

| Property | Trident | EdgeHTML | WebView2 |
|----------|---------|----------|----------|
| **Process model** | In-process (crash = app crash) | Out-of-process (single renderer) | **Multi-process** (browser, renderer, GPU, network, utility — same as Chrome) |
| **Renderer crash** | Takes host app down | Host app can detect but WebView is dead | Host app gets `ProcessFailed` event; can recreate WebView or reload |
| **GPU crash** | N/A (no GPU rendering) | Takes renderer down | Isolated in GPU process; `ProcessFailed` with `ProcessFailedKind.Gpu` |
| **IFrame isolation** | Same-process (no security boundary) | Site-per-process (limited) | Site-isolation (each origin in its own sandboxed process, Spectre mitigations) |
| **Memory usage (idle React SPA)** | ~80 MB (IE11) | ~120 MB (EdgeHTML) | ~50 MB (WebView2, same as Chrome) |
| **Startup time** | Fast (in-process) | Moderate | Fast (pre-warmed renderer via `AdditionalBrowserArguments`) |

---

## 4. API Surface & Control

### 4.1. Zoom

| Engine | Programmatic zoom | Ctrl+Scroll | Persistence |
|--------|-------------------|-------------|-------------|
| **Trident** | `IWebBrowser2.ExecWB(OLECMDID_ZOOM)` — limited, buggy | Native, no control | None |
| **EdgeHTML** | `WebView.ZoomFactor` (0.1–10.0) | Native | Per-app |
| **WebView2** | `CoreWebView2.SetBoundsAndZoomFactor()` / `window.setZoom()` — array of discrete levels | **Customizable** — can override with preferred levels | **Full — read/write any KV store** |

WebView2's `SetZoomFactor` accepts any float, but the fleet standard steps through
discrete levels (`0.8, 1.0, 1.25, 1.5, 2.0, 3.0`) and persists to localStorage
so the preference survives app restarts and is independent of the browser profile.

### 4.2. Script ↔ Host Communication

| Engine | Direction | Mechanism |
|--------|-----------|-----------|
| **Trident** | Host → Script | `IHTMLWindow2.execScript()` — IE5-era, limited to strings |
| | Script → Host | `window.external` — must implement `IDocHostUIHandler` |
| **EdgeHTML** | Host → Script | `WebView.InvokeScriptAsync()` — async, returns string |
| | Script → Host | `ScriptNotify` event — string only |
| **WebView2** | Host → Script | `CoreWebView2.ExecuteScriptAsync()` — any JSON-serializable value |
| | Script → Host | `chrome.webview.postMessage()` — structured JSON, no string wrapping |
| | Host → Script (postMessage) | `CoreWebView2.PostWebMessageAsJson()` — arbitrary structured data |
| | Bidirectional | DevTools Protocol — full Chrome DevTools Protocol over WebSocket |

### 4.3. Navigation & Request Control

| Engine | Request interception | Custom schemes | Cookie management |
|--------|---------------------|----------------|-------------------|
| **Trident** | No | No | `IWebBrowser2.Document.cookie` |
| **EdgeHTML** | Limited (`WebView.NavigationStarting` can cancel, not modify) | No | Windows.Web.Http filters |
| **WebView2** | `CoreWebView2.AddWebResourceRequestedFilter()` + `WebResourceRequested` event — **modify headers, body, redirect, or replace response entirely** | `CoreWebView2.RegisterCustomScheme()` — handle `tauri://`, `app://`, custom protocols | `CoreWebView2.CookieManager` — full CRUD, per-origin, session/persistent |

### 4.4. Notifications

| Engine | Native toast | Action centre | Icon customisation |
|--------|-------------|---------------|--------------------|
| **Trident** | No | No | — |
| **EdgeHTML** | Via UWP `ToastNotificationManager` | Yes | Yes |
| **WebView2** | Via `CoreWebView2.NotificationReceived` — host app handles it; OR `core:default` capability for Tauri | Yes (via host app) | Host app controls icon, title, body, actions, expiry |

---

## 5. Security

| Aspect | Trident | EdgeHTML | WebView2 |
|--------|---------|----------|----------|
| **ActiveX / Flash** | Supported (major attack surface) | Not supported | **Not supported** — zero legacy plugin surfaces |
| **XSS filters** | XSS Filter (deprecated, bypassable) | No built-in | `Trusted Types` API + strict CSP enforcement |
| **CSP** | No enforcement | Partial | **Full CSP Level 3** — `script-src`, `style-src`, `connect-src`, `report-to`, etc. |
| **`file://` access** | Full local file access | Restricted | Restricted + host controls via `SetVirtualHostNameToFolderMapping` |
| **Sandbox** | None | AppContainer (UWP) | **Chromium sandbox** + optional AppContainer + `--no-sandbox` override for debugging |
| **Autofill** | User can disable | Managed | **Controlled by host app** — `CoreWebView2.Settings.IsPasswordAutosaveEnabled`, `IsGeneralAutofillEnabled` |
| **DevTools in prod builds** | Can't be disabled | Environment variable | **Host app controls** via `CoreWebView2.Settings.AreDevToolsEnabled` |

---

## 6. Distribution & Footprint

| Aspect | Trident | EdgeHTML | WebView2 |
|--------|---------|----------|----------|
| **Runtime size** | Built into Windows | Built into Windows 10+ | ~1 MB (bootstrapper); full runtime ~50 MB (already on most Win10/11) |
| **Ship method** | Always present | Always present (Win10+ with Edge Legacy) | **Evergreen** — shipped via Windows Update + Edge updates; no bundling needed |
| **Per-app Chromium bundle?** | N/A | N/A | **No** — unlike Electron (200 MB) or CefSharp (50–100 MB) |
| **Windows 11** | Not present | Removed | **Present by default** |
| **Windows 10** | Present (deprecated) | Removed Jan 2022 | **Present** — KB update 1809+; bootstrapper for older builds |
| **Air-gapped deployment** | N/A | N/A | Use `embedBootstrapper` + distribute `.cab` with installer |
| **Update mechanism** | Windows Update (rare) | Windows Update | **Evergreen** — automatically updated via Edge update (no app rebuild needed) |
| **Per-install isolation** | N/A | N/A | **Yes** — `--user-data-dir` per app, or all apps share Edge profile |

**Practical impact for fleet:** A 200 MB Electron app becomes a 15 MB NSIS installer.
No Chromium bundles to redistribute. Security fixes arrive via Edge updates, not
app updates. See `tauri_nsis_building.md` for the full comparison table.

---

## 7. Fleet-Specific Concerns

### 7.1. Tauri uses WebView2's evergreen model

When we ship `"webviewInstallMode": { "type": "skip" }` in `tauri.conf.json`,
we assume the runtime is already present. This works on:
- **Windows 11** — Edge + WebView2 pre-installed
- **Windows 10** (≥ 1809) — Edge installed via Windows Update
- **Windows 10** (< 1809) — need `downloadBootstrapper` or `embedBootstrapper`

The old EdgeHTML had to be explicitly enabled for each app via registry keys or
manifest (`WebViewBroker`). WebView2 Just Works — Tauri adds it as a build dependency
(`webview2-com-sys`) and the runtime is found via COM.

### 7.2. Process cleanup

WebView2 spawns child helper processes (`msedgewebview2.exe`). These survive the
parent process if the app terminates without cleanup. Tauri handles this via
bundle resources and NSIS hooks — see `TAURI_PRODUCTION_PITFALLS.md` §I.

### 7.3. CSP in WebView2

Unlike the legacy webviews, WebView2 enforces `Content-Security-Policy` strictly.
A common fleet gotcha: `fetch()` calls from `tauri://localhost` to `http://127.0.0.1:{port}`
are cross-origin and require both CORS headers on the backend AND CSP `connect-src`
in the HTML. See `TAURI_PRODUCTION_PITFALLS.md` §B.

### 7.4. No Flash, no ActiveX, no legacy plugins

This is generally a security win, but if a legacy webapp depends on ActiveX controls
(old camera viewers, PLC interfaces, proprietary hardware SDKs), it will not work in
WebView2. The correct fleet response is to port the functionality to a server-side
MCP tool + WebUI component.

---

## 8. Summary

| If you're coming from... | The gap is... | Fleet recommendation |
|--------------------------|---------------|----------------------|
| **Trident / IE WebBrowser** | Unusable for any modern web framework | Do not use. Migrate to WebView2 immediately. |
| **EdgeHTML UWP WebView** | Missing CSS Grid, ES2020+, DevTools, structured messaging | Do not use. Migrate to WebView2. |
| **Electron** | 200 MB bundle vs 5 MB; wasteful when WebView2 is already on the OS | Deprecated fleet-wide; Tauri 2.0 + WebView2 replaces it. |
| **CefSharp** | Same Chromium engine, but CefSharp bundles Chromium (50+ MB) and has no evergreen updates | Tauri + WebView2 is preferred; CefSharp is acceptable for .NET Framework apps that cannot use Tauri. |

---

*Last updated: 2026-06-22*
*Part of the fleet Tauri/WebView2 standards*
