# HomeCraft - Product Requirements Document (PRD)

**Project:** HomeCraft (`D:\Dev\repos\homecraft`, not yet created)
**Version:** 1.1.0-draft
**Date:** 2026-11-11
**Status:** Draft, all scoping decisions settled 2026-11-11 (section 12)
**Authors:** Claude (takeover), based on Antigravity's cut-off draft
**Parent framework:** [RUST_ARTCRAFT_STANDARD.md](../../standards/RUST_ARTCRAFT_STANDARD.md)
**UI standard:** [CRAFT_MENU_BAR_STANDARD.md](../../standards/rust-artcraft/CRAFT_MENU_BAR_STANDARD.md)
**Plan:** [TIERED_PLAN.md](TIERED_PLAN.md)

## 0. Provenance and what changed from the Antigravity draft

Antigravity (agy) drafted `HOMECRAFT_PRD.md` in its scratch area
(`C:\Users\<user>\.gemini\antigravity\brain\6ac58df7-...\HOMECRAFT_PRD.md`, 33 KB,
2026-11-11 15:24) and timed out before creating the repo. Kept from that draft:
Tier 1-2 validate against Sandra's Vienna LAN hardware plus a `Vendor::Demo` oracle
first; storage is `rusqlite`; the repo lives at `D:\Dev\repos\homecraft`.

Changed:

| # | agy draft | This PRD | Why |
|---|---|---|---|
| 1 | Build drivers, command bus, MCP loop and mocks from scratch | **Seed from `rust-devices-mcp`** (4 crates, ~9.7k LOC, 58 tests, drivers live-verified 2026-10-17) | It is the Pure-Rust pilot; rebuilding loses live-verified fixes (Tapo mW to W, Ring OAuth 406, JPEG APP0). |
| 2 | Page sidebar plus a menu bar | **Pattern 2 workstation** with the Session / Commands non-file menu bar | `CRAFT_MENU_BAR_STANDARD.md` section 2.1 note and section 5. |
| 3 | Optional Home Assistant bridge | **No HA at all.** HomeCraft replaces Home Assistant | Sandra 2026-11-11: HA is legacy; nothing runs on Goliath. |
| 4 | ~40 brands, Matter/BLE/Zigbee in v1 | v1 = hardware on the LAN plus local protocols; radio ecosystems on a dated roadmap | No hardware means no oracle. |
| 5 | `homecraft_device_set_power` names | Dotted command ids (`device.set_power`) across CLI, MCP and UI | `CRAFT_COMMAND_BUS.md`. |
| 6 | Per-app LLM config | `craft-ai-core` only | `CRAFT_LLM_PROVIDER_STANDARD.md`. |

## 1. Problem

Home control in the fleet is spread over three repos and two stacks:

- **`devices-mcp`** (Python/FastMCP + React): the broadest surface (~40 portmanteau
  modules), heavy (interpreter + webview), config debt, partly stubs (the AI scene
  analyzer returns a fixed `"living_room"`), last real work 2026-10-25.
- **`rust-devices-mcp`**: the lean Pure-Rust pilot (50-70 ms cold boot, ~16.8 MB
  installer, live-proven drivers), but a pre-craft-standard transition repo: no home
  model, no rules, no onboarding, Pattern 1 dashboard UI.
- **`home-assistant-mcp`**: a thin REST wrapper around a Home Assistant server that no
  longer runs.

Onboarding a device still means hand-editing `config.yaml` / `.env`, and there is no
always-on automation runtime in the fleet since HA was dropped.

## 2. Product

**HomeCraft is the home's craft app and the fleet's Home Assistant replacement.**
One Pure-Rust workspace that knows the house (rooms, devices, scenes, rules, events,
history), talks to the devices directly over the LAN, runs automations headless as an
always-on service, and exposes every capability identically to the desktop UI, the
CLI (`--json`) and MCP stdio.

