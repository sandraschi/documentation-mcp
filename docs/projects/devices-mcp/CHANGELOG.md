# Changelog

## [1.21.1] - 2026-05-25 🔧 **Webapp Bug Fixes**

### 🔧 **FIXES**
- **✅ Log Page Infinite Loop**: Fixed React `useEffect` dependency causing infinite re-renders on the Log Management page.
- **✅ Lighting Page Not Showing Lights**: Fixed `GET /api/lighting/status` extracting lights from wrong response nesting -- portmanteau `build_success_response()` nests lights under `result.result`, endpoint was reading `result.lights` (always empty).
- **✅ Lighting Scenes/Ctrl/Device/Groups Endpoints**: Rewrote 5 API endpoints that imported non-existent `LightingManagementTool` class -- now use actual portmanteau functions and Hue manager directly.
- **✅ Lighting Page Infinite Loop**: Fixed same `useEffect([load])` infinite re-render bug in the Lighting page.
- **✅ PC Health Page Hang**: Added 15s `AbortController` timeout to prevent page spinner hanging when backend APIs are slow; improved error handling for network failures.

## [1.21.0] - 2026-03-15 ⬆️ **FastMCP 3.1 Upgrade & Completion**

### 🆕 **FASTMCP 3.1**
- **✅ Bump**: `fastmcp>=3.1.0` (from 2.14.x). Skills provider, prompts, sampling-ready.
- **✅ Core server**: `from fastmcp import FastMCP`; `_register_fastmcp_31_providers_and_prompts()` registers SkillsDirectoryProvider (Cursor/Codex skills roots) and prompts (`device_status`, `list_cameras`).
- **✅ Web-SOTA**: `/api/tools` uses `list_tools()` only (removed `get_tools` fallback).
- **✅ Plex**: Removed `instructions` from FastMCP constructor; version 3.1.0.
- **✅ Ring**: Version 3.1.0; removed `instructions` from composed app.
- **✅ Nest Protect help_tool**: `get_tools()` to `list_tools()`, list-based tool handling.
- **✅ Agentic security**: Sampling check accepts `ctx.sample` or `ctx.sample_step`; messages say FastMCP 3.1+.
- **✅ inspect_server.py**: Uses `DevicesMCPServer` and `list_tools()`.

### 📝 **Docs & comments**
- README, PRD, MCPB_QUICKSTART, MCPB_IMPLEMENTATION, help.html, GLAMA checklist, assessment, FASTMCP_2.12_COMPLIANCE_GUIDE (note: now 3.1), DOCUMENTATION_INDEX references, and module docstrings updated to FastMCP 3.1.

## [1.20.0] - 2026-03-02 🚀 **Robotics Integration & Fleet Expansion**

### 🆕 **FEATURES**
- **✅ Robotics Integration**:
  - **Dreame D20 Pro**: Integrated via Home Assistant Cloud API (Dreame Vacuum component). Confirmed cloud-based control for Dreamehome-exclusive models.
  - **Yahboom ROS 2 Car**: Implemented SOTA mock client and dashboard controls for development.
- **✅ Fleet Expansion**:
  - **Second Tapo Camera**: Added support and configuration for a second C200 camera (Living Room) at `192.168.0.206`.
  - **ONVIF/OpenCV Bypass**: Implemented a robust bypass for Tapo C200 snapshot issues using direct ONVIF capture.

### 🔧 **FIXES & ALIGNMENT**
- **✅ MCP Pathing**: Fixed critical `ModuleNotFoundError` by correctly setting `PYTHONPATH` in the unified `start.ps1` script.
- **✅ Plex Port Alignment**: Standardized Plex webhook port to `10716` to match project orchestration standards.

## [1.19.0] - 2026-03-02 🎁 **USB Camera Server & Massive Code Cleanup**

### 🆕 **FEATURES**
- **✅ Windows USB Camera Server**: Integrated a local USB camera server on port 10715 into the global `start.ps1` orchestration. This provides a robust alternative for local monitoring.
- **✅ Hardware Support Documentation**: 
  - Added research and connectivity guidelines for **Insta360 X5**.
  - Confirmed and documented specifications for the **BETAFPV Pavo35** drone platform.

### 🔧 **CODE QUALITY & LINTING**
- **✅ Repository-Wide Cleanup**: Addressed over 270 linting warnings (`TRY400`, `TRY401`) across more than 160 files.
- **✅ Idiomatic Logging**: Standardized exception logging to use `logger.exception()` without redundant exception objects, reducing code noise and improving maintainability.

