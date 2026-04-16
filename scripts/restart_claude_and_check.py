"""
Restart Claude Desktop and verify MCP server loads successfully.

This script:
1. Pre-checks if server will load (optional but recommended)
2. Stops Claude Desktop
3. Restarts Claude Desktop
4. Monitors logs for successful MCP server startup
5. Reports success/failure

Note: Restarting Claude requires stopping the process (works without UAC).
Starting Claude may require UAC if installed in Program Files.

USAGE:
    # Generic usage - adapt pre_check_server() and monitor_logs_for_startup() for your MCP server
    python scripts/restart_claude_and_check.py

    # Skip pre-check
    python scripts/restart_claude_and_check.py --skip-precheck

    # Only check logs without restarting
    python scripts/restart_claude_and_check.py --no-restart

    # Custom timeout
    python scripts/restart_claude_and_check.py --timeout 60

    # Specify Claude path
    python scripts/restart_claude_and_check.py --claude-path "C:/path/to/Claude.exe"
"""

import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path


def find_claude_process():
    """Find Claude Desktop process."""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Claude.exe", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and "Claude.exe" in result.stdout:
            return True
        return False
    except Exception as e:
        print(f"[WARN] Could not check Claude process: {e}")
        return None


def stop_claude():
    """Stop Claude Desktop using taskkill.

    Uses Windows taskkill command to forcefully terminate Claude.exe.
    No UAC required - works without elevation.
    """
    print("\n[1/4] Stopping Claude Desktop (using taskkill)...")
    try:
        result = subprocess.run(["taskkill", "/F", "/IM", "Claude.exe"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("[OK] Claude Desktop stopped")
            time.sleep(2)  # Wait for process to fully terminate
            return True
        elif "not found" in result.stdout.lower() or "not running" in result.stdout.lower():
            print("[INFO] Claude Desktop was not running")
            return True
        else:
            print(f"[WARN] Unexpected response: {result.stdout}")
            return False
    except subprocess.TimeoutExpired:
        print("[WARN] Timeout stopping Claude (process may be hung)")
        return False
    except Exception as e:
        print(f"[FAIL] Error stopping Claude: {e}")
        return False


def start_claude(claude_path_arg=None):
    """Start Claude Desktop.

    Args:
        claude_path_arg: Optional path to Claude.exe (for --claude-path option)
    """
    print("\n[2/4] Starting Claude Desktop...")

    # Use provided path if given
    if claude_path_arg:
        claude_path = Path(claude_path_arg)
        if claude_path.exists():
            print(f"[INFO] Using specified Claude path: {claude_path}")
        else:
            print(f"[FAIL] Specified Claude path does not exist: {claude_path}")
            return False
    else:
        # Common Claude Desktop install locations
        possible_paths = [
            Path.home() / "AppData/Local/Programs/claude-desktop/Claude.exe",
            Path.home() / "AppData/Roaming/npm/claude",
            Path("C:/Program Files/Claude/Claude.exe"),
            Path("C:/Program Files (x86)/Claude/Claude.exe"),
        ]

        # Check if Claude is in PATH (less common but possible)
        try:
            result = subprocess.run(["where", "Claude"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                found_path = Path(result.stdout.strip().split("\n")[0])
                if found_path.exists():
                    possible_paths.insert(0, found_path)
        except Exception:
            pass

        # Try to find Claude
        claude_path = None
        for path in possible_paths:
            if path.exists():
                claude_path = path
                break

        if not claude_path:
            print("[FAIL] Could not find Claude Desktop executable")
            print("\nPlease start Claude Desktop manually, then run:")
            print("  python scripts/restart_claude_and_check.py --no-restart")
            print("\nOr specify Claude path with --claude-path option")
            return False

    try:
        # Start Claude Desktop
        print(f"[INFO] Starting Claude Desktop from: {claude_path}")
        subprocess.Popen([str(claude_path)], shell=True)
        print("[OK] Started Claude Desktop")
        print("[INFO] Waiting for Claude to initialize...")
        print("[INFO] ⚠️  Check Claude Desktop - chat window should be EMPTY (fresh restart)")
        time.sleep(5)  # Give Claude time to start and connect to MCP
        return True
    except Exception as e:
        print(f"[FAIL] Error starting Claude: {e}")
        print(f"[INFO] Try starting Claude manually from: {claude_path}")
        return False


def monitor_logs_for_startup(
    timeout_seconds=30,
    check_recent=True,
    log_file_size_before_check=None,
    log_file_paths=None,
    success_indicators=None,
    error_indicators=None,
):
    """Monitor logs for successful MCP server startup.

    Args:
        timeout_seconds: Timeout for watching new logs
        check_recent: If True, check recent logs (for --no-restart mode)
        log_file_size_before_check: Size of log file before script ran (to avoid checking our own logs)
        log_file_paths: List of possible log file paths (defaults to common locations)
        success_indicators: List of strings that indicate successful startup
        error_indicators: List of strings that indicate startup failure
    """
    print("\n[3/4] Monitoring logs for MCP server startup...")

    # Default log file paths if not provided
    if log_file_paths is None:
        log_file_paths = [
            Path("logs/mcp.log"),
            Path("logs/server.log"),
            Path("http_test.log"),
        ]

    # Default success indicators if not provided
    if success_indicators is None:
        success_indicators = [
            "registered",
            "tools registered",
            "server_startup",
            "mcp server initialized",
            "server started",
            "all tools imported successfully",
        ]

    # Default error indicators if not provided
    if error_indicators is None:
        error_indicators = [
            "error",
            "exception",
            "traceback",
            "importerror",
            "modulenotfounderror",
            "failed",
            "server_startup_error",
            "failed to import",
        ]

    # Check for log file
    log_file = None
    for log_path in log_file_paths:
        if log_path.exists():
            log_file = log_path
            break

    if not log_file:
        print("[WARN] Log file not found in expected locations")
        print(f"[INFO] Tried: {[str(p) for p in log_file_paths]}")
        print("[INFO] Server may not have started yet, or logs are elsewhere")
        return False

    # If we have a size limit, only read up to that point (avoid checking logs created by pre-check)
    max_bytes = log_file_size_before_check if log_file_size_before_check else None

    # First, check recent logs if requested (for --no-restart mode)
    if check_recent:
        print("[INFO] Checking LAST startup attempt in logs...")
        try:
            # Read log file up to the size before we started (to avoid our own pre-check logs)
            if max_bytes and log_file.stat().st_size > max_bytes:
                with open(log_file, "rb") as f:
                    content = f.read(max_bytes).decode("utf-8", errors="ignore")
                    # Get last complete line
                    if content and not content.endswith("\n"):
                        content = content.rsplit("\n", 1)[0] + "\n"
                    all_lines = content.splitlines(True)
            else:
                with open(log_file, encoding="utf-8", errors="ignore") as f:
                    all_lines = f.readlines()

                    # Check last few lines for success/error indicators
                    found_success = False
                    found_error = False

                    # Check last 50 lines (most recent)
                    for line in all_lines[-50:]:
                        line_lower = line.lower()

                        # Check for errors first
                        if any(indicator.lower() in line_lower for indicator in error_indicators):
                            if "error" in line_lower and ("startup" in line_lower or "import" in line_lower):
                                found_error = True
                                print("[FAIL] Last startup attempt FAILED:")
                                print(f"  {line.strip()[:200]}...")
                                return False

                        # Check for success
                        if any(indicator.lower() in line_lower for indicator in success_indicators):
                            if (
                                "registered" in line_lower
                                or "tools imported" in line_lower
                                or "initialized" in line_lower
                            ):
                                found_success = True
                                print("[SUCCESS] Last startup attempt succeeded!")
                                print(f"  {line.strip()[:200]}...")
                                return True

                    if found_success:
                        return True
                    elif found_error:
                        return False
                    else:
                        print("[WARN] Could not determine success/failure from recent logs")
                        print("[INFO] Check logs manually for startup messages")
                        return False

        except Exception as e:
            print(f"[WARN] Error checking recent logs: {e}")

    # If no recent success/error found, monitor for new entries
    start_time = datetime.now()
    timeout = timedelta(seconds=timeout_seconds)

    last_position = log_file.stat().st_size if log_file.exists() else 0

    print(f"[INFO] Watching log file: {log_file}")
    print(f"[INFO] Timeout: {timeout_seconds} seconds")

    while datetime.now() - start_time < timeout:
        try:
            # Check for new log entries
            if log_file.exists():
                current_size = log_file.stat().st_size
                if current_size > last_position:
                    # Read new log entries
                    with open(log_file, encoding="utf-8", errors="ignore") as f:
                        f.seek(last_position)
                        new_lines = f.readlines()
                        last_position = current_size

                        # Check for success or error
                        for line in new_lines:
                            line_lower = line.lower()

                            # Check for errors first
                            if any(indicator.lower() in line_lower for indicator in error_indicators):
                                if "error" in line_lower and ("startup" in line_lower or "import" in line_lower):
                                    print("\n[FAIL] Error detected in new logs:")
                                    print(f"  {line.strip()[:200]}...")
                                    return False

                            # Check for success
                            if any(indicator.lower() in line_lower for indicator in success_indicators):
                                if (
                                    "registered" in line_lower
                                    or "tools imported" in line_lower
                                    or "initialized" in line_lower
                                ):
                                    print("\n[SUCCESS] MCP server started successfully (new log entry)!")
                                    print(f"  {line.strip()[:200]}...")
                                    return True
        except Exception as e:
            print(f"[WARN] Error reading log: {e}")

        time.sleep(1)

    print(f"\n[WARN] Timeout after {timeout_seconds} seconds")
    print("[INFO] Check logs manually or verify Claude Desktop MCP configuration")
    return False


def pre_check_server():
    """Pre-check if server will load before restarting Claude.

    ADAPT THIS FUNCTION for your MCP server:
    - Import your MCP config module
    - Import your main server module
    - Verify MCP instance and tool registration

    Returns:
        tuple: (success: bool, log_file_size_before: int | None)
    """
    print("\n[0/4] Pre-checking server load...")

    # ADAPT: Set your log file path
    log_file = Path("logs/mcp.log")  # Change to your log file
    log_size_before = log_file.stat().st_size if log_file.exists() else None

    try:
        import sys

        src_path = Path(__file__).parent.parent / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        # ADAPT: Import your MCP config
        # Example:
        # from your_mcp.config.mcp_config import mcp
        # from your_mcp.main import YourMCPServer

        print("[INFO] ADAPT pre_check_server() for your MCP server!")
        print("[INFO] Import your MCP config and main server module here")

        # Example implementation:
        # from your_mcp.config.mcp_config import mcp
        # if mcp is None:
        #     print("[FAIL] MCP instance is None")
        #     return False, log_size_before
        #
        # from your_mcp.main import YourMCPServer
        # server = YourMCPServer()
        # print(f"[OK] Pre-check passed - MCP instance '{mcp.name}' loaded")
        # return True, log_size_before

        # For now, return True to allow testing
        print("[WARN] Pre-check not implemented - returning True")
        return True, log_size_before

    except ImportError as e:
        print(f"[FAIL] Pre-check failed - Import error: {e}")
        print("[WARN] Server may not load in Claude. Fix import issues first!")
        response = input("\nContinue anyway? (y/N): ")
        return response.lower() == "y", log_size_before
    except Exception as e:
        print(f"[FAIL] Pre-check failed: {e}")
        print("[WARN] Server may not load in Claude. Fix issues first!")
        response = input("\nContinue anyway? (y/N): ")
        return response.lower() == "y", log_size_before


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Restart Claude Desktop and verify MCP server loads")
    parser.add_argument("--skip-precheck", action="store_true", help="Skip pre-check (not recommended)")
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout for log monitoring in seconds (default: 30)",
    )
    parser.add_argument("--claude-path", type=str, help="Path to Claude.exe (auto-detected if not specified)")
    parser.add_argument("--no-restart", action="store_true", help="Only monitor logs (do not restart Claude)")

    args = parser.parse_args()

    print("=" * 60)
    print("Claude Desktop Restart & MCP Server Check")
    print("Generic MCP Server Script - Adapt for your server")
    print("=" * 60)

    # Pre-check (and get log file size before we started)
    log_file_size_before = None
    if not args.skip_precheck:
        precheck_passed, log_file_size_before = pre_check_server()
        if not precheck_passed:
            print("\n[STOP] Pre-check failed. Fix issues before restarting Claude.")
            return 1

    # Restart Claude (unless --no-restart)
    if not args.no_restart:
        print("\n[INFO] ⚠️  IMPORTANT: Make sure Claude Desktop chat has text before restart")
        print("[INFO] After restart, chat window should be EMPTY (proving restart worked)")
        time.sleep(2)  # Give user time to see the message

        if not stop_claude():
            print("\n[STOP] Failed to stop Claude. Check manually.")
            return 1

        if not start_claude(args.claude_path):
            print("\n[STOP] Failed to start Claude. Start manually and check logs.")
            return 1

        print("\n[INFO] ✅ Claude Desktop should now be restarting...")
        print("[INFO] Check Claude Desktop window - chat should be EMPTY if restart succeeded!")
    else:
        print("\n[INFO] Skipping restart (--no-restart specified)")
        print("[INFO] Assuming Claude is already running")
        time.sleep(2)  # Give it a moment to connect

    # Monitor logs (check recent if --no-restart, wait for new if restarting)
    # ADAPT: Pass your log paths and indicators
    success = monitor_logs_for_startup(
        timeout_seconds=args.timeout,
        check_recent=args.no_restart,
        log_file_size_before_check=log_file_size_before,
        # log_file_paths=[Path("logs/your-mcp.log")],  # Uncomment and set your log path
        # success_indicators=["your", "success", "messages"],  # Uncomment and set your indicators
        # error_indicators=["your", "error", "messages"],  # Uncomment and set your indicators
    )

    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] MCP server loaded successfully in Claude!")
        return 0
    else:
        print("[FAILURE] Could not verify MCP server startup")
        print("\nNext steps:")
        print("  1. Check Claude Desktop console for errors")
        print("  2. Verify Claude Desktop MCP configuration")
        print("  3. Adapt pre_check_server() and monitor_logs_for_startup() in this script")
        return 1


if __name__ == "__main__":
    sys.exit(main())
