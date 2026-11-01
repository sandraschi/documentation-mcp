# Verbatim compaction with a local scorer (no summarization, no cloud)

Date: 2026-09-19. Source idea: `tamaratran/fast-jev-compaction`
(Claude Code plugin that replaces the compaction summary with keep/drop
decisions per tool call, scored by the Jev classifier on TypeSafe's API).

## Why this matters

Standard compaction asks an LLM to *summarize* old turns. Summaries are lossy:
exact paths, error strings, constraints, commands disappear even when the next
steps still need them. The verbatim alternative never rewrites anything:

- user + assistant text stays verbatim and in order, always,
- every `tool_use` is paired with its `tool_result` by id,
- a scorer answers two questions per non-pinned call: `keepCall` (knowing it
  was made still matters) and `keepResult` (full output still needed verbatim
  AND re-running would not do),
- `keepResult >= threshold` -> keep both; `keepCall >= threshold` -> truncate
  result to a head + note; else drop call + result together,
- first message + newest N messages are pinned and never touched.

## Why NOT the upstream repo as-is

1. **Claude Code only.** It is a function-hook plugin (`session.compact`,
   needs Claude Code 2.1.274+ + `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`).
   It does **not** run in Claude Desktop (no hooks, no `session.compact`,
   no plugin marketplace for compaction), nor in opencode / Antigravity.
   In Desktop the closest equivalent is calling a compaction routine by hand
   from an MCP tool — not automatic.
2. **Cloud dependency + privacy.** Every compaction ships the whole
   conversation to `api.typesafe.ai` with a paid `TYPESAFE_API_KEY`.
3. **Text-heavy transcripts get ~nothing.** Only tool calls/results are
   candidates; if the bloat is chat, reduction < 0.25 and it falls back to
   the built-in summary anyway.

## What we built instead (1 file, stdlib only)

`patterns/verbatim_compaction_ollama.py` — faithful port of the upstream
`state.ts` (token estimator, staged `fitState`: input caps -> abridge texts ->
collapse old messages -> one-line calls -> drop call-less -> merge runs) and
`compact.ts` (pairing, batching, `decideCall`, `applyDecisions`), with the
Jev client replaced by two local scorers:

- `OllamaAsker` — `POST /api/chat`, JSON mode, parallel batches,
- `OpenAICompatAsker` — any `/v1/chat/completions` endpoint (LM Studio),
- offline `heuristic_scores` fallback (keeps errors + small results).

Usage:

```powershell
python patterns/verbatim_compaction_ollama.py --demo --backend heuristic
python patterns/verbatim_compaction_ollama.py --demo --backend lmstudio --model deephermes-3-llama-3-8b-preview
python patterns/verbatim_compaction_ollama.py --demo --backend ollama --model mistral-nemo:12b
```

Importable: `from verbatim_compaction_ollama import compact, OpenAICompatAsker`.

## Measured 2026-09-19 (Goliath, synthetic 14-msg / 6-call transcript)

| backend | result | time |
|---|---|---|
| heuristic | 20946 -> 1498 chars (0.93), stale 18k Glob listing dropped, error + grep kept | ~1 ms |
| lmstudio / deephermes-3-llama-3-8b | 0.00 reduction — model hedged 0.5 on every question, all kept | 12.6 s |
| lmstudio / qwen 27b | first-load timeout (>120 s), fell back to heuristic | 122 s |
| ollama / any model | **500 on `/api/chat` for every model** | — |

Plumbing for live local scoring is proven end-to-end (prompt -> JSON scores ->
decisions -> rebuild). Model quality is the open item: 8b hedges, 27b is slow
cold. Candidates worth one more run when warm: `qwen/qwen3.6-27b` (loaded),
`deepseek-r1-distill-qwen-32b`, or Ollama's `qwen3.8-tools` once Ollama works.

## Fleet environment notes (same day)

- **Ollama is broken:** `llama-server.exe` missing from the install dir
  (`C:\Users\<user>\AppData\Local\Programs\Ollama\`), all `/api/chat` and
  `/api/generate` calls 500. Reinstall Ollama before trusting `--backend ollama`.
  `ollama list` (registry) still works; only inference is down.
- **LM Studio is up** (`localhost:1234`): qwen3.6-27b, gemma-4, gpt-oss-20b,
  deepseek distills, nemotron-3-nano, diffusiongemma.
- `compact()` degrades gracefully: any scorer failure + `fallback_heuristic=True`
  (default) prints a warning and compacts with the heuristic instead of throwing.

## Next steps (not done)

- Warm-run `qwen/qwen3.6-27b` scorer and record real keep/drop quality vs heuristic.
- Reinstall Ollama, re-run `--backend ollama` with `mistral-nemo:12b`.
- Decide where a manual "compact this transcript" MCP tool should live
  (advanced-memory-mcp is the natural home; Claude Desktop has no auto-hook,
  so it would be an explicit tool call, not a `/compact` replacement).
