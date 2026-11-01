# Fido - Headless Microsoft ISO Downloads

Fido (Pete Batard / Rufus author, GPLv3) is a PowerShell script that resolves
genuine Microsoft CDN download URLs for Windows ISOs. No Microsoft account, no
browser form, no Media Creation Tool clicking. Verified live on Goliath
2026-10-09 (Fido v1.71): produced a working Win11 26H2 URL and pulled 8.6 GB
via BITS with zero interaction.

Upstream: `https://github.com/pbatard/Fido` (single `Fido.ps1`, ~54 KB).

## Headless usage (the verified pattern)

```powershell
& pwsh -NoProfile -ExecutionPolicy Bypass -File Fido.ps1 `
  -Win "Windows 11" -Rel "Latest" -Ed "Pro" `
  -Lang "English" -Arch "x64" -PlatformArch "x64" -GetUrl
```

- `-GetUrl` prints the bare URL instead of opening a browser. Any of `-Win`,
  `-Rel`, `-Ed`, `-Lang`, `-Arch`, `-GetUrl` toggles command-line mode.
- `-PlatformArch x64` skips a very slow WMI autodetect call. Always pass it.
- `-Rel List` shows what Microsoft currently serves. `-Rel Latest` takes the
  newest. Lesson learned 2026-10-09: asking for `24H2` failed because Microsoft
  had already pulled it; only `26H2 (Build 26300.9457)` was listed. Pinning an
  old release is a bet against Microsoft's retention, not a stable reference.

## Downloading the ISO (agent-proof pattern)

Every opencode/bash tool call runs in a brand-new stateless subshell, so a
foreground 20-minute download dies with the call. Use async BITS, which lives
in the Windows service and survives shell exit:

```powershell
$job = Start-BitsTransfer -Source <url> `
  -Destination "D:\VMs\ISOs\Win11_26H2_en-us_x64.iso" -Asynchronous
# later turns:
$j = Get-BitsTransfer -JobId <id>
# when Transferred:
Complete-BitsTransfer -BitsJob $j
```

Notes: Fido URLs are tokenized (24h-ish validity), so start BITS the same
session you resolve the URL. 280 GB free on D: was confirmed before pulling;
check `Get-PSDrive D` first on any other box. Expect ~8-9 GB for Win11 x64.

## Retail vs Eval media (read before unattended install)

- Fido serves RETAIL media (Pro/Home). The fleet's
  `virtualization-mcp/assets/unattended/win11-automated-autounattend.xml` was
  authored for EVAL media (Eval product key). A retail ISO will reject the Eval
  key, so either swap in the public generic Pro key or run unactivated
  (watermark only, fully functional for a test VM). One-line change, document
  which you chose in the VM's notes.
- Retail-unactivated has no Eval expiry cliff, which suits a test VM that may
  sit powered off for months. Eval media time-bombs; retail nags.
- The existing autounattend also assumes an 80 GB disk and BIOS-style single
  partition; on UEFI firmware verify the partition scheme or expect a
  post-install boot repair. Check with a screenshot before declaring victory.

## Provenance note

Bits come from `software.download.prss.microsoft.com` (Microsoft's own CDN);
Fido only resolves the link. Keep it that way: never substitute a mirror ISO
from anywhere else for fleet VMs. Verify size (~8.6 GB for 26H2 en-US x64)
before attaching.

---
*Maintained by: Sandra + fleet agents. Last verified: 2026-10-09.*
