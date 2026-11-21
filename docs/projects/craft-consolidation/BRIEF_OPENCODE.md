# Brief: opencode (round 2, from 2026-11-19)

Read first: `standards/CRAFT_FLEET_RULES.md`, then `projects/CRAFT_CONSOLIDATION_PLAN_2026-11.md`
(sections 1, 3, 6), then session-log entries `craft-*` from 2026-11-17 onwards.

Your previous session was lost to an update on 2026-11-17; Claude Code and agy covered your
Phase 0 and 1 work. Work in **small resumable chunks**: after each repo, tick the plan,
append to your session-log file and commit. If you get cut off, the next session must be
able to resume from the files alone.

Log file for this round: `operations/session-log/craft-opencode-<date>.md` (one per day).

## Tasks, in order

### O1. Commit the mcp-central-docs backlog (first, half an hour)
- Commit only craft-related files, in batches of max 10: the plan, `operations/craft-scorecard.*`,
  the untracked `craft-*` session logs, `standards/CRAFT_FLEET_RULES.md`,
  `projects/craft-consolidation/*`, `.cursor/rules/craft-fleet.mdc`.
- Do NOT stage the unrelated dirty files (zed integration deletions, aiwatcher log deletions,
  ecosystem README edits). List them in your log for Sandra instead.

### O2. WIP ref audit (investigation only, no deletion)
- For every active craft repo: `git ls-remote origin "refs/wip/*"`. For each remote WIP ref,
  find blobs > 5 MB (`git rev-list --objects <ref>` + `git cat-file --batch-check`).
- Find the script that creates and pushes `refs/wip/goliath/*` (search mcp-central-docs
  scripts and fleet-gate for `refs/wip`). Report whether it respects `.gitignore`.
- Output: table repo / ref / largest blobs / total MB into the log. Propose (do not run) the
  deletion commands and the snapshot-script fix. Sandra decides.

### O3. .gitignore baseline rollout (L-F)
- In every active craft, ensure `.gitignore` covers the list in CRAFT_FLEET_RULES section 3.
  One commit per repo, push. Skip archived repos. Skip forks (`photocraft`, `cadcraft`, etc.).

### O4. D5: pre-release marking
- From `operations/craft-scorecard.json`, list every repo with a non-prerelease GitHub
  release whose tier floor is not met (plan section 5 and 6).
- `gh release edit <tag> --prerelease` for each. Not a deletion, allowed.
- Log the list with test counts.

### O5. CI rollout (L-F)
- Create a reusable workflow `craft-biz/.github/workflows/rust-ci.yml`
  (`workflow_call`): `cargo fmt --check`, `cargo clippy --workspace --all-targets -- -D warnings`,
  `cargo test --workspace`, on `windows-latest`, with cargo cache.
- In each active craft add `.github/workflows/ci.yml` that calls it. Start with 3 repos
  (shopcraft, aicraft, buchcraft), wait for green, then roll out in batches of 10.
- A red CI is a finding, not something to silence. Log it; do not weaken clippy.

### O6. Back-office test top-up (Phase 4)
- billcraft, spendcraft, hirecraft, formcraft, wikicraft, assetcraft to >= 20 tests each;
  craft-biz to >= 50. Domain tests (Austrian rules, SEPA, AfA, deadlines), not getters.
- Run `cargo test --workspace` before and after; log both numbers.

### O7. AGENTS.md lines in every active craft
- Ensure each craft's `AGENTS.md` contains a "Repo rules" section with: LF only, single
  trunk, no build output in git, pointer to `mcp-central-docs/standards/CRAFT_FLEET_RULES.md`.
  Create `AGENTS.md` if missing. Batch of 10 repos per commit round.

## Not yours
Shop or AI merges, stub removal in speechcraft/homecraft/sportscraft/helmcraft/taskcraft,
README honesty audit, any deletion.
