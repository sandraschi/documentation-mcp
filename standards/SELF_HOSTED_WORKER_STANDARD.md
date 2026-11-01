---
title: "Self-Hosted Worker Standard - Bounded Execution & Token Leak Prevention"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Self-Hosted Worker Standard — Bounded Execution & Token Leak Prevention

**Established**: 2026-09-12  
**Status**: Active Fleet Standard  
**Target Hardware**: Goliath (AMD Ryzen 9 5900X, RTX 4090 24GB, 64GB RAM, Windows 11)  
**Complements**: 
- `mcp-central-docs/standards/LOCAL_LLM_FIRST_DOCTRINE.md` (local model economics)
- `mcp-central-docs/standards/TOOLING_COST_MODEL.md` (tooling ladders & cost tiers)
- `mcp-central-docs/standards/AGENT_PROTOCOLS.md` (agent interaction & safety rules)

---

## 1. Context: The September 2026 Paradigm Shift

In September 2026, commercial agentic harnesses (led by Cursor) introduced two diverging architectures:

1. **Unbounded Cloud Autonomous Swarms ("Projects")**:
   Long-lived cloud coordinators that maintain indefinite context, spawn thousands of parallel subagents, and subscribe autonomously to external event streams (PRs, Slack channels, cron triggers).
   * **Fleet Assessment**: **REJECTED**. Projects is an unbounded token sinkhole designed for enterprise corporate budgets. Autonomous multi-agent retry loops and perpetual event subscriptions cause exponential token compounding without human circuit-breakers.

2. **Decoupled Self-Hosted Execution ("Self-Hosted Machines / Pools")**:
   The cloud LLM gateway drives reasoning and tool decisions, but tool execution, filesystem access, command execution, and build steps run entirely inside the operator's local infrastructure.
   * **Fleet Assessment**: **ACCEPTED WITH HARD BOUNDS**. Allows native access to Goliath's 213-repo fleet, internal FastMCP servers, and local dependencies without cloud container spin-up delays or code exfiltration.

---

## 2. The Core Fallacy: "Local Compute Means Free Execution"

A dangerous trap in self-hosted worker setups is assuming that because terminal commands and disk operations run locally for $0, the agent session is inexpensive.

**In reality, self-hosted workers can incinerate cloud API tokens faster than pure cloud sandboxes:**
- When an agent runs a local command (e.g. `uv run pytest` or `git status`) that dumps 1,500 lines of terminal output, that raw text is appended into the LLM context.
- Every subsequent turn must resend and pay for those output tokens.
- In a 15-turn debugging loop on an open-ended problem, unmonitored stdout and blind directory crawls will burn millions of input tokens on high-tier models.

**The Golden Rule**: *Compute is free on Goliath; Reasoning context is metered at the gateway. The host environment must actively starve the agent of unnecessary context.*

---

## 3. The Five Token Sinkholes & Countermeasures

| Token Sinkhole | Mechanism of Token Waste | Mandatory Countermeasure |
|---|---|---|
| **1. Terminal Vomit (Output Explosion)** | Agent runs `pytest` or `ruff check .`; 2,000 lines of tracebacks or lint warnings flood prompt context. | **Output Muzzling**: All diagnostic commands must use brief recipes piped to `head -n 20` or `--maxfail=1`. |
| **2. Fleet Trawling (Blind Exploration)** | Agent does recursive directory traversal across 213 repos to find target files. | **Deterministic Manifest Inversion**: Host shell script / ripgrep creates targeted manifest *before* prompt. |
| **3. Quadratic Context Tax ($O(N^2)$)** | Agent session stays open for hours doing multiple tasks; turn 20 re-processes turns 1–19. | **Atomic Micro-Sessions**: Hard cap of 3–5 turns per session. Kill and reboot context between discrete tasks. |
| **4. Flail & Retry Loops** | Agent attempts 10 syntax variations to fix an environmental or import error. | **Two-Strike Circuit Breaker**: If verification fails twice consecutively, halt immediately and yield to operator. |
| **5. Dirty Worktree Negotiation** | Agent makes broken changes across multiple files, then burns tokens trying to rollback. | **Ephemeral Git Worktrees**: Run workers in temporary git worktrees (`git worktree add`). Reset via instant branch wipe. |

