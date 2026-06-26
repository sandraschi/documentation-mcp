# Moltbot — Tools and Skills

**Last updated:** 2025-01-28  
**See also:** [moltbot-00-overview](moltbot-00-overview.md) | [Tools](https://docs.molt.bot/tools) | [Skills](https://docs.molt.bot/tools/skills) | [Skills config](https://docs.molt.bot/tools/skills-config)

---

## 1. Tools Overview

The Pi agent exposes **tools** to the LLM. The Gateway wires them into the agent loop; schema is JSON (TypeBox). Key categories:

| Category | Examples |
|----------|----------|
| **Exec** | `bash`, `process` — shell and subprocess execution. |
| **Browser** | CDP-based browser control; snapshots, actions, uploads, profiles. |
| **Canvas** | A2UI push/reset, eval, snapshot. |
| **Nodes** | `camera.snap`, `screen.record`, `location.get`, etc., via `node.invoke`. |
| **Sessions** | `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn` — agent-to-agent. |
| **Cron / automation** | Cron jobs, webhooks, Gmail Pub/Sub. |
| **Slash commands** | User-facing commands (`/status`, `/new`, `/think`, etc.). |
| **Skills** | Skills add tool-usage instructions and optional tools via `SKILL.md`. |

Sandbox mode (e.g. `agents.defaults.sandbox.mode: "non-main"`) restrict which tools are available to non-main sessions (e.g. groups). Default sandbox allowlist: `bash`, `process`, `read`, `write`, `edit`, `sessions_*`; denylist includes `browser`, `canvas`, `nodes`, `cron`, `discord`, `gateway`.

---

## 2. Exec and Elevated

- **Exec:** Runs shell commands. On the host for main session; in Docker for sandboxed sessions when enabled.
- **Elevated:** Per-session toggle (`/elevated on|off`) when allowed. Gateway persists it via `sessions.patch`. Use for privileged host actions; keep allowlists tight.

---

## 3. Browser

- **Browser tool:** Dedicated Moltbot Chrome/Chromium, CDP control. Config: `browser.enabled`, `browser.color`, etc.
- **Browser login:** Assist credential flow for authenticated sites.
- **Chrome extension:** Optional extension for specific workflows.
- **Linux:** See [Browser Linux troubleshooting](https://docs.molt.bot/tools/browser-linux-troubleshooting).

---

## 4. Canvas and A2UI

- **Canvas:** Agent-driven visual workspace. Commands: push, reset, eval, snapshot. Served by the Canvas host (default `18793`).
- **A2UI:** Markup/ui system for Canvas. Bundle hash in `src/canvas-host/a2ui/.bundle.hash`; regenerate via `pnpm canvas:a2ui:bundle` when needed.

---

## 5. Session Tools (Agent-to-Agent)

- **sessions_list** — Discover active sessions (agents) and metadata.
- **sessions_history** — Fetch transcript logs for a session.
- **sessions_send** — Message another session; optional reply-back and announce behavior.
- **sessions_spawn** — Create/spawn sessions.

Use these to coordinate work across sessions without switching chat surfaces. See [Session tool](https://docs.molt.bot/concepts/session-tool).

---

## 6. Cron, Webhooks, Gmail Pub/Sub

- **Cron:** Schedule recurring jobs. [Cron jobs](https://docs.molt.bot/automation/cron-jobs).
- **Webhooks:** External triggers. [Webhook](https://docs.molt.bot/automation/webhook).
- **Gmail Pub/Sub:** Email-triggered automation. [Gmail Pub/Sub](https://docs.molt.bot/automation/gmail-pubsub).

---

## 7. Skills (Overview)

**Skills** are **AgentSkills-compatible** folders. Each skill has a `SKILL.md` with YAML frontmatter and instructions. Moltbot loads **bundled**, **managed** (`~/.clawdbot/skills`), and **workspace** (`<workspace>/skills`) skills, and filters them at load time via metadata (bins, env, config, OS).

---

## 8. Skill Locations and Precedence

1. **Bundled** — Shipped with install (npm or app).
2. **Managed** — `~/.clawdbot/skills`.
3. **Workspace** — `<workspace>/skills`.

**Precedence:** Workspace > managed > bundled. Extra dirs via `skills.load.extraDirs` (lowest).

---

## 9. Skill Format (SKILL.md)

Minimum frontmatter:

```yaml
---
name: my-skill
description: Short description.
---
```

Optional: `homepage`, `user-invocable`, `disable-model-invocation`, `command-dispatch`, `command-tool`, `command-arg-mode`. **metadata** (single-line JSON): `metadata.moltbot` for gating and install.

---

## 10. Gating (Load-Time Filters)

Under `metadata.moltbot`:

- **requires.bins** — Each must exist on `PATH`.
- **requires.anyBins** — At least one must exist.
- **requires.env** — Env var must exist or be provided in config.
- **requires.config** — List of `moltbot.json` paths that must be truthy.
- **os** — `darwin`, `linux`, `win32` allowlist.
- **always: true** — Skip other gates.
- **primaryEnv** — Env var for `skills.entries.<name>.apiKey`.
- **install** — Installer specs (brew, node, go, download) for macOS Skills UI.

Sandboxed agents: `requires.bins` checked on host at load; the binary must also exist **in** the sandbox container (e.g. via `agents.defaults.sandbox.docker.setupCommand`).

---

## 11. Config Overrides (~/.clawdbot/moltbot.json)

```json
{
  "skills": {
    "entries": {
      "my-skill": {
        "enabled": true,
        "apiKey": "GEMINI_KEY_HERE",
        "env": { "GEMINI_API_KEY": "GEMINI_KEY_HERE" },
        "config": { "endpoint": "https://…", "model": "…" }
      }
    },
    "load": { "watch": true, "watchDebounceMs": 250, "extraDirs": ["/path/to/skills"] }
  }
}
```

- **enabled: false** — Disable even if bundled/installed.
- **env** — Injected only if not already set.
- **apiKey** — Convenience when `primaryEnv` is set.
- **config** — Custom per-skill fields.
- **allowBundled** — If set, only listed bundled skills are eligible (managed/workspace unchanged).

---

## 12. ClawdHub

- **Registry:** [clawdhub.com](https://clawdhub.com). Discover, install, update, back up skills.
- **Install:** `clawdhub install <skill-slug>` (into `./skills` or workspace).
- **Update:** `clawdhub update --all`.
- **Sync:** `clawdhub sync --all`.

---

## 13. Plugins and Skills

Plugins can ship skills via `moltbot.plugin.json` (`skills` dirs). Plugin skills load when the plugin is enabled and follow normal precedence. Gate via `metadata.moltbot.requires.config` on the plugin config.

---

## 14. Security Notes

- Treat third-party skills as **trusted code**; review before enabling.
- Prefer sandboxed runs for untrusted inputs and risky tools.
- `skills.entries.*.env` and `apiKey` inject into the **host** process for that agent run, not the sandbox. Keep secrets out of prompts and logs.

---

## 15. Token Impact

Eligible skills are injected as a compact XML list into the system prompt. Base overhead ~195 chars; per-skill ~97 chars plus escaped `name`, `description`, `location`. See [Skills](https://docs.molt.bot/tools/skills) for the formula.

---

## 16. Session Snapshot and Watcher

- Skills are snapshotted **when a session starts** and reused for subsequent turns. Changes apply on **new** sessions.
- **Skills watcher:** `skills.load.watch: true` (and `watchDebounceMs`) to refresh when `SKILL.md` files change; next agent turn picks up changes.

---

## References

- [Tools](https://docs.molt.bot/tools)
- [Skills](https://docs.molt.bot/tools/skills)
- [Skills config](https://docs.molt.bot/tools/skills-config)
- [ClawdHub](https://docs.molt.bot/tools/clawdhub)
- [Session tool](https://docs.molt.bot/concepts/session-tool)
- [Sandboxing](https://docs.molt.bot/gateway/sandboxing)
