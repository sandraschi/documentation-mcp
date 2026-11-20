# HomeCraft - Tiered Execution Plan

**Version:** 1.1.0-draft
**Date:** 2026-11-11
**PRD:** [PRD.md](PRD.md)
**Method:** ArtCraft tiered delivery ([CONTAINMENT_AND_CRATES.md](../../standards/rust-artcraft/CONTAINMENT_AND_CRATES.md) Layer 4), seeded via `repconv` shadow-then-swap ([REPCONV_SOP.md](../../patterns/REPCONV_SOP.md))
**Total estimate:** about 1-2 hours of agent work per tier, roughly a working day end to end (re-baselined 2026-11-11: the first day-based estimate was out by about 100x). Wall-clock is bounded by the three LAN sessions with Sandra present and the 7-day service soak, not by coding.

Every tier closes on the 6-gate bar and a CHANGELOG line. No checkbox is ticked until
its gate output has been run and recorded in `HANDOVER.md`. A gate that examined
nothing is a failure, not a pass.

```text
Tier 0  Seed from rust-devices-mcp              v0.1.0   ~30 min
Tier 1  Home model + generic device layer       v0.2.0   ~1-1.5 h
Tier 2  Discovery + onboarding engine           v0.3.0   ~1-1.5 h   (+ LAN session)
Tier 3  Pattern 2 workstation UI                v0.4.0   ~1.5-2 h
Tier 4  HA replacement: service, rules, events,
        appliances, presence, motion, VLM, PTZ  v0.5.0   ~2 h       (+ LAN session)
Tier 4.1 Energy charts + alert board            v0.5.1   ~1 h       (done 2026-11-17)
Tier 4.2 Climate history, overview, camera fixes v0.5.2   ~1 h       (done 2026-11-17)
Tier 5  ONNX detection                          v0.6.0   ~1 h       (+ LAN session)
Tier 6  Release, docs set, soak, cutover        v1.0.0   ~1 h       (+ 7-day soak)
```

## Tier 0 - Seed (v0.1.0, ~30 min)

Goal: a renamed, green copy of `rust-devices-mcp` with the craft repo skeleton. No new features.

- [x] Create `D:\Dev\repos\homecraft`, `git init -b main`, `.gitattributes`
      (`* text=auto eol=lf`), `.gitignore` (target, *.bak, *.cache, *.exe, .env, *.onnx).
- [x] Copy the 4 crates from `rust-devices-mcp` HEAD (SHA recorded in CHANGELOG); rename
      `devices-*` to `homecraft-*`, binaries `homecraft` and `homecraft-mcp`.
- [x] `#![forbid(unsafe_code)]` per crate root.
- [x] Verify the real MCP tool count via `tools/list`; write it in README.
- [x] `AGENTS.md` from rust-devices-mcp plus: LF only, single trunk `main`, no leftover
      agent branches, no em dash characters, 10 files or fewer per commit, one repo per commit.
- [x] README with Status block (DOES-TODAY / NEXT-WEEK / NON-GOALS), CHANGELOG,
      LICENSE-MIT, LICENSE-APACHE, CONTRIBUTING, justfile (`check`, `test`, `fmt-check`,
      `clippy`, `ci`, `run-mcp`, `smoke`).
- [x] Move PRD.md and TIERED_PLAN.md into `docs/`; this hub folder keeps a pointer README.
- **Gate:** 6 gates; 58 carried tests green; stdio probe byte-clean; CLI
  `plug-stats --vendor demo --json` identical to rust-devices-mcp (diff recorded).

## Tier 1 - Home model and generic device layer (v0.2.0, ~1-1.5 h)

- [x] `homecraft-store` schema v2 (on top of the inherited v1 telemetry tables): rooms,
      devices, scenes, events, settings; versioned migrations; WAL; connection per call so
      `dispatch` stays `Send`. **Deferred to Tier 4 (with the service that needs them):**
      rules, persons, 1m/1h/1d rollup tables, poller lock row. Floors are a room attribute.
      Entities are folded into device capabilities (one row per device).
