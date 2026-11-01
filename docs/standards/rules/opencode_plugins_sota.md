---
title: "OpenCode Plugins — Fleet Standard & Writeup (SOTA 2026)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-10-28
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# OpenCode Plugins — Fleet Standard & Writeup (SOTA 2026)

**Established**: 2026-08-02
**Reference impl**: global plugins in `~/.config/opencode/plugins/` (`powershell-guard.ts`, `port-guard.ts`, `just-wrapper.ts`, `batch-mutation-guard.ts`), `opencode-cli-mcp` (`web_sota` Plugins page, `api/routes/opencode_config.py`). **Versioned source of truth**: [`standards/opencode-plugins/`](../opencode-plugins/README.md) in this repo — the live directory above is not git-tracked; see that README for the sync process.
**Official docs**: https://opencode.ai/docs/plugins/ | https://opencode.ai/docs/ecosystem/
**Cross-refs**: [powershell-script-standards.md](./powershell-script-standards.md), [session_context_injection.md](./session_context_injection.md), [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md)

---

## 1. What an opencode plugin is

A plugin is a **JavaScript/TypeScript module** that exports one or more plugin
functions. Each function receives a context object and returns a hooks object.
Hooks fire on opencode events (tool calls, session lifecycle, file edits,
permissions, shell env) and can **modify the behavior before/after the fact,
throw to block an action, or register brand-new custom tools**.

Plugins are loaded from four sources, in order (later sources add, not
override):

1. Global config (`~/.config/opencode/opencode.json` — `plugin` array)
2. Project config (`opencode.json` — `plugin` array)
3. Global plugin directory (`~/.config/opencode/plugins/` — auto-discovered)
4. Project plugin directory (`.opencode/plugins/` — auto-discovered)

Two ways to distribute:

| Source | How | Notes |
|---|---|---|
| **Local files** | Drop `.ts`/`.js` into a plugins dir | Auto-loaded at startup; external npm deps need a `package.json` in the config dir |
| **npm packages** | `"plugin": ["opencode-foo", "@scope/bar"]` in config | Auto-installed via Bun into `~/.cache/opencode/node_modules/`; duplicates loaded once |

The fleet uses **local global plugins** (user-machine specific, paths
hardcoded) and ships **project plugins + custom tools** via `opencode-cli-mcp`.

---

## 2. The fleet's own plugins (reference implementations)

Three global plugins live at `~/.config/opencode/plugins/` and are loaded for
every opencode session on this machine. Together they encode fleet SOTA rules
into the agent runtime — the agent cannot break them silently because the
plugin **throws before the command executes**.

### 2.1 `powershell-guard.ts` — PowerShell SOTA enforcement

Hooks `tool.execute.before` for the `bash` tool, scans the command for fleet
banned patterns, and **throws with the canonical fix** when found.

```ts
import { type Plugin } from "@opencode-ai/plugin"

const RG = "C:\\Users\\sandr\\AppData\\Local\\Microsoft\\WinGet\\Links\\rg.exe"

const RULES: [RegExp, string][] = [
  [/\&\&/, '&&  use ";" or "if ($?) { ... }"'],
  [/\|\|/, '||  use "if (-not $?) { ... }"'],
  [/(?:^|[\s;|&])grep\s+/, `grep  Select-String -Pattern "<regex>" or ${RG}`],
  [/(?:^|[\s;|&])tail\s+/, "tail  Get-Content <path> -Tail <n>"],
  [/(?:^|[\s;|&])cat\s+/, "cat  Get-Content"],
  [/(?:^|[\s;|&])ls\s+/, "ls  Get-ChildItem"],
  [/(?:^|[\s;|&])rm\s+-[rf]+/, "rm -rf  Remove-Item -Recurse -Force"],
]

export const PowerShellGuard: Plugin = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool !== "bash") return
      const cmd = output.args.command as string
      if (!cmd) return
      const hits: string[] = []
      for (const [pattern, suggestion] of RULES) {
        if (pattern.test(cmd)) hits.push(suggestion)
      }
      if (hits.length > 0) {
        throw new Error(
          `PowerShell SOTA violation(s) in bash call:\n\n` +
            `  Command: ${cmd.split("\n")[0]}\n\n` +
            `  Fix:\n    ${hits.join("\n    ")}`
        )
      }
    },
  }
}
```

