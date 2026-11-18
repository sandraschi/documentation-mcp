# Scoop Package Manager Guide (Windows 11)

**Added:** 2026-11-15  
**Scope:** Practical guide to Scoop on Windows 11—how it works, essential commands, and why it avoids Windows auto-updater breakages.

---

## 1. How Scoop Works (and Why It Doesn't "Vanish" Apps)

Unlike traditional Windows installers (Inno Setup, NSIS, MSI) that overwrite files in-place inside `Program Files` or `%LOCALAPPDATA%\Programs`:

- **Versioned directories:** Every install goes into `~\scoop\apps\<pkg>\<version>\` (no UAC prompts, no registry clutter).
- **`current` junction:** `~\scoop\apps\<pkg>\current` is a Windows directory junction pointing to the active version. Updating installs the *new* version alongside the old one and flips the junction—if a file is locked, the old version stays intact.
- **`shims/`:** `~\scoop\shims\` is on `PATH` and holds tiny shim `.exe` wrappers pointing at `current\...`, so your `PATH` stays short and clean.
- **`persist/`:** App data/configs declared in the manifest live in `~\scoop\persist\<pkg>\` and are symlinked/junctioned into each new version automatically.

---

## 2. Directory Layout

| Path | Purpose |
|---|---|
| `~\scoop\apps\<pkg>\<ver>\` | Installed app versions (`current` points to active) |
| `~\scoop\shims\` | Lightweight CLI shims added to `PATH` |
| `~\scoop\persist\<pkg>\` | Persistent user data/config preserved across updates |
| `~\scoop\buckets\` | Git-backed manifest repos (`main`, `extras`, `versions`) |
| `~\scoop\cache\` | Downloaded installers/archives (clear with `scoop cache rm *`) |

---

## 3. Essential Commands

| Task | Command |
|---|---|
| Search across buckets | `scoop search <name>` |
| Install (explicit bucket) | `scoop install extras/zed` |
| Check what's outdated | `scoop status` |
| Update Scoop + all apps | `scoop update *` |
| Update one app | `scoop update zed` |
| Remove old versions (keep `current`) | `scoop cleanup *` |
| Clear download cache | `scoop cache rm *` |
| Pin / freeze an app version | `scoop hold <pkg>` (undo: `scoop unhold <pkg>`) |
| Roll back to an older installed version | `scoop reset <pkg>@<version>` |
| Switch between variants (e.g. nightly ↔ stable) | `scoop uninstall zed-nightly; scoop install extras/zed` |
| List / add buckets | `scoop bucket list` · `scoop bucket add <name>` |

---

## 4. Buckets on Goliath

| Bucket | Role |
|---|---|
| **`main`** | Core CLI tools, runtimes, utilities (non-GUI) |
| **`extras`** | GUI apps & developer tools (e.g. `zed`, `vscode`, etc.) |
| **`versions`** | Alternative/prerelease/nightly channels (e.g. `zed-pre`, `zed-nightly`) |

---

## 5. Scoop vs. Winget & In-App Auto-Updaters

- **Prefer Scoop** for CLI tools, dev utilities, and portable/zip-distributed apps (`zed`, `ripgrep`, `uv`, `just`, `ffmpeg`, `ollama`, etc.)—cleanest upgrades, instant rollback, and `persist/` isolation.
- **Use Winget / native installers** for system-wide drivers, Microsoft Store apps, or apps that strictly require `Program Files` / Explorer shell integration.
- **Disable built-in auto-updaters on Scoop-managed GUI apps:**  
  If an app updates itself behind Scoop's back, it can install into a different folder or break Scoop's `current` junction. Example: set `"auto_update": false` in `%APPDATA%\Zed\settings.json` so `scoop update zed` stays the single source of truth.
- **Avoid in-place auto-updaters when background processes hold locks:**  
  Apps like Ollama (`ollama serve`) and Antigravity (`antigravity-updater`) can break mid-update if background helpers lock files during an in-place overwrite. Managing them via Scoop (or quitting background processes first) prevents half-deleted installs.

---

## Related

- [Zed IDE Integration](../ecosystem/zed/README.md)
