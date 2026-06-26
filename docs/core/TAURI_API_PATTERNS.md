# Tauri API Patterns for MCP Webapps

> **Purpose:** Practical usage of `@tauri-apps/api` v2 modules inside React/Vite webapps
> that run both as Tauri NSIS installers (production) and in a dev browser (Vite).
> Every import is guarded by `try/catch` so dev mode never breaks.
>
> **⚠️ Tauri v1 vs v2:** In Tauri 2, `dialog`, `notification`, `http`, `fs`, `shell`,
> `clipboard-manager` and `process` are **separate npm packages** under `@tauri-apps/plugin-*`.
> They are NOT subpaths of `@tauri-apps/api` (which was the v1 layout).
> `@tauri-apps/api/window.getCurrentWindow()` replaces v1's `@tauri-apps/api/window.currentWindow`.
> If code uses v1 paths (`@tauri-apps/plugin-dialog`), TypeScript will fail with
> `Cannot find module` — that is the telltale sign of stale v1 imports.

See also:
- [tauri_nsis_building.md](rules/tauri_nsis_building.md) (Rust side, backend spawn, NSIS hooks)
- [TAURI_PRODUCTION_PITFALLS.md](TAURI_PRODUCTION_PITFALLS.md) "Tauri v1 vs v2 module paths" pitfalls section

---

## Setup

### 1. Install the package

```json
"dependencies": {
  "@tauri-apps/api": "^2.2.0"
}
```

```bash
cd webapp/frontend
npm install
```

### 2. Detect Tauri at runtime

```typescript
/** True when running inside the Tauri WebView (NSIS installer). */
export function isTauri(): boolean {
  return typeof window !== "undefined" && "__TAURI_INTERNALS__" in window;
}
```

`__TAURI_INTERNALS__` is injected by the Tauri 2.0 runtime. It does not exist in
the dev browser. Use this for one-shot UI decisions (hide/show a button).

### 3. Safe import pattern (always)

Every Tauri API module is imported dynamically so the dev browser never crashes:

```typescript
try {
  const { someFunction } = await import("@tauri-apps/api/module");
  await someFunction();
} catch {
  // Not running inside Tauri — fall back to browser API or no-op
}
```

**Never** use static imports for Tauri modules:

```typescript
// WRONG — crashes dev browser:
import { invoke } from "@tauri-apps/api/core";

// RIGHT — safe everywhere:
const { invoke } = await import("@tauri-apps/api/core");
```

### 4. Graceful degradation by module

| Module | In Tauri (NSIS) | In browser (dev) |
|--------|----------------|------------------|
| `core:invoke` | Calls Rust commands | `catch` → no-op or fallback logic |
| `event:listen` | Real-time Rust events | `catch` → HTTP polling (already done for backend-status) |
| `dialog:open` | Native OS file picker | No fallback — show `<input type="file">` or message |
| `notification:sendNotification` | OS toast | `catch` → use `new Notification()` (Web Notification API) |
| `window:setTitle` | Real window titlebar change | `catch` → `document.title` (still updates tab title) |
| `window:onCloseRequested` | Intercept window close | Not applicable — browser tab close cannot be intercepted reliably |
| `plugin-shell:open` | OS default browser | `catch` → `window.open(url, "_blank")` |
| `plugin-fs:readTextFile` | App data directory | `catch` → use `localStorage` |
| `plugin-process:exit` | Kill the app | `catch` → `window.close()` (may not work in all browsers) |
| `plugin-clipboard-manager:writeText` | System clipboard | `catch` → `navigator.clipboard.writeText()` |
| `plugin-updater:checkUpdate` | Native update check | `catch` — not applicable in dev; hide the feature |
| `http:fetch` | CORS-free HTTP | `catch` → use `fetch()` (browser CORS applies) |

### 5. Centralized `useTauri` hook (recommended)

One hook per app that exposes all Tauri operations with built-in fallbacks:

