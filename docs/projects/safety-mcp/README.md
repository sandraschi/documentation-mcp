# safety-mcp

Threat forensics and verdict engine. Reads Windows Defender detections,
security event channels, and network evidence - then correlates them with
fleet intel from aiwatcher to produce an AI-assisted verdict
(benign / suspicious / incident) with a full evidence chain.

## What You Can Do

- **See what Defender flagged**: `defender_ops(operation="detections")`
  lists detections with threat names, severity, and flagged resources.
- **Correlate instead of guess**: `correlate(threat_id=...)` gathers every
  signal in the window (defender + processes + logons + powershell +
  firewall + connections + aiwatcher intel) and returns a graded verdict
  with evidence and recommendations.
- **AI triage, full chain**: verdicts are reasoned by the host LLM
  (`ctx.sample()`), fall back to Ollama, then a deterministic classifier -
  so it always works, even offline.
- **Fleet-aware**: verdicts push into aiwatcher's Fleet Events feed, and
  worm/campaign intel is pulled back as correlation context.
- **Never silent**: collectors fail loudly with recovery hints (elevation,
  missing cmdlets, disabled firewall logging) - no fabricated telemetry.

## Quick Install

```bash
git clone https://github.com/sandraschi/safety-mcp
cd safety-mcp
uv sync --all-extras
uv run python -m safety_mcp.server        # stdio MCP server
```

For the web dashboard: `just serve` (backend 11146, frontend 11147).
See [INSTALL.md](INSTALL.md) for all paths.

## Example Prompts

- "What did Defender detect in the last 24 hours?"
- "Is this detection a false positive or a real threat?" (paste the name)
- "Correlate threat 2147941383 and give me a verdict"
- "Show me firewall blocks and active connections from the last day"
- "What's the current safety posture?" (safety_health)

## Documentation

| Doc | Contents |
|-----|----------|
| [Installation](INSTALL.md) | All install methods, prerequisites |
| [Architecture](docs/ARCHITECTURE.md) | Collectors, verdict engine, data flow |
| [Configuration](docs/CONFIGURATION.md) | Env vars (SAFETY_*) |
| [Tool Reference](docs/TOOLS.md) | All MCP tools |
| [Development](docs/DEVELOPMENT.md) | Local setup, tests, mock fixtures |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues |

## Requirements

- Windows 11 (Defender cmdlets, Event Log, Firewall log) - Linux collector
  support is a future milestone
- PowerShell 7 (`pwsh`) recommended, PowerShell 5.1 works
- **Admin** for Security event channels (4688/4624)
- aiwatcher-mcp (port 10946) for fleet intel; optional, degrades gracefully
- Ollama (optional) for local LLM verdict triage
- No LLM? The deterministic classifier still produces verdicts

## License

MIT
