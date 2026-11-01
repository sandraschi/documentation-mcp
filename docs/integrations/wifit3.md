---
title: "wifit3 — USB-only cross-platform Wi-Fi auditor (reference)"
category: integration
status: parked
audience: mcp-dev
related:
  - projects/reversing-mcp/README.md
last_updated: 2026-09-29
---

# wifit3 — Reference

**Standalone USB Wi-Fi auditor for Linux, Windows, macOS.**
Upstream: [derv82/wifit3](https://github.com/derv82/wifit3) — "Wifite but USB-only & cross-platform."
Same author as original `wifite` (derv82). 1498 stars, 122 forks, 2 open issues (as of 2026-09-29).

**Fleet stance: parked — no compatible USB adapter on hand (2026-09-29). No MCP server, no install on Goliath. Reference only until hardware exists.**

| Fact | Value |
|---|---|
| Latest | `v0.3.4 (BETA)` 2026-09-27 (20 releases since 2026-08-03, very active) |
| License | Code GPL-2.0 (matches upstream Linux drivers); vendor firmware blobs redistributed verbatim |
| Stack | Pure Python + PyUSB + Textual, zero runtime deps (no aircrack-ng/reaver) |
| How | Userland "mini-drivers" (`src/wifit3/chips/`) drive USB adapters directly — bypasses Windows NDIS + Linux kernel driver locking |
| Binaries | `wifit3-windows-x64.exe` (36.8 MB), `wifit3-linux-x64`, `wifit3-linux-arm64`, `wifit3-macos-universal2` |
| Windows sha256 (v0.3.4) | `1043a9398a40dbccbaa27e18004ac0f242bc667ab90ab01b4ad7dcf999934b51` |

## What it does

- **Recon:** multi-card aggregation, real-time 2.4/5 GHz channel-hopping scanner, signal/encryption/WPA3-SAE tracking, AP+client vendor fingerprinting, router make/model from WPS beacons, hidden-network (VAP) decloaking via BSSID correlation, packet-rate dashboard.
- **Capture/attack:** WPA/WPA2 passive + deauth handshake capture (validates crackable pairs, exports `.pcap` + `.hc22000`), PMKID active+passive harvest (`.hc22000`), EvilTwin WPA3-downgrade (clones AP, evicts via CSA/BTM/deauth), WPS suite (PixieDust Null-Secret + Static-Secret, PBC plaintext-PSK extract on button press, resumable PIN brute-force with lock monitoring + known-PIN DB), WEP suite (ARP replay, ChopChop, fake auth, PTW).

## Hardware gate (why parked)

Requires **at least one supported USB adapter**. Onboard Intel/Qualcomm does nothing.

Common supported: ALFA AWUS036NHA (AR9271), AWUS036ACHM (MT7610U), AWUS036ACM (MT7612U), AWUS036AXML (MT7921AU), AWUS036ACH / AWUS1900 (RTL8812AU/RTL8814AU), TP-Link TL-WN722N **V1 only** (V2/V3 = different chip), Archer T2U Plus/T3U Plus, Panda PAU05/06/09, Netgear A9000 (MT7925U), ASUS USB-BE93 (RTL8922AU). Full table + per-device limits: [SUPPORTED-HARDWARE.md](https://github.com/derv82/wifit3/blob/master/docs/SUPPORTED-HARDWARE.md).

## Install (when hardware exists)

Upstream recommends prebuilt. Do NOT `uv sync` unless auditing/modifying.

```powershell
# Windows — verify hash first
# Release: https://github.com/derv82/wifit3/releases/latest
# Run wifit3-windows-x64.exe, click START, accept one-time UAC (installs WinUSB for that dongle)
```

```bash
# Linux (non-sudo run)
chmod +x wifit3-linux-x64 && ./wifit3-linux-x64
# One-time: app prompts via pkexec/sudo for udev + modprobe blocklist in /etc/modprobe.d/

# macOS
xattr -d com.apple.quarantine wifit3-macos-universal2
chmod +x wifit3-macos-universal2
./wifit3-macos-universal2

# From source (audit path)
uv sync
uv run wifit3

# Self-build
uv run pyinstaller wifit3.spec --noconfirm --clean
# -> dist/
```

Uninstall/restore adapter to OS stack: splash screen -> select card -> `Uninstall` -> accept elevation -> unplug/replug. Linux deletes udev/modprobe rules; Windows uninstalls WinUSB binding + PnP rescan.

VirtualBox: add device to USB Filters *before* plugging in.

## Caveats

- BETA, operates on USB hardware registers without kernel guardrails — author's disclaimer.
- PyInstaller exe will likely trip Defender/AV — expected, verify sha256.
- One-time driver bind hijacks the dongle from the OS Wi-Fi stack (by design).
- Legal: own/authorized networks only.
- No MCP surface — standalone TUI exe, not a library. Fleet integration (if ever) would be a wrapper MCP, not native.

## Next step when un-parked

1. Buy/borrow one supported dongle (e.g. ALFA AWUS036ACM or Panda PAU09 for dual-band).
2. Test prebuilt on spare host or VM with USB passthrough first, not Goliath main.
3. If it earns a place, consider `wifit3-mcp` wrapper proposal.

## References

- Repo: https://github.com/derv82/wifit3
- Releases: https://github.com/derv82/wifit3/releases/latest (v0.3.4 notes: ZeroCD auto-eject, MT7921AU loud fail on firmware mismatch)
- Porting methodology: https://github.com/derv82/wifit3/blob/master/docs/porting/METHODOLOGY.md
- Credits (Linux driver authors): https://github.com/derv82/wifit3/blob/master/docs/CREDITS.md
- Firmware licenses: https://github.com/derv82/wifit3/blob/master/docs/FIRMWARE.md

---
*Last updated: 2026-09-29 — parked, no adapter. Revisit on hardware purchase.*
