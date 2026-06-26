# DeepSeek Architectural Patterns → Fleet Application Map

**Source:** [awesome-deepseek-agent overview](./awesome-deepseek-agent-overview.md)
**Status:** Actionable — apply to fleet repos
**Last Updated:** 2026-05-24

---

## Pattern 1: Cache-First LLM Loop

**Source:** Reasonix's architecture — reuses cached responses, Flash-first iteration, Pro on demand.
**Core idea:** System prompts and repeated context should be KV-cached. Second call to same model with same prefix should cost near-zero tokens.

### Apply to: dark-app-factory (HIGH IMPACT)

**Problem:** 19 specialists × N files × 3 retry attempts. Every specialist call receives the full specs blob (3K-8K tokens) verbatim. Identical context transmitted on every file generation call.

**Fix: Add a prompt cache layer**
```
# Before: every specialist call sends full specs
response = await llm.generate(system_prompt + specs + file_task)

# After: cache the common prefix
CACHE_KEY = hash(specs)
if cache_key in kv_cache:
    response = await llm.generate(file_task, cache_prefix=cache_key)
else:
    response = await llm.generate(specs + file_task)
    kv_cache[cache_key] = response.cache_id
```

**Estimated savings:** 60-80% token reduction on Worker phase. Specs are identical across all 19 specialists — only the file-task prompt varies. This is the single highest-ROI optimization in the fleet right now.

**Implementation:** 1-2 files changed in `worker.py`. Add a `PromptCache` class that hashes the spec context, stores the cache ID returned by the LLM API, and reuses it on subsequent calls.

### Apply to: aiwatcher-mcp (MEDIUM IMPACT)

**Problem:** Sandra-persona system prompt is 2K+ tokens, identical for every item scored in a batch (20-50 items per batch).

**Fix:** Cache the system prompt across batch scoring calls. Each item's payload is unique but the persona prefix is constant.

**Estimated savings:** ~25-40% token reduction on distillation phase. 2K tokens × 30 items × 4 batches/day = 240K tokens/day saved.

---

## Pattern 2: Plan → Agent → YOLO Mode System

**Source:** DeepSeek-TUI and OpenCode both use a three-mode cycling system.
**Core idea:** Stateful mode toggle: Plan (read-only research) → Agent (tool use with approval) → YOLO (auto-approve all). User cycles via a keybinding.

### Apply to: meta-mcp (HIGH IMPACT)

**Problem:** Fleet management operations currently have no safety gating. `launch_fleet_app`, `stop_fleet_app`, toolchain execution — all auto-execute without confirmation.

**Fix: Add a mode state to the fleet orchestrator**
```
class FleetMode(Enum):
    PLAN = "plan"       # Read-only: get_fleet_status, ping_fleet, probe_fleet_health
    AGENT = "agent"     # Interactive: launch/stop requires confirmation
    AUTO = "auto"       # Auto-approve: scheduled maintenance, self-healing
```

- **PLAN mode:** Only read-only tools work. `get_fleet_status`, `ping_fleet`, `probe_fleet_health`.
- **AGENT mode:** Mutating tools (`launch_fleet_app`, `stop_fleet_app`) require explicit approval.
- **AUTO mode:** Full automation for scheduled tasks (e.g., auto-restart degraded services).

**Implementation:** Add `fleet_mode` state to the meta_mcp server instance. Gate mutating tools behind mode check. Expose `/mode` or mode toggle endpoint.

### Apply to: deepfang (EXISTING — ENHANCE)

**Problem:** Deepfang already has a pipeline, but no user-facing mode toggle.

**Fix:** Expose Plan/Agent/Auto modes for the sanitizer-adjudicator-worker pipeline:
- **Plan:** Dry-run only — show what would be sanitized/adjudicated/dispatched.
- **Agent:** Normal mode with confirmation for worker execution.
- **Auto:** Air-gapped auto-execution (current default).

---

## Pattern 3: Sandboxed Tool Execution

**Source:** DeepSeek-TUI — OS-level sandboxing (macOS Seatbelt, Linux Landlock, Windows).
**Core idea:** Every code execution tool runs in an OS-enforced sandbox. No regex-based filtering, no "please don't run rm -rf" prompts.

### Apply to: freecad-mcp (CRITICAL GAP)

**Problem:** FreeCADCmd executes arbitrary Python scripts via direct subprocess on the host. FluidX3D compiles and runs native GPU C++ binaries unsandboxed. OpenFOAM runs via Docker but with host filesystem mounts. This is the **highest security gap in the fleet**.

**Fix: Containerize all execution paths**
```python
# FreeCADCmd: run in Docker with read-only input + write-only output
docker run --rm \
  --read-only \
  -v /path/to/input.step:/input.step:ro \
  -v /path/to/output:/output \
  freecad-mcp-worker \
  FreeCADCmd /script.py /input.step /output

# FluidX3D: same pattern — isolate GPU-accelerated binaries
# OpenFOAM: already Docker but tighten volume mounts
```

