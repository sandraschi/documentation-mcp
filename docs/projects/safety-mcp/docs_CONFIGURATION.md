# Configuration

## Environment Variables

All settings use the `SAFETY_` prefix and are read from the environment.

| Variable | Default | Description |
|----------|---------|-------------|
| `SAFETY_HOST` | `127.0.0.1` | HTTP bind host |
| `SAFETY_PORT` | `11146` | HTTP/MCP backend port |
| `SAFETY_DEFAULT_WINDOW_H` | `24` | Default lookback window (hours) for collectors |
| `SAFETY_MAX_EVENTS` | `500` | Max events per collector call |
| `SAFETY_POWERSHELL` | `pwsh` | PowerShell executable (pwsh or powershell.exe) |
| `SAFETY_DEFENDER_MODULE` | `ConfigDefender` | Defender module for cmdlets |
| `SAFETY_CUSTOM_CHANNELS` | `` | Comma-separated extra event channels |
| `SAFETY_FIREWALL_LOG` | `C:\Windows\System32\LogFiles\Firewall\pfirewall.log` | Firewall log path |
| `SAFETY_PACKETSNIFFER_URL` | `http://127.0.0.1:10920` | packetsniffer-mcp backend (sniff deep-dive) |
| `SAFETY_AIWATCHER_URL` | `http://127.0.0.1:10946` | aiwatcher-mcp backend (push/pull) |
| `SAFETY_AIWATCHER_TOKEN` | `` | Bearer token for aiwatcher (optional) |
| `SAFETY_VERDICT_SAMPLE` | `1` | Enable ctx.sample() LLM triage stage |
| `SAFETY_VERDICT_OLLAMA` | `1` | Enable Ollama triage stage |
| `SAFETY_OLLAMA_URL` | `http://127.0.0.1:11434` | Ollama endpoint |
| `SAFETY_OLLAMA_MODEL` | `qwen2.5:7b` | Ollama model for verdicts |
| `SAFETY_PUSH_AIWATCHER` | `1` | Push verdicts to aiwatcher fleet feed |
| `SAFETY_RECOMMEND_MIN_CONF` | `0.5` | Min confidence to include recommendations |
| `SAFETY_DB_PATH` | `%LOCALAPPDATA%\safety-mcp\safety.db` | SQLite verdict log |
| `SAFETY_LOG_LEVEL` | `INFO` | Logging level |

## Setting Variables

In `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "safety-mcp": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\safety-mcp", "run", "safety-mcp"],
      "env": {
        "SAFETY_AIWATCHER_URL": "http://127.0.0.1:10946",
        "SAFETY_OLLAMA_MODEL": "qwen2.5:7b"
      }
    }
  }
}
```

## Verdict engine chain

1. `ctx.sample()` — the connected host LLM (disable with `SAFETY_VERDICT_SAMPLE=0`)
2. Ollama probe — local LLM at `SAFETY_OLLAMA_URL` (disable with `SAFETY_VERDICT_OLLAMA=0`)
3. Deterministic classifier — always available, never disabled; encodes the
   PowhidSubExec false-positive rules

The deterministic stage guarantees verdicts even with no LLM available.

## Enabling firewall logging (for network evidence)

```powershell
Set-NetFirewallProfile -Profile Domain,Public,Private -LogBlocked 1 -LogAllowed 1
```

The log appears at `SAFETY_FIREWALL_LOG` (default pfirewall.log).
