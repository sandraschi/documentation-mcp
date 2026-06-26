# PowerShell Scripting Standards (SOTA)

## 1. Error Handling (MANDATORY)

### 1.1. Principles
1.  **NEVER fail silently**: All scripts must use `$ErrorActionPreference = "Stop"`.
2.  **NEVER exit without logging**: Log all exceptions with full context (message, type, stack trace).
3.  **Graceful Degradation**: Continue on partial failures where appropriate using individual `try/catch` blocks.
4.  **Actionable Feedback**: Provide paths, values, and potential solutions in error messages.

### 1.2. Pattern: Exponential Backoff Retry
Always implement retries for transient failures (network, file locks):

```powershell
function Invoke-WithRetry {
    param(
        [scriptblock]$ScriptBlock,
        [string]$OperationName,
        [int]$MaxRetries = 3,
        [int]$InitialDelaySeconds = 2
    )
    
    $attempt = 0
    $delay = $InitialDelaySeconds
    
    while ($attempt -le $MaxRetries) {
        try {
            return & $ScriptBlock
        } catch {
            $attempt++
            if ($attempt -gt $MaxRetries) {
                Write-ErrorLog "Operation '$OperationName' failed after $MaxRetries retries" "Error" $_
                throw
            }
            
            Write-ErrorLog "Operation '$OperationName' failed (attempt $attempt/$MaxRetries). Retrying in $delay seconds..." "Warning" $_
            Start-Sleep -Seconds $delay
            $delay = [math]::Min($delay * 2, 60) # Exponential backoff
        }
    }
}
```

## 2. Resource Management

- **Prerequisite Validation**: Test paths, permissions, and disk space *before* starting operations.
- **Cleanup**: Use `finally` blocks to close handles, dispose objects, and remove partial temp files.

## 3. Script Structure

Every SOTA script MUST include:
1.  **SYNOPSIS/DESCRIPTION**: Proper PowerShell Help headers.
2.  **CmdletBinding**: Enable standard parameters like `-Verbose`, `-ErrorAction`.
3.  **Helper Functions**: Dedicated regions for logging, validation, and retry logic.
4.  **Main Try/Catch**: Wrap the entire execution for fatal error logging.
5.  **Exit Codes**: `0` for success (including partial success), `1` for fatal failure.

## 4. Why This Matters
- **Production reliability**: Scripts don't crash unexpectedly.
- **Easier debugging**: Full error context in logs.
## 5. Process Orchestration: Background Polling

To ensure a smooth user experience in distributed systems (e.g., waiting for Vite before opening a browser), use non-blocking background polling tasks.

### 5.1. Pattern: Poll and Open Browser
This pattern pings a URL in a separate, hidden PowerShell instance for up to 60 seconds.

```powershell
# Definition of the target URL and the polling command
$targetUrl = "http://127.0.0.1:$WebPort/"
$pollScript = "for (`$i = 0; `$i -lt 60; `$i++) {
    try {
        `$null = Invoke-WebRequest -Uri '$targetUrl' -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
        Start-Process '$targetUrl'
        exit
    } catch {
        Start-Sleep -Seconds 1
    }
}"

# Launch the polling task in a hidden background process
Start-Process powershell -ArgumentList "-NoProfile", "-WindowStyle", "Hidden", "-Command", $pollScript
```

### 5.2. Why Use This?
- **Zero Latency**: The main script can continue or finish without waiting for the webapp to be fully ready.
- **Resilience**: Eliminates "Connection Refused" errors by only launching the browser once the port is listening.
- **Background execution**: The `-WindowStyle Hidden` flag prevents extra terminal windows from flashing.

## 6. Unicode (MANDATORY)

**EM DASH is never allowed** in `.ps1`, `.psm1`, `.bat`, or `justfile` - not in comments, not in strings.

Fleet rule and checker: [patterns/unicode_safety.md](./patterns/unicode_safety.md).

```powershell
powershell.exe -NoProfile -File D:\Dev\repos\mcp-central-docs\scripts\check-unicode-safe.ps1 -RepoPath .
```
