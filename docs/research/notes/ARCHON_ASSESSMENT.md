---
title: Archon (coleam00/Archon) — Fleet Assessment
status: active
tags: [archon, workflow-engine, third-party, assessment, liftable-patterns, claude-code]
source: https://github.com/coleam00/Archon
last_updated: 2026-05-19
---

# Archon — Fleet Assessment

**Repo:** https://github.com/coleam00/Archon  
**Stars:** ~21.6k (May 2026)  
**License:** MIT  
**Language:** TypeScript (Bun)  
**Latest:** v0.3.12  
**Tagline:** "The first open-source harness builder for AI coding. Make AI coding deterministic and repeatable."

---

## What It Is

Archon is a workflow engine for AI coding agents. Define dev processes as YAML DAG workflows (plan → implement → validate → review → PR) and execute them deterministically against Claude Code (or Codex, Pi). Think **n8n for software development**, or **what Dockerfiles did for infra and GitHub Actions did for CI/CD**.

### Architecture

```
Platform Adapters (Web UI, CLI, Telegram, Slack, Discord, GitHub)
         │
         ▼
 Orchestrator (Message Routing & Context Management)
         │
    ┌────┴────┐
    │         │
 Command    Workflow    AI Assistant Clients
 Handler   Executor    (Claude / Codex / Pi)
 (Slash)   (YAML)
    │         │
    └────┬────┘
         │
         ▼
 SQLite / PostgreSQL (7 tables)
```

### Default Workflows (17 bundled)

`archon-assist`, `archon-fix-github-issue`, `archon-idea-to-pr`, `archon-plan-to-pr`, `archon-smart-pr-review`, `archon-comprehensive-pr-review`, `archon-create-issue`, `archon-validate-pr`, `archon-resolve-conflicts`, `archon-feature-development`, `archon-architect`, `archon-refactor-safely`, `archon-issue-review-full`, `archon-ralph-dag`, `archon-remotion-generate`, `archon-test-loop-dag`, `archon-piv-loop`

---

## Objections to Full Use

These are the reasons Archon should **not** be adopted as a fleet dependency:

### 1. Architecture Mismatch: CLI Process Orchestration vs MCP Tool Composition

Archon's model is "orchestrate Claude Code as an external CLI process" — it manages `CLAUDE_BIN_PATH`, spawns subprocesses, and parses output. Our fleet's model is "compose MCP tools via FastMCP transport" — every server is a deterministic, typed, composable primitive. These are fundamentally different IO paradigms. Introducing Archon as a meta-orchestrator creates a leaky abstraction: tool definitions, state, and error handling would need to bridge two incompatible execution models.

### 2. Redundant with Existing Fleet Infrastructure

| Fleet Asset | What It Provides |
|---|---|
| `workflow_2026.md` | EXPLORE → PLAN → IMPLEMENT → COMMIT loop (same semantics) |
| `deepfang` (10956-10963) | Execution pipeline with sanitizer/adjudicator/worker + Prometheus/Grafana |
| `hermes-agent` (10972) | Fleet conductor with platform-aware routing |
| `mcp_registration.md` | Deterministic, repeatable tool execution via `@mcp.tool(annotations=...)` |
| `docstrings_sota.md` | Schema-first parameter documentation for AI consumption |

Every core value Archon claims ("repeatable", "isolated", "composable") is already delivered by our MCP-native architecture.

### 3. Duplicate State Management

Archon brings:
- Its own SQLite/Postgres database (7 tables: codebases, conversations, sessions, workflow runs, isolation environments, messages, events)
- Git worktree isolation management
- YAML DSL for workflow definitions
- Platform adapter state (Telegram/Slack/Discord sessions)

All of these duplicate transport, state, and persistence layers already handled by FastMCP + our existing server fleet. Adding Archon doubles the state surface area for zero marginal gain.

### 4. Vendor Lock to Claude Code CLI

Archon is built primarily as a harness **for** Claude Code's CLI (`CLAUDE_BIN_PATH`). This couples us to:
- Claude Code's subprocess protocol (non-standard, undocumented edge cases)
- Binary versioning and path management across platforms
- Features that only exist in the CLI but not in the MCP transport

Our fleet is deliberately model-agnostic (Gemini, Claude, local via Ollama) via MCP's standard transport. Adopting Archon would re-introduce vendor coupling.

### 5. Per `architecting_sota.md` Rule 2: Default to a Shim

