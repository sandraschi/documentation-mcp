# Unicode Safety (fleet mandatory)

**Status:** Active  
**Version:** 2.0  
**Applies to:** All fleet MCP repos, `mcp-central-docs`, and any file an agent might copy into scripts

## Rule (non-negotiable)

**EM DASH (U+2014) is never allowed** in fleet repositories.

Also forbidden in the same scope: **EN DASH** (U+2013), **smart single/double quotes** (U+2018–U+201D).

Use ASCII only:

| Forbidden | Use instead |
|-----------|-------------|
| `—` EM DASH | ` - ` or ` -- ` (ASCII hyphens) |
| `–` EN DASH | `-` |
| `'` `'` | `'` |
| `"` `"` | `"` |

## Agent rule (batch replace)

Do **not** run recursive `ReadAllText`/`WriteAllText` over `src/**/*.py` until [GIT_REPOSITORY_SAFETY.md](../GIT_REPOSITORY_SAFETY.md) is satisfied (git log + checkpoint commit). Prefer `check-unicode-safe.ps1` report + per-file fixes over blind mass rewrite.

## Scope

Applies to **every line** in these paths (including `#` comments and `Write-Host` strings):

| Paths | Extensions |
|-------|------------|
| Repo root launchers | `start.ps1`, `start.bat`, `install-mcp.ps1` |
| `justfile`, `Justfile` | whole file |
| `src/`, `scripts/`, `tests/`, `assets/` | `.py`, `.ps1`, `.bat`, `.cmd`, `.ts`, `.tsx`, `.js`, `.jsx` |
| `webapp/`, `web_sota/`, `web/` | same as above |
| Fleet docs copied into prompts | `assets/prompts/*.md`, root `INSTALL.md` when it contains PS examples |

**Markdown elsewhere:** prefer ASCII dashes for consistency; em dash in README prose is **discouraged** and should be removed in standards/docs sweeps so agents do not paste broken characters into `start.ps1`.

## Why (Windows PowerShell 5.1)

`start.bat` launches **`powershell.exe`** (5.1), not PowerShell 7. Files saved as UTF-8 **without BOM** often mis-decode em dashes as `â€"` inside double-quoted strings. That **terminates the string early** and produces cascading parser errors (`Missing '}'`, `The ampersand (&) character is not allowed`, etc.).

This is **not** "comments are safe" - a bad byte in a comment or `Write-Host` line breaks the whole script.

## Enforcement

### Fleet checker (canonical)

**Scripts only** (default - use in pre-commit):

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\Dev\repos\mcp-central-docs\scripts\check-unicode-safe.ps1 -RepoPath D:\Dev\repos\{repo}
```

**Include markdown** (docs sweep):

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\Dev\repos\mcp-central-docs\scripts\check-unicode-safe.ps1 -RepoPath D:\Dev\repos\{repo} -IncludeMarkdown
```

Reads files as **UTF-8**. Skips `node_modules`, `.venv`, `dist`, and other vendor/cache dirs. Exit **1** if any forbidden character is found; **0** if clean.

### Pre-commit (per repo)

```yaml
- repo: local
  hooks:
    - id: unicode-safety
      name: No em dash / smart quotes in scripts
      entry: powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:/Dev/repos/mcp-central-docs/scripts/check-unicode-safe.ps1 -RepoPath .
      language: system
      pass_filenames: false
      always_run: true
```

### Just recipe (per repo)

```just
check-unicode:
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:/Dev/repos/mcp-central-docs/scripts/check-unicode-safe.ps1" -RepoPath "{{justfile_directory()}}"
```

## Agent instructions

- When editing **`start.ps1`**, **`start.bat`**, or **`justfile`**: use **ASCII hyphen `-` only**.
- Do not let editors "smart punctuation" replace `-` with `—`.
- If a user pastes text containing em dashes into a script, replace before save.

## Related standards

- [NAKED_PC_INSTALL_STANDARD.md](../NAKED_PC_INSTALL_STANDARD.md) - `start.ps1` / `start.bat`
- [START_SCRIPT_STANDARD.md](../START_SCRIPT_STANDARD.md) - fleet launcher template
- [POWERSHELL_STANDARDS.md](../POWERSHELL_STANDARDS.md) - §6 Unicode
- [AGENT_INSTALL_REFERENCE.md](../AGENT_INSTALL_REFERENCE.md) - anti-patterns for agents editing install docs

## Reference implementation

- Checker: `mcp-central-docs/scripts/check-unicode-safe.ps1` (from `virtualization-mcp` pattern, fleet `-RepoPath`)
- First remediation example: `chip-design-mcp/start.ps1` (2026-05-31)
