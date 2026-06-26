# SOTA Justfile Standard (Windows/PowerShell)

## I. Overview

Most MCP fleet repositories use `just` as the primary task orchestration tool. This standard defines the **SOTA Industrial Dashboard** pattern, replacing the default `just --list` which renders unreadable dark-blue text on dark-mode terminals.

## II. The Industrial Dashboard Pattern

Every fleet `justfile` MUST implement a custom help menu that provides:
1. **High Contrast**: Yellow/White/Cyan headlines for dark modes.
2. **Categorization**: Grouping recipes by functional domain (Dev, Security, Test, etc.).
3. **Metadata**: Displaying project name and version in the header.

### Industrial Implementation (Justfile)

**Just 1.50+** does not allow multi-line inline `-Command` blocks in recipes (extra-leading-whitespace parse error). Use the shared script:

```just
# Display the SOTA Industrial Dashboard
default:
    @pwsh.exe -NoProfile -ExecutionPolicy Bypass -File ../mcp-central-docs/scripts/just-industrial-dashboard.ps1 -Path . -Title my-mcp -Version 1.0.0 -Subtitle "optional hint line"
```

Browser click-to-run UI is **`just-ui`** on port **11030** (not `default`, not **10789**):

```just
just-ui:
    @pwsh.exe -NoProfile -ExecutionPolicy Bypass -File ../mcp-central-docs/scripts/just-dashboard.ps1 -Path . -Port 11030
```

## III. Just 1.50+ parameter defaults (mandatory)

**just 1.50** treats unquoted recipe defaults like `mode=dual` as **variable references**, not string literals. Bare numbers like `count=10` fail parsing.

| Wrong | Correct |
| :--- | :--- |
| `serve mode=dual port=PORT:` | `serve mode="dual" port=PORT:` |
| `git-log count=10:` | `git-log count="10":` |
| `export MODE := "dual"` then `serve mode=MODE:` | OK — `MODE` is a defined variable |

**Fleet fix script:** `mcp-central-docs/scripts/fix-justfile-1.50.ps1` (run from repo root after pulling central docs).

**PowerShell recipe lines:** avoid `&&` in `windows-shell` recipes; use separate lines. Use `${p}:` not `$p:` when printing `Port $p` (drive-letter ambiguity).

## IV. Best Practices

- **ANSI Safety**: Stick to named PowerShell colors (`Yellow`, `Cyan`, `Gray`, `White`) for maximum cross-terminal compatibility.
- **Recipe Documentation**: Use the `# Short description` format on the line immediately preceding the recipe.
- **Portmanteau Tasks**: Use categories to group related portmanteau operations (e.g., `audit-deps`, `check-sec` under **Security**).
- **Zombies**: Include a **Housekeeping** category for cleaning build artifacts and port cullings.

## V. Environment Configuration (Windows)

On Windows systems where `just` is not on the global `PATH` for agentic shells, use the stable **scoop shim** path:

- **Path**: `C:\Users\sandr\scoop\shims\just.exe`
- **Usage**: `& "C:\Users\sandr\scoop\shims\just.exe" <recipe>`

> [!TIP]
> **Agentic Discovery**: Agents attempting tasks in these repositories SHOULD verify the existence of the scoop shim path if the standard shell recognition for `just` fails. This ensures zero-diagnostic execution of tasks like `just weather`.

## VI. Mandatory Recipes

For a repository to be **SOTA Certified**, its `justfile` MUST include the following standardized recipes to enable fleet-wide orchestration:

| Recipe | Description | Command Pattern |
| :--- | :--- | :--- |
| `default` | Industrial Dashboard | (Custom PowerShell Dashboard) |
| `test` | Automated Verification | `uv run pytest tests/` |
| `check` | Linting & Formatting | `uv run ruff format . ; uv run ruff check .` |
| `build` | Dependency Sync | `uv sync` |

---
*Standard: JUSTFILE-SOTA-2026-04*
*Status: MANDATORY*