It absorbs `rust-devices-mcp` and the in-scope parts of `devices-mcp`. At cutover all
three predecessor repos (`rust-devices-mcp`, `devices-mcp`, `home-assistant-mcp`) get
a superseded banner and are archived, not deleted.

Fit test (craft-fleet hub): single model (the home graph), headless verbs, files
in/out (home profile, snapshots, exports), three obvious recipes (energy report,
camera sweep, onboarding dry run). Passes.

### 2.1 What "replaces Home Assistant" means for v1

The HA jobs Sandra actually used, and where each lands:

| HA job | HomeCraft v1 |
|---|---|
| Always-on hub | `homecraft-mcp watch` as a Windows service (installed via wincraft NSSM) |
| Device integrations | Native drivers (section 6) |
| Automations | Rules engine (6.6) with dry-run and event log |
| Dashboards | Pattern 2 workstation (section 8) |
| History / recorder | `home.db` telemetry with rollups and retention |
| Energy dashboard | Energy view, `energy.*` commands, anomaly flags |
| Notifications | `bridge.event` (aiwatcher), `bridge.speak` (speech-mcp), webhook |
| Presence | Phone-on-Wi-Fi presence (6.8) |
| Backup | Session > Backup Home (home.db + profile export; vault excluded) |

Not in v1 and on the roadmap (section 10): Zigbee, Matter/Thread, BLE, remote access
from outside the LAN, mobile app.

## 3. Users and jobs

1. **Sandra at the desk:** see the flat at a glance, toggle things, glance at cameras,
   check energy and climate, read what happened overnight.
2. **Sandra adding a device:** scan, pick it, 2-4 guided steps, land it in a room.
3. **An agent:** `device.list`, `energy.summary`, `camera.describe_scene`,
   `scene.apply` over MCP, behind the same safety fences as the UI.
4. **The service:** `watch` polls, records, evaluates rules, raises alerts, 24/7.

## 4. Architecture

Standard ArtCraft 4-crate seam, renamed from `rust-devices-mcp`:

```text
homecraft/
  Cargo.toml            virtual workspace, [workspace.lints.clippy] 5 denies
  justfile              check / test / fmt-check / clippy / ci / run-mcp / smoke / release
  AGENTS.md  HELP.md  KIBITZ.md  CHANGELOG.md  README.md  LICENSE-MIT  LICENSE-APACHE  CONTRIBUTING.md
  docs/  PRD.md  TIERED_PLAN.md  ARCHITECTURE.md  TOOLS.md  UI_PARITY.md  HANDOVER.md
  docs/brochure/  homecraft-brochure.{html,epub,pdf}
  installer/installer.nsi
  crates/
    homecraft-core    L1  home graph, drivers, discovery, onboarding, rules, vision, Command bus, i18n
    homecraft-store   L1  rusqlite (WAL) home.db: registry, telemetry + rollups, events; keyring vault
    homecraft-mcp     L2  clap CLI (--json) + `mcp` stdio server (2024-11-05) + `watch` service loop
    homecraft-app     L3  eframe/egui 0.37 Pattern 2 workstation, calls dispatch in-process
```

Invariants (from `CONTAINMENT_AND_CRATES.md`):

- `#![forbid(unsafe_code)]` per crate; `unwrap_used`, `expect_used`, `panic`, `todo`,
  `unimplemented` all `deny` at workspace level.
- One door: `homecraft_core::dispatch(Command) -> Result<Value, HomeError>`. L2/L3 never
  touch device state directly. `dispatch_future_is_send` test stays.
- Hostile input fence on everything from the network.
- `mcp` stdout is pure JSON-RPC; logs to stderr only.
- Zero ports claimed; no HTTP server anywhere. `bridge.rs` is an outbound client.
- When the app and the `watch` service both run, they share `home.db` (WAL) and the
  app does not poll devices the service already polls; a lock row in `home.db` says
  who the active poller is.
- Secrets: explicit arg > OS keyring vault > env > `.env`. Never in logs, errors,
  JSON output, `home.db`, exports or UI snapshots.