**Implementation steps:**
1. Create a `freecad-mcp-worker` Docker image with FreeCADCmd + FluidX3D + OpenFOAM
2. Rewrite `bridge.py` / subprocess mode to proxy through Docker SDK
3. Mount inputs read-only, outputs to a dedicated output volume
4. Add 300s timeout, 50MB output cap, network disabled for worker containers

**Effort:** Medium (3-5 files changed in server, new Dockerfile, test suite update)

### Apply to: virtualization-mcp sandbox (ENHANCE)

**Problem:** `sandbox_management` already uses Docker for isolation, but no network-level isolation.

**Fix:** Add `network_enabled: false` default for all sandbox containers. Add an `air_gapped` mode that uses `internal: true` Docker network (no WAN egress) — same as deepfang's worker.

---

## Pattern 4: Recursive-LM (Context Compression)

**Source:** DeepSeek-TUI's RLM — processes oversized inputs in sandboxed Python REPL without polluting parent context.
**Core idea:** When a document/task exceeds context window, spawn a sub-agent to process it first, summarize, and return only the result.

### Apply to: dark-app-factory (HIGH IMPACT)

**Problem:** Specs are passed verbatim to every one of 19 specialists. Many specialists only need a small relevant subset. 3K-8K tokens of specs per file × 19 specialists × N files = massive waste.

**Fix: Spec summarization per specialist domain**
```python
# Before: every specialist gets the full spec blob
for specialist in specialists:
    specialist.generate(full_specs + file_task)

# After: recursive summarization by domain
domain_summaries = {}
for domain in ["css", "react", "python", "html", "config"]:
    summary = await llm.summarize(full_specs, focus=domain)
    domain_summaries[domain] = summary

for specialist in specialists:
    relevant_summary = domain_summaries[specialist.domain]
    specialist.generate(relevant_summary + file_task)
```

**Estimated savings:** 50-70% context reduction per specialist call. A CSS specialist doesn't need the full Python backend architecture spec.

**Implementation:** Add a `SpecSummarizer` pre-processing step in `worker.py` that creates domain-specific summaries before the specialist generation loop.

---

## Pattern 5: Sub-Agent Spawning with Lifecycle

**Source:** DeepSeek-TUI's `agent_spawn` → `agent_wait` → `agent_result` → `agent_cancel` lifecycle.
**Core idea:** The main agent can spawn child agents for parallel/sub-tasks, wait for results, and cancel if needed. Full lifecycle management.

### Apply to: meta-mcp (HIGH IMPACT)

**Problem:** Fleet operations like "audit fleet → find degraded servers → auto-restart" are sequential and monolithic.

**Fix: Agentic fleet repair workflow**
```python
# Spawn parallel health-check sub-agents
audit_agent = await spawn_agent("audit", task="probe all fleet ports")
repair_agent = await spawn_agent("repair", task="prepare restart scripts")
log_agent = await spawn_agent("log", task="tail error logs")

# Wait for audit to complete
audit_results = await agent_wait(audit_agent)

# Spawn targeted repair agents for each degraded service
for degraded in audit_results.degraded:
    await spawn_agent(f"fix_{degraded.app_id}", 
        task=f"restart {degraded.app_id} via launch_fleet_app")

# Cancel log agent when done
await agent_cancel(log_agent)
```

**Implementation:** Already has toolchain infrastructure. Add `agent_spawn` / `agent_wait` / `agent_cancel` tools to the fleet launcher tool suite. Each spawned agent is an isolated context running a subset of fleet tools.

### Apply to: dark-app-factory (EXISTING — ENHANCE)

**Problem:** The 19 specialists run in dependency-level parallelism (Level 0 → Level 1 → Level 2) — rigid scheduling.

**Fix:** Dynamic sub-agent spawning instead of fixed dependency levels.
```python
# Before: rigid dependency levels
for level in [0, 1, 2]:
    await asyncio.gather(*[s.generate() for s in level_specialists[level]])

# After: dynamic sub-agent spawning
agents = [spawn_agent(s.name, task=s.task) for s in specialists]
results = await agent_wait_all(agents)
# Auto-detects dependencies, runs in parallel where possible
```

**Estimated improvement:** 30-50% faster builds by eliminating unnecessary sequential dependencies.

---

## Pattern 6: Flash-First / Pro-on-Demand Model Routing

**Source:** Reasonix's cost architecture — Flash by default, `/pro` to arm V4-Pro for next turn, `/preset max` for full Pro session.
**Core idea:** Not every LLM call needs the expensive model. Route cheap model for easy tasks, escalate to expensive model only when needed.

### Apply to: aiwatcher-mcp (HIGH IMPACT)

**Problem:** Single model scores everything. Same Anthropic API call for "local cat show announcement" and "critical security vulnerability."

