# Spec Kit — GitHub's Spec-Driven Development Toolkit

**Provenance:** GitHub (`github/spec-kit`)
**License:** MIT
**Homepage:** https://github.com/github/spec-kit
**Docs:** https://github.github.io/spec-kit/
**Version:** Check [Releases](https://github.com/github/spec-kit/releases/latest)
**Added to fleet:** 2026-07-03

---

## What It Is

Spec Kit is GitHub's open-source toolkit for **Spec-Driven Development (SDD)** — a
methodology where specifications are not scaffolding you discard but **executable
artifacts** that directly generate working implementations.

It consists of two parts:

1. **`specify` CLI** — Python CLI tool (installed via `uv tool install`) that scaffolds
   a project with templates, shell scripts, and agent slash commands.

2. **`/speckit.*` slash commands** — A set of structured prompts loaded into your
   AI coding agent that guide development through constitution → spec → clarify →
   plan → tasks → implement phases.

The core insight: instead of one-shot "vibe coding" prompts, SDD front-loads the
*what* and *why* before the *how*, with each phase producing a validated artifact
that the next phase consumes. Mistakes caught at the spec level cost zero code;
mistakes caught at the implementation level cost a rewrite.

---

## Provenance

| Attribute | Detail |
|-----------|--------|
| **Org** | GitHub (Microsoft) |
| **Maintainers** | GitHub Next / open-source team |
| **Lead** | Heavily influenced by [John Lam](https://github.com/jflam)'s research |
| **License** | MIT |
| **Language** | Python 3.11+ |
| **Package manager** | `uv` (Astral) |
| **Install method** | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z` |
| **Stars** | ~16K+ (July 2026, growing fast) |
| **Integrations** | 30+ AI coding agents including **opencode**, Claude Code, Cursor, Copilot, Gemini CLI, Codex, Windsurf, Qwen Code, Goose, Mistral Vibe, Kiro, Tabnine, ZCode, and more |

---

## The SDD Workflow (7 Phases)

```
/speckit.constitution → /speckit.specify → /speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.implement
                                                                                      ↓
                                                                          /speckit.taskstoissues (GitHub issues)
```

### Phase 1: Constitution (`/speckit.constitution`)
Establish project governing principles — coding standards, test requirements,
performance goals, UX consistency. These become the "constitution" that the agent
references during all subsequent phases. Output: `.specify/memory/constitution.md`

```text
/speckit.constitution Create principles focused on code quality, testing
standards, user experience consistency, and performance requirements.
Include governance for how these principles should guide technical
decisions and implementation choices.
```

### Phase 2: Specify (`/speckit.specify`)
Describe **what** you want to build — user stories, functional requirements,
acceptance criteria. Do NOT mention tech stack. The agent produces a structured
spec. Output: `specs/{feature-number}-{name}/spec.md`, new git branch.

```text
/speckit.specify Build an application that can help me organize my photos
in separate photo albums. Albums are grouped by date and can be re-organized
by dragging and dropping on the main page. Albums are never in other nested
albums. Within each album, photos are previewed in a tile-like interface.
```

### Phase 3: Clarify (`/speckit.clarify`)
Structured Q&A to resolve underspecified areas **before** planning. Sequential,
coverage-based questioning that records answers in a Clarifications section.
Run this BEFORE `/speckit.plan` to reduce rework.

### Phase 4: Plan (`/speckit.plan`)
Declare tech stack and architecture. The agent produces implementation detail
documents including data model, API contracts, research notes, quickstart.
Output: `specs/{feature}/plan.md`, `data-model.md`, `contracts/`, `research.md`, `quickstart.md`

```text
/speckit.plan The application uses Vite with minimal number of libraries.
Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not
uploaded anywhere and metadata is stored in a local SQLite database.
```

### Phase 5: Analyze (`/speckit.analyze`)
Cross-artifact consistency & coverage analysis. Validates that the spec, plan,
and tasks are coherent before implementation begins.

### Phase 6: Tasks (`/speckit.tasks`)
Break the plan into actionable, dependency-ordered tasks with file paths.
Tasks are organized by user story with parallel execution markers `[P]`.
Output: `specs/{feature}/tasks.md`

### Phase 7: Implement (`/speckit.implement`)
Execute all tasks in dependency order. Validates prerequisites (constitution,
spec, plan, tasks exist), then iterates through the task list.

### Optional: Converge (`/speckit.converge`)
Post-implementation assessment: compares codebase against spec/plan/tasks and
appends any remaining work as new tasks. Use when implementation drifted.

### Optional: Taskstoissues (`/speckit.taskstoissues`)
Convert the generated `tasks.md` into actual GitHub issues for tracking.

---

## Installation & Setup

### Prerequisites
- Python 3.11+ (met by fleet — Python 3.13)
- `uv` (met by fleet)
- Git (met by fleet)
- A supported AI coding agent (opencode, Claude Code, Cursor, Copilot, etc.)

### Install the CLI

```powershell
# Replace vX.Y.Z with latest tag from https://github.com/github/spec-kit/releases
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z
```

### Initialize a project (with opencode)

```powershell
# New project
specify init my-project --integration opencode
cd my-project

# Existing project (current directory)
specify init . --integration opencode --force
```

This scaffolds:

```
my-project/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # Created by /speckit.constitution
│   ├── scripts/
│   │   └── bash/
│   │       ├── check-prerequisites.sh
│   │       ├── common.sh
│   │       ├── create-new-feature.sh
│   │       ├── setup-plan.sh
│   │       └── setup-tasks.sh
│   └── templates/
│       ├── plan-template.md
│       ├── spec-template.md
│       └── tasks-template.md
└── .opencode/
    └── commands/                     # Slash commands registered for opencode
        ├── speckit.constitution.md
        ├── speckit.specify.md
        ├── speckit.clarify.md
        ├── speckit.plan.md
        ├── speckit.tasks.md
        ├── speckit.implement.md
        ├── speckit.analyze.md
        ├── speckit.checklist.md
        ├── speckit.converge.md
        └── speckit.taskstoissues.md
```

After initialization, your agent has access to all `/speckit.*` slash commands.

### Check for updates

```powershell
specify self check           # Read-only: is a newer release available?
specify self upgrade         # Upgrade in-place
specify self upgrade --tag vX.Y.Z  # Pin a specific release
```

### List available integrations

```powershell
specify integration list
```

---

## Extensions, Presets & Bundles

Spec Kit has a composable customization system with clear priority resolution:

| Priority | Layer | What it does | Location |
|----------|-------|-------------|----------|
| 1 (highest) | **Project-Local Overrides** | One-off template adjustments | `.specify/templates/overrides/` |
| 2 | **Presets** | Customize existing workflow outputs | `.specify/presets/templates/` |
| 3 | **Extensions** | Add entirely new commands/workflows | `.specify/extensions/templates/` |
| 4 (base) | **Spec Kit Core** | Built-in SDD commands & templates | `.specify/templates/` |

### Extensions — Add New Capabilities

Use when you need functionality beyond the core SDD commands (e.g., Jira
integration, compliance checklists, security gates).

```powershell
specify extension search              # Browse available extensions
specify extension add <name>          # Install one
```

### Presets — Customize Existing Workflows

Use when you want to change *how* Spec Kit works — enforce a compliance format,
use domain-specific terminology, adapt to Agile/Kanban/Waterfall methodology,
localize to a different language, or enforce test-first task ordering.

```powershell
specify preset search                 # Browse available presets
specify preset add <name>             # Install one
```

Multiple presets stack with priority ordering.

### Bundles — Role-Based Setups

A bundle packages curated extensions + presets into a single versioned,
role-oriented setup (product manager, business analyst, security researcher,
developer).

```powershell
specify bundle search [<query>]       # Discover bundles
specify bundle info <bundle-id>       # Inspect what it will add
specify bundle install <bundle-id>    # Install in one command
specify bundle list                   # See what's installed
specify bundle remove <bundle-id>     # Non-destructive removal
```

---

## Full Example: Taskify (from the official walkthrough)

The official walkthrough builds a Kanban team productivity app called Taskify
with .NET Aspire + Blazor + Postgres. Here's the compressed version:

### 1. Initialize

```powershell
specify init taskify --integration copilot
cd taskify
```

### 2. Constitution

```text
/speckit.constitution Create principles focused on code quality, testing
standards, user experience consistency, and performance requirements.
```

### 3. Specify

```text
/speckit.specify Develop Taskify, a team productivity platform. It should
allow users to create projects, add team members, assign tasks, comment
and move tasks between boards in Kanban style. [... full requirements ...]
```

Creates branch `001-create-taskify` and `specs/001-create-taskify/spec.md`.

### 4. Clarify (optional but recommended)

```text
/speckit.clarify
```

Sequential Q&A to pin down underspecified areas.

### 5. Plan

```text
/speckit.plan We are going to generate this using .NET Aspire, using Postgres
as the database. The frontend should use Blazor server with drag-and-drop
task boards, real-time updates. [...]
```

Produces `plan.md`, `data-model.md`, `contracts/`, `research.md`, `quickstart.md`.

### 6. Validate plan

```text
Now I want you to go and audit the implementation plan and the
implementation detail files. Read through it with an eye on determining
whether or not there is a sequence of tasks that you need to be doing...
```

### 7. Tasks

```text
/speckit.tasks
```

Produces `tasks.md` with dependency-ordered tasks, parallel markers, and file paths.

### 8. Implement

```text
/speckit.implement
```

Executes all tasks in order. Tests, then build, then iterate on runtime errors.

### Directory after implementation

```
taskify/
├── .specify/
│   ├── memory/constitution.md
│   ├── scripts/bash/
│   └── templates/
├── specs/
│   └── 001-create-taskify/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── data-model.md
│       ├── research.md
│       ├── quickstart.md
│       └── contracts/
│           ├── api-spec.json
│           └── signalr-spec.md
├── src/
│   └── Taskify/
│       ├── Program.cs
│       ├── Components/
│       └── Data/
└── CLAUDE.md
```

---

## Relationship to Fleet Workflow (workflow_2026.md)

The fleet's `workflow_2026.md` already practices a 4-phase loop:

```
EXPLORE → PLAN → IMPLEMENT → COMMIT & VERIFY
```

Spec Kit maps onto this almost 1:1, but formalizes and **file-persists** each phase:

| Fleet Phase | Spec Kit Equivalent | What Spec Kit adds |
|-------------|-------------------|--------------------|
| EXPLORE | `/speckit.specify` + `/speckit.clarify` | Structured spec file, coverage questions, answers persisted |
| PLAN | `/speckit.plan` + `/speckit.analyze` | Data model, API contracts, research notes, cross-artifact validation |
| IMPLEMENT | `/speckit.tasks` + `/speckit.implement` | Dependency-ordered tasks with file paths, parallel markers |
| COMMIT & VERIFY | `/speckit.converge` | Post-impl gap analysis between codebase and spec |

### What the fleet already has that Spec Kit doesn't
- Playwright E2E testing (`playwright_e2e_sota.md`)
- CUA-NSIS smoke testing (`cua_nsis_smoke_testing.md`)
- Fleet port registry & webapp SLOP
- Tauri/NSIS build pipeline
- `SPEC.md` interview pattern (ad-hoc but flexible)

### What Spec Kit adds that the fleet doesn't have
- **Persistent artifact chain**: Constitution → Spec → Plan → Tasks all in `.md` files
  that survive context resets. Currently, fleet plans live in agent memory and vanish.
- **Cross-artifact validation**: `/speckit.analyze` checks that the plan covers
  every spec requirement and every task maps to a plan section.
- **Dependency-ordered tasks**: Manual task breakdown is error-prone; Spec Kit
  produces tasks with `[P]` parallel markers and file paths.
- **`/speckit.converge`**: Post-implementation gap analysis — catches drift between
  what was planned and what was built.
- **GitHub issue generation**: `/speckit.taskstoissues` converts tasks to tracked
  issues without manual copy-paste.

---

## When to Use It vs. Not

### Use Spec Kit when:
- **Greenfield projects** — new MCP server, new webapp, new fleet tool
- **Complex features** — multi-file, multi-endpoint, new database schema
- **Brownfield modernization** — replacing a legacy module with a new implementation
- **Team handoffs** — spec survives when the implementing agent is not the planning agent
- **Compliance contexts** — need a documented trace from requirements → implementation
- **IDE-hopping** — spec and plan are plain Markdown, travel across agents/IDEs

### Skip Spec Kit when:
- **Single-file fixes** — one-tool add, bug fix, config change
- **Exploratory spikes** — you don't yet know what you need
- **Trivial changes** — updating a dependency, adding a docstring
- **Rapid iteration on a hot reload** — Playwright-aided webapp improvement loop
- **Existing repo with established workflow** — don't retrofit just because

### Hybrid approach

For fleet repos, the recommended pattern is:

1. **Use Spec Kit for the initial scaffold** of a new MCP server or complex feature
2. **Use the fleet's existing PRD/SPEC.md pattern** for medium-complexity changes
3. **Use the Playwright loop** (`workflow_2026.md` Phase 5) for webapp UI iteration
4. **Use CUA-NSIS smoke test** for pre-release certification

The artifacts Spec Kit produces (constitution, spec, plan, tasks) are compatible
with fleet verification gates — you can still run `ruff`, `tsc --noEmit`, `pytest`,
and `just cua-nsis-test` after `/speckit.implement`.

---

## Supported Agents (30+ Integrations)

Spec Kit writes slash commands into the agent's config directory. For opencode:

```
.opencode/commands/
├── speckit.constitution.md
├── speckit.specify.md
├── speckit.clarify.md
├── speckit.plan.md
├── speckit.analyze.md
├── speckit.checklist.md
├── speckit.tasks.md
├── speckit.implement.md
├── speckit.converge.md
└── speckit.taskstoissues.md
```

Other supported integrations include: Claude Code, Cursor, GitHub Copilot,
Gemini CLI, Codex CLI, Windsurf, Qwen Code, Goose, Mistral Vibe, Kiro CLI,
Tabnine CLI, Qoder CLI, Pi Coding Agent, Oh My Pi, Forge, ZCode, Roo Code,
Amazon Q Developer CLI, and more.

For agents supporting **skills mode**, pass `--integration-options="--skills"`:

```powershell
specify init . --integration codex --integration-options="--skills"
```

This installs agent skills (`$speckit-*`) instead of slash-command prompt files.

---

## Spec Storage & Git Hygiene

Spec Kit creates a `specs/` directory with numbered feature folders:

```
specs/
├── 001-initial-feature/
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   └── ...
├── 002-next-feature/
│   └── ...
```

**Commit these to git.** They are the living record of *why* the code exists.
They survive agent context resets, team changes, and IDE switches. This is the
key advantage over storing plans only in agent memory.

The `.specify/` directory (templates, scripts, constitution) should also be
committed — it is the project's SDD configuration.

**Do NOT commit** the `specify` CLI itself — it's installed via `uv tool install`
at the user level, not per-project.

**Do NOT bundle** Spec Kit into MCPB packages or NSIS installers — it's a
developer tool, not a runtime dependency.

---

## Greenfield vs. Brownfield

### Greenfield (0-to-1)
Spec Kit shines. Full constitution → spec → plan → tasks → implement pipeline
with no existing codebase to conflict with. The `specify init` creates a clean
scaffold.

### Brownfield (existing codebase)
Spec Kit supports this with `specify init . --force` — it merges into an existing
directory without overwriting source files. The workflow adapts:

1. **Constitution first** — document existing principles in `.specify/memory/constitution.md`
2. **Spec per feature** — `/speckit.specify` for each new feature, not the whole project
3. **Plan references existing code** — the plan should identify what stays and what changes
4. **Converge is critical** — `/speckit.converge` catches drift between plan and reality

The official [Evolving Specs guide](https://github.github.io/spec-kit/docs/guides/evolving-specs.html)
documents the full brownfield loop.

---

## CLI Reference (Quick)

```powershell
# Project management
specify init <name> [--integration <agent>] [--force] [--here]
specify init . --integration opencode --force

# Self-management
specify self check                  # Check for updates
specify self upgrade                # Upgrade in-place
specify self upgrade --tag vX.Y.Z  # Pin version
specify integration list            # List supported integrations

# Extensions & presets
specify extension search [<query>]
specify extension add <name>
specify preset search [<query>]
specify preset add <name>

# Bundles
specify bundle search [<query>]
specify bundle info <id>
specify bundle install <id>
specify bundle list
specify bundle remove <id>
```

---

## Verdict for Fleet Use

Spec Kit is a **high-value addition** to the fleet toolchain. It solves a real
pain point — plans that live only in agent memory, vanish on context compaction,
and can't be reviewed by the human between phases.

**Strengths for fleet:**
- `uv`-native, Python 3.11+ — zero new toolchain dependencies
- opencode supported natively — `/speckit.*` slash commands in `.opencode/commands/`
- MIT license — no vendor lock-in
- Artifact chain persists to disk — survives context resets, IDE switches, team changes
- Extensions/presets/bundles system — composable, not monolithic
- Active GitHub org maintained — not a hobby project

**Gaps for fleet:**
- No NSIS/Tauri build awareness — plan phase doesn't know about PyInstaller specs or NSIS hooks
- No port registry integration — won't auto-assign from `WEBAPP_PORTS.md`
- No fleet-specific presets yet — would need `spec-kit-fleet-preset` for our stack (React/Vite/Bun/Tailwind/Zustand/Starlette/FastMCP)
- Shell scripts are bash (`.sh`) — run on Windows via Git Bash; no native PowerShell scripts yet
- Does not replace verification gates — you still run `ruff`, `tsc --noEmit`, `pytest`, `just cua-nsis-test` after implement

**Recommendation:** Adopt for new MCP server scaffolds and complex greenfield
features. Keep the existing `SPEC.md` + `workflow_2026.md` pattern for
medium-complexity changes. Consider building a fleet preset to customize Spec
Kit's templates with the standard stack (React/Vite/Bun/Tailwind/Zustand +
Starlette/FastMCP + FastMCP 3.4+ portmanteau pattern).

---

*Last updated: 2026-07-03 by Sandra*
*Cross-references: `standards/rules/workflow_2026.md`, `standards/rules/architecting_sota.md`, `tools/OPENCODE.md`*