```typescript
// src/hooks/useTauri.ts
export function useTauri() {
  const isTauri = typeof window !== "undefined" && "__TAURI_INTERNALS__" in window;

  // --- invoke ---
  const invoke = useCallback(async <T>(cmd: string, args?: Record<string, unknown>): Promise<T | null> => {
    if (!isTauri) return null;
    try {
      const m = await import("@tauri-apps/api/core");
      return await m.invoke<T>(cmd, args);
    } catch { return null; }
  }, [isTauri]);

  // --- listen ---
  const listen = useCallback(async <T>(event: string, handler: (payload: T) => void): Promise<(() => void) | null> => {
    if (!isTauri) return null;
    try {
      const m = await import("@tauri-apps/api/event");
      return await m.listen<T>(event, handler);
    } catch { return null; }
  }, [isTauri]);

  // --- dialog + fs (open/save files with browser fallbacks) ---
  const openFile = useCallback(async (extensions?: string[]): Promise<{ name: string; data: ArrayBuffer; path?: string } | null> => {
    // Tauri: native dialog + read via plugin-fs
    if (isTauri) {
      try {
        const { open } = await import("@tauri-apps/plugin-dialog");
        const { readFile } = await import("@tauri-apps/plugin-fs");
        const r = typeof (await open({ multiple: false, filters: extensions ? [{ name: "Files", extensions }] : undefined })) as string | null;
        if (!r) return null;
        return { name: r.split(/[/\\]/).pop() || r, data: await readFile(r), path: r };
      } catch { return null; }
    }
    // Browser: hidden <input type="file">
    return new Promise((resolve) => {
      const input = document.createElement("input");
      input.type = "file"; input.style.display = "none";
      if (extensions) input.accept = extensions.map(e => `.${e}`).join(",");
      input.onchange = async () => {
        const file = input.files?.[0];
        if (!file) { resolve(null); return; }
        resolve({ name: file.name, data: await file.arrayBuffer() });
        input.remove();
      };
      document.body.appendChild(input);
      input.click();
    });
  }, [isTauri]);

  const saveFile = useCallback(async ({ filename, content, mimeType }: { filename?: string; content: string | Blob; mimeType?: string }): Promise<string | null> => {
    // Tauri: native save dialog + write via plugin-fs
    if (isTauri) {
      try {
        const { save } = await import("@tauri-apps/plugin-dialog");
        const { writeTextFile, writeFile } = await import("@tauri-apps/plugin-fs");
        const path = await save({ defaultPath: filename });
        if (!path) return null;
        if (typeof content === "string") await writeTextFile(path, content);
        else await writeFile(path, content);
        return path;
      } catch { return null; }
    }
    // Browser: <a download> blob URL
    const blob = typeof content === "string" ? new Blob([content], { type: mimeType || "text/plain" }) : content;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename || "download"; a.style.display = "none";
    document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 1000);
    return filename || "download";
  }, [isTauri]);

  const showMessage = useCallback(async (msg: string, title?: string) => {
    if (!isTauri) { alert(msg); return; }
    try {
      const m = await import("@tauri-apps/plugin-dialog");
      await m.message(msg, { title });
    } catch { alert(msg); }
  }, [isTauri]);

  const confirmAction = useCallback(async (msg: string, title?: string): Promise<boolean> => {
    if (!isTauri) return window.confirm(msg);
    try {
      const m = await import("@tauri-apps/plugin-dialog");
      return await m.ask(msg, { title });
    } catch { return window.confirm(msg); }
  }, [isTauri]);

  // --- notification ---
  const notify = useCallback(async (title: string, body?: string) => {
    if (!isTauri) {
      try { new Notification(title, { body }); } catch { /* notifications blocked */ }
      return;
    }
    try {
      const m = await import("@tauri-apps/plugin-notification");
      await m.sendNotification({ title, body });
    } catch {
      try { new Notification(title, { body }); } catch {}
    }
  }, [isTauri]);

  // --- window ---
  const setWindowTitle = useCallback(async (title: string) => {
    document.title = title; // always works (tab title)
    if (!isTauri) return;
    try {
      const m = await import("@tauri-apps/api/window");
      await m.getCurrentWindow().setTitle(title);
    } catch {}
  }, [isTauri]);

  // --- shell / open external ---
  const openUrl = useCallback(async (url: string) => {
    if (!isTauri) { window.open(url, "_blank"); return; }
    try {
      const m = await import("@tauri-apps/plugin-shell");
      await m.open(url);
    } catch { window.open(url, "_blank"); }
  }, [isTauri]);

  // --- clipboard ---
  const copyToClipboard = useCallback(async (text: string) => {
    if (!isTauri) {
      try { await navigator.clipboard.writeText(text); } catch {}
      return;
    }
    try {
      const m = await import("@tauri-apps/plugin-clipboard-manager");
      await m.writeText(text);
    } catch {
      try { await navigator.clipboard.writeText(text); } catch {}
    }
  }, [isTauri]);

  // --- fs (app data dir — Tauri) / localStorage (dev browser) ---
  /**
   * Both backends are persistent across tab closes, server restarts, and reboots.
   *
   * Tauri: reads from `%LOCALAPPDATA%\{identifier}\{key}.json`.
   * Browser: reads from `localStorage` — cleared only when user explicitly
   *          wipes site data or uses private/incognito mode.
   */
  const readSettings = useCallback(async <T>(key: string): Promise<T | null> => {
    if (!isTauri) {
      try { return JSON.parse(localStorage.getItem(key) ?? "null"); } catch { return null; }
    }
    try {
      const { readTextFile } = await import("@tauri-apps/plugin-fs");
      return JSON.parse(await readTextFile(`${key}.json`));
    } catch { return null; }
  }, [isTauri]);

  /**
   * Both backends are persistent across tab closes, server restarts, and reboots.
   *
   * Tauri: writes to `%LOCALAPPDATA%\{identifier}\{key}.json`.
   * Browser: writes to `localStorage`.
   */
  const writeSettings = useCallback(async (key: string, data: unknown) => {
    if (!isTauri) {
      localStorage.setItem(key, JSON.stringify(data));
      return;
    }
    try {
      const { writeTextFile } = await import("@tauri-apps/plugin-fs");
      await writeTextFile(`${key}.json`, JSON.stringify(data, null, 2));
    } catch {}
  }, [isTauri]);

  return {
    isTauri,
    invoke, listen,
    openFile, saveFile, showMessage, confirmAction,
    notify,
    setWindowTitle,
    openUrl,
    copyToClipboard,
    readSettings, writeSettings,
  };
}
```

