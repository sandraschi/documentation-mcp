---
title: "Antipattern - Dialogic Tool Fluff"
category: pattern
status: active
audience: mcp-dev
skill_candidate: true
related:
  - standards/AGENT_PROTOCOLS.md
last_updated: 2026-02-08
---

# Antipattern: Dialogic Tool Fluff

**Status**: Must fix across all MCP server repos  
**Last Updated**: 2026-02-08

---

## Summary

Tool return values and error messages that use vague, reassuring "conversational" language instead of surfacing the **actual error**. The client (LLM or human) cannot act because the return does not say WHAT happened.

## The Antipattern

- "Something unexpected happened"
- "Don't worry, let's try again"
- "I'm here to help you through it"
- "Oops, we hit a snag"
- Emoji in error paths (encoding issues, crashes)

## Why It Fails

1. **Retry loop** — "Try again" with no concrete cause → client retries same failing call repeatedly
2. **Not actionable** — no concrete cause, no clear next step
3. **Token waste** — fluff consumes context without information
4. **Breaks programmatic use** — structured clients need machine-readable error codes
5. **Unicode issues** — emojis cause crashes in some MCP clients

## Wrong vs Correct

```python
# WRONG
return "Something unexpected happened! Don't worry, let's try again."

# CORRECT
return {
    "success": False,
    "error": "NOTE_NOT_FOUND",
    "message": f"Entity '{identifier}' not found in project '{project_name}'",
    "recovery_options": [
        "Verify identifier with adn_content('read', identifier='...')",
        "Use full permalink if note is in a folder",
    ],
}
```

## Long-Running Operations

When a tool fails because a dependency is in progress (model download, docker build, agent execution):

```python
{
    "success": False,
    "error": "MODEL_PULL_IN_PROGRESS",
    "message": "Model 'llama3' is being downloaded. Typical duration: 60-120s.",
    "recovery_options": [
        "Run 'ollama list' to check when model appears",
        "Wait for pull to complete (non-blocking: poll every 10s)",
        "Retry only after model is listed",
    ],
    "estimated_wait_seconds": 90,
}
```

**Agent execution case**: If a tool starts an agent, the return must say "wait for agent to finish before fetching completion report." Never "try again immediately."

## Audit Checklist

- [ ] Error returns state the concrete failure (what, where, why)
- [ ] No "something unexpected" or equivalent vagueness
- [ ] No "don't worry" / "I'm here to help" / "oops"
- [ ] No emojis in logger output, tool returns, or API responses
- [ ] `recovery_options` are specific, not generic
- [ ] Success returns include identifiers (path, permalink, ID)
