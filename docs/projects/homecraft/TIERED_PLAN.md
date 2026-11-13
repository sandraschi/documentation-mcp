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

- [ ] Menu bar exactly as PRD 8.1: Session, Edit, View, Add, Device, Automate, Commands,
      Window, Help; `switch_on_hover`; hotkey tooltips; every item a `Command`.
- [ ] Help 5-item suite: Command Palette (Ctrl+Shift+P / Ctrl+K), Keyboard Shortcuts
      (F1 / Ctrl+/), Project Files & Docs, Licenses & Notices, About HomeCraft.
- [ ] Toolbox (home tree, Discovered, Scenes, Rules), persistent viewport with six modes
      (Home, Floorplan, Cameras, Energy, Climate, Events), Inspector, status bar, quick row.
- [ ] Cards / List / JSON switcher with filter, numeric-aware sort, pagination, CSV/MD/TXT/JSON export
      for Home, Events, Discovered.
- [ ] Floorplan: rooms as rectangles; drag device onto room dispatches `room.assign`.
- [ ] Onboarding wizard window; confirm modal; Undo/Redo for registry edits.
- [ ] High-contrast light and dark themes, Ctrl+mouse-wheel zoom (persisted), language
      selector, sun/moon toggle, hairline borders.
- [ ] No network on the UI thread.
- [ ] `--smoke` dispatches every menu command against Demo.
- **Gate:** 6 gates; `egui_kittest` goldens per view mode in both themes plus the wizard;
  tofu guard; menu-bar checklist (standard section 4) ticked with screenshots in
  `docs/UI_PARITY.md`.

## Tier 4 - Home Assistant replacement (v0.5.0, ~2 h + LAN session)

- [ ] Events model: `event.list/ack`, retention; sensor health (stale, low battery, offline).
- [ ] Rules: `rule.list/save/enable/test`; triggers time, sunrise/sunset, threshold-for-N,
      device event, presence; actions scene/command/alert/`bridge.*`; no confirm targets;
      critical alerts unmutable.
- [ ] `homecraft-mcp watch` (+ `--status`): polling, rollups, rules, alerts; poller lock
      shared with the app; timers rebuilt from `home.db` on restart. NSSM install
      documented via wincraft.
- [ ] Appliances: iKettle driver; `energy.anomalies` from learned per-plug bands.
- [ ] Climate: Netatmo valves set-target (confirm above 26 C), `climate.summary`.
- [ ] Nest Protect: port devices-mcp's path if it works live, else dated `down` receipt.
- [ ] Presence: phone MAC/IP via ARP + ping with grace period; `presence.status`.
- [ ] Motion (FR-VIS-01): frame diff, ONVIF motion events, Ring dings into one event;
      `motion.events`, `motion.configure`.
- [ ] Scene description (FR-VIS-02): `camera.describe_scene` via `craft-ai-core`, default
      local Ollama Gemma 4 12B; cloud only with per-camera opt-in.
- [ ] Tapo PTZ if supported by the camera on the LAN, else dated skip.
- [ ] **LAN session:** `watch` installed as a service; a threshold rule on a real plug
      fires `bridge.event`; presence flips when a phone leaves Wi-Fi; one live
      describe_scene recorded with latency.
- **Gate:** 6 gates; rule engine tests with a fake clock (Vienna sunset on a fixed date,
  threshold-for-N, no double fire, restart rebuild); frame-diff fixtures (static, flicker
  below threshold, motion inside mask); presence grace-period test; anomaly band test;
  describe_scene opt-in refusal test.

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
