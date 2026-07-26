# Install

**Status: day 2, render tools real.** There is no one-click naked-PC install
yet - no `start.bat`/`start.ps1`, no webapp, no `.mcpb` release.
`render_svg`/`render_png` work; `mermaid_to_excalidraw` and `batch_render`
are still stubs. This is a dev-only install for now.

## Option A: dev checkout (current, only option)

Requires: [uv](https://docs.astral.sh/uv/), Python 3.11+.

```powershell
git clone https://github.com/sandraschi/sketchboard-excalidraw-mcp.git
cd sketchboard-excalidraw-mcp
uv sync --extra dev
uv run playwright install chromium
uv run pytest
```

`render_svg`/`render_png` need the Chromium binary Playwright drives, which
`uv sync` does not install by itself - that's what the
`playwright install chromium` step is for (one-time per machine, `just
playwright-install` also runs it). They also need outbound network access
to esm.sh on first render per process, since the excalidraw JS bundle isn't
vendored locally yet (see `docs/DESIGN.md`).

`just test` skips the real-renderer tests (they launch Chromium and hit the
network); run them explicitly with `just test-render`.

Register with an MCP client (stdio transport) pointing at:

```powershell
uv run python -m sketchboard_excalidraw_mcp.server
```

## Option B: naked-PC one-click install (not built yet)

Planned for day 2/3 once the canvas server and webapp land, following the
fleet's `start.ps1` + `Require-Command` pattern
([NAKED_PC_INSTALL_STANDARD.md](../mcp-central-docs/standards/NAKED_PC_INSTALL_STANDARD.md)).

## Option C: `.mcpb` bundle for Claude Desktop (not built yet)

`render_svg`/`render_png` are real now, so this is unblocked; packaging
(bundling the Chromium dependency, `mcpb validate`/`pack`) hasn't happened
yet - still pending remaining day 2/3 items (webapp, canvas bridge).