- [x] Vault on `keyring` (inherited, service renamed, legacy read fallback); env/.env fallbacks.
- [x] `home.import_fleet` writes the devices-mcp inventory into the registry (idempotent,
      keeps operator edits; Tapo bulbs/strips listed as plugs are imported as lights).
- [x] Commands (29, self-describing registry feeding MCP, CLI `commands`/`describe`/`run`):
      `device.list/get/state/add/update/remove/set_power/set_level/set_color`,
      `room.list/add/remove/assign`, `scene.list/save/apply/remove`, `energy.now/summary/top`,
      `event.list/ack`, `home.status/sim/seed_demo/import_fleet/export/import/backup`.
      Restore = `home.import` of an export, or swapping in a backup file. Real Hue color is a
      typed `unsupported` until Tier 2.
- [x] `readonly` and `confirm_required` enforced inside `dispatch` (direct and scene paths;
      scenes pre-flight all steps); sim mode via `--sim`, `HOMECRAFT_SIM=1` or `home.sim`.
- [x] Demo home (3 rooms, 2 plugs incl. a readonly server plug, 3 lights, 1 camera,
      1 weather station, 1 confirm-required kettle, 2 scenes).
- [ ] **Moved to Tier 4:** delete `llm.rs`, depend on `craft-ai-core`. craft-ai-core only has
      single-turn text `complete()`; HomeCraft needs multi-turn chat now and image input for
      `camera.describe_scene`. Extend craft-ai-core first, then swap.
- [ ] **Moved to Tier 3:** `i18n.rs` (7 locales, key enum) lands with the UI it translates.
- **Gate:** 6 gates; tests: readonly per entry path, confirm-less call changes nothing,
  secret redaction over `device.get` + export, migration from empty DB, scene per-step
  results, rollup maths on a fixture.

## Tier 2 - Discovery and onboarding (v0.3.0, ~1-1.5 h + LAN session)

- [x] Discovery: TCP probe kept; mDNS (`mdns-sd`), SSDP M-SEARCH (plain UDP), ARP + OUI hint;
      merged per IP; source tag per result; suggested flow per candidate.
- [x] Onboarding session state machine (persisted, 10 min TTL, resumable by id); flows: Hue,
      Tapo, Kasa, Shelly, camera (tapo/onvif), generic, demo. **Not as onboarding flows:** Netatmo
      and Ring keep their existing auth commands (`netatmo.stations` token, `ring.auth` +
      `ring.auth_2fa`); iKettle moves to Tier 4 with its driver.
- [x] Pre-flight (latency, authenticated read as proof, readonly decision enforced at finish).
      Room suggestion from names: not done (rooms are chosen explicitly at finish).
- [x] Commands `discover.scan`, `onboard.start/step/finish/cancel`.
- [ ] **LAN session:** scan the subnet, onboard one Hue light and one Tapo plug from zero
      with a stopwatch; the .38 server plug must land readonly.
- **Gate:** 6 gates; fixture tests for mDNS/SSDP parsing and OUI lookup; state-machine
  tests per flow (timeout, wrong password, resume); live rows dated or `down`.

## Tier 3 - Pattern 2 workstation (v0.4.0, ~1.5-2 h)

Rebuilds `devices-app` (today a Pattern 1 sidebar of pages) as a workstation; reuses its
widgets, charts and RTSP player.

- [x] Menu bar as PRD 8.1: Session, Edit, View, Add, Device, Automate, Commands, Window,
      Help; `switch_on_hover`; hotkey tooltips; actions go through the command bus.
      Deviations recorded in `docs/UI_PARITY.md` (no Save: home.db autosaves).
- [x] Help 5-item suite: Command Palette (Ctrl+Shift+P / Ctrl+K), Keyboard Shortcuts
      (F1 / Ctrl+/), Project Files & Docs, Licenses & Notices, About HomeCraft.