> For every external dependency, the model must answer: "Why can't this be a 50-line Python/FastAPI script?"

Archon's core loop (read YAML → dispatch to AI → collect result → check conditions → loop or advance) is ~200 lines of Python. The YAML DSL is straightforward to parse. The worktree isolation is a `git worktree add` + `Remove-Item -Recurse` wrapper. None of it justifies a 1,400+ commit TypeScript/Bun dependency with its own database and four platform adapters.

---

## Liftable Patterns ("What to Filch")

These four patterns are worth extracting as micro-implementations in our Python MCP servers. Each includes a spec.

---

### Pattern 1: Git Worktree Isolation for Parallel Runs

**Source:** Archon creates a fresh `git worktree` per workflow run, so N parallel fixes operate on independent working directories with zero state conflict.

**Why we want it:** MCP tools that modify repos (e.g., `depot-mcp`, `git-github-mcp`, `qcad-mcp`) currently operate on the working tree directly. Concurrent tool calls risk interference (half-applied patches, dangling branches, merge conflicts mid-operation).

**Spec:**

```
Module: fleet/infra/worktree_context.py

class WorktreeContext:
    """Context manager that creates a temp git worktree, scopes operations,
    and cleans up. Supports parallel, isolated repo modifications."""

    def __init__(repo_path: Path, branch_prefix: str = "worktree/"):
        # Store repo path, generate unique branch name
        self._repo = repo_path
        self._branch = f"{branch_prefix}{uuid4().hex[:8]}"
        self._worktree_dir: Path | None = None

    async def __aenter__() -> WorktreeContext:
        # 1. Verify repo is clean (stash if needed, warn)
        # 2. git branch <self._branch> from HEAD
        # 3. git worktree add <tmpdir> <self._branch>
        # 4. Set self._worktree_dir = tmpdir
        # Return self

    async def __aexit__(*exc_info):
        # 1. Commit any staged changes to self._branch
        # 2. git worktree remove <self._worktree_dir>
        # 3. git branch -D <self._branch> (unless --keep-branch)
        # 4. Clean up temp dir

    async def snapshot() -> Path:
        # Return path to isolated worktree directory
        return self._worktree_dir
```

**Usage in an MCP tool:**

```python
@mcp.tool(annotations=MUTATING)
async def parallel_fix(
    repo: Annotated[str, Field(description="Repo path.")],
    patches: Annotated[list[str], Field(description="Patches to apply.")]
) -> dict:
    results = []
    async with WorktreeContext(repo) as wc:
        for patch in patches:
            isolated = await wc.snapshot()
            result = await apply_patch(isolated, patch)
            results.append(result)
    return {"success": True, "results": results}
```

---

### Pattern 2: Loop Nodes with `fresh_context: true`

**Source:** Archon's loop node restarts with a clean context window each iteration (`fresh_context: true`), preventing context drift in iterative workflows (implement → test → fail → retry).

**Why we want it:** Our portmanteau tools that iterate (retry-until-pass, multi-step validation) accumulate context across iterations, causing LLM drift — the model gets lost in earlier failed attempts.

**Spec:**

```
Module: fleet/patterns/loop_until.py

class LoopUntil:
    """Execute a callable with fresh context per iteration until a condition is met.

    Each iteration gets its own isolated context (in-memory, no accumulation).
    Termination is evaluated via a typed condition enum + optional predicate callable.
    """

    class Condition(str, Enum):
        ALL_TASKS_COMPLETE = "all_tasks_complete"
        APPROVED = "approved"
        TESTS_PASS = "tests_pass"
        MAX_ITERATIONS = "max_iterations"
        TIMEOUT = "timeout"

    def __init__(
        max_iterations: int = 10,
        timeout_seconds: float = 300.0,
        condition: LoopUntil.Condition = LoopUntil.Condition.MAX_ITERATIONS,
        predicate: Callable[[dict], bool] | None = None,
    ):
        ...

    async def run(
        fn: Callable[[int], Awaitable[dict]],  # fn receives iteration index
    ) -> dict:
        # For i in range(max_iterations):
        #   result = await fn(i)     # fresh callable/context each time
        #   evaluation = self._evaluate(result)
        #   if evaluation.terminate:
        #       return evaluation.summary
        # Raise TimeoutError or MaxIterationsError
```

**Usage:**

