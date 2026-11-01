# wifi-mcp — SPEC (draft)

**Status:** draft · **Date:** 2026-09-29 · **Owner:** Sandra
**Related:** [integrations/wifit3.md](../integrations/wifit3.md) (parked auditor reference) · `projects/yahboom-mcp/` · `projects/raspberrypi-mcp/`

## 1. Goal

A FastMCP server for **robot Wi-Fi connectivity management** — not auditing.
Primary use case: **robot AP hopping** between 2 APs in test space (Vienna lab),
then general fleet link health (Pi robots first, Goliath/Windows second).

**Non-goals (v0.1):** no monitor mode, no injection, no handshake/PMKID/deauth/WPS
cracking. That is wifit3's job (parked, needs dongle + separate iface). wifi-mcp
never reimplements `src/wifit3/chips/` mini-drivers.

## 2. Hardware recommendation

**Buy: 2x Panda PAU09 N600 (Ralink RT5572, 2.4/5 GHz, 2x external antennas).**

| Why PAU09 | Detail |
|---|---|
| In-kernel driver | `rt2800usb` on Pi Bookworm — no DKMS, survives `apt upgrade` |
| Dual-band | Lets 2 APs test real policy: 5 GHz preferred vs 2.4 GHz fallback |
| Antennas | ~2-3x usable range vs Pi PCB antenna; decisive for robots low to ground |
| wifit3-compatible | RT5572 is on wifit3's supported list — same dongle can later serve as audit iface (`wlan2`) |
| Power | ~350-500 mA — Pi 4/5 USB can drive one directly; two dongles or +LIDAR → powered hub |

**Why not the others:**
- PAU05/06 (RT5370/72): cheap, in-kernel, but 2.4 GHz only — hopping test degrades to RSSI-only, no band-steering signal.
- ALFA NHA (AR9271): great sensitivity, but 2.4-only, EOL, overpriced used in EU.
- ALFA ACM/ACH (MT7612U/RTL8812AU): good RF, but MT76 USB / RTL DKMS on Pi is fragile — avoid on field robots.
- RTL8821AU/CU trinkets (Archer T2U Nano etc): DKMS hell, no antenna — worst robot choice.

**EU sourcing:** Panda is US; on Amazon.de search `Panda PAU09 N600` (usually ~35-45 EUR via intl seller) or `ALFA AWUS036NH` fallback if impatient. Avoid no-name `RTL8188EUS` sticks — fine for wifit3 audit, deaf for roaming.

**Test with 2 APs:** same SSID on both APs, different BSSIDs/channels (e.g. AP1 ch36 5 GHz near dock, AP2 ch11 2.4 GHz far corner). Robot should prefer AP1 when close, hop to AP2 on signal death, hop back with hysteresis. Log everything.

## 3. Architecture

- **Runtime:** FastMCP `>=3.4.4,<4`, Python `uv`, portmanteau tool `wifi` with `operation` enum (fleet TOOL_DESIGN_STANDARDS).
- **Transports:** stdio (Claude Desktop) + SSE/HTTP for robot-side daemon.
- **Platform backends (v0.1):**
  - Linux primary: NetworkManager (`nmcli`) if present, else `wpa_supplicant` via `wpa_cli`. Pi Bookworm ships NM — standardize on `nmcli`.
  - Windows secondary: `netsh wlan show networks/interfaces` parse (Goliath link health only, no hopping).
  - macOS: deferred.
- **Concurrency:** watchdog runs in background thread; tools query state, never block on scans. No 10 s poll loops in tool bodies (RAG_OPERATIONS_STANDARD).
- **Prefab:** `@mcp.tool(app=True)` status card: current BSSID/RSSI/bitrate/IP + last 5 hops.
- **Sampling:** `ctx.sample()` for `rank_aps` explanation only; roam decision itself is deterministic policy (no LLM in the hot loop).

