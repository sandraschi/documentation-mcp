# ADN — Agent Development Notes

Short, dated notes for **decisions and operational context** that would otherwise scatter across chat logs. Naming: `ADN-YYYY-MM-DD-NNN-topic.md`.

**Topic hub (long-form):** `../integrations/gemini-deep-research-interactions-2026.md`

## Podman & Platform Integration (July 2026)

| ID | File | One-line purpose |
|----|------|------------------|
| 001 | [ADN-2026-07-20-001-podman-mcp-daemonless-transition.md](ADN-2026-07-20-001-podman-mcp-daemonless-transition.md) | Transitioning from monolithic Docker daemon to daemon-less async Podman CLI wrappers. |
| 002 | [ADN-2026-07-20-002-forgejo-integration.md](ADN-2026-07-20-002-forgejo-integration.md) | Scaffolding local, self-hosted git VCS and CI pipelines using Forgejo Actions. |
| 003 | [ADN-2026-07-20-003-kubernetes-orchestration.md](ADN-2026-07-20-003-kubernetes-orchestration.md) | Local multi-container development bridge from Podman Pods to Kubernetes manifests. |

## Fleet strategy (June 2026)

| ID | File | One-line purpose |
|----|------|------------------|
| 001 | [ADN-2026-06-05-001-fleet-strategy-gap-closure.md](ADN-2026-06-05-001-fleet-strategy-gap-closure.md) | Gap-closure roadmap: trust, secrets, orchestrator, life MCP, comms. |

## ittybitty / videogen-mcp (June 2026)

| ID | File | One-line purpose |
|----|------|------------------|
| 001 | [ADN-2026-06-12-001-ittybitty-fable5-live-validation.md](ADN-2026-06-12-001-ittybitty-fable5-live-validation.md) | Fable 5 live validation credit; not a provider — harness + R1/R2/planner fixes. |
| 002 | [ADN-2026-06-12-002-ittybitty-fable5-status-and-shutdown.md](ADN-2026-06-12-002-ittybitty-fable5-status-and-shutdown.md) | Status note (R1–R3 validated); global Fable/Mythos shutdown + policy post-mortem. |

## Gemini / Deep Research / Interactions (April 2026)

| ID | File | One-line purpose |
|----|------|------------------|
| 001 | [ADN-2026-04-22-001-announcement-synthesis.md](ADN-2026-04-22-001-announcement-synthesis.md) | What changed Dec 2025 → Apr 2026 and what to trust. |
| 002 | [ADN-2026-04-22-002-tailscale-funnel-mcp-ingress.md](ADN-2026-04-22-002-tailscale-funnel-mcp-ingress.md) | Why Funnel is the fleet-default public ingress for remote MCP. |
| 003 | [ADN-2026-04-22-003-starter-repos-index.md](ADN-2026-04-22-003-starter-repos-index.md) | Which GitHub starters are official vs adjacent. |
| 004 | [ADN-2026-04-22-004-pilot-and-guardrails.md](ADN-2026-04-22-004-pilot-and-guardrails.md) | Pilot order and guardrails before scaling MCP count. |
| 005 | [ADN-2026-04-22-005-meta-mcp-vs-gemini-bridge.md](ADN-2026-04-22-005-meta-mcp-vs-gemini-bridge.md) | MetaMCP stays orchestration; thin bridge for Interactions / Deep Research. |
