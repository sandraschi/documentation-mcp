# MSI Build Standard

**Scope**: Microsoft Installer — optional enterprise Windows installer format.
**Parent doc**: `tauri_nsis_building.md` (Tauri architecture + embedded backend templates)
**Fleet status**: ❌ Not shipped by any fleet repo. Documented for reference.

---

## When to Use MSI

MSI is for **enterprise deployment scenarios** only:

| Requirement | MSI | NSIS |
|-------------|-----|------|
| Group Policy deployment | ✅ `Computer Configuration → Software Installation` | ❌ |
| Active Directory publishing | ✅ | ❌ |
| Silent mass deployment | ✅ `msiexec /i setup.msi /qn` | ✅ `setup.exe /S` |
| Per-user install (no admin) | ❌ Machine-wide only | ✅ `currentUser` mode |
| Installer hooks (kill processes) | ❌ Not supported by Tauri MSI | ✅ PREINSTALL/PREUNINSTALL |
| Custom UI during install | ❌ | ✅ NSIS pages |
| Single-file artifact | ✅ `.msi` | ✅ `.exe` |

**Fleet recommendation**: Start with NSIS. Only add MSI if an enterprise customer explicitly
requires it for Group Policy distribution.

---

## Tauri MSI Limitations

Tauri 2.0 can generate MSI installers via `npx @tauri-apps/cli build --bundles msi`,
but the resulting MSI has significant limitations:

1. **No installer hooks** — The `installerHooks` config in `tauri.conf.json` only works
   for NSIS. The MSI has no PREINSTALL/PREUNINSTALL equivalent. If `backend.exe` is
   running when the MSI installs, file-lock conflicts will occur.

2. **Workaround**: The Rust `free_port()` function in `backend.rs` must handle the case
   where a stale backend from a previous version is running. This is already implemented
   for NSIS (zombie cleanup on launch) and works identically for MSI — the app kills
   orphaned processes at startup rather than at install time.

3. **No currentUser mode** — MSI always installs machine-wide, requiring administrator
   privileges. This means the uninstaller is registered in `HKLM` (not `HKCU`).

4. **Larger artifact** — MSI bundles the same content as NSIS but the wrapper adds
   ~1-2 MB overhead.

---

## Configuration

In `tauri.conf.json`, add `"msi"` to `targets`:

```json
{
  "bundle": {
    "targets": ["nsis", "msi"],
    "windows": {
      "msi": {
        "installMode": "machine",
        "wix": {
          "language": "en-US",
          "template": "msi"
        }
      }
    }
  }
}
```

---

## Silent Install / Uninstall

```powershell
# Install silently (no UI, no reboot)
msiexec /i {Product}_{version}_x64-setup.msi /qn /norestart

# Uninstall
msiexec /x {Product}_{version}_x64-setup.msi /qn /norestart

# Uninstall by product code
msiexec /x {PRODUCT_CODE} /qn /norestart
```

| Flag | Meaning |
|------|---------|
| `/i` | Install |
| `/x` | Uninstall |
| `/qn` | Quiet, no UI |
| `/qb` | Basic UI (progress bar only) |
| `/norestart` | Suppress reboot |
| `/l*v log.txt` | Verbose log to file |

---

## Group Policy Deployment

1. Build MSI: `npx @tauri-apps/cli build --bundles msi`
2. Place `.msi` on a network share accessible by target machines
3. In Group Policy Management Editor:
   - `Computer Configuration → Software Settings → Software Installation`
   - `New → Package` → select the `.msi` → `Assigned`
4. Next GP refresh, clients install silently

---

## Known Issues

| Issue | Cause | Mitigation |
|-------|-------|------------|
| "Another version is already installed" | MSI product code collision | Bump version in `tauri.conf.json` (auto-generates new product code) |
| Files in use during install | Backend running from previous version | Kill processes before launching MSI, or rely on `free_port()` at next app launch |
| Windows Installer service not running | Disabled by admin policy | `net start msiserver` or enable via Group Policy |
