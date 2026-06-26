---
title: "Agentic Mesh - robofang Integration Spec"
category: architecture
status: draft
audience: mcp-dev
skill_candidate: false
related:
  - architecture/AGENTIC_MESH_ARCHITECTURE.md
  - architecture/AGENTIC_MESH_SECURITY.md
  - patterns/GITHUB_MAINTAINER_HEARTBEAT.md
last_updated: 2026-04-10
---

# Agentic Mesh — robofang Integration Spec

**Status:** Design — Phase 4 target  
**Date:** 2026-02-23  
**Owner:** Sandra Schi  

---

## Why robofang is the Right Home

robofang is already defined as the "nervous system" for a federated fleet of MCP servers. Its PRD describes: Universal Discovery, Capability Mapping, Council of Dozens, Hardware Bridge. Every one of these maps directly onto the agentic mesh architecture.

---

## robofang Mesh Components

### 1. Bridge Registry (`configs/bridge_registry.json`)

Declarative config defining which server can bridge to which, with scope constraints. Each server entry includes `tier`, `can_bridge_to`, and `bridge_scope` with `allowed_paths`.

### 2. robofang Bridge Factory

Generates validated bridge callables from the registry at startup. Enforces path allowlists, hop_count limits, and tier constraints in Python — not in LLM prompts.

### 3. Council of Dozens — Mesh Mapping

| Council member | Bridges | Typical workflow |
|---|---|---|
| `council_research_synthesiser` | advanced-memory, local-llm | arxiv + github → synthesis → skill note |
| `council_camera_event_handler` | camera, filesystem, advanced-memory, local-llm | motion → classify → log → archive |
| `council_knowledge_curator` | advanced-memory, local-llm | find stale notes → re-tag → summarise |
| `council_fleet_health_monitor` | all Tier 0-3 (read-only) | ping all servers → log status → alert |
| `council_github_maintainer_triage` *(optional)* | **git-github-mcp** (`github_ops`) | daily heartbeat: `pr_list` / `issue_list` per fleet repo → flag stale threads → draft ack comments (human or policy-approved send) — see **[patterns/GITHUB_MAINTAINER_HEARTBEAT.md](../patterns/GITHUB_MAINTAINER_HEARTBEAT.md)** |
| `council_robotics_coordinator` | robotics (Tier 4, confirmation gate) | sense → plan → confirm → actuate → log |

### 4. Input Sanitization

Applied to all external content before it enters a `workflow_prompt` or `messages` argument. Strips instruction-like patterns (ignore previous instructions, system:, you are now, override, call bridge_, execute_trajectory, emergency_stop).

---

## Robotics Integration Notes

`council_robotics_coordinator` is **disabled by default**. Enabling requires: `robotics_enabled: true` in config, confirmation endpoint configured, DRY_RUN mode for 48+ hours with adversarial prompt testing, physical safety perimeter confirmed.

Emergency stop endpoint (`http://localhost:10840/emergency_stop`) is registered in robofang's health monitor — callable directly from dashboard, bypasses the mesh.

---

## Implementation Phases

**Phase 4a:** Bridge Registry + Factory + Sanitization  
**Phase 4b:** Council meta-tools (camera, knowledge, fleet health)  
**Phase 4c:** Robotics gate (DRY_RUN default, adversarial test suite before live)  
**Phase 4d:** Dashboard integration (bridge registry visualised, live mesh activity, emergency stop always visible)

---

## Maintainer: GitHub fleet triage (operational)

Orchestrators (robofang, OpenManus, OpenClaw, etc.) are the natural home for a **recurring** “check all fleet repos for open PRs/issues” job — MCP tools are **on-demand** only. Use **`github_ops`** from **git-github-mcp**; mirror the same repo list in the **web `/inbox`** for human review. Full pattern: **[GITHUB_MAINTAINER_HEARTBEAT.md](../patterns/GITHUB_MAINTAINER_HEARTBEAT.md)**.