**Usage in any page:**

```typescript
import { useTauri } from "../hooks/useTauri";

function MyPage() {
  const { isTauri, notify, confirmAction, openFile, setWindowTitle } = useTauri();

  // Works in both Tauri and browser — each method degrades internally
  const handleImport = async () => {
    const file = await openFile(["blend", "stl", "obj"]);
    if (!file) return;
    if (file.path) {
      // Tauri: backend reads from disk directly
      await invoke("import_file", { path: file.path });
    } else {
      // Browser: upload the raw bytes
      await fetch("/api/upload", {
        method: "POST",
        body: file.data,
        headers: { "X-Filename": file.name },
      });
    }
  };

  const handleExport = async (name: string, svgContent: string) => {
    await saveFile({ filename: name, content: svgContent, mimeType: "image/svg+xml" });
  };

  const handleRender = async () => {
    await renderScene();
    await notify("Render Complete", "Scene finished rendering");
  };
}
```

---

## Module Reference

---

### `@tauri-apps/api/core` — IPC bridge (invoke commands)

| Export | Signature | What it does |
|--------|-----------|-------------|
| `invoke` | `invoke<T>(cmd: string, args?: Record<string, unknown>) => Promise<T>` | Call any registered Rust `#[tauri::command]` |

**MCP patterns:**

- **Restart backend** (already wired):
  ```typescript
  const { invoke } = await import("@tauri-apps/api/core");
  await invoke("start_backend");
  ```

- **Get app version** (no Rust command needed — built-in):
  ```typescript
  const { invoke } = await import("@tauri-apps/api/core");
  const version: string = await invoke("plugin:app|version");
  ```

- **Get app data dir**:
  ```typescript
  const { invoke } = await import("@tauri-apps/api/core");
  const dir: string = await invoke("plugin:path|app_data_dir");
  ```

**Rule of thumb:** Any Rust function you write with `#[tauri::command]` is callable via `invoke`. Use this for backend lifecycle (restart, status) and FS operations that need Rust permissions.

---

### `@tauri-apps/api/event` — Tauri event bus

| Export | Signature | What it does |
|--------|-----------|-------------|
| `listen` | `listen<T>(event: string, handler: (payload: T) => void) => Promise<() => void>` | Subscribe to a Tauri event |
| `once` | `once<T>(event: string, handler: (payload: T) => void) => Promise<() => void>` | Subscribe once |
| `emit` | `emit(event: string, payload?: unknown) => Promise<void>` | Emit event to Rust side |

**MCP patterns:**

- **Backend status updates** (already wired):
  ```typescript
  const { listen } = await import("@tauri-apps/api/event");
  const unlisten = await listen<string>("backend-status", (event) => {
    if (event.payload === "ready") { setOnline(true); }
  });
  // cleanup:
  unlisten();
  ```

