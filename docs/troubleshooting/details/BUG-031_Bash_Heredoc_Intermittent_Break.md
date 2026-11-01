# BUG-031: Bash heredoc intermittently breaks the shell parser on long multi-line content

**Discovered:** 2026-09-08 (mcp-central-docs, safety/ doc authoring)
**Severity:** P2 (no data loss — Write tool fallback always available — but wastes turns and produces confusing partial output)
**Component:** The Bash tool's Git-Bash transport on Windows, as used for `cat > file <<'EOF' ... EOF` style multi-line file creation
**Status:** Unreproduced root cause; mitigated by blocking the pattern (see Resolution)

## Symptom

A single-quoted heredoc (`<<'EOF'`, the textbook-safe form that disables all
expansion inside the body) used to write a long markdown file failed with:

```
/usr/bin/bash: -c: line 111: unexpected EOF while looking for matching `''
```

The failing command had the shape:

```bash
cp file "file.$(date +%Y%m%d_%H%M%S).bak" && cat > file <<'EOF'
... ~190 lines of real markdown prose (headers, tables, links, contractions) ...
EOF
echo "written: $(wc -l < file) lines"
```

Exit code 2, no file written. The Write tool, used immediately after as a
fallback, succeeded on the identical content with zero issues — this ruled out
the content itself being invalid, and pointed at the heredoc transport instead.

## Investigation

`<<'EOF'` heredocs are specified to be 100% literal inside the body — no quote
pairing, no expansion, no backtick interpretation — so apostrophes,
scare-quotes, em dashes, and markdown syntax inside the body should never be
able to break the parse. Three escalating repro attempts were built to test
this assumption:

1. Short heredoc (12 lines) with heavy contractions (`it's`, `doesn't`,
   `isn't`, `OpenAI's`) — **passed**.
2. Heredoc with a markdown table, inline code span, and mixed apostrophes —
   **passed**.
3. ~480-line / ~43KB synthetic body matching the failing document's density:
   scare-quoted phrases (`'motivated reasoning'`), em dashes, markdown links,
   nested double/single quotes, tables, chained with the same
   `cp ... && cat > ... <<'EOF'` structure — **passed**.

No deterministic trigger was found. This is itself informative: it rules out
a specific-character root cause and points at something environment-level —
most plausibly an intermittent issue in how the harness's Bash tool streams a
very long multi-line `command` string to the underlying Git-Bash/MSYS
process on Windows (buffering, line-ending translation, or an IPC chunk
boundary interacting badly with heredoc terminator matching). This class of
bug is consistent with the PowerShell tool's own documented here-string
fragility on this platform (`@'...'@` closing delimiter must be at column 0,
no leading whitespace — a similar terminator-matching sensitivity).

Effort was capped after three escalating repro attempts failed to reproduce;
further isolation would require access to the harness's own IPC transport,
which is outside this repo.

## Resolution

Root cause not fixable from application code — this lives in the CLI
harness's shell bridge, not in any fleet repo. Given an unreproducible,
intermittent failure with a 100%-reliable alternative already in hand, the
correct move is to block the risky pattern rather than keep chasing it:

**Rule added to fleet root `CLAUDE.md`:** do not use Bash heredocs
(`cat > file <<EOF` / `<<'EOF'`) to create or overwrite files with multi-line
content. Use the Write tool instead, even under auto-mode's general
Bash-first bias — that bias is for commands, not for authoring file content.
Heredocs remain fine for short, single-purpose inline use (piping a few lines
to a command) where a parse failure is cheap to notice and retry.

## Log Snippet

```
/usr/bin/bash: -c: line 111: unexpected EOF while looking for matching `''
```

Exit code: 2. No partial file was left on disk (the `cp` backup step
completed; the `cat > file` step did not).
