# BUG-039: Inline `python - <<'PY'` silently mangles backslash escapes when patching code

**Discovered:** 2026-09-17 (mcp-central-docs, fleet-gate work — three separate incidents in one session)
**Severity:** P1 (silent content corruption; one variant produces valid syntax with wrong behaviour and no error at all)
**Component:** Any `python - <<'PY' ... PY` (or `python -c "..."`) used to edit files, where the replacement text contains backslashes
**Status:** Root cause fully understood and deterministic. Mitigated by a hard rule (see Resolution)

## Symptom

A heredoc-delivered Python script that rewrites a file appears to succeed —
exit 0, "patched" printed — but the file on disk contains corrupted content.

Three distinct failure shapes were hit in a single session:

### 1. Windows path destroyed (loud, but confusing)

```python
t = t.replace(old, "...the fork API in D:\Dev\repos\rustdesk, and the MCP backend...")
```

Landed on disk as:

```
  orchestrates the whole rustdesk++ stack (hbbs/hbbr relays, the fork API in
  D:\Deveposustdesk, and the MCP backend in D:\Deveposustdesk-mcp).
```

`\r` became a carriage return and `\D` stayed literal (emitting only a
`SyntaxWarning: invalid escape sequence '\D'`). The embedded CRs then split
what looked like one line into four physical lines, so the follow-up Edit
could not string-match it and the cleanup took three attempts.

### 2. Escape inside an f-string (loud)

```python
t = t.replace(..., 'print(f"\\nCOVERAGE: {coverage_msg}")')
```

Landed as a real newline inside the f-string:

```python
        print(f"
COVERAGE: {coverage_msg}")
```

`SyntaxError: unterminated f-string literal`. Caught immediately by running
the file, but only because it was run.

### 3. Comment insertion swallowing a line (SILENT — the dangerous one)

```python
t = t.replace('_ASCII_MAP = {', '_ASCII_MAP = {  # noqa: RUF001 - ...')
```

Landed as:

```python
_ASCII_MAP = {  # noqa: RUF001 - these ARE the characters being normalised"→": "->", ...
              "‘": "'", "’": "'", ...
```

Everything after `#` became a comment, so the arrow and dash mappings were
silently deleted from the dict. **This is valid Python.** It compiles, it
lints, it runs — and the normaliser it defines quietly stopped normalising
arrows and em dashes. No error, no warning, no exit code. It was caught only
by reading the file back.

## Root cause

Nothing to do with the heredoc transport (that is BUG-031, a different bug).
`<<'PY'` correctly passes the body through literally. The corruption happens
one level further in: **Python's own string-literal parser** then interprets
the backslash sequences in the replacement text.

`"D:\Dev\repos\rustdesk"` is not a path to Python. It is `D:` + `\D` (invalid
escape, kept literally with a warning) + `ev` + `\r` (CARRIAGE RETURN) +
`epos` + `\r` again + `ustdesk`. Python is behaving exactly as specified; the
mistake is writing a Windows path or an escape-bearing code fragment into a
non-raw string literal.

The reason this is P1 rather than cosmetic is failure shape 3: when the
mangling happens to produce syntactically valid code, **nothing anywhere in
the toolchain reports a problem.** Compilation passes, ruff passes, tests that
do not exercise that path pass. Only reading the file catches it.

## Why the obvious defences do not help

- `<<'PY'` quoting does not help — the shell is not the layer that mangles.
- `SyntaxWarning: invalid escape sequence` fires only for *invalid* escapes
  (`\D`). The genuinely dangerous ones — `\r`, `\n`, `\t`, `\b`, `\f`, `\v`,
  `\a` — are *valid*, so they convert silently.
- Running the patched file catches shapes 1 and 2, but not shape 3.
- `ruff check` catches neither shape 2 (file does not parse, so it is skipped
  or errors confusingly) nor shape 3 (valid code).

## Resolution

Root cause is a known Python semantic, not a harness defect, so the fix is to
stop writing the risky construct:

**Hard rule added to fleet root `CLAUDE.md`:** do not use `python - <<'PY'`
or `python -c` to patch files when the content involves backslashes. Use the
Edit tool for targeted replacements and the Write tool for whole files. If a
script genuinely must do the patching, use raw strings (`r"D:\Dev\repos"`) or
forward slashes, and always read the result back.

This sits alongside the existing BUG-031 rule and covers the opposite failure
mode: BUG-031 is a heredoc that fails loudly and writes nothing, BUG-039 is a
heredoc that succeeds and writes something wrong.

## Detection

If a mangled file is suspected, these find the signatures:

```bash
# stray carriage returns mid-line (the \r signature)
perl -ne 'print "$.\n" if /\r(?!\n)/' FILE

# other control chars from \b \f \a \v \e
rg -n $'[\x07\x08\x0b\x0c\x1b]' FILE

# orphaned path fragments left by a mangled D:\Dev\repos\...
rg -n 'Deveposustdesk|D:\\Deve|^\s*epos$|^\s*ustdesk' .
```

A fleet-wide sweep with these after the 2026-09-17 session found no further
instances beyond the three listed above — the blast radius was contained
because every other file in that session was authored with the Write tool,
which performs no escape interpretation.