- **Scene change notifications** (Rust emits: `app.emit("scene-changed", "Kitchen scene")`):
  ```typescript
  const { listen } = await import("@tauri-apps/api/event");
  await listen<string>("scene-changed", (event) => {
    setActiveScene(event.payload);
    document.title = `Blender MCP — ${event.payload}`;
  });
  ```

- **Render progress** (Rust emits progress percentage):
  ```typescript
  await listen<number>("render-progress", (event) => {
    setRenderProgress(event.payload); // 0-100
  });
  ```

**Always return the `unlisten` function from the effect cleanup.**

---

### `@tauri-apps/plugin-dialog` — Native file dialogs

| Export | Signature | What it does |
|--------|-----------|-------------|
| `open` | `open(opts?: OpenDialogOptions) => Promise<string \| string[] \| null>` | Native OS file/folder picker |
| `save` | `save(opts?: SaveDialogOptions) => Promise<string \| null>` | Native OS save dialog |
| `message` | `message(message: string, opts?: DialogOptions) => Promise<void>` | Native info dialog |
| `ask` | `ask(message: string, opts?: DialogOptions) => Promise<boolean>` | Native yes/no dialog |
| `confirm` | `confirm(message: string, opts?: DialogOptions) => Promise<boolean>` | Native confirm dialog |

**MCP patterns:**

- **Import .blend / .stl / .obj file**:
  ```typescript
  async function pickBlendFile(): Promise<string | null> {
    try {
      const { open } = await import("@tauri-apps/plugin-dialog");
      const selected = await open({
        multiple: false,
        filters: [{ name: "Blender", extensions: ["blend", "stl", "obj", "fbx"] }],
      });
      return typeof selected === "string" ? selected : null;
    } catch { return null; }
  }
  ```

- **Save screenshot / render**:
  ```typescript
  async function saveRender(): Promise<string | null> {
    try {
      const { save } = await import("@tauri-apps/plugin-dialog");
      return await save({
        defaultPath: "render.png",
        filters: [{ name: "PNG", extensions: ["png"] }],
      });
    } catch { return null; }
  }
  ```

- **Confirm destructive action**:
  ```typescript
  async function confirmDeleteObject(name: string): Promise<boolean> {
    try {
      const { ask } = await import("@tauri-apps/plugin-dialog");
      return await ask(`Delete "${name}" permanently?`, {
        title: "Delete Object",
        kind: "warning",
      });
    } catch { return true; } // fallback: allow in dev
  }
  ```

- **Pick a directory for batch export**:
  ```typescript
  const { open } = await import("@tauri-apps/plugin-dialog");
  const dir = await open({ directory: true, multiple: false });
  ```

---

### `@tauri-apps/plugin-notification` — OS toast notifications

| Export | Signature | What it does |
|--------|-----------|-------------|
| `sendNotification` | `sendNotification(opts: NotificationOptions \| string) => Promise<void>` | Show OS notification |
| `isPermissionGranted` | `isPermissionGranted() => Promise<boolean>` | Check permission |
| `requestPermission` | `requestPermission() => Promise<Permission>` | Request notification permission |

**MCP patterns:**

- **Render complete**:
  ```typescript
  async function notifyComplete(sceneName: string) {
    try {
      const { sendNotification } = await import("@tauri-apps/plugin-notification");
      sendNotification({
        title: "Render Complete",
        body: `"${sceneName}" finished rendering.`,
        icon: "path/to/icon.png",
      });
    } catch {}
  }
  ```

- **Script error alert**:
  ```typescript
  sendNotification({ title: "Script Error", body: error.message });
  ```

- **Long operation finished** (batch export, mesh analysis, etc.):
  ```typescript
  sendNotification({ title: "Export Done", body: `Exported ${count} objects.` });
  ```

---

### `@tauri-apps/api/window` — Window control

| Export | Signature | What it does |
|--------|-----------|-------------|
| `getCurrentWindow` | `getCurrentWindow() => Window` | Get the current window handle |
| `getAllWindows` | `getAllWindows() => Promise<WebviewWindow[]>` | List all windows |
| `.setTitle()` | `setTitle(title: string)` | Change window title |
| `.setSize()` | `setSize(size: PhysicalSize)` | Resize window |
| `.setPosition()` | `setPosition(pos: PhysicalPosition)` | Move window |
| `.center()` | `center()` | Center on screen |
| `.minimize()` | `.maximize()` `.unmaximize()` `.close()` | Window state |
| `onCloseRequested` | `onCloseRequested(handler) => Promise<() => void>` | Intercept close (confirm) |

