# Fleet MCP Observability: stdio interceptor lane (proposal)

**Date:** 2026-10-18 · **Source:** Gemini ArtCraft docs (Drive, 2026-10-18) + `rust-arr-mcp` Phase 2 review
**Status:** proposal — no code, no new repo, decision required before building

## Idea in one paragraph

A fleet-level `LinesCodec` JSON-RPC proxy that sits between the MCP host's stdio
and a child MCP binary's piped stdio, metering every `tools/call` (payload log,
round-trip latency, error capture) with all diagnostics on stderr so the
JSON-RPC stream stays pure. Transparent to Claude Desktop / Cursor / Antigravity /
OpenCode; gives per-tool latency + failure telemetry no single repo can produce alone.

## Where it belongs (and where it does NOT)

- **Belongs:** fleet observability lane — a `fleet-mcp-proxy` supervisor binary
  (or the weekly hygiene job) metering *third-party/opaque* binaries, plus the
  `id_to_key` lesson (request IDs are num-or-string; every `run_mcp_stdio` must
  accept both from day one — adopted into `rust-arr-mcp` Phase 3 requirements).
- **Does NOT belong:** inside any `rust-*-mcp` repo. Our L2/L3 dispatch in-process
  (zero-hop containment standard); wrapping our own CLI as a child process would
  violate the same Gemini doc that proposes the interceptor (native binary over
  stdio, never CLI-subprocess wrappers) and add a hop, a failure mode, and latency
  to every call for zero functional gain.

## Adopted into `rust-arr-mcp` from the same docs (no new deps)

- Handshake-test script pattern (`initialize` → expect `result`) — Phase 3 probe.
- `cargo machete` + `cargo audit` justfile recipes — hygiene lane.
- `--compact` tool-list trimming — dual-alias design note for Phase 3.
- Rejected: `artcraft-bridge` subprocess supervisor, edition-2024/`anyhow` stack,
  `tokio = "full"`, `tracing` in L1 (typed errors + `eprintln!` purity stand).

## Decision needed

1. Build `fleet-mcp-proxy` as its own repo (ArtCraft 6-gate, Bucket A), or as a
   mode of an existing supervisor (which one)?
2. Sink for telemetry: weekly hygiene report (`file,aiwatcher`) first, live
   dashboard later?
3. Scope: all fleet binaries, or opaque/third-party ones only?
