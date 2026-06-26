# VRChat MCP -- Project Status

**Last Updated**: 2026-04-13
**Repo**: `D:\Dev\repos\vrchat-mcp` | [GitHub](https://github.com/sandraschi/vrchat-mcp)
**Version**: v14.1.0 (SOTA Industrial)
**Python**: 3.12+ | **Build**: UV / MCPB / Just
**Status**: 🔵 SOTA INDUSTRIAL

---

## What It Is

A professional-grade unified control plane for VRChat interactions, combining high-fidelity OSC simulation with official REST API telemetry and real-time Websocket events.

**Capabilities**: Character state management, 2026 Creator Economy tracking, world discovery, and real-time social event monitoring.

---

## Architecture

Industrialized Portmanteau architecture consolidating protocol-level logic into high-utility entry points:
- **OSC Core**: Bidirectional communication with VRChat (Ports 9000/9001).
- **REST Client**: Official Web API integration with 60s proactive caching.
- **Pipeline Websocket**: Real-time event monitoring for invites, friend activity, and social telemetry.
- **Portmanteau Tools**: Consolidated `manage_*` tools for reduced cognitive load.

---

## Current State

| Feature | Status | Notes |
|---------|--------|-------|
| OSC Transport | Working | reliable bidirectional message flow |
| Avatar Control | Working | Full metadata (OSC + REST enrichment) |
| World Discovery | Working | REST-backed search and info retrieval |
| Creator Economy | Working | Credit balance and Udon product tracking |
| real-time Pipeline | Working | Websocket notifications integrated |
| MCPB Packaging | Working | SOTA 2026 compliant bundle (v14.1.0) |

---

## Port Allocation

| Service | Port | Status |
|---------|------|--------|
| **Backend (MCP)** | `10795` | Reserved/Active |
| **Web UI (SOTA)** | `10796` | Reserved/Active |
| **OSC Send** | `9000` | Standard |
| **OSC Receive** | `9001` | Standard |
