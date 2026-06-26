# CLAUDE.md — Agent Behavioral Instructions (SOTA 2026)

## The Trick

Both **Claude Code** and **opencode** read `~/.claude/CLAUDE.md` (or `%USERPROFILE%\.claude\CLAUDE.md` on Windows) as their **global behavioral instructions file**. This file is loaded at session start and governs every interaction across every project.

This is the single highest-leverage configuration point in the fleet. Shape this file, and you shape every agent session.

## File Hierarchy

Instructions are merged in order (later overrides earlier for conflicts):

```
1. ~/.claude/CLAUDE.md              ← Global (this file, all sessions)
2. <repo-root>/CLAUDE.md            ← Per-repo (project-specific)
3. <repo-root>/CLAUDE.md in git     ← Per-repo committed (team-shared)
4. Inline instructions in prompt    ← Per-session (user message)
```

## What Goes in the Global File

The global CLAUDE.md should contain **cross-project behavioral rules** only:

| Section | Content | Example |
|---------|---------|---------|
| Identity & Tone | How the agent should behave | "Peer collaborator, zero sycophancy" |
| Global Standards | Cross-cutting requirements | PowerShell syntax, port conventions |
| Context Hygiene | Session management rules | When to compact, when to clear |
| Coding Philosophy | How to approach code changes | Karpathy's Think/Simplify/Surgical/Goal-Driven |

**Do NOT** put project-specific instructions (repo paths, build commands, API keys) in the global file. Those go in per-repo `CLAUDE.md`.

## Fleet Practice: Global + Per-Repo

```
~/.claude/CLAUDE.md                          ← Behavioral rules, tone, coding philosophy
D:\Dev\repos\mcp-central-docs\.cursorrules   ← IDE rules (Cursor-specific)
D:\Dev\repos\mcp-central-docs\standards\     ← Reference docs (loaded via instructions)
```

The global CLAUDE.md delegates to `mcp-central-docs` via `## Global Context & Standards` sections rather than duplicating content.

## Merging External Guidelines

To incorporate third-party behavioral guidelines (e.g. `andrej-karpathy-skills`), append them as a new section rather than replacing content. This preserves existing structure:

```markdown
## Existing Section
...

## Karpathy-Inspired Coding Behavior
### 1. Think Before Coding
...
### 4. Goal-Driven Execution
...
```

## Verification

The CLAUDE.md is working if:
- Sessions consistently apply the configured tone and rules
- Per-repo CLAUDE.md files contain only repo-specific info
- New agents inherit fleet standards without explicit prompting
