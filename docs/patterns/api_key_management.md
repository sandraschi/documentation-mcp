# API Key Management Pattern

**Status**: Active  
**Version**: 1.0  
**Applies to**: All fleet MCP servers with LLM-dependent features

## Rationale

Every MCP server that uses LLMs (chat, security analysis, code review, agentic tools,
etc.) needs API keys. Without a standard approach, each repo reinvents the wheel:
some use `.env`, others hardcode, others build bespoke config UIs. This pattern
establishes a single, predictable interface so the fleet-wide Settings UI component
works everywhere with zero per-repo customization.

## The Pattern

### Backend: Two endpoints

```
GET  /api/v1/settings/keys   -> returns masked keys + key definitions
POST /api/v1/settings/keys   -> accepts { keys: { ID: value } }, persists + returns masked
```

### Data flow

```
User enters key in Settings UI
  → POST /api/v1/settings/keys { keys: { ANTHROPIC_API_KEY: "sk-..." } }
    → backend writes to %LOCALAPPDATA%/<server>/keys.json
    → backend sets os.environ[ID] = value  (live update, no restart needed)
    → returns masked keys for display
```

### Storage

- **Path**: `%LOCALAPPDATA%\<server>\keys.json` (e.g. `C:\Users\<user>\AppData\Local\virtualization-mcp\keys.json`)
- **Format**: Simple JSON dict `{ "KEY_ID": "value", ... }`
- **Precedence**: User-saved keys override `.env` file values at runtime via `os.environ`
- **Security**: Never expose full keys in API responses; always mask.

### Masking

Show first 8 + `...` + last 4 characters:
```
sk-ant-abcdefgh...wxyz
```

Implementation (Python):
```python
def _mask_key(key: str) -> str:
    if len(key) < 16:
        return key[:4] + "..." + key[-4:] if len(key) > 8 else "****"
    return key[:8] + "..." + key[-4:]
```

### Key definitions

Each server declares its required keys as a `KEY_DEFINITIONS` list returned by the GET
endpoint. The frontend renders the form dynamically from this list.

```python
KEY_DEFINITIONS = [
    {"id": "ANTHROPIC_API_KEY", "label": "Anthropic (Claude)", "link": "https://console.anthropic.com/settings/keys"},
    {"id": "OPENAI_API_KEY",    "label": "OpenAI",           "link": "https://platform.openai.com/api-keys"},
    {"id": "GOOGLE_API_KEY",    "label": "Google (Gemini)",  "link": "https://aistudio.google.com/app/apikey"},
    {"id": "DEEPSEEK_API_KEY",  "label": "DeepSeek",         "link": "https://platform.deepseek.com/api_keys"},
]
```

### Frontend: Settings section

The fleet Settings UI already implements the "API Keys" section (sidebar item, password
inputs with show/hide toggle, Save Keys button). Any server that implements the two
endpoints above gets full key management with zero additional frontend work.

### Migration from .env

1. Add the two endpoints to the backend
2. On server startup, check `keys.json` first, then fall back to `.env`:
   ```python
   val = saved.get(id) or os.environ.get(id, "")
   ```
3. On key save via API, write to `keys.json` AND set `os.environ[id] = val` so
   existing code that reads env vars picks up the new value immediately
4. No changes needed to existing LLM client code

## Reference Implementation

See `virtualization-mcp` repo:
- `webapp/backend/app/main.py` — `GET /api/v1/settings/keys`, `POST /api/v1/settings/keys`
- `webapp/frontend/src/pages/settings.tsx` — API Keys UI section

## Adding to a new server

1. Copy the `_load_keys`, `_save_keys`, `_mask_key` helpers and `KEY_DEFINITIONS`
2. Copy the two endpoint handlers
3. Add `KeyRound` icon + `"API Keys"` to sidebar nav in settings.tsx
4. Copy the API Keys JSX section
