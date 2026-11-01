# SPEC: Single-Writer Enforcement for advanced-memory-mcp (BUG-048 root fix)

**Status:** Phase 1 implemented 2026-10-05. Phases 2-3 planned.
**Owner:** fleet / advanced-memory-mcp
**Related:** `troubleshooting/details/BUG-048_Memops_Notes_Write_Unreliable.md` (OPEN),
`BUG-062_Stdio_Proxy_Wedge_No_Timeout.md`, commit `d9decdd6` (indexing half-fix),
2026-10-05 fire-and-forget fix in `knowledge_router.py` (uncommitted).

## 0. Why this spec exists

`adn_notes` writes have failed 5+ times with the same symptom (client timeout,
server eventually lands the write). Each fix repaired one layer and regressed
because the architecture allows the failure, and no test guards the property.

Evidence gathered 2026-10-05 ~03:30 (Goliath):

- **3 concurrent writers** on one SQLite/LanceDB/vault: NSSM daemon +
  stdio PID 79036 + stdio PID 102084 (both `--transport stdio`, started
  2026-10-04 19:08, i.e. running code from *before* the named-mutex guard).
- Our own session cycled PIDs 8556 → 89176 → 69748 → 53060 → 47496, every one
  reporting `Role: writer / Stdio lock: held by this instance` — **the daemon
  probe never succeeds in practice**, so every stdio client becomes a writer.
- `mcp.py` only probes when `ADVANCED_MEMORY_HTTP_PROXY` is explicitly set;
  the "default" (`http://127.0.0.1:10732/mcp`) claimed in AGENTS.md exists
  nowhere in code. Any client config missing that env var = silent writer.
- `tests/conftest.py:60` forces `ADVANCED_MEMORY_SYNC_INDEX=1`, bypassing the
  production async index path — the suite cannot see the path that breaks.
- UPDATE 04:05: second-DB hypothesis DISPROVEN. Daemon's own log
  (`logs/daemon-service-stderr-20261005T011612.713.log:4`) shows
  `db_url: sqlite+aiosqlite:///C:\Users\<user>\.advanced-memory\memory.db` —
  NSSM pinning works, one shared DB. So every extra writer is pure WAL/lock
  contention, no split-brain. BUG-048 phantoms = same-DB index/file races
  under concurrent writers, not two databases. Rollout step 5 closed.
- Unverified (needs elevated shell): nothing remaining on this point.

## 1. Goal

**Exactly one writer process per vault, ever.** All stdio clients proxy to the
NSSM daemon. Any violation fails loud at startup, never silent at 3am.

Non-goals: changing the daemon itself, the HTTP transport, LanceDB tuning,
multi-machine sync.

## 2. Design

### Rule 1 — Proxy by default (implemented, Phase 1)

`mcp --transport stdio` resolves the daemon URL as
`ADVANCED_MEMORY_HTTP_PROXY` if set, else `http://127.0.0.1:10732/mcp`.
No more "unset env = silent writer".

### Rule 2 — Writers proxy-or-die (implemented, Phase 1)

- Read-write stdio: probe succeeds → proxy (as today, BUG-062 55s timeout).
  Probe fails → process exits non-zero with a one-line actionable error
  (daemon down? start it: `nssm start advanced-memory-mcp-daemon`).
  Escape hatch: `ADVANCED_MEMORY_STANDALONE=1` = explicit local writer
  (maintenance only; status banners it).
- Read-only stdio (`ADVANCED_MEMORY_READONLY=1`): unchanged (proxy if
  reachable, else local reader — readers cannot corrupt).

Rationale: a loud outage pages the watchdog and gets fixed in minutes; silent
multi-writer corruption costs weeks (BUG-048 is 10 days old).

### Rule 3 — Version gate (implemented, Phase 1)

Before serving, a read-write stdio compares its own git SHA against daemon
`/health` `git_sha`. Definite mismatch → exit(1) with message (forces the
client to respawn; converges once daemon + clients run the same commit).
Undeterminable SHA → warn, proceed (fail-open, avoids bricking exotic setups).
Opt-out: `ADVANCED_MEMORY_SKIP_VERSION_GATE=1`.

This kills the "stale writer from yesterday predates today's fix" class that
produced tonight's 79036/102084 pair.

### Rule 4 — DB-layer guard (IMPLEMENTED 2026-10-05 ~04:20, `db.py:claim_writer_lock`)

