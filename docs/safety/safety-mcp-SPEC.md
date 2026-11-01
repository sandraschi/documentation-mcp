# SPEC: safety-mcp — Threat Forensics & Verdict Engine

**Status**: APPROVED 2026-08-04 (decisions locked below)
**Established**: 2026-08-04
**Trigger incident**: `Trojan:Win32/PowhidSubExec.B` false positive during
zoji-mcp build (see `mcp-central-docs/safety/defender-agent-false-positive-powhidsubexec.md`).
The manual forensics loop performed there (Defender detections -> process
correlation -> verdict) is the exact workflow this server automates.

## 0. Locked decisions (2026-08-04)

| # | Question | Decision |
|---|----------|----------|
| 1 | Verdict LLM chain | **Full sequence**: `ctx.sample()` -> Ollama probe -> deterministic classifier. Deterministic must reproduce the PowhidSubExec manual verdict offline (regression test). |
| 2 | Ports | **11146** (backend) / **11147** (frontend) - register in WEBAPP_PORTS.md |
| 3 | Webapp | **Full catch-them-all**, with informative dashboard: visible, **graded**, immediate alert banner (benign/suspicious/incident + color + latest verdict summary). |
| 4 | aiwatcher | **Bidirectional**: push verdicts via `/api/fleet/ingest` AND pull fleet-intel reports (worm/campaign mentions) as correlation context. |

---

## 1. Goal

A FastMCP server that automates the **forensics + correlation loop** for
Windows security telemetry and produces an **AI-assisted verdict** with an
evidence chain:

```
Defender detections + security event channels + network evidence
        |                         |                          |
        +----------- correlate(threat_id, window) -----------+
                            |  (LLM triage)
                            v
              VERDICT: benign | suspicious | incident
                            |
                            +--> POST /api/fleet/ingest -> aiwatcher
```

It is a **correlation engine, not another telemetry collector**. It reads
what Windows already records (Defender, Event Log, Firewall) and lets an LLM
reason across it - the step that currently requires a human.

## 2. Scope (v1 - Verdict engine + AI triage)

- Collect: Defender detections/status/history, security event channels,
  network evidence (Firewall logs + on-demand packetsniffer trigger).
- Correlate: detections + processes + events + network + optional external
  intel (aiwatcher reports) -> verdict with evidence chain.
- Push: verdicts to aiwatcher via `/api/fleet/ingest` (existing connector
  contract: `{title, summary, source, url, urgency_hint}`).
- **No auto-quarantine, no kill-process, no block-IP** in v1. Verdicts are
  advisory; remediation stays human/agent-gated.

## 3. Out of scope (v1)

- Continuous packet capture (packetsniffer-mcp stays on-demand; continuous
  evidence comes from Windows Firewall logs / ETW).
- Auto-remediation / SOAR actions.
- Non-Windows hosts (Linux later; Defender is Windows-only anyway).
- Fleet-wide remote forensics (localhost only in v1).

## 4. Repo layout

```
safety-mcp/
├── pyproject.toml, justfile, uv.lock
├── README.md, INSTALL.md, CHANGELOG.md, AGENTS.md, CLAUDE.md
├── llms.txt, llms-full.txt, glama.json
├── .env.example, .gitignore, .mcpbignore
├── .github/workflows/ci.yml
├── assets/prompts/ (3-4-100), assets/icon.png
├── src/safety_mcp/
│   ├── server.py            # FastMCP + FastAPI (lifespan=_mcp_http.lifespan)
│   ├── config.py            # ZOJI-style env config (SAFETY_* prefix)
│   ├── defender.py          # Get-MpThreatDetection / Get-MpThreat / status
│   ├── events.py            # Get-WinEvent 4688/4624/4104/Sysmon
│   ├── network.py           # Firewall logs + packetsniffer trigger
│   ├── correlate.py         # evidence gathering + LLM verdict call
│   ├── aiwatcher.py         # /api/fleet/ingest pusher
│   ├── runtime.py, db.py    # module state + SQLite verdict log
│   ├── skills/safety-expert/SKILL.md
│   └── tools/               # portmanteau: defender_ops, security_events,
│                            #   network_evidence, correlate, safety_health
├── tests/                   # mocked Defender/EventLog via declared fixtures
├── docs/ (ONBOARDING, CONFIGURATION, DEVELOPMENT, TOOLS, TROUBLESHOOTING, ARCHITECTURE)
└── webapp/ (React+Vite+Tailwind: Dashboard, Verdicts, Events, Help, Settings)
```

## 5. MCP tools (one portmanteau + helpers)

| Tool | Operation | Returns |
|------|-----------|---------|
| `defender_ops` | `detections` (recent, by threat_id), `status`, `history`, `threat_info` | structured detections: time, threat id/name, severity, resources, process |
| `security_events` | `process_creation` (4688), `logons` (4624), `powershell` (4104), `sysmon`, `custom` | WinEvent rows within window |
| `network_evidence` | `firewall_blocks` (window), `connections` (active), `sniff` (triggers packetsniffer on-demand) | evidence rows |
| `correlate` | `threat(threat_id, window)` | **verdict** + evidence chain + confidence + recommendations |
| `correlate` | `window(hours)` | all signals in window -> verdict (no specific threat) |
| `safety_health` | status of all collectors + last verdict + aiwatcher link | diagnostics |

## 6. The verdict contract (the AI part)

```json
{
  "verdict": "benign" | "suspicious" | "incident",
  "confidence": 0.0-1.0,
  "threat": "Trojan:Win32/PowhidSubExec.B" | null,
  "window": {"from": "...", "to": "..."},
  "evidence": [
    {"kind": "defender", "detail": "...", "ts": "...", "flagged": true},
    {"kind": "process", "detail": "pwsh -Command Start-Process -WindowStyle Hidden", "ts": "...", "flagged": false},
    {"kind": "network", "detail": "127.0.0.1:11144/mcp/ POST", "ts": "...", "flagged": false},
    {"kind": "intel", "detail": "no matching aiwatcher worm reports", "flagged": false}
  ],
  "reasoning": "hidden-window spawn + port kill + localhost JSON-RPC probe matches fleet dev workflow; no file resource flagged; no egress; verdict benign",
  "recommendations": ["add scoped Defender exclusion", "monitor if repeats"],
  "is_mock": false
}
```

**LLM triage**: uses `ctx.sample()` (FastMCP sampling) when a connected LLM
is available; falls back to a deterministic heuristic classifier (severity +
file-resource presence + egress + process provenance) otherwise. The
deterministic path must reproduce the manual PowhidSubExec verdict.

## 7. aiwatcher extension (second deliverable)

aiwatcher-mcp gains one optional consumer: `safety-mcp` verdicts land in the
Fleet Events feed via the **existing** `POST /api/fleet/ingest` endpoint
(`{title, summary, source: "safety-mcp", url, urgency_hint}`). No aiwatcher
code change required in v1 - the contract already exists. If a `safety`
field is later wanted, extend `ingest_fleet_event` with an optional
`extra_tags`/`category` param (small, additive).

## 8. Non-negotiables

- **No fake verdicts**: if collectors return nothing, verdict says "no
  signals" - never fabricate an incident.
- Declared mock mode (replay fixtures) for tests/CI, `is_mock` flagged.
- Hardware/OS calls fail loudly (Defender cmdlet missing, no admin) with
  recovery suggestions.
- Verdicts logged to SQLite; `safety_health` shows collector status.
- PowerShell SOTA: fleet-standard ps1 wrappers, no `&&`, no em dashes.

## 9. Open questions

**RESOLVED (2026-08-04)** — see §0. All four locked.