- [x] Toolbox (home tree, Discovered, Scenes), persistent viewport with six modes
      (Home, Floorplan, Cameras, Energy, Climate, Events), Inspector, status bar, quick row.
      Rules join the toolbox in Tier 4.
- [x] Cards / List / JSON with filter, numeric-aware sort, paging (50), CSV/MD/TXT/JSON export
      on Home and Events. Discovered stays a toolbox list (deviation, see UI_PARITY).
- [x] Floorplan: rooms as drop zones; dropping a device dispatches `room.assign`.
- [x] Onboarding wizard window; confirm modal; Undo/Redo for registry edits.
- [x] High-contrast light and dark themes, Ctrl+mouse-wheel zoom, language selector,
      sun/moon toggle, hairline borders.
- [x] No network on the UI thread (all dispatches spawn; the only `block_on` is `--smoke`).
- [x] `--smoke` runs 26 menu commands against a temp demo home in sim mode.
- **Gate (closed 2026-11-12, v0.4.0):** clippy / fmt / tests green; 10 goldens (5 views x 2
  themes, wizard included) checked by eye; tofu guard; menu-bar checklist ticked in
  `docs/UI_PARITY.md`. Open: live-window check at 150 % scaling and CJK goldens.
## Tier 4 - Home Assistant replacement (v0.5.0, ~2 h + LAN session)

- [x] Events: `event.list/ack`, retention prune (default 90 days, `retention_days`); device health
      (offline after 3 failed reads, back-online event). **Not done:** low-battery (no battery
      readings are wired yet).
- [x] Rules: `rule.list/save/enable/remove/test/fire`; triggers time, sunrise/sunset,
      threshold-for-N, event, presence; actions scene / device / alert / notify / speak; never
      confirm; confirm_required and readonly targets refused at save; rule/actuation events can
      not trigger rules (no loops). Rules have no action that acks or mutes alerts.
- [x] `homecraft-mcp watch` (`--once`, `--status`, `--force`): meters, health, presence, motion,
      Ring dings (auth failures pause Ring for 6 h: a failed login sends an SMS code), hourly
      rollups, anomalies, prune, rules; poller lock with heartbeat; state in `home.db`.
      App: Session > Start / Stop Service, status bar. NSSM install documented in HELP.md.
