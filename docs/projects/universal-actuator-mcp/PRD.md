# Product: Universal Actuator Federation Gateway (PRD)

**Objective:** To provide a unified, performant, and agent-accessible routing layer for the diverse RoboFang consumer fleet.

---

## 🚀 Vision Statement

A single gateway that empowers agents to search, track, and command a heterogeneous fleet of MCP servers without needing individual port management or protocol knowledge.

## Targeted Features

| Feature | Description | Priority |
|---------|-------------|----------|
| **Federated Search** | One-stop search across Plex, Calibre, and Immich with result ranking. | P0 |
| **Fleet Discovery** | Zero-config discovery of new MCP nodes via port-scanning. | P0 |
| **Milestone Log** | Centralized audit of agent accomplishments across the ecosystem. | P1 |
| **App Lifecycle** | Remote start/stop of fleet webapps through standardized scripts. | P1 |
| **Fleet Telemetry** | High-level CPU/Memory/Health metrics dashboard. | P2 |

## User Experience (Agentic & Human)

1.  **Agentic Interface**: Clean, portmanteau-focused tools (`glom_on`, `search_federated`) that hide complexity.
2.  **Human Dashboard**: High-fidelity Glassmorphic UI (Next.js) showing live telemetry and media inventory.

## Technical Constraints

- **Language**: Python 3.12 (Backend) / Next.js 16 (Frontend).
- **Transport**: Stdio for agentic use; SSE for web-streaming; REST for dashboard API.
- **SOTA Compliance**: Mandatory port range 10700-10800; zero-rust aesthetics.

---
*Product Vision v1.1.0 | RoboFang Engineering*