```python
@mcp.tool()
async def implement_with_retry(
    spec: Annotated[str, Field(description="Feature spec.")]
) -> dict:
    loop = LoopUntil(
        condition=LoopUntil.Condition.TESTS_PASS,
        max_iterations=5,
    )

    async def attempt(iteration: int) -> dict:
        code = await generate_code(spec, iteration)
        test_result = await run_tests()
        return {"code": code, "tests_passed": test_result.success, "output": test_result.output}

    return await loop.run(attempt)
```

---

### Pattern 3: Human Approval Gates

**Source:** Archon's `interactive: true` + `until: APPROVED` pauses workflow execution and waits for human sign-off before proceeding (especially around destructive operations).

**Why we want it:** `DESTRUCTIVE`-annotated tools currently execute immediately. Adding an automatic approval gate before destructive filesystem or git operations aligns with safety best practices without requiring manual wrapping in every tool.

**Spec:**

```
Module: fleet/patterns/approval_gate.py

class ApprovalGate:
    """Decorator / context manager that pauses before destructive operations.

    On an interactive TTY: prompt y/n with a diff preview.
    On non-interactive (CI/API): check env var or auto-deny.
    Supports timeout: auto-deny if no response within N seconds.
    """

    def __init__(
        message: str = "This operation is destructive. Proceed?",
        timeout_seconds: float = 30.0,
        auto_deny_if_no_tty: bool = True,
    ):
        ...

    async def wait_for_approval(diff_preview: str | None = None) -> bool:
        # If not interactive and auto_deny_if_no_tty: return False
        # If INTERACTIVE_APPROVAL=always in env: return True
        # If INTERACTIVE_APPROVAL=never in env: return False
        # Prompt user via stderr (not stdout, to avoid corrupting MCP response)
        # Return True if "y", False if "n" or timeout
```

**Integration via decorator:**

```python
@mcp.tool(annotations=DESTRUCTIVE)
@approval_gate("Delete branch and all commits?")
async def force_delete_branch(
    repo: str, branch: str
) -> dict:
    ...
```

**Integration via `@mcp.tool` mixin (preferred):**

This could be baked into FastMCP itself: a tool annotated `DESTRUCTIVE` that also registers a `confirmation_required` hook. FastMCP 3.2's sampling context could deliver the prompt before execution.

---

### Pattern 4: `until` Condition DSL

**Source:** Archon's workflow nodes declare termination conditions declaratively: `until: ALL_TASKS_COMPLETE`, `until: APPROVED`, `until: TESTS_PASS`.

**Why we want it:** A formal, composable condition language lets us express loop termination in tool definitions rather than in imperative Python. This is especially valuable for portmanteau tools where the loop structure is core to the tool's contract.

**Spec:**

```
Module: fleet/patterns/conditions.py

class Condition DSL:
    """A lightweight state machine that evaluates termination conditions
    against a running result accumulator.

    Conditions are composable:
      - ALL_TASKS_COMPLETE: all expected output keys present
      - APPROVED: result.get("approved") is True
      - TESTS_PASS: result.get("tests_passed") is True
      - and/or/not combinators
      - Custom predicate: Callable[[dict], bool]
    """

    @dataclass
    class CompositeCondition:
        type: Literal["all", "any", "not", "predicate", "state_key"]
        # all/any: list of sub-conditions
        # not: single sub-condition
        # predicate: Callable[[dict], bool]
        # state_key: str key to check in result + optional expected value

    class ConditionEvaluator:
        def __init__(self, condition: CompositeCondition):
            self._condition = condition

        def evaluate(state: dict) -> Evaluation:
            # Recursively evaluate condition tree against state
            # Returns Evaluation(terminate=True/False, reason=str)

    # Shorthand factory functions:
    def all_tasks_complete(task_count: int) -> CompositeCondition: ...
    def approved() -> CompositeCondition: ...
    def tests_pass() -> CompositeCondition: ...
    def any_of(*conditions) -> CompositeCondition: ...
    def all_of(*conditions) -> CompositeCondition: ...
```

**Usage with LoopUntil:**

```python
condition = all_of(
    tests_pass(),
    approved(),
)
loop = LoopUntil(condition=condition, max_iterations=10)
```

---

## References

- Repo: https://github.com/coleam00/Archon
- Docs: https://archon.diy
- License: MIT
- Fleet standards this assessment applies: `workflow_2026.md`, `architecting_sota.md`, `mcp_registration.md`, `tauri_godot_sota.md`
- Fleet pipelines this intersects: `deepfang` execution architecture, `hermes-agent` fleet conductor, `depot-mcp` multi-repo ops