---

## 4. Implementation Protocols on Goliath

### Protocol 1: The Muzzled Recipe Standard

Never allow an agent to run raw test or lint commands. Every repo `justfile` must expose muzzled diagnostic targets:

```just
# Mandatory muzzled recipes for agent consumption
test-brief:
    uv run pytest --tb=short -q --maxfail=2 | head -n 30

lint-brief:
    uv run ruff check . --output-format=concise | head -n 20

typecheck-brief:
    uv run mypy . --no-error-summary | head -n 25
```

If an error occurs, the agent gets the file path, line number, and error type in under 400 tokens, rather than dumping 30,000 tokens into history.

### Protocol 2: Inverted Discovery (Pre-Computation)

Before invoking a self-hosted worker on multi-repo fleet changes:
1. Run a local deterministic script via PowerShell / `rg.exe` / `fd.exe`.
2. Generate an exact target list:
   ```powershell
   # Run locally on host:
   rg "class LegacyTool" --files-with-matches > D:\Dev\repos\_junk\targets.txt
   ```
3. Dispatch the agent with the exact target file path only. **Never ask the agent to search the fleet.**

### Protocol 3: Ephemeral Worktree Isolation

For self-hosted runs involving multi-file edits or speculative refactoring:

```powershell
# Create an ephemeral worktree on Goliath
git worktree add D:\Dev\repos\worktrees\task-worker-01 -b worker/task-01

# Point worker pool or machine to worktrees\task-worker-01
# If run fails:
git worktree remove --force D:\Dev\repos\worktrees\task-worker-01
git branch -D worker/task-01
```
*Token cost of resetting a broken run: **0 tokens**.*

### Protocol 4: Two-Strike Circuit Breaker

The system prompt or instruction header for any self-hosted agent worker must enforce:

> **Execution Circuit Breaker**:
> 1. Formulate change plan.
> 2. Apply change.
> 3. Run `just test-brief`.
> 4. If test fails, analyze output and make ONE corrective attempt.
> 5. If test fails a second time: **STOP IMMEDIATELY**. Do not guess. Report the failure and exact diff to the user.

---

## 5. Platform Constraints: Windows 11 Host Specifics

Cursor's self-hosted machines release introduces "Computer Use" (virtual desktop, mouse/keyboard driving, browser screenshots), but with a strict platform note:
- **Computer Use is Linux and Mac only.**
- On **Windows 11 (Goliath)**, self-hosted workers operate via **CLI, shell, tool calls, and filesystem operations**. GUI desktop driving is not currently supported natively by Cursor's worker daemon on Windows.
- **PowerShell 7 (`pwsh`)** is the mandatory execution shell. Avoid `cmd` or naked bash paths.
- Ensure full tool path resolution as mandated in `standards/AGENTS.md` (`uv.exe`, `just.exe`, `rg.exe`).

---

## 6. Decision Flowchart: Model & Worker Tier Selection

```
Is the task fleet-wide mechanical maintenance or bulk edits?
├── YES ──> Sunk-Cost Local (Ollama / Qwen3.8:27B on RTX 4090 via opencode/Cline)
│           Marginal Cost: $0.00
└── NO  ──> Does it require frontier reasoning on local code/FastMCP?
            ├── NO  ──> Keep on Local 4090
            └── YES ──> Self-Hosted Worker (Cursor / Antigravity via Goliath Pool)
                        ├── Enforce Muzzled Output (Protocol 1)
                        ├── Inject Pre-Computed Manifest (Protocol 2)
                        ├── Cap Session at 3-5 Turns (Protocol 3)
                        └── Apply Two-Strike Circuit Breaker (Protocol 4)
```