- LLM and vision-language calls go through `craft-ai-core`; `llm.rs` is deleted.

## 5. The home model

- **Home** > **Floor** > **Room** > **Device** > **Entity** (capability instance).
- **Device:** stable id (uuid v5 of vendor + MAC or serial; IP is a changeable
  attribute), vendor, model, room, tags, `readonly`, `confirm_required`.
- **Capabilities:** `power`, `level`, `color`, `power_meter`, `energy_meter`,
  `temperature`, `humidity`, `co2`, `pressure`, `camera`, `doorbell`, `alarm_panel`,
  `climate_target`, `kettle`, `smoke_co`, `presence`.
- **Scene:** named list of `(device, capability, value)`, applied as a batch with
  per-step results.
- **Rule:** `when <trigger> [if <condition>] then <action>`. Triggers: time of day,
  sunrise/sunset (Vienna default), threshold for N minutes, device event (ding,
  motion, detection, smoke), presence change. Actions: scene, command, alert,
  `bridge.*`. No scripting language.
- **Event:** everything that happened (state change, motion, detection, alert, rule
  fired, onboarding), with ack state. This is the "logbook".

Persisted in `home.db`; JSON home profile export/import for backup and moving machines.

## 6. Functional requirements

### 6.1 Carry-over (Tier 0, byte-compatible)

- **FR-CAR-01:** Every `rust-devices-mcp` command keeps its id, params and output shape
  (`status`, `plug.*`, `camera.*`, `hue.*`, `netatmo.stations`, `ring.*`,
  `weather.now`, `bridge.*`, scan, video). Tool count verified at seed time (docs
  disagree: 18 vs 24).
- **FR-CAR-02:** Zero-config import of `devices-mcp` `config.yaml`, `hue_bridge.cache`,
  `.env`, `ring_token.cache`, writing into the registry.
- **FR-CAR-03:** All 58 existing tests pass under the new crate names.

### 6.2 Generic device layer (Tier 1)

- **FR-DEV-01:** `device.list {room?, capability?, online_only?}`, `device.get {id}`.
- **FR-DEV-02:** `device.set_power`, `device.set_level`, `device.set_color`, routed by capability.
- **FR-DEV-03:** `room.list`, `room.assign`, `scene.list`, `scene.save`, `scene.apply`.
- **FR-DEV-04:** `energy.now`, `energy.summary {period}`, `energy.top {limit}`.
- **FR-DEV-05:** `Vendor::Demo` home: deterministic 3-room flat for CI, first paint
  and brochure screenshots; output carries `"vendor": "demo"`.

### 6.3 Discovery and onboarding (Tier 2, hero feature)

- **FR-DIS-01:** `discover.scan {subnet?, timeout_s}` merges the existing TCP probe
  (`scan.rs`), mDNS/DNS-SD, SSDP M-SEARCH and a compile-time OUI table. Registered
  devices are marked, not re-offered.
- **FR-DIS-02:** Every result says how it was identified (`mdns`, `ssdp`,
  `http-probe`, `oui`, `port-guess`).
- **FR-ONB-01:** `onboard.start/step/finish/cancel` session state machine with
  timeouts and resume.
- **FR-ONB-02:** Guided flows: Hue (link-button countdown), Tapo plug/cam, Shelly,
  Kasa, Netatmo (refresh-token paste with dev-console link), Ring (+2FA),
  RTSP/ONVIF/URL camera, iKettle.
- **FR-ONB-03:** Pre-flight: reachability, one authenticated read, the "server on a
  plug?" question that sets `readonly`.
- **FR-ONB-04:** Room suggestion from names, never applied silently.

### 6.4 Cameras

- **FR-CAM-01:** Snapshot and live RTSP (retina + openh264), as today.
- **FR-CAM-02:** Cameras view mode with N tiles, per-tile frame rate cap.
- **FR-CAM-03 (Tier 4):** Tapo PTZ move and presets, ported from `devices-mcp` `ptz/`,
  if the camera on the LAN supports it.