### 🛠️ **CLI & ARCHITECTURE**
- **✅ CLI Restoration**: Fixed critical syntax and singleton usage in `cli_v2.py`.
- **✅ Unified Transport**: Improved stability of the MCP transport runner for more reliable agentic integration.

## [1.18.1] - 2026-02-04

### Fixed
- **Asyncio RuntimeError**: Resolved "Already running asyncio in this thread" error by properly managing event loop contexts in the CLI entry point.
- **Stdout Corruption**: Redirected all diagnostic messages, initialization banners, and non-RPC data to `stderr`. This prevents plain-text strings from polluting the MCP JSON-RPC stream and causing client disconnections.
- **Stability**: Enhanced server resilience when running within agentic IDEs (Antigravity/Cursor).

## [1.18.0] - 2026-01-18 🏠 **HomeAware Motion Detection & Robust Error Handling**

### 🎯 **HOMEAWARE MOTION DETECTION** ✅

#### **Zigbee Mesh Signal Strength Monitoring**
- **✅ Bridge Pro Detection**: Automatic detection of Philips Hue Bridge Pro (BSB002 model)
- **✅ Signal Analysis**: Real-time monitoring of Zigbee mesh signal strength changes
- **✅ Motion Detection**: Passive presence detection using signal attenuation between lights
- **✅ No Extra Sensors**: Uses existing Hue lights as distributed motion sensors
- **✅ Security Integration**: Motion events trigger alerts and can activate security systems
- **✅ Dashboard UI**: Dedicated HomeAware monitoring panel in the web dashboard

#### **Hue API v2 CLIP Integration**
- **✅ API Upgrade**: Transitioned from Hue API v1 to v2 (CLIP) for HomeAware endpoints
- **✅ Motion Area Support**: Full support for both `convenience_area_motion` and `security_area_motion` configurations
- **✅ Multi-Bridge Support**: Compatible with all Hue Bridge Pro models on latest firmware
- **✅ Polling System**: Real-time motion edge detection with false-to-true state tracking
- **✅ Status Dashboard**: REST endpoints for current HomeAware status and motion history

### 🛡️ **CIRCUIT BREAKER & AUTO-RECOVERY**
- **✅ Smart Retry**: Implements exponential backoff for device reconnection attempts
- **✅ Circuit Breaker**: After 5 consecutive failures, a device check is paused for 15 minutes to prevent log spam and system load
- **✅ Auto-Recovery**: Automatically resumes health checks after the circuit breaker interval expires
- **✅ All Devices**: Circuit breaker protection applies to all monitored device types

### 🧠 **POWER MACHINE CONFIGURATION & MONITORING**
- **✅ Configuration**: Added `power_machines` section to config.yaml for defining power-consuming appliances
- **✅ Status Tracking**: REST endpoints for current power consumption status per machine
- **✅ History**: Time-series data for power consumption trends and anomaly detection
- **✅ Status Dashboard**: Dedicated power machine monitoring panel in the web dashboard

### 🐛 **BUG FIXES**
- **✅ AsyncIO Task Management**: Fixed race conditions in asyncio task creation within camera management
- **✅ Health Check Parallelism**: Resolved timeout errors when checking multiple devices simultaneously
- **✅ Memory Leak Prevention**: Properly cleaned up stale health check results to limit memory growth
- **✅ Message Queue**: Fixed message accumulation in the messaging service preventing memory leaks
- **✅ Audio Service**: Proper cleanup of audio service resources
- **✅ Cache Invalidation**: Better cache freshness policies for camera and weather data
- **✅ Debug UI**: Removed debug port 3000 exposure from production configurations
- **✅ Version Alignment**: Ensured all endpoints return consistent version strings

### 📝 **DOCUMENTATION**
- **✅ Full PRD Update**: Product Requirements Document updated with all v1.18 features
- **✅ New Pages**: Added HomeAware, Power Machine pages to DOCUMENTATION_INDEX
- **✅ API Reference**: Updated endpoint documentation for all new features
- **✅ Troubleshooting Guide**: Added HomeAware setup and calibration guides

## [1.17.0] - 2025-12-26 🎄 **Performance Optimization & Log Management**

### ⚡ **PERFORMANCE & RELIABILITY**
- **✅ Email Deduplication**: Ring detection emails are deduplicated by `@id`, reducing MCP processing overhead.
- **✅ Improved Camera Reconnection**: Reconnection logic reset on success, avoiding repeated init cycles.
- **✅ Startup stability**: Graceful handling of missing config sections with stop-level retries.

