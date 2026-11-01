# Prime Agent

Created: 2026-08-27

Prime Agent (Prime Intellect). Open source (MIT), TUI coding/research agent CLI. Not a library, not an MCP server. Standalone terminal agent, same slot as opencode, Claude Code, Cursor CLI.

- Paper: arXiv:2608.23552, "Prime Agent: A Self-Improving RLM Harness", submitted 24 Aug 2026. Ingested to arxiv-mcp depot at `data/arxiv_mcp/markdown/2608.23552v1.md`.
- Repo: https://github.com/PrimeIntellect-ai/prime-agent (18.1k stars, 4561 commits, MIT, active CI)
- Install: `curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh` (macOS/Linux only, so WSL2 on Goliath)
- Built on top of `pi` (earendil-works/pi)

## Core mechanisms

- **RLM (Recursive Language Model)**: context treated as variables in a persistent IPython REPL, subagent calls as function calls (`rlm(...)` spawns child agents programmatically)
- **Continual Harness**: durable supplemental prompts, memories, skill descriptions, subagent specs, refined via `/refine` with recorded history and rollback. Never touches the immutable base system prompt.
- **Direct agent-to-agent communication**: running agents discover each other, exchange messages, steer active work laterally, not routed through the user for every exchange
- **Daemon-backed sessions**: detach/reattach, heartbeats, schedules, persistent goals, bounded autonomous mode with user-defined quality gates

## Explicit vendor warning

Readme states worker/kernel isolation improves lifecycle recovery but is explicitly NOT a security sandbox. Vendor's own guidance: use trusted repos/instructions only, run untrusted code in an external sandbox.

## Relevance to the fleet

- **opencode-cli-mcp**: direct competitor CLI in the same slot as the local-4090-backed opencode effort, natural benchmark target
- **nekomimi-mcp / fritz-coworker**: lateral agent-to-agent messaging is a working reference implementation of chaining multiple fleet MCP servers without a hub-and-spoke pattern
- **mcp-fleet meta-tooling / basic-memory**: Continual Harness `/refine` + rollback is a more formalized version of ad hoc memory-note updates

See also: [PLAN.md](PLAN.md), [ASSESSMENT.md](ASSESSMENT.md), [SAFETY_REVIEW.md](SAFETY_REVIEW.md)
