# MCP Git/GitHub Tool Consolidation Plan

**Created:** 2026-04-06  
**Status:** ACTIVE — pending execution  
**Author:** Sandra / Claude  

---

## Problem

The fleet currently has three overlapping git implementations active in Claude Desktop simultaneously:

| Server | Git tools | GitHub tools | Notes |
|---|---|---|---|
| `gitops` (`git-github-mcp`) | `git_ops` (43 actions) | `github_ops` (58 actions) | **Canonical. Keep.** |
| `fileops` (`filesystem-mcp`) | `repo_ops` (14 ops) + 16 standalone tools | none | Redundant. Broken subset. |
| `winops` (`windows-operations-mcp`) | `git_operations_async` (~30 actions) | none | Redundant. No unique value. |

### Why this is a problem

- **~30 extra tools in CodeMode BM25 budget** for every session — git tools from fileops/winops compete with gitops and confuse tool selection
- **Parameter naming is inconsistent**: `fileops:repo_ops` uses `add_all`/`paths`; `gitops:git_ops` uses `all_files`/`files` — agents pick the wrong one mid-workflow
- **fileops git tools are a broken subset**: `repo_ops` has 14 ops vs gitops's 43. Missing: stash_drop, clean, submodules, bisect, worktrees. Agents fall through to other tools mid-workflow
- **No GitHub capability in fileops/winops**: Any GitHub task already requires gitops, so a pure-git-only tool adds nothing
- **`fileops` standalone git tools** (git_merge_branch, git_rebase_branch, git_rename_branch, git_list_stashes, git_apply_stash, git_push_changes, etc.) are individually weaker than the equivalent gitops operation and exist as fragments of what repo_ops already partly does

### One operation that fileops has that gitops may lack

`fileops:git_rename_branch` (standalone) — `gitops:git_ops` doesn't list `branch_rename` explicitly in its 43 actions. Needs verification before fileops git tools are removed. If missing, add to gitops first.

---

## Canonical tool routing (post-consolidation)

| Task | Use |
|---|---|
| Any local git operation | `gitops:git_ops` |
| Any GitHub operation | `gitops:github_ops` |
| Natural language multi-step git/GitHub | `gitops:git_agentic_workflow` |
| GitHub repo/org discovery | `gitops:git_github_search_workflow` |
| Check git/gh availability | `gitops:git_github_status` |

**Rule for AGENT_PROTOCOLS.md**: Never use `fileops` or `winops` for git operations. Always use `gitops:git_ops` and `gitops:github_ops`.

---

## Execution plan

### Phase 1 — Verify gitops coverage (before cutting anything)

Check `gitops:git_ops` for `branch_rename`. If missing:
- Add it to `git-github-mcp/server.py` under the branch operations section
- Test, commit, push

### Phase 2 — fileops: remove git tools

Repo: `D:\Dev\repos\filesystem-mcp`

Remove or stub the following tools with a docstring redirect ("Use gitops:git_ops instead"):

**Portmanteau to gut:**
- `repo_ops` — all 14 operations (init_repo, clone_repo, get_repo_status, commit_changes, read_repo, get_repo_info, get_commit_history, show_commit, diff_changes, blame_file, get_file_history, revert_commit, reset_to_commit, cherry_pick)

**Standalone tools to delete:**
- `git_merge_branch`
- `git_rebase_branch`
- `git_rename_branch`
- `git_list_stashes`
- `git_apply_stash`
- `git_push_changes`
- `git_create_branch`
- `git_switch_branch`
- `git_delete_branch`
- `git_fetch_updates`
- `git_pull_changes`
- `git_list_branches`
- `git_list_remotes`
- `git_add_remote`
- `git_remove_remote`
- `git_create_tag`
- `git_list_tags`
- `git_delete_tag`
- `git_stash_changes`
- `git_resolve_conflicts`

**Keep everything non-git:**
- `file_ops`, `file_ops_safe`, `dir_ops`, `search_ops`, `agentic_file_workflow`, `test_concurrency_safety`

### Phase 3 — winops: remove git_operations_async

Repo: `D:\Dev\repos\windows-operations-mcp`

- Delete `git_operations_async` tool entirely
- Keep: `file_operations`, `directory_operations`, `command_execution`, `archive_management`, `json_operations`, `process_management`, `system_management`, `windows_services`, `agentic_operations`

### Phase 4 — Update AGENT_PROTOCOLS.md

Add to the Tool Use section:

```
## Git/GitHub Tool Routing

**ALWAYS use gitops (git-github-mcp) for all git and GitHub operations.**

- Local git: `gitops:git_ops` (43 actions)
- GitHub API/CLI: `gitops:github_ops` (58 actions)
- Agentic multi-step: `gitops:git_agentic_workflow`
- Discovery: `gitops:git_github_search_workflow`

**NEVER use fileops or winops for git operations.** These servers no longer
expose git tools as of the 2026-04-06 consolidation. If you see git tools
in fileops/winops, the servers need to be restarted after the code change.
```

### Phase 5 — Restart Claude Desktop

After Phases 2–4 are committed and pushed, restart Claude Desktop so the new tool registrations take effect. Verify with `gitops:git_github_status`.

---

## Risk assessment

| Risk | Mitigation |
|---|---|
| Antigravity or Windsurf sessions using fileops git tools break | Low risk — both IDEs use gitops preferentially; fileops git tools were never reliable enough to depend on |
| branch_rename missing from gitops | Check in Phase 1, add if missing before cutting fileops |
| Forgetting to restart Claude Desktop | Add to checklist |

---

## Estimated effort

- Phase 1: 15 min (read gitops source, add branch_rename if needed)  
- Phase 2: 30 min (fileops: delete/stub git tools, test remaining tools still import)  
- Phase 3: 10 min (winops: delete git_operations_async)  
- Phase 4: 10 min (AGENT_PROTOCOLS.md edit)  
- Phase 5: 2 min (restart)  

**Total: ~1 hour**

---

## Status tracking

- [x] Phase 1: Verify gitops branch_rename coverage — **ADDED** (`git_ops.py`, 44 actions, `branch='old', source_branch='new'`)
- [x] Phase 2: fileops git tools removed — `portmanteau_git_mgmt.py` and `portmanteau_repository.py` replaced with redirect stubs (2026-04-06)
- [x] Phase 3: winops git_operations_async removed — `tools/portmanteau/git_operations.py` replaced with no-op stub (2026-04-06)
- [x] Phase 4: AGENT_PROTOCOLS.md updated — git routing table added
- [ ] Phase 5: Commit all three repos + restart Claude Desktop ← **MANUAL STEP REQUIRED**

## Manual commits needed

MCP servers were timing out during Phase 5. Run these in a terminal:

```powershell
$git = "C:\Program Files\Git\cmd\git.exe"

cd D:\Dev\repos\git-github-mcp
& $git add -A
& $git commit -m "feat(git_ops): add branch_rename, 44 actions total"
& $git push

cd D:\Dev\repos\filesystem-mcp
& $git add -A
& $git commit -m "chore: remove git tools, consolidated into git-github-mcp (2026-04-06)"
& $git push

cd D:\Dev\repos\windows-operations-mcp
& $git add -A
& $git commit -m "chore: remove git_operations_async, consolidated into git-github-mcp (2026-04-06)"
& $git push
```

Then restart Claude Desktop to drop the old tool registrations from CodeMode.
