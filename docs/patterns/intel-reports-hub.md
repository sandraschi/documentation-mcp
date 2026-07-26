# Intel Reports Hub — fleet-wide publish pattern

Any MCP repo on Goliath can publish HTML reports to the shared hub on **port 11027**. Fritz and AIWatcher already use this; others need only HTTP.

## Prerequisites

Hub running (one of):

```powershell
Set-Location D:\Dev\repos\fleet-agent-mcp
.\scripts\start-intel-hub.ps1
```

## Publish API

```http
POST http://127.0.0.1:11027/api/reports/publish
Content-Type: application/json

{
  "title": "arxiv-mcp — code hunt drop",
  "source": "arxiv-mcp",
  "markdown": "# New weights repo\n\n…",
  "summary": "3 new code drops in cs.LG",
  "tags": ["arxiv", "code-hunt"]
}
```

Use `html` instead of `markdown` if you already have rendered HTML (AIWatcher digests).

Response includes `url_path` → open `http://<host>:11027{url_path}` on iPad.

## Python (any fleet repo)

```python
import httpx

async def publish_fleet_report(
    *,
    title: str,
    source: str,
    markdown: str = "",
    html: str = "",
    summary: str = "",
    hub_url: str = "http://127.0.0.1:11027",
) -> dict:
    async with httpx.AsyncClient(timeout=12.0) as client:
        resp = await client.post(
            f"{hub_url.rstrip('/')}/api/reports/publish",
            json={
                "title": title,
                "source": source,
                "markdown": markdown,
                "html": html,
                "summary": summary,
                "tags": [source, "fleet"],
            },
        )
        resp.raise_for_status()
        return resp.json()
```

Copy `aiwatcher_mcp/intel_hub_client.py` or `fleet_agent/intel_hub/client.py` as a template — both are thin wrappers.

## Via Fritz MCP (remote orchestration)

If the producer only talks MCP and Fritz is up:

```text
fleet_call_tool(
  server="fleet-agent",
  tool="intel_reports_publish",
  arguments={"title": "…", "markdown": "…", "source": "meta-mcp"}
)
```

## Source badge

Hub UI shows badges for `fritz`, `aiwatcher`, and a generic badge for any other `source` string — use your repo alias (`arxiv-mcp`, `meta-mcp`, `vla-mcp`, …).

## Urgent path (Fritz)

Fritz sends **urgent email + cursor inbox** when:

| Flow | Trigger |
|------|---------|
| **Devices Watch** | devices-mcp `/api/fleet/priority` — CO/smoke emergency, kitchen ≥45°C, Ring intrusion, Shelly threshold |
| Fleet Pulse | Pipeline critical, >50% MCP offline |
| Day Prep | AIWatcher hot items ≥ `urgent_email_threshold` (default 8.0) |
| Cursor spend | warn/critical (existing) |

devices-mcp exposes `GET http://127.0.0.1:10717/api/fleet/priority` — Fritz polls every **5m** (`coworker_devices_watch`).

Settings in `~/.fleet-agent/settings.json`:

| Key | Default |
|-----|---------|
| `urgent_email_enabled` | `true` |
| `urgent_email_threshold` | `8.0` |
| `heartbeat_email` + SMTP | required for email |

Other repos: publish to hub for iPad; call Fritz `aiwatcher_push_event` with `urgency_hint ≥ 8` to surface in AIWatcher bundles; or POST Fritz `/api/chat` / MCP for orchestration.

## Env

| Variable | Default |
|----------|---------|
| `INTEL_REPORTS_HUB_URL` | `http://127.0.0.1:11027` |
| `INTEL_REPORTS_DIR` | `%USERPROFILE%\.fleet-intel` |

See `fleet-agent-mcp/docs/INTEL_REPORTS_HUB.md` for Tailscale / Funnel.
