# tiny-mcp-servers

Minimal single-file MCP servers — one concern each. Each server is a standalone Python file you run directly. No install required beyond `uv`.

## Usage

```bash
uv run python src/tiny_mcp/timestamp.py
uv run python src/tiny_mcp/clipboard.py
# etc.
```

Or use `just`:

```bash
just run timestamp
just run clipboard
```

## Servers

| Server | File | Deps | What it does |
|--------|------|------|-------------|
| clipboard | `clipboard.py` | pyperclip | Read/write system clipboard |
| timestamp | `timestamp.py` | — | Timezone-aware time conversions |
| qr | `qr.py` | qrcode+pil | QR code encode/decode |
| color | `color.py` | — | Hex/RGB/HSL conversion + palettes |
| ipcalc | `ipcalc.py` | — | CIDR subnet math |
| uuid | `uuid_mcp.py` | — | UUID generation + parsing |
| units | `units.py` | pint | Unit conversion |
| weather | `weather.py` | httpx | Current weather (no API key) |
| hash | `hash_mcp.py` | — | File/text hashing |
| diff | `diff.py` | — | Text/file diffing |
| mime | `mime.py` | — | MIME type detection |
| crontab | `crontab.py` | — | Cron expression parsing |

## Install deps (per-server extras)

```bash
uv sync --extra qr       # for qr server
uv sync --extra weather  # for weather server
uv sync --all-extras     # all
```
