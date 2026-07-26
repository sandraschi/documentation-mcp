# Temporal Evaluation

**Date:** 2026-06-25  
**Status:** Not yet — powerful but overkill for current patterns  
**Source:** https://github.com/temporalio/temporal  
**License:** MIT (server + all SDKs)  

---

## 1. What it is

A **durable execution engine** — guarantees your code runs to completion even if the process crashes mid-way. It persists every step of execution, so after a crash the exact state is restored and execution resumes from the last completed step. Think "operating system for async code."

It is **not** a task queue (Celery), **not** a scheduler (cron), **not** a container orchestrator (K8s). It's the layer that makes individual multi-step processes crash-proof.

---

## 2. License

**MIT** — server, all SDKs (Python, Go, Java, TypeScript, .NET, Ruby, Rust). No AGPL, no dual licensing, no enterprise-gate features. Temporal Cloud (managed SaaS) is paid, but self-hosted is entirely MIT.

---

## 3. Stars & activity

21k stars (server), v1.31.1 (Jun 2026), 9k+ commits. Python SDK at v1.29.0, actively maintained. Backed by Temporal Technologies (founded by ex-Uber Cadence team). Production at Stripe, Netflix, Snap, Box.

---

## 4. Core concepts

| Concept | What it is | Fleet analogy |
|---|---|---|
| **Workflow** | Deterministic async function, replayed from event history | Multi-step MCP tool chain |
| **Activity** | Regular function that does real IO (API calls, file ops, subprocess) | A single tool execution |
| **Retries** | Configurable per-activity (interval, backoff, max attempts) | Tool call with auto-retry |
| **Signal** | Push a message into a running workflow | User says "cancel this" or "use different params" |
| **Query** | Read current workflow state without mutating it | Dashboard status polling |
| **Heartbeat** | Periodic progress ping from an activity | 8-hour CFD sim reporting "still alive at step 5000" |

---

## 5. Fleet fit — where it would help

### High-value candidates (multi-step, long-running, failure-prone)

| Pipeline | Steps | Risk | Temporal value |
|---|---|---|---|
| **CFD simulation** | Mesh → OpenFOAM/FluidX3D → Post-process → Export | 8-hour sim crashes at 7h | Resume from last completed activity |
| **Godot game build** | Design → Worlds → Compose → Logic → Export → Ship | 15-min pipeline, halfway failures | Retry failed step, not whole pipeline |
| **Rendering pipeline** | Stage → Frames → Compose → Upload | Frame-level failures | Per-frame heartbeats, retry only failed frames |
| **Multi-MCP chain** | qcad draw → freecad extrude → freecad FEM → godot import | Cross-repo orchestration | Full pipeline state persisted, survives any crash |

### Lower value (short, single-step, or fully synchronous)

| Pattern | Temporal value |
|---|---|
| Single MCP tool call | None |
| Quick API fetch | None |
| Chat conversation | None |

---

## 6. The inflection point

| Factor | Asyncio + retry | Temporal |
|---|---|---|
| Steps in pipeline | 1-3 | 3+ |
| Duration | < 1 minute | > 5 minutes |
| State size | In-memory, small | Persisted, any size |
| Crash cost | Rerun from scratch | Resume from last step |
| Monitoring | Console logs | Web UI (port 8233) + query API |
| Infra overhead | None | Server (Go binary) + DB (SQLite dev / PG prod) |

**The question:** Are you regularly running pipelines where a crash costs meaningful time? For the fleet today, the answer is **mostly no** — CFD and rendering are occasional, not daily. A single failed run is an annoyance, not a catastrophe.

---

## 7. Dev environment

Lowest-friction way to try it:

```bash
# Single binary dev server (SQLite, no Docker)
temporal server start-dev --db-filename temporal.db
# Web UI at http://localhost:8233
```

```python
# Python worker
@workflow.defn
class CfdPipeline:
    @workflow.run
    async def run(self, case_name: str) -> dict:
        mesh = await workflow.execute_activity(generate_mesh, case_name,
            start_to_close_timeout=timedelta(hours=1))
        result = await workflow.execute_activity(run_solver, mesh,
            start_to_close_timeout=timedelta(hours=12),
            heartbeat_timeout=timedelta(minutes=5))
        export = await workflow.execute_activity(export_results, result,
            start_to_close_timeout=timedelta(minutes=30))
        return export
```

---

## 8. Resource requirements

- **Dev server:** ~100-300 MB RAM, single Go binary, SQLite
- **Production:** PostgreSQL + optional Elasticsearch, ~2-4 GB total

---

## 9. Limitations

- **Workflow determinism** — workflow code cannot use `random`, `time.time`, network IO, or non-deterministic iterators. The Python SDK sandbox catches most violations, but it adds friction.
- **Event history limit** — 50k events per workflow (use Continue-As-New for long-lived ones)
- **Python SDK maturity** — good but behind Go SDK in edge features
- **Operational complexity** — production deployment needs PostgreSQL + Elastisearch management
- **No native MCP** — would need to write activities that call MCP tools via httpx

---

## 10. Verdict

**Not yet.** Temporal is excellent engineering but solves a problem that isn't acute in the fleet today. The CFD/FEM pipelines are occasional experiments, not daily production workflows. The determinism constraints and server dependency add overhead without proportional benefit at current scale.

**Revisit when:**
- CFD/FEM/rendering pipelines run daily and crash losses are visible
- The fleet ships a multi-MCP orchestration product that needs crash-proof execution
- A pipeline exceeds 10 minutes of cumulative activity time

For occasional multi-step pipelines, structured logging + idempotent tool design + simple SQLite checkpointing (store `{pipeline_id, step, params}` before each step, resume on restart) covers the use case with zero new infrastructure.
