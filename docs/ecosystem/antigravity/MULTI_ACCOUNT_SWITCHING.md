# Antigravity CLI (`agy`) — Multi-Account Switching

**Added:** 2026-11-15

`agy` stores its auth session and configuration under `~/.gemini` (`%USERPROFILE%\.gemini` on Windows). To use two accounts (e.g., two Pro accounts) without logging out and back in, you isolate the `.gemini` directory per profile.

> [!NOTE]
> Pooling or rotating multiple personal accounts to bypass rate limits may violate provider Terms of Service.

---

## Linux / WSL2 (`unshare` / `bwrap`)

On Linux, `unshare` uses kernel **user** and **mount** namespaces to bind-mount a second folder over `~/.gemini` for just that process tree—without `sudo` and without changing `$HOME` (so `.gitconfig`, `.ssh`, and caches stay intact):

```bash
alias agy2='unshare -U -r -m sh -c "mount --bind ~/.gemini2 ~/.gemini && exec agy"'
```

- **`-U -r`**: Creates a user namespace mapping your user to UID `0` inside the namespace so `mount --bind` is permitted without real root.
- **`-m`**: Creates a private mount namespace; the bind mount is invisible to other processes and disappears on exit.
- **`exec agy`**: Replaces `sh` with `agy`.

**Caveats:**
- Everything in `~/.gemini` is split (`settings.json`, skills, MCP configs, history) unless you symlink shared items into `~/.gemini2` or bind-mount only auth subdirectories.
- Tools that check `id -u` and refuse to run as root may complain under `-r`; **Bubblewrap** avoids faking UID `0`:
  ```bash
  alias agy2='bwrap --dev-bind / / --bind ~/.gemini2 ~/.gemini agy'
  ```

---

## Windows 11

Windows 11 has no native per-process mount namespace like Linux `unshare`. Practical options:

### 1. PowerShell wrapper (simultaneous runs, native)

Override `USERPROFILE` and `HOME` for the duration of the call in your `$PROFILE`:

```powershell
function agy2 {
    $oldProfile = $env:USERPROFILE
    $oldHome = $env:HOME
    $env:USERPROFILE = "$oldProfile\.agy2"
    $env:HOME = $env:USERPROFILE
    New-Item -ItemType Directory -Force -Path $env:USERPROFILE | Out-Null
    try { agy @args }
    finally {
        $env:USERPROFILE = $oldProfile
        $env:HOME = $oldHome
    }
}
```

- **Pros:** Native Windows, runs both accounts simultaneously.
- **Cons:** Child tools spawned by `agy` (`.gitconfig`, `.ssh`, etc.) also look in `.agy2` unless copied or symlinked there.

### 2. Directory junction swap (keeps `$HOME` intact, sequential only)

Keep `~/.gemini-1` and `~/.gemini-2` and swap a Windows junction at `~/.gemini` (`New-Item -ItemType Junction` or `mklink /J`).
- **Pros:** Doesn't affect `.ssh` or `.gitconfig`.
- **Cons:** Only one account can be active at a time.

### 3. WSL2

Run `agy` inside WSL2 and use the Linux `unshare` / `bwrap` alias directly.

### 4. Second Windows local user (`runas`)

Create a second local Windows account and launch `agy` under it—cleanest native isolation, heavier setup.

---

## Related

- [Antigravity 2.0 — SDK & CLI](ANTIGRAVITY_2.0_SDK_CLI.md)
- [Third-Party Antigravity Ecosystem](THIRD_PARTY_ECOSYSTEM.md) (GUI account managers like `cockpit-tools`)
