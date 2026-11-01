# NSSM + LocalSystem Ambient Path Resolution: Postmortem and Fleet Audit

**Date:** 2026-07-26
**Trigger:** advanced-memory-mcp (memops) notes written via MCP tools were invisible in the webapp at 127.0.0.1:10704. Roughly 71 notes over ~12 days were affected.
**Status:** memops fixed (2026-07-26 initial, **re-verified 2026-07-27** after weeks of silent split-brain). Four other services confirmed same defect class; two actively split-brained at audit time.
**Tags:** [nssm, mcp-fleet, postmortem, path-resolution, critical]

---

## 1. What actually happened with memops

The `advanced-memory-mcp` Windows service is wrapped by NSSM and runs as `LocalSystem`.
Nothing in the service definition overrode the process environment.

The application resolves its storage like this:

```python
# config.py
base = os.getenv("ADVANCED_MEMORY_HOME") or Path.home()
db = base / ".advanced-memory" / "memory.db"
```

`Path.home()` on Windows resolves via `USERPROFILE`. For a `LocalSystem` service that is:

```
C:\WINDOWS\system32\config\systemprofile
```

So the service happily created and used:

```
C:\WINDOWS\system32\config\systemprofile\.advanced-memory\memory.db
```

Meanwhile the webapp backend (`uvicorn advanced_memory.server:app` on port 10705, launched from a
normal user shell by `advanced-memory-start.bat`) resolved `Path.home()` to `C:\Users\sandr` and used:

```
C:\Users\sandr\.advanced-memory\memory.db
```

Two processes, one codebase, two databases, zero errors.

### Why it stayed invisible for twelve days

This is the important part. Every layer reported success:

1. **The write succeeded.** `adn_notes` returned `{"success": true}` because the note genuinely was
   written. To the correct database, for that process. Write success and read visibility are
   different guarantees and the API conflated them.
2. **No error was ever raised.** Neither process knew the other existed. There was no lock
   contention, no schema mismatch, no permission denial. `LocalSystem` has more filesystem rights
   than the user, so nothing failed on the way down.
3. **`status` did not report the DB path.** The instance role, PID, and read-write mode were all
   shown and all correct. The single field that would have exposed the split was absent.
4. **Restarting Claude Desktop did not restart the service.** The NSSM service is independent of
   the MCP host. PID 4928 persisted across host restarts, so "I restarted it" was true and useless
   at the same time. This burned a lot of diagnostic time.
5. **Vault and DB were governed by different variables.** `ADVANCED_MEMORY_HOME` controlled the
   SQLite index; the markdown vault path was keyed off `Path.home()` directly. Setting only the
   first produced a state where the DB moved but the files did not, which read like a partial fix
   and generated a second round of confusion.

### The actual fix applied

```
nssm set advanced-memory-mcp AppEnvironmentExtra ADVANCED_MEMORY_HOME=C:\Users\sandr<newline>USERPROFILE=C:\Users\sandr
net stop advanced-memory-mcp
net start advanced-memory-mcp
```

Both variables are required. `ADVANCED_MEMORY_HOME` for the app-level config, `USERPROFILE` because
`Path.home()` reads it directly and is used in code paths the app-level variable does not cover.
Then 71 orphaned markdown files were copied from the systemprofile vault into the real vault and a
full `sync` reindexed them.

Also added: `DB location` and `ADVANCED_MEMORY_HOME` lines to the `adn_nav status` output, so this
failure mode is diagnosable in one call instead of an hour of process archaeology.

**Repo bug report (2026-07-27):** `advanced-memory-mcp/docs/troubleshooting/BUG_REPORT_NSSM_SPLIT_BRAIN.md` — user-facing symptoms, verification checklist, HTTP daemon mitigation.

---

## 2. The generalised defect

> An application resolves a storage path from ambient process state (`Path.home()`, `Path.cwd()`,
> `USERPROFILE`, `%APPDATA%`, a relative `env_file`) instead of from an explicitly configured
> absolute path. The service host supplies different ambient state than the developer's shell.
> The application silently uses a different location and reports success.

The severity comes from three properties combining:

