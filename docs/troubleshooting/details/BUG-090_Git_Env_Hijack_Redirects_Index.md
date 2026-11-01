# BUG-090 — Inherited `GIT_DIR` / `GIT_INDEX_FILE` silently redirects git to the wrong repo

- **Severity**: `P1` (major feature failure: `git add`/`commit` broken fleet-wide for affected servers; silent success)
- **Date**: 2026-10-25
- **Found in**: `git-github-mcp` (`git_ops add` → `commit`, issue #3); fleet audit below
- **Status**: Fixed in git-github-mcp (`3fa8d66` + follow-up hardening); other repos reported, not fixed

## Symptom

`git_core(operation='add', files=[5 tracked modified files])` returns
`{success: true, staged_files: [...5 files...], count: 5}` — then `commit`
fails with "no changes added to commit", and ground-truth
`git status --short` / `git diff --cached --name-only` in the target repo show
an empty index. Raw `git add -- <paths>` via shell stages correctly on the
first try. Deterministic, twice in a row.

## Root cause

The MCP server process inherited `GIT_DIR` (or `GIT_INDEX_FILE`) from its
launcher environment (NSSM service env / Claude Desktop `env` block /
`opencode.json` environment / spawning shell). Both git helpers built the
child env with a bare `os.environ.copy()` and passed no `--git-dir`:

- with `GIT_DIR=<S>/.git` alone (work tree defaults to cwd), `git add`
  **exits 0** and stages the files into **S's index** — the wrong repo;
- with `GIT_INDEX_FILE=<alt>` alone, `git add` exits 0 and writes an
  alternate index file nobody reads.

Either way the tool echoed its *input list* as `staged_files` without ever
reading the index back — a silent lie — and the real index stayed empty, so
the follow-up `commit` correctly reported nothing to commit. Reproduced
bit-for-bit with two scratch repos (target R + bystander S): tool
`success:true` + empty ground-truth index in both variants.
(`GIT_DIR`+`GIT_WORK_TREE` together fail loudly on pathspec instead —
same family, less silent.)

Precedence refresher: `git -C <path>` does **not** beat `GIT_DIR`; only
`--git-dir` on the command line outranks the env var, and **nothing** on the
command line overrides `GIT_INDEX_FILE`. Scrubbing the env is the only
robust fix — flags alone cannot cover it.

## Resolution (git-github-mcp)

1. `_git_env()` (`tools/git_ops.py`) and `_no_prompt_env()`
   (`utils/gh_cli.py` — gh shells out to git for repo resolution) now drop
   `GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE, GIT_COMMON_DIR, GIT_PREFIX,
   GIT_NAMESPACE, GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES,
   GIT_CEILING_DIRECTORIES` + `GIT_CONFIG_*` overrides.
   `GIT_AUTHOR_*/GIT_COMMITTER_*` are kept (commit identity relies on them).
2. `add` uses `--`, then re-reads the index (`git diff --name-only` +
   `git diff --cached --name-only` scoped to the requested paths), reports
   **actually-staged** files with a truthful count, fails LOUDLY naming
   still-dirty paths, and says "already clean" instead of echoing when
   there was nothing to do. Same for `all_files`.
3. Follow-up: `_preflight_repo()` runs `git rev-parse --absolute-git-dir`
   and refuses `add`/`commit`/`push`/`tag_push` when git resolves a different
   repo than `repo_path` names (catches stale copies/symlinks too, not just
   env hijacks). Runs AFTER argument validation so arg errors keep priority.
4. Server lifespan logs a warning when hijack vars are inherited, so the
   next occurrence is a log line instead of a mystery.
5. Regression tests: hijack e2e (fails on pre-fix code), mocked silent-success,
   already-clean, missing-file, env-scrub x2, foreign-git-dir refusal.

## Fleet audit 2026-10-25 (read-only)

`rg -l 'os.environ.copy()|env=os.environ' --glob '*.py'` intersected with
git/gh invokers, `_upstream/ _archives/ external/ node_modules/ .venv/
target/ mcpb/ web/dist` excluded. 18 files; FreeCAD-vendored pandas excluded
as third-party. Triage:

**Confirmed same pattern (copied env straight into a git/gh child):**

| File | Child | Exposure |
| :--- | :--- | :--- |
| `arxiv-mcp/src/arxiv_mcp/utils/gh_cli.py` | `gh` via `run_gh` | latent (explicit `--repo` wins today; one hijacked `gh` call away from wrong-repo) |
| `grandorgue-mcp/.../utils/gh_cli.py` | same | same |
| `japanophile-mcp/.../utils/gh_cli.py` | same | same |
| `inkscape-mcp/.../utils/gh_cli.py` | same | same |
| `ocr-mcp/.../utils/gh_cli.py` | same | same |
| `qcad-mcp/.../utils/gh_cli.py` | same | same |
| `resonite-mcp/.../utils/gh_cli.py` | same | same |
| `winrar-mcp/.../utils/gh_cli.py` | same | same |
| `mcp-central-docs/templates/apps-page/backend/utils/gh_cli.py` | `gh` via `run_gh` | **contagion vector — every scaffold from this template inherits it** |
| `comfyops-mcp/src/comfyops_mcp/manager_install.py:85` | bare `"git"` with NO env at all (inherits server env raw) | direct: clone/install retargetable |
| `mcp-central-docs/scripts/align_ruff_pyproject.py:86` | `git checkout HEAD -- pyproject.toml` via `run_cmd` | direct: operator-run fleet script would overwrite the WRONG repo's pyproject |
| `mcp-studio/scripts/studio_dashboard.py:2271` | `git rev-parse`/`git status` via `check_output` without env | direct read-only: wrong-repo status shown (plus env.copy at :1705/:2590 passed into spawned MCP children — transitive) |

**Checked, not affected:** `kyutai-mcp/webapp/backend/app.py:326`
(env.copy feeds the moshi inference server, which never invokes git);
`git-github-mcp/smoke_status.py` (read-only `--version` diagnostics);
`comfyops-mcp manager_install.py:214` feeds `cm-cli` (transitive only —
flagged because cm-cli shells out to git for installs).

**Fix recipe for each** (repo-by-repo, not a blind sweep): copy the
`_GIT_DISCOVERY_HIJACK_VARS` scrub from git-github-mcp
`tools/git_ops.py::_git_env` into the env builder, or set `env=` explicitly
where none is passed. Template first, so new scaffolds stop inheriting it.

## Adjacent vector (noted, not hit)

`GH_REPO` env var retargets `gh` repo resolution the same way `GIT_DIR`
retargets git. Our `github_ops` always passes explicit `--repo` (wins over
env), but any wrapper that relies on cwd discovery is exposed. Worth one
line in the same scrub wherever `gh` is shelled out without `-R`.
