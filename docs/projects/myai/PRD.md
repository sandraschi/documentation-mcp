# MyAI Platform – Product Requirements Document

_Last updated: 2025-11-10_

---

## 1. Executive Summary
MyAI is a production-ready AI platform that unifies ten specialized AI microservices, a FastAPI-based operations dashboard, and an MCP server into a single orchestrated stack. The platform must enable operators to provision, observe, and control AI workloads with minimal manual effort while providing rich APIs and MCP tooling to downstream clients such as Claude Desktop. This PRD defines the functional scope, architectural requirements, and success metrics for the platform’s ongoing evolution toward a 9.5+/10 production readiness score.

---

## 2. Goals & Non-Goals

### 2.1 Goals
- Deliver a dependable control plane (dashboard + MCP server) for starting, stopping, and monitoring microservices.
- Provide a curated set of AI workloads (conversation, RAG, multimodal generation, media augmentation) with consistent ops contracts.
- Offer first-class observability (metrics, logs, health checks) and secure default configurations (non-root, API keys, CORS).
- Support dual-mode operation: REST APIs for human operators and MCP tools for AI copilots.
- Maintain compliance with FastMCP 2.12+ documentation standards, Docker security baselines, and central documentation guidelines.

### 2.2 Non-Goals
- Hosting arbitrary third-party services without onboarding work (new services require adherence to service contract).
- Building proprietary LLM models; the platform integrates existing back-ends (Ollama, vLLM, Gemini, etc.).
- Providing multi-tenant SaaS features; focus remains on a single-tenant operator experience.

---

## 3. Stakeholders & Users

| Persona | Needs | Touchpoints |
| --- | --- | --- |
| **Platform Operator** | Start/stop services, inspect health, review logs/metrics, apply updates | Dashboard UI, Grafana, Portainer, MCP tools |
| **AI Engineer** | Extend services, integrate new models, run tests, enforce standards | Repo, developer workflows, docs, scripts |
| **AI Assistant (Claude Desktop)** | Structured tools to gather status, manipulate services | MCP tools (`start_ai_service`, `get_platform_status`, etc.) |
| **End User** | Consume AI experiences (chat, document RAG, image/video generation) | Service-specific UIs/APIs |

---

## 4. Product Scope

### 4.1 Control Plane
- FastAPI dashboard on port 3060 with REST endpoints for service lifecycle management, health summaries, and configuration.
- MCP server (FastMCP 2.12+) exposing at least eleven operations with 50+ line docstrings and no `description=` decorators.
- API key enforcement (`X-API-Key`) and CORS whitelist (3060, 3020, 8000).

### 4.2 AI Microservices
- **Conversation:** `bob_and_alice`, `character_conversation`, `future_you`, `teams_debate`.
- **Content Generation:** `stablediff_gradio`, `talking_avatar`, `gemini_tools`.
- **Document & Media:** `document_viewer`, `calibre_plus`, `plex_plus`.
- Every service must provide: Dockerfile, health endpoint, resource limits, logging to stdout, config entry in `core/dashboard/config.json`, and compose definition.

### 4.3 Infrastructure Components
- Traefik gateway, Prometheus, Grafana, Loki, Promtail, Portainer, Weaviate, PostgreSQL, vLLM (GPU).
- Shared Docker network `ai-network`, standard volume mounts, GPU reservations where required.

### 4.4 Observability & Ops
- Liveness and readiness endpoints aggregated at `/api/v1/health/status`.
- Grafana dashboards bundled in `monitoring/grafana/`.
- Loki/Promtail shipping container logs with 7-day retention (configurable).
- Scripts for diagnostics (e.g., `scripts/diagnostics/*.ps1`) and maintenance tasks.

---

## 5. Functional Requirements

### 5.1 Dashboard
- Display real-time service status (running, stopped, unhealthy) with resource data.
- Allow operators to start/stop/restart services individually or in groups.
- Surface platform-wide health (Docker daemon reachability, GPU availability, free disk).
- Offer configuration viewer/editor for `config.json` (future enhancement).