- **Silent.** Divergence produces no error, only absence of expected data.
- **Bidirectional.** The service writes where you cannot see, and cannot see what you write.
- **Privileged.** `LocalSystem` can create the wrong directory without a permission error, and
  the resulting directory is not readable by the user without elevation, which obstructs diagnosis.

`Path.cwd()` is the same defect with a different variable. NSSM's `AppDirectory` masks it for the
service, so it appears to work until any other launch path (a Claude Desktop stdio instance, a
different shell, a scheduled task) uses a different working directory.

---

## 3. Fleet audit results

All eleven fleet services run as `LocalSystem`. Ten are NSSM-wrapped. So the precondition is
universal. What varies is whether the application resolves paths from ambient state.

| Service | State | Idiom | Verdict |
|---|---|---|---|
| advanced-memory-mcp | RUNNING | `Path.home()` | **FIXED 2026-07-26.** Was split. 71 notes recovered. |
| fleet-agent-mcp | RUNNING | `Path.home()/.fleet-agent`, `Path.home()/.fleet-intel` | **ACTIVE SPLIT.** See below. |
| devices-mcp | RUNNING | `Path.home()/.local/share/devices-mcp`, `Path.home()/.config/devices-mcp`, `Path.cwd()` | **LIKELY ORPHANED.** See below. |
| arxiv-mcp | RUNNING | `Path.cwd()`, empty `ARXIV_MCP_DATA_DIR` | **ALREADY SPLIT.** Two corpus DBs. See below. |
| tvtropes-mcp | RUNNING | `Path.cwd()/"data"` | At risk. Masked by `AppDirectory`. |
| mcp-pywinauto-mcp | STOPPED | `Path.home()/Documents`, `~/.config`, `~/.cua-mcp/missions`, `Path.cwd()` | Same defect, currently dormant. 31 hits. |
| aiwatcher-mcp | RUNNING | anchors `Path(__file__).resolve().parents[2]` | **CORRECT PATTERN.** Reference implementation. |
| aiwatcher-frontend | STOPPED | n/a | No storage. |
| mcp-federation-hub | RUNNING | `Path.home()` only to locate `nssm.exe` | Read-only lookup. Acceptable. |
| mcp-fleet-agent-mcp | STOPPED | duplicate of fleet-agent-mcp | Redundant service, candidate for removal. |
| FastSearchMCP | RUNNING | not NSSM (direct binary) | Out of scope for this audit. |

### fleet-agent-mcp: split happening right now

```
C:\Users\sandr\.fleet-intel    1248 files, newest 2026-07-26 10:32  <- written seconds ago
C:\Users\sandr\.fleet-agent      93 files, newest 2026-07-23 13:58
```

`.fleet-intel` was modified during this audit, so a **user-context** process is actively writing
there. The `fleet-agent-mcp` service is simultaneously RUNNING as `LocalSystem`, which means its
`Path.home()` resolves to systemprofile. Two instances, two stores, both live. This is the memops
situation before anyone noticed, and it covers `identity/soul.py` and `intel_hub/store.py`, i.e.
agent identity and accumulated intel.

### devices-mcp: stale under a running service

```
C:\Users\sandr\.local\share\devices-mcp    3 files, newest 2026-07-11 18:45
```

Two weeks stale while the service runs continuously. Either the service writes to systemprofile,
or it writes nothing. Both warrant investigation.

### arxiv-mcp: already split, different mechanism

`.env` contains `ARXIV_MCP_DATA_DIR=` with an **empty value**. Pydantic coerces `""` on a
`Path | None` field to `Path(".")`, which is not `None`, so the intended fallback never fires:

```python
def resolved_data_dir(self) -> Path:
    base = self.data_dir              # Path(".") because "" was coerced, not None
    if base is None:                  # never taken
        base = Path.cwd() / "data" / "arxiv_mcp"
    base.mkdir(parents=True, exist_ok=True)
    return base                       # returns ".", a RELATIVE path
```

Verified empirically:

```
data_dir field = WindowsPath('.')
resolved       = .
```

This is worse than the memops case. memops resolved to a wrong but stable absolute path. arxiv-mcp
resolves to a **relative** path, so the storage location follows the process working directory and
is not stable even within one process if anything calls `os.chdir()`.

