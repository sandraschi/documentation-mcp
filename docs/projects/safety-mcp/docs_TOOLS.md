# Tool Reference

## defender_ops

Query Windows Defender telemetry.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `operation` | Literal[detections, status, threat_info, history] | yes | What to query |
| `threat_id` | int | threat_info | Threat ID for metadata |
| `since_hours` | int | no | Lookback window (default configured) |

**Operations:**

- `detections` — recent threat detections (threat names, severity, resources, process)
- `status` — protection state (real-time protection, signature age, scan age)
- `threat_info` — metadata for one threat ID (name, severity, category, active, resources)
- `history` — detections with a wide window (default 1 year)

**Example:**

```
defender_ops(operation="detections", since_hours=24)
defender_ops(operation="threat_info", threat_id=2147941383)
```

**Errors:** CollectorError with recovery suggestions (module missing, elevation).

## security_events

Query security event channels.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `channel` | Literal[process_creation, logons, powershell, sysmon, custom] | yes | Channel |
| `event_id` | int | no | Event ID filter (custom) |
| `log_name` | str | custom | Log name for custom channel |
| `since_hours` | int | no | Lookback window |
| `limit` | int | no | Max events (1-1000) |

**Channels:**

- `process_creation` — Security 4688 (new processes)
- `logons` — Security 4624 (successful logons)
- `powershell` — PS Operational 4104 (script-block logging)
- `sysmon` — Sysmon/Operational when installed
- `custom` — any log name + event ID

**Example:**

```
security_events(channel="process_creation", since_hours=24, limit=100)
security_events(channel="custom", log_name="Security", event_id=1102)
```

**Errors:** ACCESS_DENIED (elevation required) with recovery hints.

## network_evidence

Network evidence collection.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `operation` | Literal[firewall_blocks, connections, sniff] | yes | Operation |
| `since_hours` | int | no | Lookback window |
| `seconds` | int | no | Sniff duration (1-120) |

**Operations:**

- `firewall_blocks` — DROP/BLOCK entries from pfirewall.log
- `connections` — active established TCP connections
- `sniff` — on-demand packetsniffer-mcp capture (deep-dive)

**Example:**

```
network_evidence(operation="firewall_blocks", since_hours=24)
network_evidence(operation="sniff", seconds=15)
```

**Errors:** firewall log not enabled (with the enable command), sniffer unreachable.

## correlate

The verdict engine.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `threat_id` | int | no | Correlate around a specific threat ID |
| `window_h` | int | no | Lookback window (default configured) |

Gathers Defender detections, security events, network evidence and
aiwatcher intel, then produces a graded verdict:

```json
{
  "verdict": "benign" | "suspicious" | "incident",
  "confidence": 0.0-1.0,
  "threat": "Trojan:Win32/PowhidSubExec.B" | null,
  "evidence": [{"kind": "defender|process|logon|powershell|sysmon|network|intel", "detail": "...", "flagged": bool}],
  "reasoning": "human/LLM-readable explanation",
  "recommendations": ["..."],
  "triage_source": "llm-sample" | "llm-ollama" | "deterministic"
}
```

Verdicts are persisted to SQLite and (optionally) pushed to aiwatcher.

**Example:**

```
correlate()
correlate(threat_id=2147941383, window_h=48)
```

## safety_health

Collector + persistence diagnostics.

**Example:**

```
safety_health()
```

Returns per-collector status (defender cmdlets, aiwatcher), verdict count,
latest verdict, and mock flag.

## Prefab cards

- `show_verdict_prefab(limit)` — recent verdicts, graded by color
- `show_health_prefab()` — collector health