### 6.5 Home appliances, safety sensors, climate (Tier 4, from devices-mcp)

- **FR-APP-01:** iKettle driver (status, boil, keep warm, stop), ported from
  `ikettle_management`; boil is `confirm_required` from MCP and rules.
- **FR-APP-02:** Appliance monitoring: per-plug normal power band learned from
  history; `energy.anomalies` flags a plug outside its band (fridge stopped, heater
  left on). Replaces `appliance_monitor_management`.
- **FR-APP-03:** Climate: Netatmo station and valves (read + set target), Open-Meteo
  outdoor reference; `climate.summary` per room.
- **FR-APP-04:** Nest Protect smoke/CO: port the `devices-mcp` `nest_protect` access path
  if it works live (Google's official Device Access API does not expose Protect);
  otherwise a dated `down` receipt and roadmap entry. Smoke/CO events are always
  `urgency: critical` alerts.
- **FR-APP-05:** Sensor health: stale reading, low battery, offline device become
  events (replaces `sensor_health` and `alerts_management`).

### 6.6 Rules, events, alerts and the service (Tier 4)

- **FR-RUL-01:** `rule.list`, `rule.save`, `rule.enable`, `rule.test {id}` (dry run).
- **FR-RUL-02:** Rules may not target `confirm_required` actions in v1.
- **FR-EVT-01:** `event.list {since?, kind?, unacked_only?}`, `event.ack {id}`;
  retention configurable, default 90 days raw.
- **FR-SVC-01:** `homecraft-mcp watch` runs polling, rollups, rules, alerts and
  vision triggers headless; installed as a Windows service through wincraft's NSSM
  tooling (documented, not reimplemented). `homecraft-mcp watch --status` reports
  health for the app status bar and fleetwatcher.
- **FR-SVC-02:** Service restart loses nothing: rule timers and threshold windows are
  rebuilt from `home.db`.

### 6.7 Vision (Tier 4 and Tier 5)

`devices-mcp`'s scene analyzer is a stub and is not ported. Vision is built fresh on
frames HomeCraft already decodes.

- **FR-VIS-01 (Tier 4) Motion:** pure-Rust frame-difference detector (downscaled
  grayscale, per-camera sensitivity and ignore masks), plus ONVIF motion events and
  Ring dings, normalized into one `motion` event. `motion.events`, `motion.configure`.
- **FR-VIS-02 (Tier 4) Scene description:** `camera.describe_scene {camera, question?}`
  via `craft-ai-core`, default local Ollama Gemma 4 12B multimodal; returns text,
  model id, latency. No model configured means a typed `VisionUnavailable` error.
- **FR-VIS-03 (Tier 5) Detection:** ONNX detector (person, car, bicycle, dog, cat,
  package-like) via `ort`, CUDA on the 4090 with CPU fallback, cargo feature
  `vision-onnx`. Runs on motion events only. `vision.detect`; detections stored as
  events with boxes; overlay in the Cameras view.
- **FR-VIS-04 (Tier 5):** Detection triggers in rules ("person at the front door
  22:00-06:00").
- **FR-VIS-05:** Weights outside the repo; `vision.models` lists them; permissive
  licence only (RT-DETR or YOLOX, Apache-2.0; not Ultralytics AGPL-3.0 weights).
- **Deferred:** embeddings / similarity search, NVR recording. **Not planned:** face recognition.

### 6.8 Presence (Tier 4)

- **FR-PRS-01:** Presence per person from phone MAC/IP seen on the LAN (ARP table plus
  ping), with a grace period to absorb phones sleeping their Wi-Fi. `presence.status`.
  Usable as a rule trigger ("everyone away: plugs X off").
- **FR-PRS-02:** Presence data never leaves the machine and is not in MCP output
  unless a tool asks for it explicitly.

## 7. Safety (sharp edge: actuators, the front door, heat)

| Fence | Rule | Proof |
|---|---|---|
| `readonly` | State changes on a readonly device return `HomeError::ReadOnly` from every path (CLI, MCP, UI, scene, rule) | test per path |
| `confirm_required` | Ring alarm disarm, kettle boil, climate targets above 26 C, toggling a plug above a set wattage need `confirm: true` (MCP/CLI) or a modal (UI) | call without confirm changes nothing |
| No siren | `ring.alarm` never sounds the siren | existing test |
| `sim` mode | `--sim` / `HOMECRAFT_SIM=1` routes every actuator to Demo; CI and democraft always sim | `just ci` has no network |
| Rules can't escalate | No `confirm_required` targets in rules (v1) | rule.save validation test |
| Frames stay local | Snapshots go to a cloud vision model only if one is configured and the camera is opted in | refusal test |
| Secrets | Never in stdout JSON, logs, errors, `home.db`, exports, UI snapshots | redaction test over `device.get` + export |
| Critical alerts | Smoke/CO and "plug over limit" alerts cannot be muted by rules | test |

## 8. Desktop workstation (`homecraft-app`)

Pattern 2 viewport-centric workstation. HomeCraft is a non-file, service-oriented app,
so per `CRAFT_MENU_BAR_STANDARD.md` section 2.1 the `File` menu is replaced by
`Session` and the baseline menus are Edit, Add (the standard's Insert/Add), View,
Commands and Help. Spelled `Commands` to match the shipped craft apps (celcraft,
databasecraft, moneycraft, travelcraft).

```text
+--------------------------------------------------------------------------------------------+
| Session  Edit  View  Add  Device  Automate  Commands  Window  Help     [En] [sun/moon] 0 unsafe |
+--------------------------------------------------------------------------------------------+
| [Home] [Floorplan] [Cameras] [Energy] [Climate] [Events]   quick row = shortcuts into View |
+---------------+-------------------------------------------------------+-------------------+
| TOOLBOX       |  VIEWPORT (persistent, never unloaded)                | INSPECTOR         |
| Home tree     |  Home: device cards by room  [Cards|List|JSON] filter | selected device   |
|  Wohnzimmer   |  Floorplan: 2D rooms, drag devices in                 | state, caps       |
|  Kueche       |  Cameras: video wall, motion/detection overlay        | actions, readonly |
|  Buero        |  Energy: live W, kWh, anomalies                       | history sparkline |
| Discovered(3) |  Climate: rooms, Netatmo, outdoor                     | describe scene    |
| Scenes, Rules |  Events: logbook, ack, filters                        |                   |
+---------------+-------------------------------------------------------+-------------------+
| service: running | 14 devices, 1 offline | 412 W | 2 unacked alerts | sim: off | 60 FPS     |
+--------------------------------------------------------------------------------------------+
```

### 8.1 Menus (front bookend, domain middle, tail bookend)

| Menu | Items (hotkey) |
|---|---|
| **Session** | Open Home Profile... (Ctrl+O), Save Home Profile (Ctrl+S), Export Profile... (Ctrl+E), Import from devices-mcp..., Backup Home..., Restore Home..., sep, Service: Start / Stop / Status, Simulation Mode (toggle), sep, Quit (Ctrl+Q) |
| **Edit** | Undo (Ctrl+Z), Redo (Ctrl+Y), sep, Cut, Copy, Paste, Select All, sep, Rename (F2), Delete (Del), sep, Preferences... (Ctrl+,) |
| **View** | the six view modes (Ctrl+1..6), sep, Zoom In / Out / Reset (Ctrl+= / Ctrl+- / Ctrl+0; Ctrl+mouse wheel anywhere), sep, Cards / List / JSON (for list-like views), Show Offline Devices, Show Readonly Badges, sep, Interface Theme > Dark / Light / System, Language > 7 locales |
| **Add** | Scan Network (F5), Add Device Wizard... (Ctrl+N), sep, Add Room..., Add Floor..., Add Scene..., Add Rule..., Add Person (presence)... |
| **Device** | Toggle Power (Space), Set Level..., Set Color..., Snapshot (Ctrl+Shift+S), PTZ..., sep, Mark Read-Only, Require Confirmation, Move to Room..., Re-run Pre-flight, Remove Device |
| **Automate** | Apply Scene (1-9), Test Rule (dry run), Enable/Disable Rule, sep, Acknowledge Alert (A), Acknowledge All |
| **Commands** | Describe Scene (current camera), Run Detection Now, Recompute Energy Rollups, Learn Appliance Bands, Check Sensor Health, Ping All Devices, Export Diagnostics... |
| **Window** | Reset Panel Layout, sep, Toolbox, Inspector, Status Bar, Event Log Dock, Onboarding Wizard |
| **Help** | Command Palette... (Ctrl+Shift+P / Ctrl+K), Keyboard Shortcuts... (F1 / Ctrl+/), Project Files & Docs..., Licenses & Notices..., About HomeCraft |

Rules:
- `switch_on_hover` between open top menus; tooltips show hotkeys; dialogs non-modal
  except the confirm modal for `confirm_required` actions.
- Every menu item dispatches a registered `Command`, so it also appears in the Command
  Palette. `--smoke` dispatches every menu command against the Demo home headless.
- Extension contract (standard section 5): a new capability adds a `View`/`Window`
  toggle, a Toolbox/Inspector entry, optionally a quick-row button, and a `Command`.
  Never a new page in a sidebar.

### 8.2 Visual rules

- High contrast in both themes; no light grey text on white; hairline panel and card
  borders; vector sun/moon toggle in the top bar.
- Ctrl+mouse-wheel zoom on the whole UI, persisted.
- List-like views (Home, Events, Discovered) use the fleet Cards / List / JSON
  switcher with live filter, numeric-aware sort, pagination and CSV / MD / TXT / JSON
  export.
- Charts are zero-dep painter charts reading `home.db` (as in rust-devices-mcp today).
- No network call on the UI thread; offline devices render as offline, never as a
  frozen frame.
- 7 locales (En, De, Fr, Es, Ja, Ko, Zh) in `homecraft-core/src/i18n.rs`; De and Ja
  reviewed by Sandra.
- Brochure PDF/EPUB buttons in Help and About.
- `egui_kittest` goldens per view mode in both themes; tofu glyph guard.

## 9. Agent surface

- CLI: every command has a subcommand with `--json`; `commands --json` and
  `describe <id>` list the registry.
- MCP: `tools/list` generated from the same registry; read-only vs mutating and
  `confirm` requirements stated in each description.
- `HELP.md` and `docs/TOOLS.md` generated from `commands --json` and checked in.

## 10. Scope boundaries

**In v1:** Tapo plugs/cams, Kasa, Shelly, Hue, Netatmo, Ring, iKettle, Nest Protect
(if its path works), USB/RTSP/ONVIF/URL cameras, Open-Meteo, presence, rooms,
scenes, rules, events, energy and appliance anomalies, vision (motion, scene
description, optional ONNX detection), the `watch` service.

**Roadmap after v1 (dated in the plan when picked up):**
1. v1.1: WLED, Nanoleaf, Govee LAN, LIFX, ESPHome native API, Tasmota (local, cheap).
2. v1.2: Zigbee via a USB coordinator (the biggest HA-replacement gap; needs hardware).
3. Later: Matter/Thread, BLE, Sonos/Cast media, remote access, mobile companion
   (admiral-pager chassis).

**Where each devices-mcp module goes:**

| devices-mcp module | Destination |
|---|---|
| tapo, hue, ring, netatmo, shelly, camera, usb, ptz, energy, lighting, climate, security, weather | HomeCraft (most already in rust-devices-mcp) |
| ikettle, kitchen, appliance_monitor, sensor_health, alerts, messages, nest_protect, motion | HomeCraft (Tier 4) |
| ai_analysis / scene_analyzer, vision/dinov3 | HomeCraft vision, rebuilt (6.7); stubs dropped |
| audio ("Alexa 2": TTS, announce, VLC) | speech-mcp / speechcraft; HomeCraft calls `bridge.speak` |
| dymo, supvan label printers | makercraft (physical output hardware) |
| medical (USB microscopes, document scan) | makercraft |
| thermal (MLX90640 sensor) | makercraft HAL; HomeCraft may read its values later |
| sdr (RTL-SDR capture) | makercraft; HomeCraft may later consume decoded 433 MHz sensor readings |
| robotics (Moorebot) | robotcraft |
| grafana | dropped; in-app charts replace it |
| home_assistant_management | dropped; HomeCraft replaces HA |

**Neighbours:** wincraft (installs `watch` as a service), speech-mcp/speechcraft
(TTS), aiwatcher (event feed), craft-ai-core (LLM and VLM), fleetwatcher (reads
`watch --status`).

## 11. Non-functional requirements

- **NFR-01:** 6-gate merge bar on every tier closure.
- **NFR-02:** Cold CLI/MCP boot under 100 ms (today 50-70 ms).
- **NFR-03:** `homecraft-mcp` under 15 MB (default features), app under 40 MB, installer
  under 25 MB, app idle RAM under 60 MB with the video wall closed, `watch` idle
  RAM under 30 MB.
- **NFR-04:** `watch` survives device outages, network loss and reboots; runs 7 days
  without restart in the Tier 6 soak.
- **NFR-05:** `just ci` needs no network, hardware, credentials or model weights.
- **NFR-06:** AGENTS.md: LF line endings only (`.gitattributes` `* text=auto eol=lf`),
  single trunk `main`, no leftover agent branches, no em dash characters, commits of
  10 files or fewer, one repo per commit.
- **NFR-07:** Release: local cut on Goliath; assets are the NSIS installer, the plain
  `homecraft.exe` and `homecraft-mcp.exe`, and `SHA256SUMS.txt`. No zip. Sandra
  publishes; agents do not.

## 12. Decisions (all settled 2026-11-11)

1. **Absorb, later archive.** All `rust-*-mcp` repos are transition repos from before
   the ArtCraft craft app standard. HomeCraft is seeded from `rust-devices-mcp`; it is
   archived after cutover. No cross-repo dependency on it.
2. **devices-mcp leftovers** go where section 10 says (Claude's call, delegated by Sandra).
   `devices-mcp` is archived after cutover once makercraft/robotcraft/speech have
   their pieces or have explicitly declined them.
3. **No Home Assistant.** Nothing runs on Goliath; HomeCraft replaces HA, no bridge is
   built, `home-assistant-mcp` is archived at cutover.
4. **Menu bar:** non-file Session / Edit / View / Add / Device / Automate / Commands /
   Window / Help, per the standard.

## 13. Definition of done (v1.0.0)

1. Everything `rust-devices-mcp` could do, HomeCraft does with the same command ids.
2. A new Hue bridge or Tapo plug goes from "plugged in" to "in a room, controllable"
   in under 60 s with no typing except credentials, timed on the real LAN.
3. `watch` runs as a service for a 7-day soak with rules firing and no restarts.
4. Live verification table re-run on Sandra's LAN, every row dated, `sim`/`down`
   receipts where hardware is missing.
5. Craft minimum standard met: README with status block, HELP.md, PRD, CHANGELOG,
   KIBITZ.md, docs/, tests, justfile, CLI, LICENSE + CONTRIBUTING, brochure, one green
   democraft recipe.
6. Menu bar checklist (standard section 4) ticked with goldens and screenshots in
   `docs/UI_PARITY.md`.
7. `rust-devices-mcp`, `devices-mcp` and `home-assistant-mcp` carry superseded banners
   pointing at HomeCraft and are archived; MCP client configs point at
   `homecraft-mcp mcp`.
