---
title: "Agent Action Gates: Destructive Tools Need a Gate the Model Cannot Open"
category: standards
status: active
audience: mcp-dev, all-agents
last_updated: 2026-10-02
---

# Agent Action Gates

## Why (the 2026-10 finding)

Anthropic's research note "GLM-5.3 and the spread of advanced cyber capabilities"
(https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities)
reports that a frontier-class open-weight model (Zhipu GLM-5.3) can be "abliterated"
(refusal behaviour removed by editing weights) 100% of the time, cheaply, and runs on
expensive consumer hardware. Its reasoning trace in a hospital-style test environment shows
the failure shape: the model notices the safety warnings, hesitates, then resolves the
conflict by deferring to an operator instruction ("I want funerals, not headlines").

Consequence for this fleet: **model-side refusal is no longer a safety layer we can count
on.** Any agent, including a local abliterated one, may end up driving our MCP servers.
Safety has to live at the actuator (the tool), outside the model's control.

## Rule

Every tool that can destroy data, execute code, send messages, or move something physical
MUST be gated by a mechanism **the calling model cannot satisfy by itself**.

### Gates that count

| Gate | How it works | Use for |
|---|---|---|
| Operator env flag | Class is OFF unless `<REPO>_ALLOW_<CLASS>=1` is set in the server's `.env`. Tool returns a clear "disabled, set X" message. Agent cannot set it. | Physical actuators, flashing, exec, mass delete. Reference: jtag-swd-mcp `OPENOCD_ALLOW_FLASH` |
| MCP elicitation | Server asks the human via the client (`ctx.elicit`) and shows exactly what is about to happen. | Single destructive actions: delete VM/snapshot, send email, kill process |
| Client permission prompt | Host asks the human per call. | Useful, but NOT sufficient alone: auto mode and allowlists bypass it |
| Out-of-band check | Independent system verifies (second sensor, human sign-off, readback). | Clinical-style writes, power/thermal safety |

If elicitation is unsupported by the client, the server MUST fall back to **refusing**, never
to allowing.

### Gates that do NOT count

- `confirm=true`, `ack=true`, `force=true`, `dry_run=false` parameters. The calling model
  sets these itself. They are fine as ergonomics and typo-guards, worthless as safety.
- A docstring saying "be careful".
- Anything that only exists in the client (allowlists make it vanish).

### Always

- Annotate tools honestly: `readOnlyHint`, `destructiveHint`, `idempotentHint`.
- Reads stay frictionless; only mutations are gated.
- Fail closed: gate unreadable, client unsupported, flag missing -> refuse.
- Log every gated call (who/what/when/outcome).

## Client elicitation support (2026-10-02, from docs/issues, NOT yet probed live)

| Client | Elicitation | Basis |
|---|---|---|
| Claude Code (and the Desktop app's Code tab) | Yes | Docs have "Respond to MCP elicitation requests"; fixed in v2.1.76 (anthropics/claude-code#2799) |
| Claude Desktop chat | Unconfirmed, one user report says no | Separate client from Claude Code |
| Cursor | Yes | Docs protocol table lists Elicitation as Supported |
| VS Code | Unconfirmed | MCP docs page does not mention it |
| OpenCode 1.18.32 | Unreliable | Open bug anomalyco/opencode#51856: advertises elicitation but never answers, tool call hangs to the 30 s timeout (reported against a remote server); partial ACP/forms work merged 2026-10-01 |
| Antigravity | Unknown | MCP docs mention only tools/resources |

Consequence: the operator env flag is the primary gate everywhere; elicitation is an optional
second layer with a short server-side timeout where timeout means refuse. Never block on it.

### Verify per client: `scripts/elicit_probe.py`

Single-file stdio server (`uv run` installs fastmcp itself). Register it in a client, then call:

- `probe_capabilities`: what the client claims (a claim is not proof)
- `probe_elicit`: asks you to click Accept; reports SUPPORTED / UNHANDLED (hang) / AUTO-CANCEL / UNSUPPORTED with elapsed time
- `probe_gated_action`: reference fail-closed pattern (`human_confirmed()` returns True only on explicit accept)

```
claude mcp add elicit-probe -- uv run D:\Dev\repos\mcp-central-docs\scripts\elicit_probe.py
```
OpenCode (`opencode.json`): `"mcp": {"elicit-probe": {"type": "local", "command": ["uv", "run", "D:\\Dev\\repos\\mcp-central-docs\\scripts\\elicit_probe.py"]}}`.
Antigravity: add the same command to its MCP config. Record the verdicts in the table above.

## Triage list (2026-10-02, regex heuristic, fleet-wide)

Method: scan of every repo under `D:\Dev\repos` (excluding `_upstream`, `_junk`, vendored
FreeCAD, venvs, node_modules, tests) for `destructiveHint`, delete/exec primitives, and
`operation` enums containing dangerous verbs. Heuristic only: it misses destructive paths
behind generic names and counts any file mentioning `force`/`confirm` as gated, so true
exposure is higher. Only 30 repos declare `destructiveHint=true`; 159 run subprocesses in
non-test code; ~69 files in ~37 repos define dangerous operations with no gate keyword.

Tier 1, physical actuators (do first): `raspberrypi-mcp` (GPIO write/PWM),
`robotics-mcp`, `devices-mcp`, `universal-actuator-mcp`.
Tier 2, whole-machine control: `windows-operations-mcp` (PowerShell/cmd exec, registry,
process kill, services, accounts, event-log clear), `autohotkey-mcp`, `pinokio-mcp`,
`opencode-cli-mcp`, `cursor-mcp`, `fleet-agent-mcp`, `pywinauto-mcp`, `uitars-mcp`.
Tier 3, irreversible data loss / outbound messages: `podman-mcp`, `virtualization-mcp`,
`opencode-cli-mcp` backups, `jellyfin-mcp`, `plex-mcp`, `arr-mcp`, `ms-graph-mcp`,
`email-mcp`.

## Rollout status

| Repo | Status |
|---|---|
| power-supply-mcp | `psu_safety` interlock added (software; latched trip, fail-safe heartbeat). Its `reset(ack=true)` is model-satisfiable: TODO move to operator flag/elicitation |
| raspberrypi-mcp | DONE (b651ff7): operator `RASPBERRYPI_MCP_ALLOW_*` flags gate GPIO write/pwm, I2C write, SPI, Pico flash/repl_exec on the real backend; simulator and reads ungated; 4 refusal-path tests. Pattern to copy |
| everything else in the triage list | not started |

## Rules of engagement for the rollout

One repo at a time, max 10 files per commit, `.bak` per file first (see Batch Mutation
Safety), tests that prove the refusal path (flag off -> refused, flag on -> allowed).

## See also

- [SAFETY_PROTOCOLS.md](./SAFETY_PROTOCOLS.md): atomic writes and dual backups (data integrity, a different problem)
- [GIT_REPOSITORY_SAFETY.md](./GIT_REPOSITORY_SAFETY.md)
- [TOOL_DESIGN_STANDARDS.md](./TOOL_DESIGN_STANDARDS.md)
