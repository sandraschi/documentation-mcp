# CoderCraft — Assessment

**Repo:** `D:\Dev\repos\codercraft` · **Date:** 2026-11-05 · **Grade: C+**

## What it is

Local-first agentic IDE + universal MCP server — subsuming Claude Desktop,
OpenCode, Cursor, Zed, Antigravity into one zero-tax native binary
(`egui` + `wgpu`, sub-ms rendering, <30 ms startup, ~35 MB RAM).
Port `14128`. Most ambitious claim in the fleet.

## Model / verbs

- **Model:** workspace + agent session + tool gate (compiler gatekeeper).
- **Crates:** `codercraft-core`, `codercraft-agent`, `codercraft-mcp`, `codercraft-app`.
- Agent/core split is right (cognition vs plumbing); Timmy/Linus dual UX per matrix.
- `PRD.md` + `SPEC.md` + `HELP.md` + `AGENTS.md` present at root.

## Architecture

Rust ArtCraft 3-tier, MIT, Tokio. `start.ps1`/`start.bat` present. No `docs/`
folder (specs at root), no `justfile`, no test evidence at triage. Last commit
2026-11-04 (fleet i18n).

## Strengths

- Specified like moneycraft (PRD/SPEC/HELP) — above its generation's bar.
- Agent-crate seam plus compiler-gatekeeper concept shows real IDE thinking.
- Performance targets are concrete and falsifiable (<30 ms, ~35 MB).

## Gaps / risks

- Boldest claim + thinnest proof: an IDE competes with five mature products;
  nothing at triage evidences editing, LSP/tree-sitter, or agent-loop depth.
- Scope is the risk: IDE + universal MCP server + dual UX + AST + gatekeeper.
  Ship the editor first, agent second, "universal server" last or never.
- No `docs/`, no headless tests (open fixture → edit → artifact is the hello world).
- Must not become a second opencode-wrapper; state the native-editor difference in writing.

## Next 3 steps

1. Ruthless scope cut in `docs/PRD.md`: editor milestone 1, agent milestone 2.
2. Headless tests (fixture file → programmatic edit → byte-identical artifact).
3. One democraft recipe: `coder/edit-roundtrip` (no LLM in CI — deterministic edit only).

## Verdict

Biggest vision, least proof per claim. C+ for the specs; the next grade requires
a headless edit roundtrip, not more architecture prose.
