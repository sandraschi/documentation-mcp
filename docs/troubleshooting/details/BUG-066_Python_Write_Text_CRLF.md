# BUG-066: Python `write_text` / `open(w)` silently converts repo files to CRLF on Windows

**Discovered:** 2026-10-06 (opencode-cli-mcp Help.tsx praise-tab session — one script, one file)
**Severity:** P2 (silent whole-file rewrite; biome gate red on every line; phantom diffs; hook churn)
**Component:** Any Python script that patches repo files on Windows (agent tooling, not a repo)
**Status:** Root cause fully understood and deterministic. Mitigated by rule (see Resolution)

## Symptom

A Python patch script that inserts one JSX block into `Help.tsx` appears to
succeed — "inserted ok" printed — but `biome check` then flags **every line of
the 600-line file** (`␍` markers on lines the script never touched), burying
the one genuine formatting issue inside whole-file noise. `git diff` shows a
full-file rewrite. Nothing in the script's output suggests anything happened
beyond the intended insert.

## Root cause

Four line-ending policies, three saying LF and one saying "whatever Windows does":

1. **Python is the writer.** `Path.write_text()` / `open(p, "w")` default to
   `newline=None`, which means universal newlines on read and **translate
   `\n` → `os.linesep` on write** — `\r\n` on Windows. Every "obvious"
   patch script converts the entire file to CRLF even when it changed one line.
2. **The read half masks it.** `read_text()` translates all endings to `\n`,
   so the script sees clean LF, previews look fine, and the CRLF only
   materialises at write time. The bug is write-only and invisible until
   something else trips over it.
3. **Biome trips file-wide.** Default `lineEnding: "lf"` (no repo overrides
   anywhere in the fleet) — a CRLF file is not one error but a rewrite of
   every line, so the real signal drowns.
4. **Git amplifies.** `* text=auto eol=lf` in `.gitattributes` normalises on
   commit, but the working-tree CRLF still shows as a full-file modification,
   and the pre-commit `fix end of files` hook may rewrite the file mid-commit
   (stash/restore churn observed in the same session).

Verified with a scratch proof script (since removed):

```
write_text default      -> b'a\r\nb\r\n'   CRLF!
write_text newline=LF   -> b'a\nb\n'       LF ok
write_bytes normalized  -> b'a\nb\n'       LF ok
read_text of mixed file -> 'a\nb\n'        (masking: CRLF invisible on read)
```

Same failure class as BUG-039 (stdlib defaults silently rewriting your bytes;
that one was escape interpretation, this one is newline translation) and the
writer-side complement of BUG-061 (which covers CRLF already sitting in web
sources tripping the biome hook — this covers how CRLF gets *introduced* by
agent scripts).

## Resolution

Stop writing the risky construct. Template for any Python file patch on this fleet:

```python
from pathlib import Path
p = Path(r"D:\path\to\file")
text = p.read_text(encoding="utf-8")
# ... modify text ...
p.write_text(text, encoding="utf-8", newline="\n")  # newline kwarg since 3.10
```

Bulletproof variant (normalises pre-existing mixed endings too):

```python
p.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))
```

Rules:

- Never bare `open(p, "w")` / `write_text()` without `newline="\n"` for repo
  files on Windows.
- After any Python patch, assert `data.count(b"\r\n") == 0` before writing —
  read-side looks clean is not evidence.
- Prefer the Edit/Write tools for patching (no newline interpretation at all);
  scripts are for insertions the tools cannot express (e.g. content containing
  `{...}` sequences the edit tools reject), and then only via the template above.

Note: `Path.write_text(..., newline=...)` requires Python 3.10+. The fleet
floor is 3.13, so this is always available. `open()` has accepted
`newline=` since 3.0.

## Detection

CRLF already introduced by a script:

```powershell
# files with CRLF under a repo (run from repo root)
Get-ChildItem -Recurse -Include *.py,*.ts,*.tsx,*.md,*.json -File |
  Where-Object { (Get-Content -Raw $_.FullName) -match "`r`n" } |
  Select-Object FullName
```

Fix in place (LF normalize, then re-run the repo's formatter gate):

```powershell
$b = [IO.File]::ReadAllBytes($file)
[IO.File]::WriteAllBytes($file, ([Text.Encoding]::UTF8.GetString($b) -replace "`r`n","`n"))
```

A same-session check of the patched file confirmed 0 remaining CRLF after the
byte-level rewrite, with `biome check` and `tsc` green.