- [x] Appliances: `energy.anomalies` from learned hourly bands. iKettle ported but UNVERIFIED
      (devices-mcp's guessed HTTP API; no kettle in the fleet config).
- [x] Climate: `climate.summary` (read-only). **Down 2026-11-14:** valve set-target, no valves in
      the fleet config.
- [x] Nest Protect: **down 2026-11-14.** devices-mcp only has Google's Device Access (SDM) API,
      which does not expose Protect; nothing to port.
- [x] Presence: `person.add/list/remove`, `presence.status/scan` (ARP + ping, 10 min grace).
- [x] Motion: frame difference with masks, Ring dings and Ring motion into `motion` /
      `doorbell` events; `motion.configure`, `motion.events`. ONVIF event subscription not wired.
- [x] Scene description: `camera.describe_scene` via Ollama `/api/chat` with the image
      (default `gemma4:e4b`, the local model with a vision projector). Deviation:
      craft-ai-core is text-only, so not through it yet. Cloud only with per-camera opt-in.
- [ ] Tapo PTZ: **skipped 2026-11-14**, moves real hardware; needs a session at the camera.
- [ ] **LAN session (partly done 2026-11-14, on a copy of home.db):** one live `watch --once`
      cycle 4.0 s, 397.6 W over 2 meters, 21 devices healthy, Ring auth expired (found the SMS
      retry problem, fixed). Live describe_scene on the USB webcam: 12.0 s model latency, real
      answer (the frame was black). Still open: `watch` as an NSSM service, a threshold rule on a
      real plug firing `bridge.event`, presence flip with a real phone.
- **Gate (closed in code 2026-11-14, v0.5.0):** clippy / fmt / tests green; fake-clock rule tests
  (Vienna sun times against published 2026 tables, time once + missed, threshold-for-N with
  re-arm, event cursor, presence all_away); frame-diff fixtures; presence grace test; band test;
  lock test; vision local/cloud refusal test.
## Tier 4.1 - Charts and alert board (v0.5.1, done 2026-11-17)

- [x] `energy.series`: per-meter points bucketed by range (1 min to 6 h), normal band, house total;
      hourly rollups fill hours whose raw readings are gone.
- [x] Time-series chart widget (`chart.rs`): local time axis with day breaks, nice value ticks,
      gradient fills, gaps, bands with out-of-band markers, hover crosshair, drag-zoom /
      Shift-pan / double-click reset shared across charts, legend toggles.
- [x] Energy view rebuilt: range picker, KPI tiles, all-meters chart, per-meter small multiples;
      the legacy live meter kept as a folded section.
- [x] Store v4 `alerts`; `alert.list/move/raise/note/sync`; the watch cycle turns logbook events
      into deduplicated cards, back-online resolves offline cards, snoozes wake.
- [x] Alerts view (Ctrl+7): four-column board with drag and drop, buttons and right-click menu.
- [x] Climate series (indoor/outdoor temperature): done in Tier 4.2.

## Tier 4.2 - Climate history, Home overview, camera fixes, e2e tests (v0.5.2, done 2026-11-17)

- [x] Watch records climate every 15 min (Netatmo live, demo/sim synthetic, Open-Meteo outdoor);
      `climate.series`, `climate.record`, `climate.configure`; silent sources become alert cards.
- [x] Climate view charts (temperature, humidity, CO2 with healthy band); fitted value axes.
- [x] Home overview tiles, redesigned device cards with live readings and pills; Inspector
      history chart; Events in local time with coloured severity.
- [x] Per-camera logins (`camera.set_login`, devices-mcp per-IP entries): .206 captures live.
- [x] USB warm-up + black-frame detection; Describe Scene refuses black frames.
- [x] `camera.capture`, `device.ping` (Device > Ping Device).
- [x] End-to-end tests over the real binary (CLI + MCP stdio).
- [ ] .164 C520WS: Tapo `password_shadow` (SHA-crypt) login transform, driver work.
- [ ] USB webcam on Goliath delivers only black frames (covered / shutter / virtual camera?):
      check at the machine.

## Tier 5 - Detection (v0.6.0, ~1 h + LAN session)

- [ ] Cargo feature `vision-onnx`: `ort` with CUDA on the 4090, CPU fallback; default
      build size checked with and without the feature.
- [ ] Permissively licensed detector (RT-DETR or YOLOX, Apache-2.0); weights outside the
      repo; `vision.models`.
- [ ] Detection on motion events only; stored as events; overlay in the Cameras view.
- [ ] `vision.detect`; detection triggers in rules.
- [ ] **LAN session:** a person walking past the front door camera is detected and fires
      `bridge.event`; ms per frame measured on GPU and CPU.
- **Gate:** 6 gates with and without the feature; fixture images with known detections
  above threshold; `just ci` without the feature needs no model.

## Tier 6 - Release, soak and cutover (v1.0.0, ~1 h + 7-day soak)

- [ ] `docs/`: ARCHITECTURE, TOOLS (generated), UI_PARITY, HANDOVER; `HELP.md` (generated);
      `KIBITZ.md` started.
- [ ] Brochure HTML, then `build-craft-brochure.ps1` for EPUB/PDF; buttons in Help/About.
- [ ] democraft recipe `home/energy-report-sim` (fixture-only, `run.json` + report with
      measured ms/rows); registered in democraft.
- [ ] NSIS current-user installer (offers to install the `watch` service); release assets =
      installer + `homecraft.exe` + `homecraft-mcp.exe` + `SHA256SUMS.txt`, no zip.
      Sandra publishes.
- [ ] 7-day `watch` soak on Goliath; uptime, RAM and rule-fire counts recorded.
- [ ] Final live verification table, every row dated.
- [ ] Cutover (REPCONV 7 points): superseded banners on `rust-devices-mcp`, `devices-mcp`,
      `home-assistant-mcp`; MCP client configs (Claude, agy, OpenCode, LM Studio) point at
      `homecraft-mcp mcp`; makercraft/robotcraft/speechcraft notes for the modules they
      take over; FLEET_INDEX and craft-fleet hub updated; the three repos archived, not
      deleted.
- [ ] Craft-fleet spoke `projects/craft-fleet/homecraft.md` with grade and evidence.
- **Gate:** 6 gates; PRD section 13 walked line by line with evidence.

## GDoc Architecture Sync (2026-11-17)

Synced from `Homecraft Architecture & README` and `Homecraft & Hybrid UI Architecture Chat History` (2026-11-17):

- [x] **Embedded ACID storage + schema versioning:** already implemented in `homecraft-store` via `rusqlite` (SQLite WAL, schema v4) instead of `redb`. Keep `rusqlite` unless a dedicated `redb` migration is needed.
- [x] **Hybrid UI (telemetry dashboard + reactive Kanban) with non-blocking async channels:** already implemented in `homecraft-app` (`Energy` charts in `chart.rs`, 4-column `Alerts` Kanban board in `insight.rs`, background Tokio/spawned dispatches).
- [x] **Native stdio JSON-RPC MCP tools (`get_device_state`):** already covered by `device.state` (85 total MCP tools in `homecraft-mcp`).
- [x] **Offline/stale device health tracking:** already implemented in `watch` (offline after 3 failed reads, back-online events, `alert.sync` auto-resolve).
- [ ] **30-second last-seen heartbeat watchdog (`Online` -> `OfflineStale`):** optional enhancement over the 3-failed-reads poll counter if sub-minute staleness is needed.
- [x] **`device.ping`:** done in v0.5.2 (ICMP + service-port TCP latency). `device.restart` stays
      open: rebooting a plug cuts what hangs off it, so it needs the readonly / confirm fences and a
      per-vendor call first.
- [ ] **Simultaneous split-view dashboard + Kanban layout in `egui`:** optional `View` toggle combining the live telemetry radiator and `Alerts` board side-by-side in one viewport.
- [x] **Status indicator pills:** done in v0.5.2 (OFFLINE / READ-ONLY / CONFIRM on device cards).
- [ ] **Embedded JetBrains Mono typography:** open (font size and licence notice to weigh).
- [ ] **Post-v1.0 / optional: Eclipse Zenoh pub/sub mesh (`goliath/home/**`):** evaluate only if multi-node telemetry routing is needed beyond local `home.db` + `watch` polling.

## Risks

| Risk | Mitigation |
|---|---|
| Rename churn breaks something subtle in Tier 0 | Byte-diff CLI JSON against rust-devices-mcp before any new code |
| `keyring` access from the service account | Run `watch` as Sandra's user; env/.env fallback documented |
| mDNS blocked by Windows firewall | Results state which sources ran; TCP probe still works; installer adds the rule |
| Ring changes its API again (406 history) | Typed error, Ring tile shows "auth needed", rules keep running |
| Nest Protect has no working local or official path | Dated `down` receipt; roadmap; smoke detection is not silently claimed |
| Phones randomize Wi-Fi MAC | Per-network fixed MAC setting documented; fallback to static IP / ping |
| ONNX Runtime CUDA setup on Windows is fiddly | Feature-gated, CPU fallback, numbers measured either way |
| Tier 3 UI scope creep | Six view modes; anything else is a View toggle in v1.1 |
| App and service both polling | Poller lock row in `home.db`; test for single active poller |
