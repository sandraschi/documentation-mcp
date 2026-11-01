---
title: "In-Server about Tool - Documenting the MCP + Webapp Combo"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-09
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# In-Server `about` Tool - Documenting the MCP + Webapp Combo

**Status:** Official Fleet Standard
**Version:** 1.0 (2026-08-27)

---

## 1. Why this exists

Most fleet repos ship **two halves of one product**: an MCP server (the AI-tool surface,
discoverable and installable via the MCP Registry and Claude Desktop) and a **webapp**
(the visual dashboard / full product). The MCP server is what a new user actually installs
from the registry - the `.mcpb` bundle deliberately excludes `web_sota/`. So a user who
discovers a repo through the registry can run the tools but has **no in-band way to learn the
webapp exists**, what it adds, or how to get it. The README documents it, but an MCP-client
user often never opens the README.

This standard adds a single, small `about` tool to every server that carries a meaningful
webapp, so the combo is explained **inside the chat where the user already is**.

## 2. When it is required

- **Required:** any repo that ships both an MCP server and a real webapp (the fleet default).
- **N/A:** a server-only repo with no webapp component - write `about: N/A` in that repo's
  `docs/DEVELOPMENT.md` with a one-line rationale, and skip the tool.
- **Scope:** the tool is an onboarding blurb, **not a manual**. Keep it compact.

## 3. Tool contract

One MCP tool named `about` (no `operation` portmanteau - this is a single, stateless intro).

```python
@mcp.tool()
def about() -> str:
    """Explain what this MCP server is, the webapp it pairs with, and where to get the full install."""
```

Returns a short markdown string (roughly 12-25 lines) covering, in order:

1. **What this is** - one to two lines: the MCP server, what it controls.
2. **The webapp** - what it adds on top of the tools (visualization, dashboard, richer UX),
   and its **live URL**.
3. **Full install** - a link to the GitHub repository (where the webapp + `INSTALL.md` +
   docs live), i.e. the "everything" option.

The GitHub link must come from the repo's actual remote; the webapp URL must come from
**configuration, never a hardcoded assumption** (see §4).

## 4. Webapp URL - config-driven, not hardcoded

The webapp URL is environment-dependent (host, port). Rules:

- Read it from an env var first, e.g. `RESONITE_WEBAPP_URL`, `GODOT_WEBAPP_URL`, i.e.
  `<APP>_WEBAPP_URL`.
- Fall back to a default derived from the repo's **registered webapp port** (the one in
  `mcp-central-docs/operations/WEBAPP_PORTS.md`), defaulting the host to `127.0.0.1`.
- Never embed a hardcoded URL that ignores the configured host/port.

```python
_WEBAPP_URL = os.environ.get("RESONITE_WEBAPP_URL", "http://127.0.0.1:10978")
```

## 5. Reference implementation

```python
import os
import re


def _repo_url(default: str) -> str:
    """Return the GitHub repo URL, preferring the git remote."""
    try:
        out = os.popen("git remote get-url origin 2>nul").read().strip()
        out = out.replace(".git", "").replace("git@github.com:", "https://github.com/")
        if re.match(r"^https?://", out):
            return out
    except Exception:
        pass
    return default


_WEBAPP_URL = os.environ.get("RESONITE_WEBAPP_URL", "http://127.0.0.1:10978")
_REPO_URL = _repo_url("https://github.com/sandraschi/resonite-mcp")


@mcp.tool()
def about() -> str:
    """Explain this MCP server, its paired webapp, and where to get the full install."""
    return f"""# Resonite MCP

**MCP server:** control the Resonite social VR platform from chat - sessions, avatars,
inventory, OSC, ResoniteLink world editing, the cloud REST API, and the cross-fleet asset
pipeline.

## Paired webapp
This server ships with a **web dashboard** that visualizes everything the tools can do:
connection health, the live world node tree, inventory, gallery, and controls.

Open it at: **{_WEBAPP_URL}**
(Requires the webapp to be running - see the repo below for how.)

## Full install
The webapp and all setup docs live in the repo:
{_REPO_URL}

**Quick start:** INSTALL.md -> clone -> just bootstrap -> just serve (webapp on the URL
above, backend + MCP alongside).
"""
```

## 6. Also expose as a `help` topic

In addition to the `about` tool, register the same content as a `help` topic so users coming
through `help()` find it too, e.g. `help("basic", "get_started")` or `help("basic", "about")`
returns the combo blurb. The `about` tool is the discoverable entry point; the help topic is
the fallback for users already inside the help system.

## 7. Verification

- The `about` tool returns the combo blurb with a valid webapp URL and a reachable repo link.
- The webapp URL reflects the configured host/port (or the `<APP>_WEBAPP_URL` override).
- Runs without error under both `stdio` and `http` transports.
- Listed in `docs/TOOLS.md` under the system/help tools.

## 8. Relationship to existing tools

This complements, not replaces, the existing `help()` / `status()` tools and Prefab
`app=True` cards. `about` is the *product* story (what am I + the webapp + full install);
`help` is the *tool* reference; `status` is *health*; Prefab cards are *live UI*. Keep the
division: `about` does not enumerate tools.
