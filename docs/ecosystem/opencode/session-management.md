# OpenCode Session Management

**Scope:** Cross-project session export/import  
**Source:** opencode.ai/docs/cli (May 2026)  
**Last updated:** 2026-05-04

---

## Sessions Are Project-Scoped

OpenCode sessions are tied to the working directory where `opencode` was started. The agent reads `AGENTS.md`, project config, and repo structure at launch. Switching project directories requires explicit session transfer.

## Export / Import Flow

```bash
# ── From source project ─────────────────────────────────
opencode session list                    # find the session ID
opencode export <session-id>             # writes session.json to disk

# ── Switch to target project ────────────────────────────
cd /path/to/target/project

# ── Import ───────────────────────────────────────────────
opencode import session.json             # resumes session in new context
```

## Share URL Alternative

```bash
# If already shared via opencode.ai/share:
opencode import https://opncd.ai/s/<share-id>
```

This works from any project — the share server stores the full conversation.

## What Transfers

| Property | Transfers? | Notes |
|----------|-----------|-------|
| Conversation history | Yes | Full message/response chain |
| Tool output | Yes | Shell output, file contents, etc. |
| File references | Partial | Paths are absolute; may need remapping |
| Project context (AGENTS.md, etc.) | No | Re-read from target project root |
| Workspace directory | No | Session re-initializes in new CWD |

## CLI Reference

```bash
# Export specific session (interactive picker if no ID given)
opencode export [sessionID]

# Import from file or share URL
opencode import <file>
opencode import https://opncd.ai/s/<share-id>
```

## Use Case: Multi-Repo Handoff

Common in the Sandra-class fleet: work across `robofang`, `deepfang`, and `mcp-central-docs` in a single reasoning chain. Export from one repo and import to another to continue the same analysis without starting fresh.

---

*See also: [opencode-cli-mcp integration guide](../../opencode-cli-mcp/docs/integration-guide.md)*
