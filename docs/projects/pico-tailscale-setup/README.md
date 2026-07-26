# Pico 4 revive pack (Windows)

One folder to **download + ADB-install** the sideload stack for fleet WebXR teleop and general Pico utility.

**Full docs:** [mcp-central-docs/pico/](../mcp-central-docs/pico/README.md)

## Quick start

```powershell
Set-Location D:\Dev\repos\pico-tailscale-setup

# Download all APKs (~200 MB)
.\Install-PicoRevivePack.ps1 -DownloadOnly

# USB: Pico developer mode + USB debugging → install required pack
.\Install-PicoRevivePack.ps1

# Required only (Tailscale + ObtainX + Aurora)
.\Install-PicoRevivePack.ps1 -SkipOptional
```

Legacy single-app installer: `Install-TailscaleOnPico.ps1`

## Contents

| Path | Role |
|------|------|
| `manifest.json` | APK URLs and versions |
| `apks/` | Downloaded APKs (created on first run) |
| `platform-tools/adb.exe` | Android Debug Bridge |
| `Install-PicoRevivePack.ps1` | Download + install |
| `Install-TailscaleOnPico.ps1` | Tailscale only |

## After install (headset)

1. **AnExplorer** — from Pico Store (not in pack; best file manager)
2. **Tailscale** — sign in (same tailnet as Goliath)
3. **Aurora Store** — install Discord, Jellyfin, etc.
4. **ObtainX** — track updates for sideloads
5. **Teleop** — Pico Browser → `https://goliath.<tailnet>.ts.net/` → Enter VR

See [WEBXR.md](../mcp-central-docs/pico/WEBXR.md) and [teleoperator-mcp](../teleoperator-mcp/docs/BRINGUP.md).