## 4. Tool surface (v0.1)

`wifi(operation=...)`:

| op | Args | Returns |
|---|---|---|
| `scan` | `iface, band_filter?` | BSSID, SSID, freq/band, channel, RSSI, security, known? |
| `status` | `iface` | iface, SSID/BSSID, RSSI, bitrate, IP, backend (nmcli/wpa/netsh) |
| `signal_poll` | `iface, seconds, interval` (cap 10 s) | RSSI timeseries + dropouts |
| `rank_aps` | `iface, policy?` | ordered candidates + reason strings (5 GHz bonus, known-SSID only, hysteresis applied) |
| `hop` | `iface, bssid, confirm` | disconnect/connect via nmcli, DHCP wait, fallback to last-good on failure; red-shelf gate (confirm token) |
| `watchdog_start/stop/config` | `iface, rssi_floor (-70 dBm), hysteresis (+8 dB), dwell_s (10), cooldown_s (60)` | background auto-hop; writes event log |
| `events` | `limit` | timestamped hop/scan/fail history |
| `allowlist` | `list/set` | which ifaces wifi-mcp may touch — **never a wifit3-bound iface** |

Policy defaults: hop only if candidate RSSI > current + 8 dB sustained for `dwell_s`; cooldown 60 s after any hop; never hop when teleop/dock-critical flag set unless RSSI < -80 dBm (dead-link override).

## 5. Safety / guards

- Interface allowlist at startup (e.g. `WIFI_IFACES=wlan1`). Refuse to manage WinUSB/libusb-bound audit ifaces.
- `hop` requires explicit confirm (fleet red-shelf pattern) unless watchdog auto-hop within configured policy.
- Dry-run mode: `rank_aps` + `hop(dry_run=True)` for planning without touching radio.
- `.bak` + checkpoint commits per fleet rules; max 5 files per commit.
- Vienna flat RF: record AP MACs/channels in `.env` (gitignored), never commit PSKs.

## 6. Fleet integration

- **yahboom-mcp:** consumes `status`/`events` for teleop quality overlay; sets no-hop flag during docking.
- **raspberrypi-mcp:** sibling bench tool (GPIO/cam); wifi-mcp owns radio only.
- **tailscale-mcp:** overlay IP survives L2 hop — recommend Tailscale on robot so agent session persists across BSSID change.
- **observability-mcp:** hop events → session log.

## 7. Test plan (2 APs)

1. `scan` from dock: both BSSIDs visible, record baseline RSSI.
2. `signal_poll` walk from AP1 to AP2: verify RSSI gradient sane.
3. `rank_aps`: at AP2 corner, AP2 ranks first with reason.
4. Manual `hop` AP1→AP2→AP1: IP renews, Tailscale session survives, cooldown enforced.
5. `watchdog_start`, walk the path: auto-hop fires once per direction max, no flap. `events` shows dwell respected.
6. Dead-link pull (unplug AP1): fallback to AP2 within `dwell_s + DHCP`.

## 8. v0.2 (gated, not now)

- Second dongle as wifit3-bridge iface: `audit_scan` subprocess wrapper (requires PAU09 #2 + prebuilt, parked per wifit3.md).
- `pandas` capture analysis: load `.pcap`/`.hc22000` paths into signal/client summaries.
- ROS topic publish (`/wifi/status`) for nav-stack costmap weighting.

## 9. Open questions

1. Pi model + OS image (Pi 5 Bookworm + NM assumed — confirm)?
2. AP models / can both broadcast same SSID on different channels?
3. NetworkManager vs `wpa_supplicant`-only image?
4. Tailscale already on robot?
5. Port claim needed (backend N / frontend N+1 via `fleet-gate/claim_ports.py` at scaffold)?

---
*Next action: answer Q1-Q4, then scaffold to assfix-zero (NEW_REPO_BUILD_COMPLETE) — this SPEC is the build input, not the build.*
