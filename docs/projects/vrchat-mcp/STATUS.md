# VRChat MCP -- Project Status

**Last Updated**: 2026-02-15
**Repo**: `D:\Dev\repos\vrchat-mcp` | [GitHub](https://github.com/sandraschi/vrchat-mcp)
**Version**: v3.1.1+.0+ (FastMCP)
**Python**: 3.8+ | **Build**: Setuptools / MCPB
**Status**: ðŸŸ¢ PRODUCTION READY

---

## What It Is

A professional-grade bridge for controlling VRChat avatars and environment assets via the Open Sound Control (OSC) protocol.

**Capabilities**: Real-time parameter management, avatar swapping, and plugin-based extension system for intelligent NPCs.

---

## Architecture

Dual-transport server supporting both high-speed stdio (for AI agents) and FastAPI (for web/third-party integration):
- **OSC Core**: Bidirectional communication with VRChat (Ports 9000/9001).
- **Plugin System**: Modular tool registration for custom avatar behaviors.
- **Parameter Indexing**: Fast lookup of avatar-specific OSC endpoints.
- **NPC Logic**: Planned integration for conversational agents within VR instances.

---

## Current State

| Feature | Status | Notes |
|---------|--------|-------|
| OSC Transport | Working | Reliable bidirectional message flow |
| Avatar Control | Working | Parameter get/set operations verified |
| Plugin Host | Working | Decorator-based extension system |
| Dual Interface | Working | Simultaneous stdio + FastAPI support |
| MCPB Packaging | Working | SOTA 2026 compliant bundle |

---

## Port Allocation

| Service | Port | Status |
|---------|------|--------|
| Backend | 10762 | Reserved |
| Frontend | 10763 | Reserved |