The damage is already on disk:

```
D:\Dev\repos\arxiv-mcp\data\arxiv_mcp\corpus.sqlite3   1.6 MB   2026-06-02   <- orphaned
D:\Dev\repos\arxiv-mcp\corpus.sqlite3                  4.3 MB   2026-07-04   <- current
```

The corpus silently forked when the empty variable was introduced. Additionally `codehunt/`,
`lancedb/`, `http_cache/`, and `markdown/` are all splattered into the repo root rather than a
data directory, because `.` is the data directory.

---

## 4. Remediation

### Immediate, per service

For every NSSM service whose app uses `Path.home()`, pin both variables:

```
nssm set <service> AppEnvironmentExtra <APP>_HOME=C:\Users\sandr<newline>USERPROFILE=C:\Users\sandr
net stop <service>
net start <service>
```

Setting only the app-specific variable is insufficient whenever `Path.home()` appears anywhere in
the codebase. That was the second round of the memops fix and it is the easiest step to get wrong.

Priority order:

1. **fleet-agent-mcp.** Active split, touches identity and intel. Audit systemprofile for orphans
   before pinning, then merge.
2. **arxiv-mcp.** Set `ARXIV_MCP_DATA_DIR` to a real absolute path. Never leave it empty. Decide
   which of the two `corpus.sqlite3` files is authoritative and merge or archive the other.
3. **devices-mcp.** Determine whether it writes to systemprofile; recover if so.
4. **tvtropes-mcp, mcp-pywinauto-mcp.** Pin before next start.

### Code-level, the actual fix

Ambient path resolution should not appear in a server that can run as a service. Replace with
explicit config, anchored to the module when a default is needed. aiwatcher-mcp already does this:

```python
repo_root = Path(__file__).resolve().parents[2]
```

`Path(__file__)` is stable regardless of user, working directory, or launch mechanism. Prefer it
over `Path.home()` and `Path.cwd()` for anything a service writes.

Additional rules worth adopting fleet-wide:

- Treat empty-string env vars as unset. Add validators that coerce `""` to `None` on optional
  `Path` fields, or the arxiv-mcp failure repeats wherever a `.env` has a bare `KEY=`.
- Resolve storage paths to absolute at startup and **log the resolved path once at INFO**. A single
  startup line stating where the data lives would have collapsed this entire investigation into
  one glance.
- Expose the resolved storage path in whatever `status` or `health` tool the server has. Done for
  memops; should be a fleet standard.
- Never return bare `success: true` from a write when the write's visibility depends on a separate
  indexing or sync step. Report the target path, or report index status alongside.
- Reconsider whether these services need `LocalSystem` at all. Most need no privileges beyond the
  user's. Running as the user removes this entire failure class by construction. The tradeoff is
  that a service account needs a stored password, which was declined here, so environment pinning
  is the pragmatic alternative.

### Diagnostic checklist for "my data disappeared"

1. `sc qc <service>` and check `SERVICE_START_NAME`. `LocalSystem` is a red flag.
2. `reg query HKLM\SYSTEM\CurrentControlSet\Services\<svc>\Parameters /v AppEnvironmentExtra`.
3. `netstat -ano | findstr :<port>` then `Get-CimInstance Win32_Process -Filter "ProcessId=<pid>"`.
   Confirm which binary and which account actually holds the port. Do not assume.
4. Compare the PID before and after a restart. If unchanged, the thing you restarted was not the
   thing you meant to restart.
5. Check for the same data directory under both `C:\Users\<user>\` and
   `C:\WINDOWS\system32\config\systemprofile\`. Reading the latter requires elevation.

---

## 5. Cost

Roughly four hours of diagnosis for memops, most of it spent on false leads that each looked
plausible: a genuine `NavSyncOp` model bug that was real but unrelated, a `watch_task` status
endpoint that reports `false` by design and was therefore misread as a crashed watcher, and several
restarts of the wrong process. None of that was necessary. A single startup log line naming the
resolved database path would have made it a two minute fix.

Twelve days of notes were recovered in full. Nothing was lost, which was luck rather than design:
had the systemprofile database been cleared by any cleanup tooling, it would have been gone with no
trace and no error.
