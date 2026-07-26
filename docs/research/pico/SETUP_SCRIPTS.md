# Pico 4 setup scripts (Windows)

**Location:** `D:\Dev\repos\pico-tailscale-setup`

Central place on Goliath to download APKs and push them to Pico 4 via ADB.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `Install-PicoRevivePack.ps1` | Download + install full revive pack from `manifest.json` |
| `Install-TailscaleOnPico.ps1` | Tailscale only (legacy single-app) |

### Examples

```powershell
Set-Location D:\Dev\repos\pico-tailscale-setup

# Download only (no headset connected)
.\Install-PicoRevivePack.ps1 -DownloadOnly

# Download + ADB install (USB connected, debugging authorized)
.\Install-PicoRevivePack.ps1

# Required apps only: Tailscale, ObtainX, Aurora
.\Install-PicoRevivePack.ps1 -SkipOptional

# Install already-downloaded APKs
.\Install-PicoRevivePack.ps1 -InstallOnly
```

---

## Manifest packages

Defined in `manifest.json`:

| Package | Required | Role |
|---------|----------|------|
| Tailscale | Yes | Tailnet VPN for `*.ts.net` WebXR |
| ObtainX | Yes | Update tracker for sideloads |
| Aurora Store | Yes | Play Store client without GMS on device |
| Wolvic (Gecko) | No | Open WebXR browser (also on Pico Store) |
| Wolvic (Chromium) | No | Better site compatibility |
| ALVR client | No | Wireless PC VR — version must match PC streamer |

**Store-only (not in manifest):** AnExplorer, Steam Link — install from Pico Store.

---

## Manual install (no ADB)

1. Run `-DownloadOnly`  
2. Copy `apks\*.apk` to headset internal storage (`Download`)  
3. File Manager → APKs → tap each file  

Or use AnExplorer Wi‑Fi transfer from phone/PC.

---

## Updating manifest URLs

APK versions drift. Refresh URLs from:

- Tailscale: [pkgs.tailscale.com/stable/#android](https://pkgs.tailscale.com/stable/#android)
- ObtainX / ALVR: GitHub latest release assets
- Wolvic: [Igalia/wolvic releases](https://github.com/Igalia/wolvic/releases) — use `Wolvic-picoxr-arm64-*` builds only
- Aurora: script resolves latest from IzzyOnDroid when `urlResolve` is set

After editing `manifest.json`, re-run `-DownloadOnly`.

---

## Related

- [REVIVE_CHECKLIST.md](REVIVE_CHECKLIST.md)
- [SIDELOAD.md](SIDELOAD.md)
- [teleoperator-mcp HTTPS guide](../../teleoperator-mcp/docs/HTTPS.md)
