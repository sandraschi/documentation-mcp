# Cursor — Multi-Account Switching

**Added:** 2026-11-15

Cursor has no native in-app account switcher. How you run two accounts (e.g., personal + work, or two Pro accounts) depends on whether you are using **Cursor IDE (GUI)** or **Cursor CLI**.

> [!NOTE]
> Pooling or rotating multiple personal accounts to bypass rate limits may violate provider Terms of Service.

---

## 1. Cursor IDE (GUI) — Native `--user-data-dir`

Because Cursor IDE is Electron/VS Code-based, you do **not** need `unshare` or `USERPROFILE` hacks. Pass `--user-data-dir` (and optionally `--extensions-dir` if you want to share installed extensions):

```powershell
# PowerShell alias/function in $PROFILE
function cursor2 {
    cursor --user-data-dir="$env:USERPROFILE\.cursor-work" @args
}
```

- Each `--user-data-dir` keeps its own login, settings, MCP config, and session state.
- Both instances can run **simultaneously** on Windows 11, macOS, and Linux.
- You can also create a separate Windows Desktop/Start Menu shortcut with `--user-data-dir="..."` appended to the Target.

---

## 2. Cursor CLI — `~/.cursor` Isolation

The Cursor CLI stores its auth session and config under `~/.cursor` (`%USERPROFILE%\.cursor` on Windows).

### Linux / WSL2 (`unshare` / `bwrap`)

Use Linux user + mount namespaces to bind-mount a second `.cursor2` directory over `~/.cursor` for a single process tree without changing `$HOME`:

```bash
alias cursor2='unshare -U -r -m sh -c "mount --bind ~/.cursor2 ~/.cursor && exec cursor-agent"'
```

If a child tool complains about UID `0` under `-r`, use **Bubblewrap**:

```bash
alias cursor2='bwrap --dev-bind / / --bind ~/.cursor2 ~/.cursor cursor-agent'
```

*(Replace `cursor-agent` with `agent` if using the newer CLI binary name.)*

### Windows 11

Windows 11 has no native per-process mount namespace like Linux `unshare`. Options:

1. **PowerShell wrapper (simultaneous runs, native):**
   ```powershell
   function cursor-cli2 {
       $oldProfile = $env:USERPROFILE
       $oldHome = $env:HOME
       $env:USERPROFILE = "$oldProfile\.cursor2-home"
       $env:HOME = $env:USERPROFILE
       New-Item -ItemType Directory -Force -Path $env:USERPROFILE | Out-Null
       try { agent @args }
       finally {
           $env:USERPROFILE = $oldProfile
           $env:HOME = $oldHome
       }
   }
   ```
   - **Pros:** Native Windows, simultaneous sessions.
   - **Cons:** Spawned tools (`.gitconfig`, `.ssh`, etc.) also look in `.cursor2-home` unless copied or symlinked there.

2. **Directory junction swap (keeps `$HOME` intact, sequential only):**
   Keep `~/.cursor-1` and `~/.cursor-2` and swap a Windows junction at `~/.cursor` (`New-Item -ItemType Junction` or `mklink /J`).

3. **WSL2:**
   Run the CLI inside WSL2 and use the `unshare` / `bwrap` alias directly.

4. **Second Windows local user (`runas`):**
   Cleanest native isolation, heavier setup.

---

## Related

- [Cursor Public Profiles](PROFILES.md)
- [Cursor IDE Overview](README.md)
- [Antigravity Multi-Account Switching](../antigravity/MULTI_ACCOUNT_SWITCHING.md)
