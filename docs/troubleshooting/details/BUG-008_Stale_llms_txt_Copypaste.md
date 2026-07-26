# BUG-008: Stale `llms.txt` Copypaste Reference

**Severity**: P3 (Low)
**Date**: 2026-07-03
**Component**: Fleet `llms.txt` auto-generation template

## Symptom

`llms.txt` files across the fleet reference "notepadpp-mcp" in their description text instead of their own repo name. Example stale descriptions:

```
**Complete guide to keeping your notepadpp-mcp repository safe**
**Guides, best practices, and lessons learned for developing notepadpp-mcp**
```

## Root Cause

The `llms.txt` generation scripts/templates were created from the `notepadpp-mcp` repo and the placeholder substitution was incomplete. The template produces generic auto-generated content with hardcoded references that aren't replaced when scaffolded into new repos.

## Affected Repos

| Repo | Fix |
|------|-----|
| `beyondcompare-mcp` | Rewrote with accurate repo description, tools, ports |
| `handbrake-mcp` | Rewrote with accurate repo description, tools, ports |
| `immich-mcp` | Rewrote with accurate repo description, tools, ports |
| `mcp-studio` | Rewrote with accurate repo description, tools, ports |
| `pywinauto-mcp` | Fixed one stale line (content was already good) |
| `local-llm-mcp` | Rewrote with accurate info + `llms-full.txt` link |

## Resolution

Each repo's `llms.txt` was rewritten to contain:
1. One-line elevator pitch of what the server does
2. Key tools/features with bullet points
3. `llms-full.txt` reference
4. Port table
5. Quick start command
6. Links to README, CHANGELOG, config files

## Prevention

Future `llms.txt` files should be written manually per-repo, not generated from a template with unsubstituted placeholders. The fleet standard requires `llms.txt` to be a curated LLM entry point, not a mechanical directory dump.
