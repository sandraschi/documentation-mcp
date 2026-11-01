# Scripting for MCP Ops: The SOTA 2026 Standard

**PowerShell**: 7.4+ (Cross-Platform Standard)
**Bash**: 5.2+ (Linux Native Standard)
**Role**: The Operational Backbone / "Glue"
**Philosophy**: Idempotency & Automation
**Linting**: ShellCheck (Bash) / PSScriptAnalyzer (PowerShell)

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for Scripting usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity Scripting Standard](#the-antigravity-scripting-standard)
    *   [The Universal Launcher Pattern](#the-universal-launcher-pattern)
    *   [Idempotency & Cleanup](#idempotency--cleanup)
    *   [Cross-Platform Strategy](#cross-platform-strategy)
3.  [Global Context: Shell Evolution](#global-context-shell-evolution)
    *   [PowerShell (The Monad Manifesto)](#powershell-the-monad-manifesto)
    *   [Bash (The GNU Standard)](#bash-the-gnu-standard)
    *   [Objects vs. Text Streams](#objects-vs-text-streams)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [Wait-For-Port Strategy](#wait-for-port-strategy)
    *   [Virtual Environment Management](#virtual-environment-management)
    *   [Signal Handling (Graceful Shutdown)](#signal-handling-graceful-shutdown)
5.  [Advanced Patterns](#advanced-patterns)
    *   [Argument Parsing (`param` vs `getopts`)](#argument-parsing-param-vs-getopts)
    *   [Error Handling Strategies](#error-handling-strategies)
    *   [Logging & Output Redirection](#logging--output-redirection)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, scripts are the **Operational Backbone**. While Python provides the logic and Rust provides the muscle, scripts provide the **nervous system for deployment and orchestration**.

**The Rule of the Launcher:**
Every MCP server **MUST** have a `start.ps1` (for Windows) and a `start.sh` (for Linux/macOS). These scripts abstract away the complexity of:
1.  Setting up the environment variables.
2.  Activating the correct Python virtual environment.
3.  Cleaning up stale processes (zombie hunting).
4.  Launching the server process with correct flags.

**Why PowerShell 7+?**
-   **Structured Data**: Passing objects instead of text strings eliminates parsing errors.
-   **Cross-Platform**: It runs identically on Windows, Linux, and macOS.
-   **Reliability**: `try/catch` blocks in PowerShell are far more robust than checking exit codes in Bash.

---

## 2. The Antigravity Scripting Standard

### The Universal Launcher Pattern

This pattern ensures that **any** developer (human or agent) can boot **any** server in the fleet without knowing its internal details.

#### Windows Standard (`start.ps1`)

```powershell
#!/usr/bin/env pwsh
# SOTA 2026 Standard Launcher

$ErrorActionPreference = "Stop"

# 1. Define Context
$RepoRoot = $PSScriptRoot
$ServerName = "my-mcp-server"

Write-Host "🚀 Launching $ServerName..." -ForegroundColor Cyan

# 2. Zombie Hunting (Idempotency)
# We find any process matching our server script and kill it.
$OldProcs = Get-Process -Name "python" -ErrorAction SilentlyContinue | 
    Where-Object { $_.CommandLine -match "server.py" }

if ($OldProcs) {
    Write-Host "💀 Killing $($OldProcs.Count) stale processes..." -ForegroundColor Yellow
    $OldProcs | Stop-Process -Force
}

# 3. Environment Activation
$VenvPath = Join-Path $RepoRoot ".venv" "Scripts" "Activate.ps1"
if (Test-Path $VenvPath) {
    . $VenvPath
    Write-Host "✅ Virtual environment activated." -ForegroundColor Green
} else {
    Write-Error "❌ Virtual environment not found at $VenvPath! Run 'uv sync' first."
}

# 4. Launch
# -u uses unbuffered binary stdout/stderr, crucial for MCP log capturing
python -u src/server.py
```

### Idempotency & Cleanup

**Scripts must be re-runnable.**
-   Running `setup.sh` twice should not break anything.
-   Running `start.ps1` while the server is already running should restart it cleanly, not spawn a duplicate or fail with "Port in use".

### Cross-Platform Strategy

While we prefer PowerShell Core (`pwsh`), the reality of cloud deployments (Docker/Linux) requires Bash proficiency.
-   **Dev Environment (Windows)**: PowerShell is King.
-   **CI/CD (Linux)**: Bash is the standard.
-   **Hybrid**: We often wrap Bash scripts inside PowerShell for Windows compatibility or vice versa.

---

## 3. Global Context: Shell Evolution

*(Ingested from Wikipedia Research)*

### PowerShell (The Monad Manifesto)

PowerShell evolved from the **Monad Manifesto**, a whitepaper by **Jeffrey Snover** (Microsoft) in 2002. Snover realized that Windows administrators were automating tasks using GUI tools because existing CLI tools (cmd.exe, WSH) were text-based and fragile.

**The Core Insight**: Instead of piping text (`ls | grep`), pipe **Objects** (`Get-ChildItem | Where-Object`).
-   In Bash: `ls -l` returns text. To get file size, you must parse columns 5-9 (fragile).
-   In PowerShell: `Get-ChildItem` returns `.NET FileInfo` objects. To get size: `$file.Length` (robust).

**Evolution**:
-   **v1.0 (2006)**: Windows only. Revolutionary object pipeline.
-   **v6.0 (2016)**: "PowerShell Core". Open-sourced, cross-platform (Linux/macOS), built on .NET Core.
-   **v7.0+ (2020+)**: The unification. Replaces Windows PowerShell 5.1 as the SOTA standard.

### Bash (The GNU Standard)

The **Bourne Again SHell (Bash)** was written by **Brian Fox** for the GNU Project as a free software replacement for the Bourne shell (`sh`). Released in 1989, it became the default shell on Linux and macOS (until recently).

**Philosophy**: "Everything is a file (or a stream of text)."
-   Composition via **Pipes** (`|`).
-   Small, single-purpose tools (`grep`, `sed`, `awk`, `cut`) combined to perform complex logic.
-   **Simplicity**: Bash scripts are incredibly portable across Unix-like systems.

### Objects vs. Text Streams

This is the fundamental divide.
-   **Bash** is faster for raw text processing and file manipulation.
-   **PowerShell** is superior for structured data (JSON, XML, CSV) and system administration (Registry, Services, WMI).

In the Antigravity Fleet, we leverage **both**:
-   Bash for low-level Docker entrypoints.
-   PowerShell for complex orchestration logic involving JSON/API interactions.

---

## 4. Fleet Integration Patterns

### Wait-For-Port Strategy

When orchestrating multiple services (e.g., launching a database before the API), scripts must wait for ports to open.

**Bash (`wait-for-it.sh` pattern):**
```bash
until nc -z localhost 5432; do
  echo "Waiting for Postgres..."
  sleep 1
done
```

**PowerShell:**
```powershell
while (-not (Test-NetConnection -ComputerName localhost -Port 5432 -InformationLevel Quiet)) {
    Write-Host "Waiting for Postgres..."
    Start-Sleep -Seconds 1
}
```

### Signal Handling (Graceful Shutdown)

MCP servers must shut down cleanly to release file locks and sockets. Scripts must trap signals.

**Bash:**
```bash
trap 'kill $(jobs -p)' SIGINT SIGTERM EXIT
```

**PowerShell:**
There is no direct `trap` for Ctrl+C in standard scripts without using `[Console]::CancelKeyPress`, but `Stop-Process` propagates signals correctly to child processes if handled well.

---

## 5. Advanced Patterns

### Argument Parsing

**PowerShell (`param` block - The Gold Standard):**
```powershell
param (
    [Parameter(Mandatory=$true)]
    [string]$Target,

    [int]$Retries = 3
)
```
This automatically provides `-Target`, `-Retries`, input validation, and help text.

**Bash (`getopts` - The Old Way):**
```bash
while getopts ":t:r:" opt; do
  case $opt in
    t) target="$OPTARG" ;;
    r) retries="$OPTARG" ;;
    \?) echo "Invalid option -$OPTARG" >&2 ;;
  esac
done
```
*Note: Bash argument parsing is verbose and error-prone compared to PowerShell.*

### Error Handling Strategies

**Bash Strict Mode:**
Always start Bash scripts with:
```bash
set -euo pipefail
```
-   `-e`: Exit immediately if a command exits with a non-zero status.
-   `-u`: Treat unset variables as an error.
-   `-o pipefail`: Return value of a pipeline is the status of the last command to exit with a non-zero status.

**PowerShell Strict Mode:**
```powershell
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
```

---

## 6. Security Best Practices

1.  **Execution Policies**: On Windows servers, we use `Set-ExecutionPolicy RemoteSigned` to allow local scripts but require signatures for downloaded ones.
2.  **No `curl | bash`**: Never pipe `curl` directly to `bash` in production scripts. Download, verify checksum/signature, then execute.
3.  **Secrets Management**: Never pass secrets as command-line arguments (they show up in process lists). Use environment variables.

---

## 7. Reference Material

-   [PowerShell Documentation](https://learn.microsoft.com/en-us/powershell/)
-   [GNU Bash Manual](https://www.gnu.org/software/bash/manual/)
-   [ShellCheck (Static Analysis for Shell Scripts)](https://www.shellcheck.net/)
-   [PSScriptAnalyzer](https://github.com/PowerShell/PSScriptAnalyzer)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
