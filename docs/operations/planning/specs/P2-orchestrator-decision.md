# P2 — Orchestrator decision (PRD sketch)

**Status:** Draft — **decision gate 2026-06-20**  
**Priority:** P2  
**Candidates:** Revive `ednaficator` **OR** new `fleet-workflow-mcp` **OR** extend Fritz + RoboFang only

---

## Problem

The fleet has **four orchestration surfaces** with overlapping intent:

| Component | Ports | Status | Role |
|-----------|-------|--------|------|
| RoboFang | 10870–10872 | Active | Install, launch, health, connector |
| MetaMCP | 10718–10719 | Active | Diagnostics, scaffolding, Tool Lab |
| fleet-agent-mcp (Fritz) | 10996–10997 | Active | Heartbeat, PR pipeline, fleet_bridge |
| ednaficator | 10942–10943 | **Inactive** | Conversational orchestrator, Austria data |
| mcp-federation-hub | — | Active | 80+ server federation |

No component owns **durable multi-step workflows** with:

- Persisted DAG state
- Retry / compensation
- Cross-MCP tool chaining with audit trail
- Human approval gates (Prefab)

Agents improvise chains; failures are opaque.

## Decision matrix

| Criterion | Revive ednaficator | New fleet-workflow-mcp | Fritz-only extension |
|-----------|-------------------|------------------------|----------------------|
| Time to MVP | Medium (code exists) | High (greenfield) | Low |
| Conversational UX | **Strong** (original vision) | Weak unless added | Weak |
| Workflow durability | Needs build | **Native** | Partial (YAML in Fritz) |
| Austria / privacy story | **Strong** | Neutral | Neutral |
| Maintenance burden | One more active flagship | One focused repo | Spreads Fritz scope |

### Recommendation (2026-06-05)

**Hybrid:**

1. **Short term:** Extend **Fritz** `workflows/` YAML for 3 golden paths (morning brief, media request, digest pipeline).
2. **Medium term:** Revive **ednaficator** as the **conversational front-end** that *starts* Fritz workflows and surfaces status — not as a second workflow engine.
3. **Defer** standalone `fleet-workflow-mcp` unless Fritz YAML hits complexity ceiling (branching >5 levels, parallel fan-out).

## Outcome (unified)

One documented orchestration path:

```text
User / Agent
    → ednaficator (chat, intent, Austria context)  [optional UI]
    → Fritz workflow_start('morning_brief')
        → fleet_bridge → glance-mcp, aiwatcher-mcp, vienna-life-mcp, email-mcp
    → RoboFang health preflight before each step
    → MemOps: workflow run logged to advanced-memory
```

## Golden workflows (v1)

### WF-001 — Morning brief

| Step | MCP | Tool |
|------|-----|------|
| 1 | glance-mcp | weather + fleet probes |
| 2 | aiwatcher-mcp | `get_digest_preview` |
| 3 | vienna-life-mcp | `calendar_today` (P3) |
| 4 | fleet-agent-mcp | `pulse_add` summary task |
| 5 | advanced-memory | `adn_notes(write)` |

### WF-002 — Media request

| Step | MCP | Tool |
|------|-----|------|
| 1 | plex-mcp or jellyfin-mcp | search |
| 2 | arr-mcp | availability check |
| 3 | virtualdj-mcp or plex | play / queue |

### WF-003 — Research ingest

| Step | MCP | Tool |
|------|-----|------|
| 1 | arxiv-mcp | search |
| 2 | readly-mcp | `content/match` |
| 3 | aiwatcher-mcp | add to bundle |
| 4 | calibre-mcp | archive digest |

## ednaficator revival spec (if chosen)

### Phase 1 — Unblock (1 week)

- [ ] Fix `start.ps1` naked-PC compliance
- [ ] Wire Fritz `fleet_bridge` as MCP client (stdio)
- [ ] Replace mock LLM with Ollama `gemma4:12b` default
- [ ] Status → **Active** in FLEET_INDEX

### Phase 2 — Workflow launcher (2 weeks)

- [ ] UI: "Run workflow" dropdown (WF-001..003)
- [ ] SSE progress from Fritz heartbeat
- [ ] No duplicate workflow engine in ednaficator backend

### Phase 3 — Austria differentiator (optional)

- [ ] Data residency banner (local Ollama default)
- [ ] Link vienna-life-assistant MCP (P3)

## fleet-workflow-mcp spec (if decision reverses)

Only build if Fritz+ednaficator cannot meet:

- Parallel steps with join
- Cron scheduling independent of Fritz heartbeat
- Visual DAG editor in web_sota

**Ports:** 11026 / 11027  
**Engine:** SQLite `workflow_runs` + YAML definitions in `workflows/`  
**Tool:** `workflow_ops(operation=define|start|status|cancel|list)`

## Non-goals

- Replacing n8n for heavy SaaS integrations (use Rube/Composio for that class).
- Another MCP federation hub.

## Acceptance

1. WF-001 runs end-to-end from Fritz CLI or ednaficator button.
2. Failed step surfaces which MCP + tool failed (RoboFang health).
3. Run record queryable in MemOps within 24h.

## References

- `fleet-agent-mcp/README.md` — workflows/, fleet_bridge
- `ednaficator` — Secession UI, Starlette backend
- [FLEET_CONTROL_PLANE.md](../../FLEET_CONTROL_PLANE.md)
