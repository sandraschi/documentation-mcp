# Prime Agent - Integration Plan

Created: 2026-08-27

Goal: evaluate Prime Agent as a possible alternative/complement to opencode-cli-mcp's local-4090 effort, without touching production repos or real remotes until the safety review's mitigations are in place.

## Stage 0: isolation setup (before any install)

- Provision a disposable WSL2 distro or a dedicated VM, not the main Goliath WSL2 instance used for other work
- No mounted access to D:\Dev\repos with write credentials; use a throwaway clone with no push remote, or a git worktree pointed at a scratch branch with origin removed
- Confirm no API keys, SSH keys, or stored credentials are reachable from that environment

## Stage 1: install and first run

- Run the installer script inside the isolated environment only
- Verify SHA-256 checksum matches what the installer reports
- `/login`, pick a provider (API key route, not a full subscription, to cap blast radius and cost)
- Run against a trivial throwaway repo first, not a real project

## Stage 2: harness and subagent behavior

- Deliberately trigger a multi-subagent task and watch the Agents View to see what agents actually say to each other
- Test `/refine` once and inspect what it wrote to supplemental harness state, confirm rollback works
- Test `/autonomous` with a tight turn/token/time budget and a real quality gate, not the default

## Stage 3: benchmark vs opencode-cli-mcp

- Same task, same local 4090 model backend, run through opencode and through Prime Agent
- Compare: wall clock, token spend, quality of output, whether subagent orchestration actually beat a flat single-agent run for the task type
- Record results in this doc's changelog; keep raw transcripts if feasible

## Stage 4: decision point

- Only after stage 3, decide whether it's worth pointing at anything in D:\Dev\repos for real, and only with the mitigations in [SAFETY_REVIEW.md](SAFETY_REVIEW.md) applied
- No go: if lateral agent comms in stage 2 produced anything that would have executed without a visible chokepoint