**Fix: Tiered distillation**
```python
# Stage 1: Cheap local model scores everything (Gemma 1B)
initial_scores = await local_llm.score_all(items, model="gemma3:1b")

# Stage 2: Only re-score borderline items (4-7 range) with pro model
borderline = [i for i in initial_scores if 4 <= i.score <= 7]
pro_scores = await anthropic.score(borderline, model="claude-sonnet")

# Stage 3: Digest always uses pro model (quality-critical)
digest = await anthropic.generate_digest(top_items)
```

**Estimated savings:** 70% reduction in Anthropic API costs. Local Ollama scoring is free. Only ~30% of items need re-scoring.

**Implementation:** 1-2 files changed in `distillation.py`. Add a `ScoreTier` enum and two-pass scoring logic.

### Apply to: dark-app-factory (MEDIUM IMPACT)

**Problem:** Foreman and Worker both use the same model. Foreman does creative planning (needs quality), Worker does bulk file generation (needs speed).

**Fix: Model tiering by role**
```python
FOREMAN_MODEL = "deepseek-v4-pro"  # Planning — needs reasoning
WORKER_MODEL = "deepseek-v4-flash" # File generation — needs speed, volume
RETRY_MODEL = "deepseek-v4-pro"    # Fixup on 3rd retry — needs reasoning
```

---

## Pattern 7: Self-Improving Agent Loop

**Source:** Hermes by Nous Research — creates skills from experience, improves them during use, persists knowledge across sessions.
**Core idea:** The agent observes what works/fails, extracts patterns, writes reusable skills for future sessions.

### Apply to: OpenCode / deepfang (MEDIUM-HIGH)

**Problem:** Every session starts fresh. No cross-session learning. Repeated mistakes are re-made.

**Fix: Session-to-session knowledge persistence**
```python
# After each successful tool call, extract the pattern
@after_tool_call
async def learn_from_success(tool_name, args, result):
    if result.success and is_new_pattern(tool_name, args):
        skill = await extract_skill_pattern(tool_name, args, result)
        await persist_skill(skill, category=tool_category(tool_name))

# Before each session, load relevant skills
@before_session
async def load_relevant_skills(goal):
    skills = await semantic_search(goal, skill_store)
    inject_into_system_prompt(skills)
```

**Implementation:** Use the existing `~/.agents/skills/` convention. Add a `learn` tool that:
1. Observes successful tool call sequences
2. Extracts the reusable pattern as a SKILL.md
3. Persists to the skills directory
4. Injects relevant skills into future sessions

### Apply to: aiwatcher-mcp (LOW-MEDIUM)

**Problem:** The same type of spam/content keeps appearing. Scrubber rules are manually maintained.

**Fix:** Auto-generate scrubber rules from distillation patterns.
```python
# Items consistently scored <2 and tagged "spam" → auto-add to spam_blocklist.txt
if item.score < 2 and "spam" in item.tags:
    pattern = extract_pattern(item.title, item.summary)
    append_to_blocklist(pattern)
    scrubber_reload()
```

---

## Pattern 8: Skill Discovery Convention Formalization

**Source:** DeepSeek-TUI, Deep Code, and OpenCode all follow the same convention: `~/.agents/skills/<name>/SKILL.md` (user-level) and `./.deepcode/skills/<name>/SKILL.md` (project-level).
**Core idea:** Standardize skill discovery paths across all fleet tools.

### Apply to: ALL FLEET REPOS

**Current state:** Inconsistent. Some repos follow the convention, some don't.

**Fix: Fleet-wide SKILL.md standard**
```python
# Standard skill discovery — use this in every fleet repo
SKILL_PATHS = [
    Path.home() / ".agents" / "skills",        # User-level (cross-tool)
    Path.cwd() / ".repo" / "skills",            # Project-level (repo-specific)
]

def discover_skills() -> list[Skill]:
    skills = []
    for base in SKILL_PATHS:
        for skill_md in base.glob("*/SKILL.md"):
            skills.append(parse_skill(skill_md))
    return skills
```

**Action:** Add this discovery pattern to `meta-mcp`'s scaffolding tool so every new repo generated gets it automatically.

---

## Priority Implementation Queue

| # | Pattern | Target Repo | Impact | Effort | Timeline |
|---|---------|-------------|--------|--------|----------|
| 1 | Cache-First Loop | dark-app-factory | 60-80% token savings | 1-2 files | This week |
| 2 | Sandboxed Execution | freecad-mcp | Security critical | 3-5 files + Docker | This sprint |
| 3 | Flash-First Routing | aiwatcher-mcp | 70% API cost reduction | 1-2 files | This sprint |
| 4 | Recursive-LM Summarization | dark-app-factory | 50-70% context reduction | 1 new file | Next sprint |
| 5 | Plan→Agent→Auto Modes | meta-mcp | Safety improvement | 2-3 files | Next sprint |
| 6 | Sub-Agent Spawning | meta-mcp | Fleet self-healing | 3-4 files | Next sprint |
| 7 | Self-Improving Loop | deepfang + OpenCode | Cross-session learning | 2-3 files | Later |
| 8 | Skill Convention | meta-mcp scaffolding | Fleet consistency | 1 file | Later |