### 🔧 **LOGGING & MONITORING**
- **✅ Log Management Dashboard**: New `/logs` page for viewing and filtering log files.
- **✅ Log Sanitization**: Automated rotation, compression, and cleanup via `/api/logs/sanitize`.
- **✅ Log Analysis**: Clustering, anomaly detection, and AI synopsis via `/api/logs/analyze`.
- **✅ JSON Logging**: Structured `JSONFormatter` for Docker/Loki/Promtail.

### 🐛 **BUG FIXES**
- **✅ Config Fallback**: Gracefully handle missing top-level keys (`logging`, `cameras`, `network`).
- **✅ Hue rescan errors**: Wrapped in try/except to prevent startup failure.
- **✅ Proper Color Bar Intervals**: Weather page corrected to use `N > -10` instead of `N >= -10`.
- **✅ Dashboard page**: Uses `allSettled` for independent loading of tiles, preventing one failure from blocking others.

## [1.16.0] - 2025-12-14 🎄 **Christmas Cards & Automation**

### ✨ **FEATURES**
- **✅ Christmas Card Automation**: Print holiday photos via Dymo LabelWriter wireless printer.
- **✅ Energy Monitoring**: Track and display smart plug power consumption per device.
- **✅ Tapo Climate**: Temperature and humidity readings from C200 cameras.
- **✅ Ollama Support**: Local Mistral/Llama as fallback LLM provider for AI features.
- **✅ Tool Registration Fix**: Lighting and camera MCP tools properly re-exported in `mcp/__init__.py` for portmanteau registration.

### 🐛 **BUG FIXES**
- **✅ Plex Media Player Initialization**: Fixed `/api/plex/media-players` failing when `media_players` is not in config.
- **✅ HTTP 422 on empty Favorites**: `get_plex_favorites()` returns empty list instead of crashing.
- **✅ Remove Redundant Webcam Add**: Dashboard no longer attempts to re-add USB webcam on every load.
- **✅ Camera Stat Keys**: Fixed mismatched key between `ptr_count` and `ptz_count` causing dashboard errors.

## [1.15.0] - 2025-11-28 🦃 **Nest Protect & Port Standardization**

### ✨ **FEATURES**
- **✅ Nest Protect Monitoring**: Smoke, CO, temperature, humidity, occupancy alerts.
- **✅ Port Standardization**: All webapp ports now use 107xx range, not 3000/5000/8000/8080.
- **✅ Home Assistant Bridge**: Proxy for devices not directly reachable (Nest, Hue).
- **✅ Webapp Startup Scripts**: `start.ps1` + `start.bat` with zombie port clearing.

### 🔧 **ENHANCEMENTS**
- **✅ Plex Watchlist**: Configurable default library for movie organization.

## [1.14.0] - 2025-11-07 🎥 **Plex Integration & Smart Plug Support**

### ✨ **FEATURES**
- **✅ Plex Media Server**: Movie catalog, watchlist, streaming, metadata, and playback control.
- **✅ Tapo P115 Smart Plugs**: Energy monitoring, ON/OFF control, and power consumption tracking.
- **✅ Philips Hue Bridge**: Light control, groups, scenes, brightness, and color temperature management.
- **✅ Ring Alarm System**: Arming/disarming, sensor monitoring, and event history with WebRTC streaming.
- **✅ SDR Scanner**: Radio frequency scanning for security monitoring (experimental).
- **✅ Unified Camera System**: Multi-protocol support (WebRTC, RTSP, ONVIF), auto-discovery, and PTZ control.
- **✅ MCP Tool Expansion**: 40+ registered MCP tools with proper categorization and documentation.
- **✅ Web Dashboard Beta**: React-based UI with dark mode, live camera feeds, energy monitoring, and lighting control panels.
- **✅ Philips Hue Pro Support**: Automatic detection and configuration of Hue Bridge Pro (BSB002) with SSH key authentication.
- **✅ Voice Assistant**: "Hey Tapo" wake word, local speech recognition using Faster-Whisper, and text-to-speech via built-in speakers.

## [1.13.0] - 2025-10-21 🚀 **v1.13 - Initial Release (pre-history)**
- Initial beta release with Tapo C200 support
- CLI MCP server via stdio and HTTP SSE
- ONVIF camera discovery and RoCL (Robust Camera Library)
- DVR recording and webhook support
- Basic web interface