### 5.2 MCP Server
- Provide toolset: `start_ai_service`, `stop_ai_service`, `restart_ai_service`, `list_ai_services`, `get_service_status`, `get_platform_status`, `start_platform`, `stop_platform`, `generate_image_gradio`, `start_ai_chat`, `myai_help`.
- Each tool must follow FastMCP docstring template (FEATURES, REQUIREMENTS, Args, Returns, Examples, Notes, Related Tools).
- Tools must handle errors gracefully (no uncaught exceptions) and return structured dictionaries.

### 5.3 Service Contract
- Service configuration entries include name, description, categories, ports, docker compose target, health endpoint, GPU requirement, docs link.
- Health endpoints must return JSON with `status` and optional `details`.
- Compose definitions enforce `user: "1000:999"`, CPU/memory limits, GPU reservations if needed.
- Logging to stdout with structured messages; no persistent log files inside containers.

### 5.4 Monitoring
- Prometheus scrapes metrics for dashboard, microservices, infrastructure.
- Grafana dashboards provide: service uptime, resource usage, request latency, GPU status.
- Loki retains logs; dashboard UI links to relevant Grafana/Loki views.

### 5.5 Security
- API gateway terminates HTTP and routes to backend services; TLS termination optional but supported.
- Dashboard enforces API key; instructions provided for rotating keys.
- Secrets stored via `.env`, `.env.local`, or Docker secrets (future).
- `Select-String` check ensures no `@mcp.tool(description=...)` regressions.

---

## 6. Non-Functional Requirements

| Category | Requirement |
| --- | --- |
| **Reliability** | Platform must recover from `docker compose up -d` without manual steps; service restarts tracked. |
| **Performance** | Dashboard should respond in <200ms median; service start operations <120s typical. |
| **Scalability** | Compose stack supports horizontal scaling for select services (documented in `docker-compose.yml`). |
| **Security** | No containers run as root; sensitive volumes read-only; CORS locked; API key required. |
| **Documentation** | README/PRD kept current; `docs/` updated when features land; central docs referenced. |
| **Standards Compliance** | Align with `mcp-central-docs/STANDARDS.md`, `FASTMCP_2.12_MIGRATION.md`, Browser Automation Testing standards. |

---

## 7. Roadmap

| Phase | Timeline | Focus | Deliverables |
| --- | --- | --- | --- |
| **Phase 1 – Stabilize** | Q4 2025 | Ops hardening, doc refresh | Updated README/PRD, status reports, MCP docstring audit, Grafana dashboards |
| **Phase 2 – Automate** | Q1 2026 | Developer workflows | Scripts for service scaffolding, config editor, CI lint/test pipeline |
| **Phase 3 – Scale** | Q2 2026 | Multi-environment & deployment | GitHub Actions pipeline, container registry integration, production TLS recipe |
| **Phase 4 – Extend** | Q3 2026 | New capabilities | Additional MCP portmanteau tools, AI workload catalog expansion, AI guardrails |

---

## 8. Success Metrics

- **Operational Score**: Raise production readiness from 7.5/10 to 9.5/10 (per status reports).
- **MCP Compliance**: 100% tools passing docstring lint checks; zero `description=` occurrences.
- **Service Health**: >99% uptime for core dashboard and monitoring services under normal load.
- **Observability Coverage**: 100% services emitting metrics and logs to Prometheus/Loki.
- **Documentation Quality**: README/PRD updated within 48 hours of major changes; linked in central docs.
- **Security**: No containers running as root; monthly audit of secrets, CORS, API key enforcement.

---

## 9. Open Questions
- Should service onboarding be automated via CLI or MCP tool?
- What is the long-term strategy for GPU resource scheduling (K8s vs Docker Compose)?
- Do we provide automated backup/restore for persistent volumes (PostgreSQL, Weaviate)?
- How do we integrate Browser Automation Testing into CI for service UIs?

---

## 10. References
- `docs/MCP_SERVER_DEVELOPMENT_PATTERNS.md`
- `docs/MYAI_STATUS_REPORT_*.md`
- `docs/monitoring/`
- `mcp-central-docs/STANDARDS.md`
- `mcp-central-docs/FASTMCP_2.12_MIGRATION.md`

The MyAI Platform PRD should be reviewed quarterly or after any major architectural change.