SQLite `busy_timeout` + an exclusive writer lockfile (`vault/.writer.lock`,
`msvcrt.locking` / `flock`), enforced in both engine-creation paths, skipped
for readonly + in-memory. Second writer dies with `RuntimeError` naming the
live holder. OS releases the lock on crash — never stale.

Trap found during implementation (would have shipped a false green): MSVCRT
`locking()` locks at the CURRENT file position and `"a+b"` opens at EOF, so
parent/child locked different offsets on any non-empty file and both
"succeeded" (14-case matrix). Fix: explicit `seek(0)` before locking, owner
claim appended before locking, lock-fd never touched after. Regression test
`test_writer_lock_rejects_second_process` (cross-process) guards it.

### Rule 5 — Client config convergence (Phase 2, NOT implemented)

Canonical matrix (all pointing at the daemon):
`claude_desktop_config.json` memops = stdio + `HTTP_PROXY` + `READONLY=1`
(unchanged, correct); opencode `memops` = `remote http://127.0.0.1:10732/mcp`
(unchanged, correct); any other IDE (Cursor/Windsurf/Antigravity) = copy the
Claude Desktop entry. Audit script: list every client config on disk, assert
no stdio writer without proxy env.

## 3. Verification (Phase 1, all must pass)

1. `ruff check` + `py_compile` on `cli/commands/mcp.py`.
2. New regression tests `tests/api/test_write_latency_regression.py`: 2 passed.
3. Live: kill stale writers → client respawns → `adn_system status`
   shows daemon PID, no `Stdio lock: held by this instance` line.
4. Live `adn_notes quick` write ACKs immediately (was `MCP -32001`).
5. Negative: stop daemon + unset `STANDALONE` → stdio exits(1) with the
   actionable message (proves no silent writer).

## 4. Rollout (runbook)

1. Merge Phase 1 + tonight's `knowledge_router`/`portmanteau` fixes.
2. `Restart-Service advanced-memory-mcp-daemon -Force` (elevated).
3. Kill stale stdio writers (`Stop-Process`; plain processes, NOT services —
   clients respawn on next tool call).
4. Each IDE session's first memops call respawns a proxy; verify via status.
5. ~~Elevated check for a second DB under systemprofile~~ — CLOSED 04:05:
   daemon log proves one shared DB (`C:\Users\<user>\.advanced-memory\memory.db`).
   No migration needed; contention model confirmed.
6. Update BUG-048 entry: mark (a) timeouts fixed + tested, keep (b) desync
   open until step 5 + Phase 2 land.

## 6. Topology resolution (04:30, netstat proof)

The "mystery sidecar" (PIDs 47496/53060/128764/69848/54632, hidden cmdlines)
was never a sidecar: `netstat` shows the serving PID LISTENING on 10732.
This host's channel is daemon-routed (like opencode remote); `adn_system
restart` was killing daemon workers (hence fetch-failed-then-recover), and
"Role: writer / lock held by this instance" is the daemon's own self-view
(the `Active (stdio)` string is hardcoded in status.py). Consequences:

- Live behavior tonight (timeouts -> instant writes) tracked daemon code
  loads across its restarts, not sidecar respawns. The knowledge_router fix
  went live with the ~03:21 daemon boot; the full tree (lock, guard) with the
  ~04:28 restart.
- The only genuine standalone writers were 79036/102084 (visible
  `--transport stdio` cmdlines, predating the mutex) - both killed.
- Current steady state: ONE writer (daemon, lock holder since 04:29:45).
  Claude Desktop (readonly+proxy), opencode (remote), this host
  (daemon-routed) all converge on it. A future old-code stdio writer dies on
  the lock at engine creation; new-code ones proxy before touching the DB.
- `enforce_single_writer_stdio()` in `mcp/stdio_guard.py` now covers BOTH
  stdio entrypoints (`cli/commands/mcp.py` refactored onto it,
   `mcp/server.py __main__` hooked) - no bypass path left in-repo.

## 5. What this spec deliberately leaves open

- BUG-048(b) phantom disk/index desync cleanup for the existing orphan file
  (`inbox/Fleet_hygiene_sweep_meshing_philosophy.md`): needs direct vault
  access, separate task.
- Phase 2 items need their own commits (≤5 files each, with `.bak`).
