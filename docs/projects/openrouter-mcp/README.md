# openrouter-mcp

FastMCP 3.2 server for the [OpenRouter](https://openrouter.ai) API — browse the
400+ model catalog, look up live pricing and context windows, check your key's
balance, and run chat completions against any model behind a single key.

## Tools

| Tool | Purpose |
|------|---------|
| `openrouter_list_models(query?)` | List / filter the OpenRouter model catalog |
| `openrouter_get_model_details(model_id)` | Context window + per-1M-token pricing for one model |
| `openrouter_check_usage()` | API key balance, limit, and usage |
| `openrouter_chat(prompt, model, ...)` | Chat completion against any model, with optional fallback routing |

`openrouter_chat` supports OpenRouter's `models` fallback array (`fallback_models`)
and a `stream` flag. **Note:** `stream=True` consumes OpenRouter's SSE
*server-side* and returns the aggregated text — MCP tools return a single result,
so this does not stream tokens to the client. It is there to exercise the
streaming endpoint, not to deliver incremental output.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.11+.

```powershell
git clone https://github.com/sandraschi/openrouter-mcp
cd openrouter-mcp
uv sync
```

Create `.env` with your key (get one at https://openrouter.ai/keys):

```
OPENROUTER_API_KEY=sk-or-v1-...
```

`.env` is gitignored — never commit your key.

## Run

```powershell
# stdio (Cursor / Claude Desktop)
uv run python -m openrouter_mcp.server
```

Claude Desktop config:

```json
{
  "mcpServers": {
    "openrouter-mcp": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/openrouter-mcp", "run", "openrouter-mcp"]
    }
  }
}
```

## Scope

Intentionally minimal: stdio MCP only, no webapp. This is a focused OpenRouter
client — model discovery, pricing, account, and chat. For local model routing
(Ollama / LM Studio) use the relevant fleet servers; OpenRouter's value here is
the unified hosted-model catalog with live pricing.

## Status

Early (v0.1.0). Not yet fleet-SOTA complete — no Prefab cards, MCPB bundle,
`llms.txt`/`llms-full.txt`, `glama.json`, or test suite yet. See repo issues /
fleet docs for the promotion checklist.

## License

MIT