Mechanics worth copying:

- **Target selection**: `if (input.tool !== "bash") return` — cheap early exit,
  the hook stays inert for every other tool.
- **Throw to block**: a thrown `Error` in `tool.execute.before` aborts the tool
  call; the agent sees the message and must comply.
- **Suggestion-first**: the error carries the exact replacement (`Select-String
  -Pattern`, `Get-Content -Tail`, etc.) — the agent can self-correct without
  another round trip.
- **Pattern table**: `[RegExp, string][]` keeps the rule set declarative and
  easy to extend (add a rule = add one row).

Known limitation: regexes match literal command text, so a command like
`git rm` false-positives on the `rm -rf` rule (accepted fleet-wide — better
safe; use `git reset --soft` per the PowerShell standard).

### 2.2 `port-guard.ts` — forbidden ports enforcement

Hooks the same event and blocks the fleet-forbidden ports in any command:

```ts
const FORBIDDEN = new Set([3000, 5000, 5173, 5174, 5175, 8000, 8080])
const PORT_PATTERNS: RegExp[] = [
  /--port[=\s]+(\d+)/gi,
  /-p\s+(\d+)/gi,
  /\$env:(\w*PORT\w*)\s*=\s*['"]?(\d+)['"]?/gi,
  /:\/\/(?:localhost|127\.0\.0\.1|0\.0\.0\.0):(\d+)/gi,
]

export const PortGuard: Plugin = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool !== "bash") return
      const cmd = output.args.command as string
      for (const pattern of PORT_PATTERNS) {
        for (const m of cmd.matchAll(pattern)) {
          const port = parseInt(m[m.length - 1], 10)
          if (FORBIDDEN.has(port)) {
            throw new Error(
              `Forbidden port ${port} in bash call:\n\n` +
                `  Command: ${cmd.split("\n")[0]}\n\n` +
                `Ports 3000, 5000, 5173, 8000, 8080 are prohibited.\n` +
                `Use a fleet port from 10700-11000. Check WEBAPP_PORTS.md\n` +
                `for your project's allocated ports.`
            )
          }
        }
      }
    },
  }
}
```

Covers the four spellings agents actually use: `--port N`, `-p N`,
`$env:PORT='N'`, and `://host:port` URLs. The `FORBIDDEN` set mirrors
[WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) — keep both in sync when
the port rules change.

### 2.3 `just-wrapper.ts` — custom tool registration

Plugins can register **new tools** via the `tool()` helper — this one gives
every opencode agent a schema'd `just` runner:

```ts
import { type Plugin, tool } from "@opencode-ai/plugin"

const JUST = "C:/Users/<user>/scoop/shims/just.exe"

export const JustWrapper: Plugin = async ({ $ }) => {
  return {
    tool: {
      just: tool({
        description: "Run just recipes from the fleet justfile. Use 'list' to discover available recipes, 'run' to execute one. Runs in the current git worktree root.",
        args: {
          operation: tool.schema.enum(["list", "run"]).describe("'list' shows available recipes, 'run' executes a recipe"),
          recipe: tool.schema.string().optional().describe("Recipe name (required for 'run' operation)"),
          extra_args: tool.schema.string().optional().describe("Additional key=value arguments for the recipe"),
        },
        async execute(args, context) {
          const cwd = context.worktree || context.directory
          if (args.operation === "list") {
            const result = await $`${JUST} --list`.cwd(cwd).nothrow().quiet()
            return result.text() || "(no recipes found or no justfile in this directory)"
          }
          if (!args.recipe) return "Error: recipe name is required for 'run' operation"
          const extra = args.extra_args ? args.extra_args.split(/\s+/).filter(Boolean) : []
          const result = await $`${JUST} ${args.recipe} ${extra}`.cwd(cwd).nothrow()
          let output = result.text() || "(no output)"
          if (result.stderr && result.stderr.length > 0) {
            const stderrText = new TextDecoder().decode(result.stderr)
            if (stderrText.trim()) output += `\n[stderr]\n${stderrText.trim()}`
          }
          if (result.exitCode !== 0) output += `\n[exit code: ${result.exitCode}]`
          return output
        },
      }),
    },
  }
}
```

Pattern points:

- `tool.schema.enum([...])` / `.string()` / `.optional()` — Zod schemas give
  the agent argument validation + discoverability (the schema renders in the
  tool list).
- `$` (Bun shell) with `.cwd(cwd).nothrow().quiet()` — never throws, always
  returns output + stderr + exit code for the agent to reason about.
- `context.worktree || context.directory` — respect worktrees (fleet runs in
  async worktrees regularly).

---

## 3. Plugin anatomy (the pieces)

### 3.1 The plugin function

```ts
import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  return { /* hooks */ }
}
```

Context fields:

| Field | Meaning |
|---|---|
| `project` | Current project info |
| `directory` | CWD |
| `worktree` | Git worktree path (fall back to `directory`) |
| `client` | opencode SDK client (calls `client.app.log(...)` for structured logging) |
| `$` | Bun shell API for executing commands |

### 3.2 Hooks / events (condensed reference)

| Event | Fires | Typical use |
|---|---|---|
| `tool.execute.before` | before any tool runs | block/modify commands (guards) |
| `tool.execute.after` | after a tool runs | cost tracking, post-processing |
| `session.created` / `session.idle` / `session.updated` / `session.deleted` | session lifecycle | notifications, persistence, cost log |
| `session.compacted` / `experimental.session.compacting` | compaction | inject/override continuation context |
| `file.edited` / `file.watcher.updated` | file changes | formatting hooks |
| `permission.asked` / `permission.replied` | permission prompts | auto-approve policies |
| `shell.env` | shell spawn | inject env vars |
| `command.executed` | slash commands | command extensions |
| `message.*` | message parts | transcript transforms |
| `lsp.*` | LSP diagnostics | type-aware tooling |
| `todo.updated` | todo state | progress tracking |
| `tui.*` | TUI events | UI integration |

### 3.3 Custom tools

`tool()` creates tools that appear alongside built-ins; **a plugin tool with
the same name as a built-in wins**. This is the same mechanism behind the
`.opencode/tools/*.ts` custom tools opencode-cli-mcp ships (fleet, sessions,
runs, system, providers, tools) and the `.opencode/skills/session-context/`
skill — see [session_context_injection.md](./session_context_injection.md).

---

## 4. Managing fleet plugins

- **Global plugins**: files in `~/.config/opencode/plugins/` (auto-discovered,
  no config entry needed — the config `plugin` array is only for explicit
  entries like `file://` paths or npm packages). That directory is **not**
  a git repo — [`standards/opencode-plugins/`](../opencode-plugins/README.md)
  in this repo is the versioned source of truth; copy changes both ways per
  that README's sync process.
- **Webapp surface**: opencode-cli-mcp's Plugins page (`/plugins`) lists
  explicit config entries + auto-discovered directory plugins, and can add/
  remove entries via `POST/DELETE /api/occonfig/plugin` (with timestamped
  `.bak` backup before every config write).
- **Reload**: plugins load at opencode startup; restart opencode (or the TUI
  session) after editing.

---

## 5. Writing a new fleet plugin — checklist

1. **Type it**: `import type { Plugin } from "@opencode-ai/plugin"`; run
   `bunx tsc --noEmit` on the file (or `bun build` to sanity-check).
2. **Follow the fleet PS rules in the plugin itself**: no em dashes, no
   `&&`/`||`, ASCII only — the plugin is a `.ts` file, same rules as scripts.
3. **Early-exit on non-target tools** (`if (input.tool !== "bash") return`).
4. **Throw with the fix** — never silently pass; the agent needs the
   correction in the error text.
5. **Declarative tables** for rule sets (`[RegExp, string][]`, `Set<number>`).
6. **Hardcoded personal paths are OK for global user plugins** (documented
   exception); publishable plugins must resolve via `which`/env instead.
7. **Test live**: restart opencode, trigger the hook with a violating command,
   confirm the block + message.
8. Add a row to this doc's plugin inventory below.

### Fleet plugin inventory

