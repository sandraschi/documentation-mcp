# BUG-048: memops `adn_notes` write path unreliable (timeout / NoneType.id)

**Severity**: P3
**Date**: 2026-09-25
**Component**: `memops` MCP server, `adn_notes` tool (`quick` and `write` operations)

## Symptom

Two consecutive attempts to save a session-summary note via `adn_notes` failed differently:

1. First attempt (before a Claude Desktop restart): `Request timed out` on both `quick` and `write` operations, no response at all.
2. After restarting Claude Desktop, `adn_project('ls')` succeeds fine — project `main` is active and default, so this is not a missing-project-context issue. `adn_notes(operation="quick", ...)` then returned a structured failure instead of timing out:

```json
{
  "success": false,
  "error": "WRITE_FAILED",
  "message": "Could not create or update note 'Fleet hygiene sweep + meshing philosophy...'",
  "diagnostic_info": {
    "title": "Fleet hygiene sweep + meshing philosophy...",
    "folder": "inbox",
    "error_details": "'NoneType' object has no attribute 'id'"
  }
}
```

3. Retrying with `operation="write"` (explicit `folder="fleet"` instead of default `inbox`) went back to a plain `Request timed out` with no error body at all.

## Root cause

Not yet isolated. `'NoneType' object has no attribute 'id'` on the `quick` path suggests the server-side note-creation flow dereferences something (likely a note/entity object, or the active project handle) that came back `None` from an earlier step — possibly a stale project/session reference left over from before the restart, or a DB/index handle that didn't reinitialize cleanly. The subsequent plain timeout on `write` (a different code path, explicit folder) suggests the server itself may be in a degraded state broadly, not something specific to the `quick` operation's title-auto-derivation.

## Update — after a full PC reboot (same day, later)

Root cause narrowed further, and it survived the reboot (this is not a stale-process/lock issue):

4. Retried `quick` with the same content post-reboot: `WRITE_FAILED`, but a **different** `error_details` this time — `"file for entity inbox/Fleet hygiene sweep + meshing philosophy... already exists: inbox\Fleet_hygiene_sweep_meshing_philosophy.md"`. This proves the earlier "failed" `quick` attempt (item 2, pre-reboot) actually **did** write the file to disk despite reporting failure.
5. `adn_notes(operation="read", identifier="inbox/Fleet_hygiene_sweep_meshing_philosophy.md")` on that exact path: **not found** — "I searched... but couldn't find any matching notes." So the file exists on disk (per the write-collision check) but is invisible to whatever index/lookup backs `read`/`search`.
6. `adn_notes(operation="delete", identifier=<same path>)`: **"Delete Failed... the note was not removed"** — can't clean up the orphan either, from either code path.
7. Retried `write` with a different title/folder (`folder="fleet"` instead of default `inbox`, to sidestep the collision): plain `Request timed out` again, no error body.

**Conclusion**: this is a real server-side bug, not a session/lock artifact — a full app + presumably server-process reboot did not clear it. Two separable problems: (a) a disk-write vs. index desync, where a write can land a file the read/search/delete paths can't see or touch, producing an unremovable phantom entry; (b) a general write-path instability (timeouts, inconsistent error shapes across otherwise-identical calls) that's independent of (a) and hits fresh titles too.

## Update — 2026-10-05 ~03:40 (Sandra + agent, live war-room)

Timeout arm (problem b) ROOT-CAUSED and fixed, with regression tests:

- Same symptom had THREE stacked causes, fixed one per incident (hence "fixed
  5 times"): (1) vector indexing awaited in response path — fixed in
  `d9decdd6` 01:28 today; (2) relation resolution + index still scheduled via
  Starlette `BackgroundTasks`, which run BEFORE the response is sent — fixed
  tonight in `knowledge_router.py` (true `asyncio.create_task`
  fire-and-forget); (3) N concurrent writers (daemon + stale stdio servers
  from 2026-10-04 predating the mutex guard) — two killed tonight.
- Live proof: `adn_notes quick` went from `MCP -32001 timeout` to instant ACK.
- `tests/api/test_write_latency_regression.py` (new): slow-fake tests that fail
  if heavy work ever re-enters the response path. 2 passed. (Found en route:
  `tests/conftest.py:60` forces `ADVANCED_MEMORY_SYNC_INDEX=1`, so the suite
  bypasses the production async path — part of why this kept regressing.)
- Structural fix spec'd: `projects/advanced-memory-mcp/SPEC_SINGLE_WRITER.md`
  (proxy-by-default, proxy-or-die, version gate). Phase 1 implemented in
  `cli/commands/mcp.py`, negative path verified (dead daemon → exit 2 with
  actionable message, no silent writer).
- Still OPEN: (a) phantom disk/index desync cleanup for
  `inbox/Fleet_hygiene_sweep_meshing_philosophy.md`; (b) single-writer rollout
  completion (host sidecar still launches a standalone writer — Rules 1-3
  don't cover entrypoints that bypass `cli/commands/mcp.py`); (c) elevated
  check whether the NSSM daemon opens a second DB under systemprofile
  (would explain phantoms as two-DB split-brain); (d) pre-existing
  `test_edit_entity_prepend` failure (`source: agent` frontmatter drift,
  fails on pristine HEAD too — unrelated).

## Workaround

None found. Filesystem-level phantom notes can't be cleaned up via any `adn_notes` operation tried so far (read/write/delete all fail differently against the same path). Skip memops for session notes; rely on written deliverable files (this repo's own docs) plus session transcripts as the source of truth. If the phantom-file cleanup matters, it likely needs direct filesystem access to the memops vault (outside MCP), not another tool call.

## Next steps

- Check memops server logs directly (filesystem access to the vault/index, not through the MCP tool) — this is likely required now, since the tool's own diagnostics are inconsistent with each other (write says exists, read says doesn't).
- Locate the actual vault directory on disk and inspect `inbox/Fleet_hygiene_sweep_meshing_philosophy.md` by hand to see whether it's a valid note, a partial/corrupt write, or empty.
- Consider whether the index (likely a separate DB/search layer, e.g. SQLite FTS or a vector index) needs an explicit rebuild/resync command — check `adn_system` for anything like `reindex` or `sync`.

## Update — 2026-10-15: Definitive Operational Procedure (NSSM HTTP REST API)

When the `advanced-memory-mcp-daemon` NSSM service is running, it holds an exclusive file lock on `C:\Users\<user>\.advanced-memory\.writer.lock`. Isolated stdio MCP callers (`adn_notes` write operation) cannot acquire the lock and fail with `WRITE_FAILED`.

Instead of calling `adn_notes` via stdio MCP, write mutations directly to the running NSSM service REST API:
- **Service URL**: `http://localhost:10705`
- **Create Note**: `POST /api/v1/main/knowledge/entities` with `{"title": "...", "folder": "...", "entity_type": "...", "content": "...", "entity_metadata": {"tags": [...]}}`
- **Update/Replace Body**: `PATCH /api/v1/main/knowledge/entities/{encoded_permalink}` with `{"operation": "replace_body", "content": "..."}`
- **Read Content**: `GET /api/v1/main/knowledge/entities/{encoded_permalink}/content`

This bypasses all lock contention, triggers proper asynchronous database updates and vector indexing, and eliminates the timeout/NoneType failures completely. Documented as a standard SOP in Memops vault at `procedures/sop-writing-to-memops-via-nssm-http-service`.

