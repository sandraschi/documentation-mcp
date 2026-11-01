---
title: "Fleet Crossconnect Standard"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Fleet Crossconnect Standard

**Status**: ACTIVE -- applies to all sandraschi MCP fleet repositories  
**Adopted**: 2026-09-12  
**Canonical Path**: `mcp-central-docs/standards/FLEET_CROSSCONNECT_STANDARD.md`  

---

## 1. Overview and Problem Statement

The `sandraschi` GitHub organization hosts over 200 FastMCP servers and AI webapps. As domain ecosystems expand (e.g. audio, vision, desktop automation, robotics, knowledge indexing), servers frequently collaborate:

- A workflow automation server (`xyz`) may send notifications through `email-mcp`.
- A robotics controller (`yahboom-mcp`) may use `speech-mcp` for voice synthesis and `reaper-mcp` for audio output.
- A research assistant (`arxiv-mcp`) may sync library records into `calibre-mcp`.

When a user on GitHub installs repo `xyz`:
1. They must be clearly informed if `xyz` can integrate with `email-mcp`.
2. They must know whether `email-mcp` is required or optional.
3. They must not fall into **transitive install hell** (installing `xyz` forcing `email-mcp`, which forces `auth-vault`, which forces `docker`, etc.).

This standard specifies how to declare, document, and handle fleet crossconnects.

---

## 2. The Core Architectural Rules

### Rule 1: Zero Mandatory Transitive Installs (Standalone by Default)
Every MCP server in the fleet MUST be able to boot, pass health checks, and execute its core tools completely standalone.

- **Soft Crossconnects Only**: Inter-server connections across the fleet MUST be optional enhancements or graceful companions.
- **Crash Immunity**: A server must NEVER throw a fatal error or refuse to start because a companion server (like `email-mcp`) is not installed or not running.
- **Library vs Server Boundary**: If repo `xyz` strictly cannot function without a component, that component MUST be distributed as an in-repo Python module or PyPI package dependency (`pyproject.toml`), NOT as a separate MCP server daemon.

### Rule 2: The 1-Hop Contract
When documenting or guiding users on crossconnects:
- Repo `xyz` documents and links **only its direct peers** (1 hop away).
- Repo `xyz` NEVER attempts to document or walk the transitive dependencies of `email-mcp`.
- `email-mcp` is responsible for its own standalone installation and documentation.

### Rule 3: Graceful Runtime Degradation (Dialogic Errors)
When a user or agent invokes a tool that relies on an uninstalled companion server:
- Do not crash or raise an unhandled exception.
- Return an actionable, structured message explaining what is missing and providing the exact GitHub URL for the companion:

```python
if not peer_available:
    return (
        "Action Required: The 'email-mcp' companion server was not detected. "
        "To enable email delivery, please install sandraschi/email-mcp: "
        "https://github.com/sandraschi/email-mcp"
    )
```

---

## 3. Repository Documentation Requirements

Any repo that connects to or enhances another fleet repo MUST include documentation in three standard locations:

### 3.1 Primary `README.md`
Add a dedicated `## Fleet Crossconnects (Companions)` section immediately following the capabilities / "What You Can Do" section.

```markdown
## Fleet Crossconnects (Companions)

`xyz` works completely standalone. You can optionally connect it with companion servers in the `sandraschi` fleet to unlock extended features:

| Companion Server | Feature Unlocked | Status | Setup |
|---|---|---|---|
| [`email-mcp`](https://github.com/sandraschi/email-mcp) | Automated digest dispatch and alerting | Optional | [Install Guide](https://github.com/sandraschi/email-mcp#quick-install) |
| [`speech-mcp`](https://github.com/sandraschi/speech-mcp) | Spoken status notifications | Optional | [Install Guide](https://github.com/sandraschi/speech-mcp#quick-install) |

> **Self-Contained Companions**: Fleet companions operate independently. Installing `email-mcp` does not require additional background services.
```

### 3.2 In `INSTALL.md`
Provide a **Combined Configuration Snippet** under an `## Optional Companions` heading so users who choose to install both can configure their MCP client in a single edit:

```markdown
## Optional Companions (Fleet Crossconnects)

If you are using `xyz` with `email-mcp`, configure both in your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "xyz": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\xyz", "run", "xyz"]
    },
    "email-mcp": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\email-mcp", "run", "email-mcp"]
    }
  }
}
```
```

### 3.3 Webapp Dashboard (`/apps` & Header Bar)
Repos shipping a companion webapp:
- Must query the companion server's registered port (`GET http://127.0.0.1:{port}/health`).
- Render a status badge:
  - **Connected (Green)**: Companion active and responding.
  - **Available / Not Running (Gray)**: Shows tooltip with GitHub link and launch hint.

---

## 4. Machine-Readable Manifest (`fleet-registry.json`)

Crossconnects are indexed centrally in `mcp-central-docs/operations/fleet-registry.json` within each server's entry:

```json
{
  "id": "xyz",
  "name": "XYZ Automation",
  "port": 10950,
  "repo_path": "D:/Dev/repos/xyz",
  "category": "Automation",
  "crossconnects": [
    {
      "id": "email-mcp",
      "kind": "optional",
      "features": [
        "email-digest",
        "incident-alerting"
      ],
      "port": 10842,
      "repo_url": "https://github.com/sandraschi/email-mcp"
    }
  ]
}
```

### Manifest Schema Fields
- `id` (string, required): The fleet repository identifier (matches peer `id` in `fleet-registry.json`).
- `kind` (string, required): Allowed values: `"optional"` (default), `"recommended"`. Values like `"mandatory"` are prohibited across the fleet to preserve standalone hermeticity.
- `features` (list of strings): User-visible features unlocked by the companion.
- `port` (integer, optional): Default registered backend port from `WEBAPP_PORTS.md`.
- `repo_url` (string, required): Canonical GitHub URL.

---

## 5. Automated Verification Tooling

The fleet maintenance tool `scripts/check-fleet-crossconnects.py` runs during CI and `just assess-and-fix`:
1. **Target Verification**: Confirms all crossconnected `id`s exist in `fleet-registry.json`.
2. **Cycle & Depth Detection**: Validates that no mandatory dependency chains exist and no unresolvable circular ties are present.
3. **Link Integrity**: Verifies that GitHub links resolve to valid repos.

---

## 6. The Long-Running Task Completion Readout Pattern (`speech-mcp`)

Any repository that executes long-running batch, training, or asynchronous processing jobs (e.g. corpus indexing, 3D world generation, video rendering, deep research sweeps, disk image backups) SHOULD implement the **Spoken Completion Readout** pattern:

### 6.1 Behavior
When a long-running job finishes, the server formats an announcement:
```
"Task <task_name> completed. Runtime: <n> minutes."
```
Example: `"Task arxiv paper corpus indexing completed. Runtime: 14 minutes."`

### 6.2 Soft Dispatch Contract
1. Check if `speech-mcp` is reachable at `http://127.0.0.1:10908` (or via the registered MCP client).
2. If available, call `spoken_status_readout(message=...)` or post to `/api/v1/tts`.
3. If `speech-mcp` is offline or not installed, gracefully fall back to local logging without error.

This provides hands-free awareness across the workspace without introducing hard coupling.
