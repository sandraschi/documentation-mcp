# Prime Agent - Safety Review

Created: 2026-08-27

## The core risk stack

Four features compound. Each alone is manageable; together they remove the human chokepoint:

1. Direct agent-to-agent communication, not routed through the user
2. Bounded but real autonomous mode (`/autonomous`), continues within budgets and can run user-defined quality gates
3. Daemon-backed sessions that survive terminal disconnect, plus heartbeats/schedules that re-enter a session on their own
4. Vendor's own admission: worker/kernel process isolation improves lifecycle recovery, it is explicitly NOT a security sandbox

Combined: a plan can form between subagents, get executed under a time/token budget, on a schedule, in a session that outlives the terminal, with no synchronous point where a human sees the plan before action. Materially different risk profile from a plain single-agent CLI session.

## Specific gaps to check before any real use

- What exactly a "passed quality gate" verifies. Vendor docs are explicit: a passed gate checks only what that gate verifies, reaching a limit does not imply task success. Do not treat gate-pass as a safety signal, at best a completion signal.
- Whether the Agents View surfaces inter-agent messages in real time or only on inspection after the fact. If pull-based, that is not equivalent to a synchronous approval gate.
- Whether `/refine`'s supplemental-state changes are shown as a diff before applying, or applied then logged. Rollback existing is good; rollback being the only recourse is not.
- Credential and filesystem exposure inside whatever environment it runs in. No API keys, SSH keys, or write-capable git remotes reachable.

## Comparison to fleet design philosophy

admiral-mcp exists specifically to put a human approval gate in front of fleet job execution from a phone. Prime Agent's lateral-comms design is the opposite bet, optimizing for removing that gate for throughput. Not automatically wrong, but Prime Agent should never be wired into anything that also touches fleet job execution without an explicit, separate decision, not an assumed one just because both are "agent tooling."

## Mitigations if trialing anyway

- Isolated WSL2 distro or VM per [PLAN.md](PLAN.md) stage 0, not the main dev environment
- API-key auth only, not a full account subscription, caps both cost and scope
- Throwaway repo, no push remote, no real credentials reachable
- Watch the Agents View live during the first several multi-subagent runs rather than reviewing after
- Treat any `/autonomous` run as unsupervised only up to its budget limits, not as "safe because bounded"

## Verdict

No install against real repos or credentials until stages 0-2 of PLAN.md are done in isolation and the Agents View behavior is confirmed to give real visibility into agent-to-agent messages, not just after-the-fact logs.
