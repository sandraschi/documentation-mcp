# sdr-mcp

**Type:** MCP Server + Webapp (incomplete)  
**Status:** Inactive — needs P1 fixes before use  
**Version:** 0.1.0  
**Ports:** MCP HTTP **10891** / WebSocket **8765** (outside fleet range — needs move)  
**Repo:** `D:\Dev\repos\sdr-mcp`  
**GitHub:** https://github.com/sandraschi/sdr-mcp  
**Last assessed:** 2026-05-01

---

## Description

MCP server wrapping RTL-SDR hardware (Software Defined Radio) into FastMCP tools. Control an RTL-SDR dongle via Claude to tune frequencies, capture IQ samples, compute FFT spectrum, stream waterfall data via WebSocket, and query station databases. Without hardware plugged in, tools degrade gracefully with setup guidance.

Hardware: RTL-SDR dongle (RTL2832U chipset) — ~€30, USB, covers 24 MHz–1.766 GHz.

---

## Architecture

```
FastMCP (17 tools, stdio or HTTP :10891)
  ├── SDRCapture    — pyrtlsdr hardware interface
  ├── SDRProcessor  — numpy 2048-pt FFT, Hamming window, waterfall history
  ├── frequency_db  — 11 hardcoded stations (LW/MW/SW/VHF) with schedules
  ├── online_db     — radio-browser.info (25k+ stations) + SigID Wiki
  └── websocket_server — real-time spectrum streaming (port 8765)

web_sota/ — React 19 + Vite + Tailwind
  Pages: Spectrum, Waterfall, Stations, Online DB, Chat, Settings, Status, Tools
  Status: NO backend API — dashboard is non-functional skeleton
```

---

## MCP Tools (17)

| Tool | Purpose |
|------|---------|
| `sdr_list_devices` | Detect connected RTL-SDR dongles |
| `sdr_initialize` | Open and configure hardware |
| `sdr_set_frequency` | Tune center frequency (24–1766 MHz) |
| `sdr_set_gain` | Set gain (auto or 0–49.6 dB) |
| `sdr_get_spectrum` | Capture + FFT spectrum snapshot |
| `sdr_get_waterfall` | Return waterfall history (100 lines) |
| `sdr_get_status` | Current device config |
| `sdr_tune_preset` | Tune to named station (BBC LW, ORF LW, France Inter, RTL LW) |
| `sdr_start_websocket_server` | Start real-time streaming server |
| `sdr_stop_websocket_server` | Stop streaming server |
| `sdr_scan_frequencies` | Sweep a frequency range, detect signals |
| `sdr_search_stations` | Search local station DB by name/band/country |
| `sdr_get_stations_by_band` | All stations on LW/MW/SW/VHF/UHF |
| `sdr_get_stations_by_country` | All stations from a country |
| `sdr_get_program_schedule` | Program schedule for a station |
| `sdr_get_frequency_database_stats` | DB coverage stats |
| `sdr_query_online_database` | Search radio-browser.info + SigID Wiki |

---

## Start

```powershell
# MCP server (stdio for Claude Desktop)
uv run sdr-mcp serve

# Or HTTP mode
$env:MCP_TRANSPORT = "http"; uv run sdr-mcp serve

# Web dashboard (no backend — limited functionality)
cd web_sota; npm run dev
```

Requires RTL-SDR hardware + Zadig drivers (Windows).

---

## Known Issues (as of 2026-05-01)

See `ASSESSMENT.md` for full detail.

**P1 — must fix before registering with Claude Desktop:**
- `@mcp.tool(task=True)` on `sdr_start_websocket_server` and `sdr_scan_frequencies` — not a valid FastMCP parameter, will cause startup error
- `sdr.read_samples()` is a blocking synchronous call inside `async` method — blocks event loop for ~0.5s; needs `asyncio.to_thread()`
- `asyncio.get_event_loop().time()` deprecated in 3.12 — use `get_running_loop()`
- `capture.py` uses legacy `typing.Optional` / `typing.List` despite `requires-python = ">=3.12"`

**P2:**
- No REST API backend for `web_sota` — dashboard is a non-functional skeleton
- WebSocket port 8765 outside fleet range (should be 10700–11000)
- `sdr_get_spectrum` hardcodes 1M sample read — should be configurable
- `pyproject.toml` uses setuptools, rest of fleet uses hatchling

---

## Stack

| Component | Version |
|-----------|---------|
| Python | ≥3.12 |
| fastmcp | ≥3.2.0 |
| pyrtlsdr | ≥0.3.0 |
| numpy | ≥1.21, <2.0 |
| scipy | ≥1.7, <2.0 |
| websockets | ≥15.0 |
| React | 19 |
| Vite + Tailwind + Radix UI | current |

---

## Tags

`[sdr-mcp, fastmcp, hardware, rtl-sdr, spectrum, radio, inactive, webapp-incomplete]`
