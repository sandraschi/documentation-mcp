# P5 — Fleet trust layer (PRD sketch)

**Status:** Draft  
**Priority:** P5 (can start immediately — no secrets dependency)  
**Targets:** `mcp-test-suite` (revive), `mcp-central-docs/operations/` (scripts), MetaMCP (optional runner)

---

## Problem

| Issue | Data |
|-------|------|
| Registry drift | ~167 meaningful repos vs 119 in `fleet-registry.json` |
| Index drift | FLEET_INDEX 140 vs disk ~167 |
| Dead servers in catalog | `sdr-mcp`, `ednaficator`, `vbox-mcp`, `mcp-links-service` |
| No contract tests | `mcp-test-suite` inactive |
| Agent false confidence | 120 tools listed, unknown % broken |

Agents waste context and user trust on **phantom capabilities**.

## Outcome

**Fleet trust layer** = three artifacts:

1. **Registry sync** — automated diff disk ↔ JSON ↔ FLEET_INDEX  
2. **Contract smoke suite** — health + `list_tools` + optional golden tool call  
3. **Trust score** — per-repo metadata in registry (`smoke_pass`, `last_smoke`, `status`)

## Non-goals

- Full integration test of every tool (combinatorial explosion)
- Blocking git push on smoke fail (advisory first; enforce later)

## Components

### 1. `sync-fleet-registry.ps1`

**Location:** `mcp-central-docs/operations/scripts/sync-fleet-registry.ps1`

```text
Input:  D:\Dev\repos\*-mcp directories
Output: fleet-registry.diff.json, FLEET_INDEX.pending.md
Logic:
  - Detect new dirs matching *-mcp
  - Read glama.json / README for description if present
  - Assign category heuristic from name
  - Flag removed dirs as archived
  - Never auto-commit — human reviews diff
```

### 2. Revive `mcp-test-suite`

**Location:** `D:\Dev\repos\mcp-test-suite`

| Test tier | What |
|-----------|------|
| T0 | Repo has `start.ps1`, `pyproject.toml`, FastMCP ≥3.1 |
| T1 | `GET /health` or stdio `tools/list` within 60s |
| T2 | One noop/safe tool call per server (server-specific map) |
| T3 | web_sota frontend returns 200 (optional) |

**Golden 20 (initial):**

advanced-memory-mcp, devices-mcp, virtualization-mcp, git-github-mcp, docker-mcp, plex-mcp, calibre-mcp, robofang, meta_mcp, fleet-agent-mcp, email-mcp, aiwatcher-mcp, arxiv-mcp, windows-operations-mcp, filesystem-mcp, observability-mcp, glance-mcp, immich-mcp, fastsearch-mcp, vienna-life-assistant

### 3. Trust metadata in `fleet-registry.json`

```json
{
  "name": "sdr-mcp",
  "status": "quarantined",
  "smoke": {
    "last_run": "2026-06-05",
    "tier1_pass": false,
    "reason": "P1: invalid task=True decorators"
  }
}
```

### 4. MetaMCP integration (optional)

- `meta_dev` recipe: `just fleet-smoke`
- Tool Lab card: red/yellow/green server grid

## Phases

### Phase 1 — Registry sync (1 week)

- [ ] `sync-fleet-registry.ps1` + document in planning README
- [ ] Manual review PR for ~58 missing entries
- [ ] Quarantine bit for known runts

### Phase 2 — Smoke harness (2 weeks)

- [ ] Revive mcp-test-suite with pytest + JSON report
- [ ] Golden 20 T1 tests
- [ ] `just smoke` in mcp-central-docs

### Phase 3 — CI + Fritz (1 week)

- [ ] Weekly GitHub Action or Fritz heartbeat job
- [ ] Failures → MemOps note + glance-mcp probe optional
- [ ] Cursor default MCP config excludes quarantined servers

## Runts handling (immediate)

| Repo | Action |
|------|--------|
| sdr-mcp | `status: quarantined` until P1 bugs fixed |
| vbox-mcp | `status: archived` — superseded by virtualization-mcp |
| mcp-links-service | archive or merge into mcp-studio |
| ednaficator | `status: reviving` — P2 decision |

## Acceptance

1. `sync-fleet-registry.ps1` produces diff with &lt;5% false positives on *-mcp detection.
2. Golden 20 T1 ≥ 90% pass on sandra's machine (document known flakes).
3. FLEET_INDEX and fleet-registry agree on status for all quarantined repos.
4. Fritz `morning_brief` includes `fleet_smoke_summary` field.

## References

- [FLEET_GRADING_STANDARDS.md](../../../standards/FLEET_GRADING_STANDARDS.md)
- [BUGS_DEPOT.md](../../../troubleshooting/BUGS_DEPOT.md)
- meta_mcp Tool Lab
