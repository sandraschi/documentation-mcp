# Troubleshooting

## "Failed to fetch" in web UI

The frontend can't reach the backend. Check:

1. Backend is running: `uv run uvicorn monitoring_mcp.server:app --port 10851`
2. Port matches `web_sota/src/lib/api.ts` (`API_BASE = "http://127.0.0.1:10851"`)
3. CORS allows `http://127.0.0.1:10850` (frontend origin)

## Backend starts but tools return connection errors

The server can't reach Grafana/Prometheus/Loki. Check:

- Are the services running? (Docker: `docker ps`)
- `MONITORING_MCP_GRAFANA_URL` etc. point to the right host:port
- For Docker, use `host.docker.internal` instead of `localhost` to reach host services
- For Docker Compose, use the service name (e.g. `http://grafana:3000`)

## Auth errors (401)

If `MCP_WEB_USER` / `MCP_WEB_PASSWORD` are not set, the web API returns 500.
Set them in `.env` or as environment variables before starting.

## "Operation X is not yet implemented"

Many advanced operations are placeholders. The tool reference in [TOOLS.md](TOOLS.md)
marks each operation's status. Use the implemented operations listed there.

## NSIS installer hangs on install/uninstall

The hooks in `native/windows/hooks.nsh` kill the backend process before install.
If a zombie process holds the port, run manually:

```powershell
taskkill /F /IM monitoring-mcp-backend.exe
taskkill /F /IM monitoring-mcp-native.exe
```

## Tauri WebView shows blank screen

Check `web_sota/dist/` exists and was built (`cd web_sota && npm run build`).
Check `tauri.conf.json` `frontendDist` points to `../web_sota/dist`.

## Windows Defender flags PyInstaller .exe

Common false positive for onefile PyInstaller binaries. Add an exclusion or
submit to Microsoft for review. Building with `--onedir` (instead of `--onefile`)
can reduce false positive rate.