**MCP patterns:**

- **Scene name in titlebar**:
  ```typescript
  useEffect(() => {
    (async () => {
      try {
        const { getCurrentWindow } = await import("@tauri-apps/api/window");
        await getCurrentWindow().setTitle(`Blender MCP — ${currentScene || "No scene"}`);
      } catch {}
    })();
  }, [currentScene]);
  ```

- **Confirm close when backend is running**:
  ```typescript
  useEffect(() => {
    let unlisten: (() => void) | undefined;
    (async () => {
      try {
        const { getCurrentWindow } = await import("@tauri-apps/api/window");
        unlisten = await getCurrentWindow().onCloseRequested(async (event) => {
          const { ask } = await import("@tauri-apps/plugin-dialog");
          if (backendRunning) {
            event.preventDefault();
            const yes = await ask("A render is in progress. Quit anyway?");
            if (yes) { await invoke("start_backend"); /* kill child */ window.close(); }
          }
        });
      } catch {}
    })();
    return () => { if (unlisten) unlisten(); };
  }, [backendRunning]);
  ```

- **Restore window position on launch**:
  ```typescript
  const { currentWindow } = await import("@tauri-apps/api/window");
  await currentWindow.center();
  ```

---

### `@tauri-apps/plugin-shell` — Open URLs & execute

| Export | Signature | What it does |
|--------|-----------|-------------|
| `open` | `open(url: string) => Promise<void>` | Open URL in default browser |

Requires `"shell:allow-open"` in `capabilities/default.json`.

**MCP patterns:**

- **Open docs / marketplace / community**:
  ```typescript
  async function openExternal(url: string) {
    try {
      const { open } = await import("@tauri-apps/plugin-shell");
      await open(url);
    } catch { window.open(url, "_blank"); }
  }
  ```

- **Usage:** Help links, "Download from Blender Market", "Report issue on GitHub"

---

### `@tauri-apps/plugin-fs` — Filesystem

| Export | Signature | What it does |
|--------|-----------|-------------|
| `readTextFile` | `readTextFile(path: string) => Promise<string>` | Read file from app data dir |
| `writeTextFile` | `writeTextFile(path: string, contents: string) => Promise<void>` | Write file to app data dir |
| `readDir` | `readDir(dir: string) => Promise<FileEntry[]>` | List directory |
| `createDir` | `createDir(dir: string) => Promise<void>` | Create directory |
| `exists` | `exists(path: string) => Promise<boolean>` | Check if path exists |
| `remove` | `remove(path: string, opts?: { recursive?: boolean }) => Promise<void>` | Delete file/dir |

Requires `"fs:allow-*"` permissions in `capabilities/default.json`.
Paths are resolved relative to the app data dir.

**MCP patterns:**

- **Persist settings locally (offline-first)**:
  ```typescript
  async function saveSettings(settings: object) {
    try {
      const { writeTextFile, readDir } = await import("@tauri-apps/plugin-fs");
      await writeTextFile("settings.json", JSON.stringify(settings, null, 2));
    } catch { /* dev mode — use localStorage */ }
  }

  async function loadSettings<T>(): Promise<T | null> {
    try {
      const { readTextFile, exists } = await import("@tauri-apps/plugin-fs");
      if (!(await exists("settings.json"))) return null;
      return JSON.parse(await readTextFile("settings.json"));
    } catch { return null; }
  }
  ```

- **Cache downloaded models/exports**:
  ```typescript
  const { createDir } = await import("@tauri-apps/plugin-fs");
  await createDir("downloads");
  await writeTextFile("downloads/robot.stl", stlData);
  ```

---

### `@tauri-apps/plugin-process` — App lifecycle

| Export | Signature | What it does |
|--------|-----------|-------------|
| `exit` | `exit(exitCode?: number) => Promise<void>` | Exit the app |

**MCP pattern — Quit button that kills both UI and backend:**

```typescript
async function quitApp() {
  try {
    const { invoke } = await import("@tauri-apps/api/core");
    const { ask } = await import("@tauri-apps/plugin-dialog");
    const willQuit = await ask("Quit Blender MCP? The backend will also stop.");
    if (!willQuit) return;
    await invoke("start_backend"); // kill child via stop_managed_child
    const { exit } = await import("@tauri-apps/plugin-process");
    await exit(0);
  } catch {
    window.close();
  }
}
```

---

