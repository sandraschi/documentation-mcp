# SOTA Justfile Standard (Windows/PowerShell)

## I. Overview

Most MCP fleet repositories use `just` as the primary task orchestration tool. This standard defines the **SOTA Industrial Dashboard** pattern, replacing the default `just --list` which renders unreadable dark-blue text on dark-mode terminals.

## II. The Industrial Dashboard Pattern

Every fleet `justfile` MUST implement a custom help menu that provides:
1. **High Contrast**: Yellow/White/Cyan headlines for dark modes.
2. **Categorization**: Grouping recipes by functional domain (Dev, Security, Test, etc.).
3. **Metadata**: Displaying project name and version in the header.

### Industrial Implementation (Justfile)

```just
# Display the SOTA Industrial Dashboard
default:
    @powershell -NoLogo -Command " \
        $lines = Get-Content '{{justfile()}}'; \
        Write-Host ' [{{NAME}}] {{DESC}} v{{VER}}' -ForegroundColor White -BackgroundColor Cyan; \
        Write-Host '' ; \
        $currentCategory = ''; \
        foreach ($line in $lines) { \
            if ($line -match '^# ── ([^─]+) ─') { \
                $currentCategory = $matches[1].Trim(); \
                Write-Host \"`n  $currentCategory\" -ForegroundColor Cyan; \
                Write-Host '  ' + ('─' * 45) -ForegroundColor Gray; \
            } elseif ($line -match '^# ([^─].+)') { \
                $desc = $matches[1].Trim(); \
                $idx = [array]::IndexOf($lines, $line); \
                if ($idx -lt $lines.Count - 1) { \
                    $nextLine = $lines[$idx + 1]; \
                    if ($nextLine -match '^([a-z0-9-]+):') { \
                        $recipe = $matches[1]; \
                        $pad = ' ' * [math]::Max(2, (18 - $recipe.Length)); \
                        Write-Host \"    $recipe\" -ForegroundColor White -NoNewline; \
                        Write-Host \"$pad$desc\" -ForegroundColor Gray; \
                    } \
                } \
            } \
        } \
        Write-Host \"`n  [System State: PROD/HARDENED]\" -ForegroundColor DarkGray; \
        Write-Host ''"
```

## III. Best Practices

- **ANSI Safety**: Stick to named PowerShell colors (`Yellow`, `Cyan`, `Gray`, `White`) for maximum cross-terminal compatibility.
- **Recipe Documentation**: Use the `# Short description` format on the line immediately preceding the recipe.
- **Portmanteau Tasks**: Use categories to group related portmanteau operations (e.g., `audit-deps`, `check-sec` under **Security**).
- **Zombies**: Include a **Housekeeping** category for cleaning build artifacts and port cullings.

## IV. Environment Configuration (Windows)

On Windows systems where `just` is not on the global `PATH`, use the absolute path to the scoop-managed executable:

- **Path**: `C:\Users\sandr\scoop\apps\just\1.49.0\just.exe`
- **Usage**: `& "C:\Users\sandr\scoop\apps\just\1.49.0\just.exe" <recipe>`

---
*Standard: JUSTFILE-SOTA-2026-04*
*Status: MANDATORY*
