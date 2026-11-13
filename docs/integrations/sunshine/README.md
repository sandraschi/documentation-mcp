# Sunshine + Moonlight - Low-Latency Remote Desktop for Goliath

Sunshine (LizardByte, MIT) is an open-source GameStream host. Moonlight clients
(free, open source, iOS/iPad app available) connect to it. Together they are the
interactive daily driver for remoting into Goliath from the iPad. RustDesk stays
as fallback + file transfer. See `../rustdesk/README.md` for the RustDesk side.

Status: evaluated 2026-10-09 on Goliath (RTX 4090, Tailscale running).
Install path verified via winget on this machine.

## Why Sunshine on this box

- The RTX 4090 carries 8th-gen NVENC with AV1: best quality per bitrate available,
  ideal for hotel/cafe uplinks from the iPad.
- Game-streaming stack: typically 10-30 ms on LAN, feels local for code scrolling,
  timelines, 3D viewports. RustDesk smears motion by comparison (tuned for static
  office screens).
- 4K / high-refresh / HDR to a Pro iPad. Clean low-latency audio passthrough.
- Tailscale is already Running on Goliath, so Moonlight reaches it anywhere with
  zero port forwarding: point the client at Goliath's tailnet address.

## NVENC cost - VRAM and compute

Short version: encoding a desktop stream costs essentially nothing on a 4090.

- NVENC is fixed-function hardware on the die, separate from CUDA cores. Encoding
  uses zero CUDA compute, so Blender renders, Comfy jobs, and local LLM inference
  lose no SMs to the stream.
- VRAM footprint is only the frames in flight (capture + reference buffers), on
  the order of tens of MB at 4K. Negligible against 24 GB.
- The only shared resource is memory bandwidth, imperceptible for desktop use.
  Total added load is roughly 1-3% GPU-adjacent (DXGI capture + encode).
- Consumer-driver concurrent-encode session limits exist but are irrelevant here:
  one remote session is one session.
- Edge case: if VRAM is pinned at 99%+ by a 24 GB model load, capture buffers can
  still squeeze in, but expect the odd stutter. Normal 4090 workloads never notice.

## Install (Goliath, verified)

```powershell
& "C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\winget.exe" install LizardByte.Sunshine
```

The installer registers firewall rules for the streaming ports. Web UI defaults to
`https://localhost:47990`. Reference ports: 47984 (HTTPS), 47989/47999/48010
(streaming), 47990 (UI). Over Tailscale none of these need public exposure.

## Pair the iPad

1. Install Moonlight from the App Store on the iPad.
2. Add Goliath by its Tailscale IP (or hostname if tailnet DNS resolves it).
3. Moonlight shows a PIN. Enter it in the Sunshine web UI under PIN pairing.
4. Pick the display + resolution. Touch acts as mouse; external keyboard/mouse
   via iPadOS work; Wake-on-LAN available for a sleeping Goliath.

## Headless note

If Goliath runs without a monitor attached, Windows may offer no usable
resolution to capture. Fixes in order of preference: dummy HDMI plug (cheapest,
zero software), or a virtual-display driver so Sunshine always has a 4K surface
regardless of physical outputs. Verify before calling the setup done: reboot
headless, connect from the iPad, confirm full resolution.

## Role split - the standing decision (2026-10-09)

| Job | Tool | Why |
|---|---|---|
| Daily interactive driving (code, Blender, Resolve, dashboards) | Sunshine + Moonlight | Latency + motion quality + HDR, rides NVENC for free |
| File transfer / remote file manager | RustDesk | Moonlight has none |
| NAT-hostile networks, dumb reliable reconnect | RustDesk | ID + password, no tailnet dependency |
| Tailscale itself down | RustDesk relay | Independent path |
| NoMachine | Uninstall | Contributes nothing the two above don't cover; its 2022 `nxusbh` virtual-USB driver sat in Error state and is prime suspect for the 0xCA green screens of Oct 2026 |

## Troubleshooting

- Black screen on connect: headless with no display surface. See Headless note.
- Stutter only under full VRAM load: expected edge case, shed model/client load.
- Cannot reach host remotely: confirm Tailscale Running on Goliath
  (`Get-Service Tailscale*`) and use the tailnet IP, not the LAN IP.
- `windbg_analyze`/`analyze_minidump` for any GSOD during testing live in
  `sysadminops` (system-admin-mcp): `list_crash_dumps` then triage-parse.

## Agent API notes (probed live 2026-10-09, Sunshine 2026.914.233613)

For agents (Fritz, opencode sessions): everything below was verified with
read-only GETs against the running Goliath instance. No POST was sent, no
pairing attempted, credentials file never read.

- Base URL is `https://<host>:47990`, HTTPS only with a self-signed cert.
  Plain HTTP is refused at connection level. Local probes must skip cert
  verification.
- There IS a JSON API router: unknown paths (e.g. `/api/clients`,
  `/api/version`) answer `{"error":"Not Found","status_code":404}`.
- Unauthenticated browser routes (`/api/apps`, `/api/config`, `/api/logs`,
  `/api/pin` via GET) return the login SPA shell (3286 bytes, identical).
  Conclusion: state-changing calls need the web-UI credentials created at
  first run (session auth). Do NOT script pairing - pair once by hand in the
  web UI, then treat the host as configured.
- Health check without credentials (all verified, cheapest first):
  1. Processes `sunshine` + `sunshinesvc` alive.
  2. TCP 47984/47989/47990 in Listen state owned by the sunshine PID.
  3. `C:\Program Files\Sunshine\config\sunshine.log` growing on activity.
- Config on disk (no API needed to read intent):
  - `C:\Program Files\Sunshine\config\apps.json` - published apps. Default
    ships two entries: `Desktop` (full desktop, no command) and
    `Steam Big Picture` (`steam://open/bigpicture` with undo + auto-detach).
    Agents launching a Moonlight session pick one of these names.
  - `sunshine.conf` - 0 bytes on fresh install means all defaults. Non-empty
    means someone tuned it; diff before overwriting.
  - `credentials` file exists after first-run setup. Never read it, never log
    it, never commit it.
- Restart path (no Sunshine API needed): `sysadminops` service/process ops,
  or `sunshinesvc` process recycle. If Moonlight cannot connect but ports
  listen, recycle before touching config.
- Upstream API reference (unverified by fleet, consult before scripting):
  `https://docs.lizardbyte.dev/projects/sunshine/` - confirm every endpoint
  against the running version before use; the probed 404s above prove paths
  shift between releases.

---
*Maintained by: Sandra + fleet agents. Last verified: 2026-10-09.*
