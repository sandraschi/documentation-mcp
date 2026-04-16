# Project: Universal Actuator Hub (Federation Gateway)

**Status:** Active / SOTA Compliant (v1.1.0)
**Role:** Federated Consumption Router & Discovery Node
**Orchestration:** RoboFang Sovereign Brain

---

## Executive Summary

The **Universal Actuator Hub** is the central discovery and routing gateway for the RoboFang MCP fleet. It refactors the old "Federation Hub" into a high-performance system that aggregates telemetry, search, and milestone tracking from satellite nodes (Plex, Calibre, Immich, etc.).

## Network Configuration

| Service | Port | Endpoint |
|---------|------|----------|
| **Frontend** | `10744` | [Next.js Dashboard](http://localhost:10744) |
| **Backend** | `10745` | [FastMCP SSE/REST](http://localhost:10745/api/v1/health) |

## Core Capabilities

### 1. Unified Fleet Federation (15+ Nodes)
Discovery and routing across 5 specialized actuator domains:
- **Infrastructure**: Filesystem, Windows Operations, Virtualization, Browser (Playwright).
- **Knowledge**: Advanced Memory (adn), DocsOps (Central Docs), FastSearch.
- **Media**: Plex, Calibre, Immich.
- **Creative**: Blender, GIMP, Inkscape.
- **Robotics**: Robotics-MCP, OSC, Unity3D, VRChat, Avatar.

### 2. Federated Search
Aggregates results from all active consumer-grade MCP servers.

### 2. Fleet Discovery (Glom-On)
Real-time monitoring of the fleet reservoir (10700-10800 range).
- `glom_on()`: Scans and caches active node schemas.
- Automatic server discovery and registration.

### 3. Unified Milestone Tracking
Global log for agentic accomplishments across the fleet.
- `universal_milestone(title, description, type)`: Persistent milestone logging.
- `get_milestones_history()`: Retrieval for fleet-level reporting.

---
*Maintained by sandraschi | RoboFang Ecosystem*
