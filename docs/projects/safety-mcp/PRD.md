# safety-mcp — PRD

**Version**: 0.1.0 (2026-08-04)
**Origin**: SPEC.md (mcp-central-docs/safety/safety-mcp-SPEC.md) — approved
2026-08-04 with locked decisions (full triage chain, ports 11146/11147,
full webapp with graded alert, bidirectional aiwatcher)
**Trigger incident**: Trojan:Win32/PowhidSubExec.B false positive during the
zoji-mcp build (mcp-central-docs/safety/defender-agent-false-positive-powhidsubexec.md)

## Purpose

Automate the forensics + correlation loop for Windows security telemetry
and produce an AI-assisted verdict with an evidence chain. It is a
**correlation engine, not a telemetry collector**: Windows already records
everything; the value is triaging the signals together.

## Architecture

- Collectors (PowerShell wrappers, JSON out, fail loudly with recovery
  hints): `defender.py` (Get-MpThreatDetection/Threat/ComputerStatus),
  `events.py` (Get-WinEvent 4688/4624/4104/Sysmon/custom),
  `network.py` (pfirewall.log DROP, connections, packetsniffer trigger)
- Verdict engine (`verdict.py`): gather evidence chain → triage chain
  (`ctx.sample()` → Ollama → deterministic classifier) → graded verdict
  (benign/suspicious/incident) + confidence + reasoning + recommendations
- Bidirectional aiwatcher: push verdicts to `/api/fleet/ingest` (source
  "safety-mcp", urgency scaled), pull worm/campaign keyword intel
- SQLite verdict log + collector health; webapp 11147 with graded alert
  banner (the flagship UI)

## Shipped

- 7 MCP tools (defender_ops, security_events, network_evidence, correlate,
  safety_health, show_verdict_prefab, show_health_prefab) + skill + prompt
- Deterministic classifier encodes the PowhidSubExec false-positive rules:
  cmdline-only + dev markers + no file + no egress + no intel → benign;
  file + severity >= 4 → incident
- Webapp: Dashboard (graded banner, KPIs, correlate-now), Verdicts
  (expandable evidence chains), Events, Tools, Skills, Chat, Logs,
  Settings, Help
- 19 pytest (incl. TestPowhidSubExecRegression) + 7 Playwright e2e
- MCPB bundle certified (clean-extract launch test: initialize + 7 tools)
- Docs: README, INSTALL, docs/{ARCHITECTURE,CONFIGURATION,DEVELOPMENT,
  ONBOARDING,TOOLS,TROUBLESHOOTING}, llms.txt/full, glama.json, AGENTS,
  CLAUDE, .cursorrules

## Known gaps (declared)

- v1 advisory only: no auto-quarantine/kill/block (by design, gated later)
- packetsniffer is on-demand, not continuous; egress evidence relies on
  firewall logs
- Non-Windows not supported (Defender/Event Log are Windows-native)
- Security channels need elevation (documented, fails loudly without it)
