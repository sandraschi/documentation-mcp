# Engineering Antipattern: Script Desynchronization

**Status**: Active
**Category**: Automation / Maintenance
**Related Patterns**: [[Hub-and-Spoke Standardization]]

## Problem Description
Utility scripts (e.g., `backup-repo.ps1`, `check-repo-standards.ps1`) are frequently cloned into multiple independent repositories. Without a central synchronization mechanism, these scripts naturally diverge as fixes and "SOTA" (State Of The Art) improvements are developed.

### Symptoms
- **Broken Automation**: A critical bug-fix in a central script is not reflected in a target repo, leading to script failure (e.g., `advanced-memory-mcp` had a broken `backup-repo.ps1`).
- **Missing Features**: A repo lacks standard scripts entirely (e.g., `songgeneration-mcp`).
- **High Maintenance**: Pushing a SOTA script update manually to 50+ repositories is error-prone and time-consuming.
- **Agent Confusion**: Different agent instances see different versions of "Standard" tools, leading to inconsistent behavior.

## The Solution: Hub-and-Spoke Synchronization

### 1. The Hub (`mcp-central-docs`)
*   **Source of Truth**: All SOTA scripts reside in `sota-scripts/` within the central docs repository.
*   **Propagation Engine**: Central scripts (like `propagate-all-sota.ps1`) can push updates to all discovered repositories.

### 2. The Spoke (Individual Repos)
*   **Registration**: Each repository contains a `sync-sota.ps1` script in its `scripts/` folder.
*   **Pull Mechanism**: Running `.\scripts\sync-sota.ps1` checks for updates from the neighboring Hub and pulls them down.

## Implementation Standards

### Path Resolution
Spoke scripts should assume the Hub is a sibling directory or use a relative path lookup:
```powershell
$hubPath = Join-Path $PSScriptRoot "..\..\mcp-central-docs"
```

### Script Manifests
The Hub should maintain a manifest of scripts that are considered "Standard SOTA" and should be available in all repositories.

## Benefits
- ✅ **Uniformity**: All repositories use the same high-quality automation.
- ✅ **Efficiency**: Fix once, propagate everywhere.
- ✅ **Reliability**: Centralized testing ensures SOTA scripts work before rollout.
