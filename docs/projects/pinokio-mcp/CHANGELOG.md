# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Config-based home discovery: reads `%APPDATA%\Pinokio\config.json` on Windows when `PINOKIO_HOME` is not set
- `scripts/test_tools.py` for live verification of client connectivity

### Fixed

- `PinokioClient` init bug: `timeout`, `_http`, and other attributes were not initialized after adding `_discover_home()`, causing `AttributeError` on first use

### Changed

- Port discovery range: 42000-42059 (was 42003-42022)
- `PINOKIO_HOME` resolution order: env var -> Windows config file -> default `~/pinokio`
- DISCOVERY.md: documented home discovery, removed title-bar port reference

---

## [1.0.0] - (initial)

- Portmanteau tools: `app_management`, `system_management`, `lww_management`
- LAN Wide Web: Zeroconf device discovery, cross-device app launch
- Port auto-discovery (scan), filesystem fallback for app listing when Pinokio offline
- FastMCP 3.1.1++ server