### `@tauri-apps/plugin-clipboard-manager` — System clipboard

| Export | Signature | What it does |
|--------|-----------|-------------|
| `readText` | `readText() => Promise<string>` | Read clipboard |
| `writeText` | `writeText(text: string) => Promise<void>` | Write to clipboard |

**MCP patterns:**

- **Copy script output or error trace to clipboard**:
  ```typescript
  async function copyToClipboard(text: string) {
    try {
      const { writeText } = await import("@tauri-apps/plugin-clipboard-manager");
      await writeText(text);
    } catch { await navigator.clipboard.writeText(text); }
  }
  ```

- **Paste coordinates from another app**:
  ```typescript
  const { readText } = await import("@tauri-apps/plugin-clipboard-manager");
  const coords = await readText(); // "10.0, 20.0, 5.0"
  ```

---

### `@tauri-apps/plugin-updater` — App updates

| Export | Signature | What it does |
|--------|-----------|-------------|
| `checkUpdate` | `checkUpdate() => Promise<UpdateResult>` | Check for update |
| `installUpdate` | `installUpdate() => Promise<void>` | Download & install |

**MCP pattern — "New version available" banner:**

```typescript
async function checkForUpdate(): Promise<string | null> {
  try {
    const { checkUpdate } = await import("@tauri-apps/plugin-updater");
    const result = await checkUpdate();
    if (result.shouldUpdate && result.manifest?.version) {
      return result.manifest.version;
    }
    return null;
  } catch { return null; }
}

// In Dashboard:
const [newVersion, setNewVersion] = useState<string | null>(null);
useEffect(() => { checkForUpdate().then(setNewVersion); }, []);
// Render banner if newVersion is non-null
```

---

### `@tauri-apps/plugin-http` — CORS-free HTTP

| Export | Signature | What it does |
|--------|-----------|-------------|
| `fetch` | `fetch<T>(url: string, options?: FetchOptions) => Promise<Response<T>>` | HTTP request (no CORS) |

**MCP patterns:**

- **Direct call to backend (no Vite proxy needed)**:
  ```typescript
  async function directHealthCheck(): Promise<boolean> {
    try {
      const { fetch } = await import("@tauri-apps/plugin-http");
      const resp = await fetch("http://127.0.0.1:10849/health");
      return resp.ok;
    } catch { return false; }
  }
  ```

- **Probe fleet peers** (other MCP webapps on the LAN):
  ```typescript
  async function probePeer(host: string, port: number): Promise<boolean> {
    try {
      const { fetch } = await import("@tauri-apps/plugin-http");
      const resp = await fetch(`http://${host}:${port}/health`, {
        method: "GET",
        connectTimeout: 3000,
      });
      return resp.ok;
    } catch { return false; }
  }
  ```

- **POST to Ollama for local LLM** (bypasses browser CORS on localhost):
  ```typescript
  const { fetch } = await import("@tauri-apps/plugin-http");
  const resp = await fetch("http://localhost:11434/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model: "llama3.2", prompt: "hello" }),
  });
  ```

---

## Fleet-standard Dashboard Integration

Every Tauri-wrapped MCP webapp MUST have at minimum:

| Feature | Module | Where |
|---------|--------|-------|
| Backend status (connected/offline) | HTTP poll + `event:listen` | Dashboard top card |
| Restart Backend button | `core:invoke` | Dashboard when offline |
| Scene/file name in window title | `window:setTitle` | Topbar or header effect |
| Render/export complete notification | `notification:sendNotification` | After long ops |

**Recommended additions** (when the feature exists):

| Feature | Module | Where |
|---------|--------|-------|
| Native file picker for import | `dialog:open` | Import page / button |
| Native save dialog for export | `dialog:save` | Export page / button |
| Quit button | `process:exit` | Settings page |
| New version banner | `updater:checkUpdate` | Dashboard top |
| Clipboard copy for script output | `clipboard-manager:writeText` | Script Console |
| Settings persisted to app data | `fs:writeTextFile` | Settings page |
| CORS-free fleet peer probe | `http:fetch` | App Hub |

---

## Capabilities (permissions)

Each plugin requires a permission in `capabilities/default.json`:

```json
{
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "dialog:default",
    "notification:default",
    "shell:allow-open",
    "fs:default",
    "process:default",
    "clipboard-manager:default",
    "updater:default",
    "http:default"
  ]
}
```

Only declare the permissions you actually use. The `:default` permission
covers read/write within the app data directory only.
