# SplatCraft — Assessment

**Repo:** `D:\Dev\repos\splatcraft` · **Date:** 2026-11-05 · **Grade: B-**

## What it is

3D Gaussian-splat + radiance-field CLI + MCP server. Unifies cloud generation
(World Labs Marble API) and zero-cost local RTX 4090 training
(Nerfstudio/Splatfacto/Postshot) behind one headless CLI + stdio MCP.
Rebuild-PLAN Wave-2 #11 (`albumcraft-DOSSIER.md` sibling context).

## Model / verbs

- **Model:** capture set (video/images) → splat world + contact-sheet artifacts.
- **Surface (richest Python craft):** `cli/cloud/engines/io/models/recipes/server/train`
  — 9 modules including `recipes.py` (democraft-facing) and `train.py`.
  10 test files — most-tested Python craft by far. `fleet-start.config.ps1` present.

## Architecture

Python FastMCP, `uv.lock`, `justfile`, `AGENTS.md`, `outbox/` present.
Scaffold lineage older than the Nov-4 six (launcher fix 2026-11-04:
UTF-8 encoding, PATH discovery, anti-flash-close menu).

## Strengths

- Only Python craft with real depth: cloud + local engine matrix, train path,
  recipes module, 10 test files.
- Cost-honesty (Marble $$ vs local $0) is the correct framing for a GPU fleet.
- `outbox/` + launcher care shows user-facing mileage.

## Gaps / risks

- GPU-train in CI is impossible; sim/fixture discipline (like benchcraft's
  sim-first) must be explicit or CI is red-or-mocked.
- World Labs API key handling (redaction, never in `run.json`) needs the same
  proof databasecraft owes for DB URLs.
- Boundary with VRCraft/metaverse ambitions (splatmaker-mcp lineage) unwritten.
- Rebuild PLAN folds related 3D work into meshcraft/albumcraft waves — splatcraft's
  survival as its own craft vs merge needs one paragraph.

## Next 3 steps

1. Sim/fixture-train discipline: fixture captures → artifact without GPU, `sim` receipts.
2. Key-redaction test for the Marble path.
3. 3 democraft recipes (fixture-only default; live paths token-gated, never in default CI).

## Verdict

B-: the deepest Python craft and the only one with double-digit test files.
Fixture-discipline + key redaction promote it toward the A/B tier's honesty bar.
