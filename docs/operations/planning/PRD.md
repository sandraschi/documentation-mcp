# PRD: MCP Central Documentation Infrastructure (MCD)

## 1. Overview
This project centralizes all documentation, standards, and metadata for the Antigravity fleet. It ensures that every agent (and developer) has a single source of truth for protocol implementation, tool design, and deployment standards.

## 2. Core Objectives
- **Zero First-Time Failures**: 100% server compliance with SOTA standards.
- **Documentation Freshness**: Automated sync of repo data to the central hub.
- **Portmanteau Adoption**: Consolidation of tools to prevent fragmentation.
- **Native-First Sensing**: Fleet-wide transition to local multimodal engines (Gemma 4).

## 3. Success Metrics
- **Performance**: < 200ms latency for Tier 2 native sensing (Zero-STT).
- **Compliance**: 100% of fleet adopts the `mcpb pack` and `llms.txt` standards.
- **Efficiency**: Sub-50ms documentation retrieval via LanceDB + documentation-mcp.
- **Fleet cold-start**: ≥ 80% `stack_ok` on full manifest probe after fix waves; zero `parse_failed`; `teardownOk` true for ≥ 95% of probed repos on goliath.

## 4. Key Features
- **Unified Metadata standards**: Standard way of declaring purpose, version, and health.
- **Proactive Discovery**: Agents can find each other via standard zero-config patterns.
- **Vectorized Search**: RAG over all fleet documentation.
- **Fleet webapp cold-start probe**: Sequential parse-check → start → backend + frontend + proxy health → teardown per repo; manifest-driven; reports at `scripts/out/fleet-webapp-report.json`; **Broken\*** re-run for failed-only iteration. Orchestrated from MetaMCP UI or `fleet-webapp-start-probe.ps1`. See [FLEET_WEBAPP_PROBE.md](docs/operations/FLEET_WEBAPP_PROBE.md).

## 5. Roadmap
- **Phase 1**: Centralize core standards (Complete).
- **Phase 2**: Launch LanceDB-powered Docs MCP (Complete).
- **Phase 3**: Implement fleet-wide "Native-First" multimodal requirements (In Progress).
- **Phase 4**: Automated SOTA quality auditing — **fleet cold-start probe + fix waves** (In Progress; Jun 2026 waves 1–2 landed; Jul 2026 contract smoke suite revived and verified).

---

*Last updated: 2026-07-20*
