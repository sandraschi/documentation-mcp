# Cursor Rules: Multi-Workspace Shell context

## 1. The Problem
In multi-workspace setups (multiple repos in one Cursor window), the terminal does not auto-switch context when the agent starts working on a different repo.

## 2. The Rule
**Add to `.cursorrules` or Cursor User Rules:**

```markdown
# Shell Context Rule for Multi-Workspace
When switching to work on a different repo in a multi-workspace setup:
1. Start a fresh shell (don't reuse existing terminals from other repos)
2. Always cd to the target repo root as the first command
3. Verify Get-Location shows correct directory before running other commands
```
