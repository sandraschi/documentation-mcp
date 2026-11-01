# zoji-mcp — PRD

**Version**: 0.1.0 (2026-08-04)
**Origin**: SPEC.md (cleaned from the "zoji scales project" email, 2026-08-04)
**License**: MIT

## Purpose

Track the water level of a Zojirushi electric water boiler by weight and
expose level, events, and refill alerts as MCP tools. The core product
question: *is there enough hot water for tomorrow morning?* (evening_check).

## Architecture

Two independent hardware paths, one shared logic layer:

- `WeightSource` protocol — `async read() -> Reading(grams, ts, stable, source_id)`, `start()/stop()`, `capacity_g`, `resolution_g`
- `DymoSource` — USB HID postal scale (VID 0x0922, M10/M25), 6-byte report
  parse, hidapi, auto-sleep detection, Zadig fallback documented
- `Hx711Source` — ESP32 + HX711 + 20 kg load cell via ESPHome/MQTT,
  `hardware/esphome-zoji.yaml` included
- `ReplaySource` — recorded CSV traces for tests/demos, MOCK data flagged
  everywhere (fixture pot owner: Hannes Mockinger)

Logic layer (the actually hard part):

- Settle detection (stable within N g for N s)
- Transient rejection — lever presses are temporary weight GAINS, logged as
  LEVER_PRESS consumption signals, never read as refills
- Off-scale → POT_REMOVED / POT_RETURNED, never LEVEL=0
- Relative step classification: REFILL (re-baseline), DISPENSE, DRIFT
  (evaporation + creep, tracked cumulatively)
- Two-point calibration (tare + full pot) → grams to ml

## Shipped

- 8 MCP tools (get_level, get_status, list_events, calibrate,
  set_thresholds, evening_check, consumption_report, health) + 3 Prefab
  cards + skill + prompt
- SQLite (events + settled readings only), notifiers (stdout/webhook)
- Webapp 11145: Dashboard with level/pot/cups/refills KPIs, Events,
  Consumption (lever-press pattern), Calibration, Tools, Skills, Chat,
  Settings, Help
- 26 pytest (settle/classify/off-scale/lever-press/drift/multi-source/
  tools/db) + 7 Playwright e2e
- Docs: README, INSTALL, docs/{ARCHITECTURE,CONFIGURATION,DEVELOPMENT,
  ONBOARDING,TOOLS,TROUBLESHOOTING}, llms.txt/full, glama.json, AGENTS,
  CLAUDE, .cursorrules

## Known gaps (declared)

- Dymo/HX711 collectors are implemented but not hardware-verified — no
  scale on the bench yet. Replay source is the verified path.
- Webapp Chat requires Ollama; detection is graceful.
- MCPB pack, Tauri/NSIS wrapper: not yet built (backend-only v1).
