---
title: "Multi-Server Orchestration Pattern"
category: pattern
status: active
audience: mcp-dev
skill_candidate: false
related:
  - architecture/DOMAIN_HUB_ARCHITECTURE.md
  - architecture/AGENTIC_MESH_ARCHITECTURE.md
  - operations/WEBAPP_PORTS.md
last_updated: 2025-12-31
---

# Multi-Server Orchestration Pattern (Dec 2025 SOTA)

## Overview

As MCP-enabled webapps scale, a single generic MCP server becomes insufficient for specialized domains. This pattern defines a standard for web applications to manage a fleet of domain-specific MCP servers locally.

## Core Logic

Instead of a monolithic backend, the webapp instantiates specialized servers at startup.

### Reserved Port Range: `13330 - 13350`
Prevents collisions with other system services. Servers assigned sequentially or via service discovery.

### Orchestration Strategies

**Standard webapp (myai):**
- `localhost:13330` → Personal Knowledge Server
- `localhost:13331` → Calendar/Email Integration
- `localhost:13332` → Project Management

**Specialized ecosystem (robotics-webapp):**
- `localhost:13330` → Physical hardware control (ROS/Unitree)
- `localhost:13331` → Social VR testing (OSC/VRChat)
- `localhost:13332` → 3D model processing

## Implementation Standards

- **Parallel Launch**: Use `asyncio.gather` for minimal startup latency
- **Health Probes**: Poll each server's health endpoint before enabling AI tool-calling
- **Zombie Protection**: Terminate child processes when main webapp exits

## Frontend Status Indicators

- GREEN: Server up, tools registered
- YELLOW: Starting/recovering
- RED: Failed or port blocked
