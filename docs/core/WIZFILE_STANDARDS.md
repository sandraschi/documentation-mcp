---
title: "WizFile Standards (SOTA 2026)"
category: standards
status: active
audience: mcp-dev
last_updated: 2026-04-20
---

# WizFile Standards

**Version**: 1.0  
**Status**: RECOMMENDED (Discovery Acceleration)  
**Substrate**: Windows (Antigravity Fleet)

## 1. Overview
WizFile is a high-speed file search utility that reads the Master File Table (MFT) directly. It is significantly faster than standard Windows search or `Get-ChildItem` for locating deeply nested files (e.g., local LLM models in Pinokio subfolders).

## 2. Canonical Configuration
- **Absolute Path**: `C:\Program Files\WizFile\WizFile64.exe`

## 3. CLI Integration Patterns
Use the following flags for agentic discovery tasks:

### 3.1. Deep Search & Export
To find a file and capture the path without manual UI interaction:
```powershell
& "C:\Program Files\WizFile\WizFile64.exe" /search="pattern" /export="C:\path\to\results.csv" /quit
```

### 3.2. Common Parameters
- `/search="pattern"`: Initialize search with the specified pattern.
- `/execute="pattern"`: Open the file immediately if a single match is found.
- `/export="filename.csv"`: Save results to CSV (high speed).
- `/quit`: Close the application immediately after an export operation.

## 4. Why WizFile?
While `rg` (ripgrep) is the standard for searching **within** files, WizFile is the standard for searching **for** files across the entire MFT when the directory structure is unknown or massive.

---
👉 [PowerShell SOTA](./rules/powershell_sota.md) | [Fleet Control Plane](../operations/FLEET_CONTROL_PLANE.md)
