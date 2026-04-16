# AvatarMCP Project Overview

## Status
- **Phase**: Production Ready
- **Standards**: SOTA 2026 Compliant
- **Architecture**: Portmanteau (16 consolidated tools)
- **Protocol**: FastMCP 3.1.1+.3+ (SEP-1577 Sampling)

## Description
State-of-the-Art MCP server for VRM avatar management, Unity/VRChat integration, and real-time OSC animation. Now fully consolidated into 16 portmanteau managers to reduce tool explosion while maintaining advanced AI-driven choreography capabilities.

## Portmanteau Architecture
The server exposes **only** these 16 portmanteau tools (no raw core-tool list). **Bootstrap first** with `system_monitor({"operation": "initialize"})` (optional: `models_dir`); then use other tools. Lifecycle: `system_monitor(operation="shutdown")` to request shutdown.

1.  `avatar_manager`: Lifecycle (load, unload, list)
2.  `animation_manager`: Animation control, sequences, layering
3.  `emotion_manager`: Emotions, micro-expressions, personality
4.  `audio_manager`: Audio playback, singing synthesis
5.  `behavior_manager`: AI conversation, learning, adaptation
6.  `chat_manager`: Session management
7.  `system_monitor`: **Initialize/shutdown**, health, diagnostics, metrics
8.  `avatar_sampling`: Agentic workflow orchestration (SEP-1577)
9.  `collaboration_manager`: Multi-user sync
10. `content_manager`: asset creation and publishing
11. `interaction_manager`: Tactical triggers and gestures
12. `performance_manager`: Optimization and profiling
13. `unity_integration`: Core Unity operations
14. `unity_window_manager`: Window control
15. `unity_config_manager`: Unity settings
16. `artifact_manager`: Artifact and export management

## Integration
- **Fleet Connectivity**: Operates in conjunction with `osc-mcp` and `resonite-mcp` for cross-platform social VR automation.
- **Web Interface**: Premium SOTA dashboard on port 10792/10793; Settings page includes Ollama model discovery and selection; Loops page consumes `/api/v1/intelligence/loops`.
- **Cursor/IDE**: Run with `python -m avatarmcp --stdio`; banner suppressed and stdout patched so stdio MCP is not corrupted. See `integrations/avatar/README.md` for config.

