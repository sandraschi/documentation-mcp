# FileCraft — Assessment

**Repo:** `D:\Dev\repos\filecraft` · **Date:** 2026-11-05 · **Grade: C**

## What it is

Filesystem, volume analytics, disk-usage, and integrity workstation.
Rebuild-PLAN Wave-1 #5 (from `filesystem-mcp` + `disk-usage-mcp` + file verbs
of `system-admin-mcp`). Highest-reuse craft: others call it in `do_with`.

## Model / verbs

- **Model:** file/dir/volume.
- **Verbs (README):** `list hash grep du find-large strings` family.
- **Surface:** `cli.py` + `mcp_server.py`, `justfile`, `AGENTS.md`. 2 test files.

## Architecture

Python FastMCP, `.venv`, `pyproject`. Scaffold committed 2026-11-04.

## Strengths

- Smallest, most composable model — every other craft's fixture/artifact story
  depends on exactly these verbs.
- Integrity verbs (hash/dupe-find) are the fleet's cheapest correctness win.

## Gaps / risks

- Path traversal is THE risk: `--automation-read-root` enforcement must be tested,
  and recipes must never touch `C:\Windows` (fixtures under `D:\Dev\repos` only).
- `strings`/`grep` on binaries can be slow — needs timeouts + `down` discipline.
- Exif/photo-file verbs belong here only if photocraft stays deferred; say so in writing.

## Next 3 steps

1. Confinement tests (traversal attempts → refusal, proven, not asserted).
2. 3 recipes: `file/hash-grep`, `file/du-top10`, `file/find-dups` (fixtures only).
3. Write the photocraft-deferred note if filecraft carries exif verbs meanwhile.

## Verdict

Grade C: the utility infielder every lineup needs. Confinement proofs + three
fixture recipes promote it fastest of the Python six.