| Plugin | Location | Hook | Enforces |
|---|---|---|---|
| `powershell-guard.ts` | global | `tool.execute.before` (bash) | PowerShell SOTA bans |
| `port-guard.ts` | global | `tool.execute.before` (bash) | forbidden ports |
| `just-wrapper.ts` | global | `tool:` custom tool | schema'd `just` runner |
| `batch-mutation-guard.ts` | global | `tool.execute.before` (bash) | Batch Size Limit (max 10 files/commit) + Batch Mutation Safety (`.bak` before multi-file writes) — added after [BUG-029](../../troubleshooting/BUGS_DEPOT.md) (155-repo fleet sweep, zero backups, no file-count check) |
| `.opencode/tools/*.ts` (6) | opencode-cli-mcp project | `tool:` custom tools | fleet/session/run diagnostics |
| `.opencode/skills/session-context/` | opencode-cli-mcp project | skill | session context injection |

---

## 6. Distribution (local vs npm)

- **Local**: `~/.config/opencode/plugins/` — fleet default; machine-specific,
  paths hardcoded, zero publishing overhead.
- **npm** (`"plugin": ["opencode-x"]`): the shareable format; publish from a
  repo with `package.json` (name `opencode-*`, deps `@opencode-ai/plugin`),
  auto-installed via Bun on startup. Candidate fleet publishes: the two guard
  plugins (generic enough for any Windows + fleet-standards user).
- **Community ecosystem**: https://opencode.ai/docs/ecosystem/ + awesome-opencode
  + opencode.cafe — review of downloadable/template plugins is **deferred**
  (tracked separately); this doc covers only the fleet's own implementations.

## 7. Fleet rollout candidates (proposals, not yet built)

| Plugin | Hook | Purpose |
|---|---|---|
| `cost-tracker.ts` | `session.idle` | Log restated cost/tokens per session (depot's stored `cost` column overcounts cache reads — see opencode-cli-mcp depot restate logic) |
| `compaction-context.ts` | `experimental.session.compacting` | Inject fleet context (port registry, repo map, active task state) into continuation prompts |
| `em-dash-guard.ts` | `tool.execute.before` (read/write) | Block em dashes in fleet `.ps1`/`.bat`/`justfile` edits, same pattern as powershell-guard (see section 8 for why chat output itself is out of scope) |

---

## 8. Response-text guard ("stop my em dashes"): investigated 2026-10-28, not buildable

**Question**: can a plugin scan the finished assistant response and force a
rewrite when it contains banned characters? That would be the deterministic
tier-1 fix for chat output, and it was explicitly requested after months of
the instruction-based approach failing.

**Answer**: no, on the installed API surface. Verified against the shipped
type definitions (`@opencode-ai/plugin` 1.14.25 and `@opencode-ai/sdk`
1.14.25 under `~/.config/opencode/node_modules`), not against memory or
docs, which lag the implementation:

- The `event` hook receives `{ event: Event }` and returns `Promise<void>`:
  observation only. The v2 event inventory was enumerated in full
  (`EventMessagePartDelta`, `EventSessionIdle`, `EventSessionStatus`,
  `EventSessionError`, plus lifecycle/file/LSP/TUI/workspace events) and
  contains no blocking or rewriting variant. Deltas fire during streaming,
  idle fires after delivery - by the time a plugin could react, the text
  the user objects to is already on screen.
- The only mutable-looking surface is `experimental.text.complete`
  (input `{sessionID, messageID, partID}`, output `{text}`). It is marked
  experimental, its write-back semantics are undocumented, and a wrong
  guess about them produces the worst possible outcome: a silent no-op
  placebo that looks enforced. Not shipped for exactly that reason.
- What *would* change the verdict: a supported response-phase hook with
  documented rewrite semantics, or provider-level token bans surfaced
  through the plugin API. Neither exists in 1.14.25; re-check on every
  plugin/SDK upgrade before assuming otherwise.

**Consequence**: enforcement stays at the boundaries that support it.
`tool.execute.before` on file writes (the section 7 em-dash-guard proposal
for `.ps1`/`.bat`/`justfile` edits) and the pre-commit ascii-fix hook
(commit boundary, added 2026-10-28: auto-replaces em/en dashes, smart
quotes, ellipsis and nbsp in PowerShell files, fail-hook stays as backstop
for anything unmapped). Chat output itself has no deterministic gate in
this harness version; flagging in chat remains the only correction path.

Do not build a placebo plugin. An unenforced guard is worse than none,
because it teaches everyone to stop checking - which is precisely how the
months-long debate survived every previous "fix".
