# tahoma2d-mcp — Tahoma2D Render Engine (fleet note)

**Upstream repo:** `D:\Dev\repos\tahoma2d-mcp`

**FastMCP 3.2** — Headless .tnz scene rendering via tcomposer.exe + ffmpeg export.

> Pivot from "2D animation compositor" to "render orchestrator." ToonzScript
> (ECMAScript automation) is not available in the current Tahoma2D 1.6.1 build.
> Instead: create/edit .tnz scenes in the Tahoma2D GUI, render them headlessly
> via tcomposer.exe, export frames to video via ffmpeg.

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\tahoma2d-mcp` |
| **Ports** | Backend **11013**, Dashboard **11012** |
| **Start** | `just start` or `start.ps1` |
| **Depends on** | Tahoma2D 1.6+ (tahooma2d.org), ffmpeg (for export) |

## Tools

| Tool | Annotation | Description |
|------|------------|-------------|
| `tahooma2d_status` | READ_ONLY | Server + tcomposer health check |
| `tahooma2d_project` | READ_ONLY | List, inspect, open .tnz scene files |
| `tahooma2d_render` | MUTATING | Headless rendering via tcomposer.exe |
| `tahooma2d_export` | MUTATING | Frame sequences → MP4 via ffmpeg |

## Workflow

```
blender-mcp GP (create 2D) → .tnz → tahoma2d-mcp (render frames) → resolveops (final edit)
```

## Webapp Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Dashboard | tcomposer status, workflow overview |
| `/render` | Render | Submit .tnz scenes to tcomposer |
| `/export` | Export | Convert frames to video via ffmpeg |
| `/projects` | Projects | Browse .tnz scene files |
| `/settings` | Settings | Server config |
| `/help` | Help | Tool reference |

## MCP Client Config

```json
{
  "mcpServers": {
    "tahoma2d": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/tahooma2d-mcp", "run", "tahooma2d-mcp-server"]
    }
  }
}
```

## Fleet Integration

- **blender-mcp** — Grease Pencil 2D creation, exports to .tnz format
- **resolveops** — Final color grade and edit of rendered frames

## See Also

- [tahooma2d.org](https://tahooma2d.org)
- [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md)
- [FLEET_INDEX.md](../FLEET_INDEX.md)
