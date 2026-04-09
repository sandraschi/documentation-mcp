# Restart Claude Desktop & Check MCP Server Script

**Location**: `scripts/restart_claude_and_check.py`  
**Status**: âœ… Tested and working  
**Source**: Adapted from calibremcp, tested on database-operations-mcp

---

## ðŸ“‹ Overview

This script automates the process of:
1. **Pre-checking** if your MCP server will load (catches import errors early)
2. **Restarting Claude Desktop** (stops and starts)
3. **Monitoring logs** for successful MCP server startup
4. **Verifying** the restart worked (empty chat window = fresh restart)

## âœ… Verification Method

**Key test**: If Claude Desktop has text in the chat window before running the script, and the chat window is **EMPTY** after the script runs, the restart succeeded!

- âœ… **Empty chat** = Successful restart
- âŒ **Chat still has text** = Restart failed (Claude didn't actually restart)

---

## ðŸš€ Quick Start

### 1. Copy Script to Your Repo

```powershell
# From your MCP server repo
Copy-Item "D:\Dev\repos\mcp-central-docs\scripts\restart_claude_and_check.py" "scripts\restart_claude_and_check.py"
```

### 2. Adapt for Your MCP Server

Edit the script and adapt these two functions:

#### A. `pre_check_server()` (Lines ~287-340)

Replace the placeholder with your MCP server imports:

```python
def pre_check_server():
    """Pre-check if server will load before restarting Claude."""
    print("\n[0/4] Pre-checking server load...")
    
    # ADAPT: Set your log file path
    log_file = Path("logs/your-mcp-server.log")  # Change this
    
    try:
        import sys
        src_path = Path(__file__).parent.parent / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
        
        # ADAPT: Import your MCP config
        from your_mcp.config.mcp_config import mcp
        
        if mcp is None:
            print("[FAIL] MCP instance is None")
            return False, log_size_before
        
        # ADAPT: Import your main server module
        from your_mcp.main import YourMCPServer
        server = YourMCPServer()
        
        print(f"[OK] Pre-check passed - MCP instance '{mcp.name}' loaded")
        return True, log_size_before
    except Exception as e:
        print(f"[FAIL] Pre-check failed: {e}")
        return False, log_size_before
```

#### B. `monitor_logs_for_startup()` Call (Lines ~407-412)

Pass your log paths and indicators:

```python
success = monitor_logs_for_startup(
    timeout_seconds=args.timeout,
    check_recent=args.no_restart,
    log_file_size_before_check=log_file_size_before,
    log_file_paths=[
        Path("logs/your-mcp-server.log"),  # Your log file
        Path("http_test.log"),
    ],
    success_indicators=[
        "your success message",
        "tools registered",
        "server initialized",
    ],
    error_indicators=[
        "your error patterns",
        "failed to import",
        "server_startup_error",
    ],
)
```

### 3. Run the Script

```powershell
# Basic usage
python scripts/restart_claude_and_check.py

# Skip pre-check
python scripts/restart_claude_and_check.py --skip-precheck

# Only check logs (don't restart)
python scripts/restart_claude_and_check.py --no-restart

# Custom timeout
python scripts/restart_claude_and_check.py --timeout 60
```

---

## ðŸ“ Examples

### Example 1: database-operations-mcp

```python
def pre_check_server():
    log_file = Path("logs/database-operations-mcp.log")
    log_size_before = log_file.stat().st_size if log_file.exists() else None
    
    from database_operations_mcp.config.mcp_config import mcp
    from database_operations_mcp.main import DatabaseOperationsMCP
    server = DatabaseOperationsMCP()
    
    print(f"[OK] Pre-check passed - MCP instance '{mcp.name}' loaded")
    return True, log_size_before
```

```python
success = monitor_logs_for_startup(
    timeout_seconds=args.timeout,
    check_recent=args.no_restart,
    log_file_size_before_check=log_file_size_before,
    log_file_paths=[
        Path("logs/database-operations-mcp.log"),
        Path("http_test.log"),
    ],
    success_indicators=[
        "FastMCP 3.1.1+ persistent storage initialized",
        "all portmanteau tools imported successfully",
    ],
)
```

### Example 2: calibremcp

```python
def pre_check_server():
    log_file = Path("logs/calibremcp.log")
    # ... calibre-specific imports
```

---

## ðŸŽ¯ What the Script Does

### Step 1: Pre-Check
- Imports your MCP server modules
- Verifies MCP instance loads
- Catches import errors **before** restarting Claude
- Saves log file size (to avoid checking pre-check logs)

### Step 2: Stop Claude Desktop
- Uses `taskkill /F /IM Claude.exe`
- No UAC required
- Waits 2 seconds for process to terminate

### Step 3: Start Claude Desktop
- Auto-detects Claude path:
  - `%APPDATA%/Local/Programs/claude-desktop/Claude.exe`
  - `%APPDATA%/Roaming/npm/claude`
  - `C:/Program Files/Claude/Claude.exe`
  - Checks PATH
- Starts Claude Desktop
- **Key**: Chat window will be EMPTY if restart worked!

### Step 4: Monitor Logs
- Watches log file for success/error indicators
- Checks recent logs (if `--no-restart`)
- Watches for new log entries (if restarting)
- Reports success or failure

---

## âœ… Success Indicators

The script looks for these in logs (adapt for your server):

**Success:**
- "registered" + "tools"
- "server initialized"
- "storage initialized" (FastMCP 3.1.1++)
- "all tools imported successfully"

**Errors:**
- "error" + ("startup" or "import")
- "exception"
- "traceback"
- "failed to import"

---

## ðŸ”§ Customization

### Custom Log File Location

```python
log_file_paths = [
    Path("logs/custom-name.log"),
    Path("custom/path/to/logs.log"),
]
```

### Custom Success/Error Messages

```python
success_indicators = [
    "your custom success message",
    "your server started",
]

error_indicators = [
    "your custom error pattern",
    "your failure message",
]
```

### Custom Claude Path

```powershell
python scripts/restart_claude_and_check.py --claude-path "C:/Custom/Path/Claude.exe"
```

---

## ðŸ§ª Testing

### Test Restart (Most Important)

1. **Before**: Make sure Claude Desktop has text in chat
2. **Run**: `python scripts/restart_claude_and_check.py`
3. **After**: Check Claude Desktop - chat should be **EMPTY** âœ…

If chat is empty = restart worked!  
If chat still has text = restart failed.

### Test Pre-Check Only

```powershell
# Just check if server will load (don't restart)
python scripts/restart_claude_and_check.py --skip-precheck --no-restart
```

---

## ðŸ“Š Output Examples

### Successful Run

```
============================================================
Claude Desktop Restart & MCP Server Check
Database Operations MCP
============================================================

[0/4] Pre-checking server load...
[OK] Pre-check passed - MCP instance 'database-operations-mcp' loaded

[1/4] Stopping Claude Desktop (using taskkill)...
[OK] Claude Desktop stopped

[2/4] Starting Claude Desktop...
[OK] Started Claude Desktop
[INFO] âš ï¸  Check Claude Desktop - chat window should be EMPTY (fresh restart)

[3/4] Monitoring logs for MCP server startup...
[SUCCESS] MCP server started successfully (new log entry)!

============================================================
[SUCCESS] MCP server loaded successfully in Claude!
```

### Failed Run

```
[FAIL] Pre-check failed - Import error: No module named 'your_module'
[WARN] Server may not load in Claude. Fix import issues first!

Continue anyway? (y/N): n
[STOP] Pre-check failed. Fix issues before restarting Claude.
```

---

## ðŸ› Troubleshooting

### Claude Path Not Found

**Solution**: Specify path manually:
```powershell
python scripts/restart_claude_and_check.py --claude-path "C:/path/to/Claude.exe"
```

### Log File Not Found

**Solution**: Update `log_file_paths` in `monitor_logs_for_startup()` call

### Pre-Check Fails

**Solution**: Fix import errors first, then run script

### Chat Window Not Empty After Restart

**Issue**: Claude didn't actually restart

**Check**:
1. Is Claude still running? (Check Task Manager)
2. Did `taskkill` actually stop it?
3. Try stopping Claude manually, then run script with `--no-restart`

---

## ðŸ“š Reference Implementations

- **calibremcp**: `D:\Dev\repos\calibremcp\scripts\restart_claude_and_check.py`
- **database-operations-mcp**: `D:\Dev\repos\database-operations-mcp\scripts\restart_claude_and_check.py`

---

## ðŸ”„ Updating the Script

When FastMCP or MCP standards change:
1. Update this script in central-docs
2. Propagate to all MCP repos
3. Test on one repo first
4. Document changes

---

**Last Updated**: 2025-01-XX  
**Tested On**: database-operations-mcp, calibremcp  
**Status**: âœ… Production-ready (after adaptation)


