# CoderCraft — Assessment

**Repo:** `D:\Dev\repos\codercraft` · **Date:** 2026-11-09 · **Grade: B** · **Origin:** fleet-owned

## What it is

Local-first agentic IDE, autonomous P0/P1 coding loop, and universal MCP server in pure Rust (`egui` + `wgpu`, port `14128`, `2,616 LOC`, `14 tests`, 4 crates + `craft-ai-core`).

## Model / verbs

- **Model:** workspace + FTS5 persistent session store + unified-diff patch engine + permission gate + autonomous P0/P1 compiler-verified runner.
- **Crates (`2,616 LOC`, `14 tests`):**
  - `codercraft-core`: P0/P1 autonomous runner (`autonomy.rs`), SQLite + FTS5 session/message persistence (`session.rs`), unified-diff patch engine (`patch.rs`), command permission gate (`permission.rs`), tool registry (`tools.rs`), and shared `craft-ai-core` multi-provider LLM client.
  - `codercraft-agent`: agent loop and prompt orchestration.
  - `codercraft-mcp`: stdio MCP server exposing workspace, patch, session, permission, and autonomy verbs.
  - `codercraft-app`: native `eframe`/`egui` workbench with LLM provider settings modal (`Ollama`, `LM Studio`, `OpenAI`, `Anthropic`, `Google`), chat/session history, diff preview, and permission controls.

## Architecture

4-crate Pure-Rust ArtCraft workspace wired to `../craft-ai/crates/craft-ai-core` (`clippy -D warnings` clean, `14` passing unit/integration tests). Includes `scripts/work-mode.ps1` for RTX 4090 VRAM coordination (unloading heavy image/splat models before starting local coding models).

## Strengths

- Graduated from a Nov-4 spec-only scaffold (`C+`) into a working `2,616 LOC` workspace (`Grade B`) with real subsystems: SQLite FTS5 session search, programmatic unified-diff patching, explicit permission gates, and `craft-ai-core` LLM integration.
- `14` deterministic tests cover patch application, permission gating, session FTS5 search, and autonomy loop transitions without requiring a live LLM in CI.

## Gaps / risks

- Path dependency on `../craft-ai/crates/craft-ai-core` works across `D:\Dev\repos`, but standalone GitHub clones of `sandraschi/codercraft` need `craft-ai` cloned alongside or published as a git dependency.
- Syntax highlighting / tree-sitter AST editing in the L3 GUI is still basic compared to the backend patch/session engine.

## Next 3 steps

1. Support git-fallback or workspace vendor for `craft-ai-core` so standalone CI builds succeed without sibling checkout assumptions.
2. Wire 3 `democraft` recipes (`coder/patch-roundtrip`, `coder/session-fts5`, `coder/permission-gate`).
3. Add tree-sitter symbol outline to `codercraft-core`.

## Verdict

Grade B: the P0/P1 autonomous runner, FTS5 session store, unified-diff patch engine, and `craft-ai-core` integration turn `codercraft` from architecture prose into a real, tested headless + GUI coding studio.
