# OSC MCP Server: The Agentic Control Layer

The OSC MCP server provides a high-level interface for sending and receiving OSC messages, abstracting the raw UDP socket management.

## 🚀 Server Registration

```json
{
  "osc": {
    "command": "python",
    "args": ["-m", "osc_mcp.server"],
    "cwd": "D:/Dev/repos/osc-mcp",
    "env": {
      "OSC_DEFAULT_IP": "127.0.0.1",
      "OSC_DEFAULT_PORT": "9000"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `send_osc_msg` | Modulation | Sends a typed value (Float, Int, String) to a specific OSC address. |
| `batch_modulate` | Animation | Sends a sequence of messages to drive complex movements. |
| `listen_for_addr` | Discovery | Registers a hook to notify the agent when a specific OSC message is received. |
| `debug_osc_stream` | Monitoring | Logs all traffic on a specific port for technical analysis. |

## 📊 Interaction Principles

- **Delta Compression**: Agents should only send messages when a parameter value has changed significantly.
- **Timeout Management**: Listeners should have an automatic expiration to prevent memory leaks.

---
*Last updated: 2026-02-14*
