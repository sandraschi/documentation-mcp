# Configuration

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HF_TOKEN` | (empty) | Hugging Face access token. Optional for read ops; required for gated models and serverless inference |
| `HFMCP_PORT` | `11152` | Backend port (HTTP mode / webapp REST) |
| `HFMCP_HOST` | `127.0.0.1` | Backend bind host |
| `HF_DEPOT_ROOT` | `D:\Dev\models\huggingface` | Model depot directory (models + `datasets/` subdir) |
| `OLLAMA_URL` | `http://127.0.0.1:11434` | Ollama base URL for `register_ollama` + local inference |
| `HF_INFER_PREFER_LOCAL` | `1` | Prefer local Ollama for `infer` when the model exists there |
| `HFMCP_PREFAB_APPS` | `1` | Set `0` to skip registering Prefab App tools (headless/CI) |
| `MCP_TRANSPORT` | `stdio` | `stdio`, `http`, or `sse` |
| `MCP_PORT` | - | Alias for HTTP mode port (PyInstaller/run_server.py pattern) |

## Setting Variables

In `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "huggingface": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\huggingface-mcp", "run", "python", "-m", "huggingface_mcp.server"],
      "env": {
        "HF_TOKEN": "your-token",
        "OLLAMA_URL": "http://127.0.0.1:11434"
      }
    }
  }
}
```

When running from source, copy `.env.example` to `.env` and fill values in.
The `.env` file is gitignored - never commit tokens.

## Config file

None - all configuration is environment variables. The SQLite database
(`data/hf.db`) and the depot are created automatically on first use.
