---
title: "GitHub CLI (gh) Standards (SOTA 2026)"
category: standards
status: active
audience: mcp-dev
last_updated: 2026-04-20
---

# GitHub CLI (`gh`) Standards

**Version**: 1.0  
**Status**: MANDATORY  
**Substrate**: Windows (Antigravity Fleet)

## 1. Overview
The GitHub CLI (`gh`) is the fallback low-level interface for repository management tasks
that exceed what `gitops` MCP tools handle (see `AGENTS.md` §5). **Primary** git/GitHub
operations MUST go through `git-github-mcp` (`git_ops`, `github_ops` tools); use `gh` only
for gap tasks not covered by the MCP tool schema.

## 2. Canonical Configuration
- **Absolute Path**: `C:\Program Files\GitHub CLI\gh.exe`
- **Fallback Discovery**: Most fleet servers (e.g., `git-github-mcp`) will attempt automatic discovery in `Program Files`, `scoop`, and `winget` links.

## 3. Agentic Usage Protocols
To ensure industrial reliability, agents should use `gh` for the following "Gap Tasks" not fully handled by existing MCP tool schemas:

### 3.1. Repository Topics
MCP `repo_list` often lacks topic management. Use `gh` for bulk tagging:
```powershell
& "C:\Program Files\GitHub CLI\gh.exe" repo edit OWNER/REPO --add-topic sota-2026 --add-topic mcp-hardened
```

### 3.2. PR & Issue Triage
For high-density triage (the "Fleet Maintainer Heartbeat"), use the `github_ops` toolset, but fallback to `gh` for specialized filtering:
```powershell
& "C:\Program Files\GitHub CLI\gh.exe" pr list --state open --search "label:bug"
```

## 4. Troubleshooting
If `gh` fails with `PATH` errors:
1. Use the **absolute path** provided in Section 2.
2. Verify authentication status: `gh auth status`.
3. Check for zombie processes using `just kill-port` or `npx kill-port`.

---
👉 [GitHub CLI Path Discovery](../operations/GITHUB_CLI_CURSOR_PATH.md) | [Fleet Control Plane](../operations/FLEET_CONTROL_PLANE.md)
