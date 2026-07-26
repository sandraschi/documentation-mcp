"""
MCP Orphan Guard - Prevents MCP servers from becoming zombie processes.

When MCP clients (Claude Desktop, Cursor, Windsurf, Zed) crash or exit abruptly,
the stdio connection may not cleanly close, leaving orphan Python processes
consuming CPU and memory.

This module provides multiple detection mechanisms:
1. Parent process monitoring - exits if parent process dies
2. Stdin EOF detection - exits when stdin pipe closes
3. Idle timeout - exits after period of inactivity
4. Heartbeat checking - periodic liveness verification

Usage:
    from mcp_orphan_guard import OrphanGuard

    guard = OrphanGuard(idle_timeout_minutes=30)
    guard.start()  # Call before mcp.run()

    # In your MCP server's main:
    mcp.run()  # Guard runs in background thread

Source: D:\\Dev\repos\\myai\\core\\dashboard\\mcp_orphan_guard.py
Documentation: docs/patterns/MCP_ORPHAN_GUARD_PATTERN.md
"""

import atexit
import logging
import os
import signal
import sys
import threading
import time
from collections.abc import Callable
from datetime import datetime, timedelta

# Guard against UnicodeEncodeError when this module's logger emits non-ASCII glyphs
# (e.g. the 🛡️ shield in status messages) on a Windows cp1252-bound stderr. Done before
# the module logger is configured so nothing downstream races us.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

logger = logging.getLogger("mcp_orphan_guard")

# Windows-specific imports
if sys.platform == "win32":
    import ctypes

    # Windows API for checking if process exists
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    kernel32 = ctypes.windll.kernel32


def is_process_alive(pid: int) -> bool:
    """Check if a process with given PID is still running."""
    if sys.platform == "win32":
        try:
            handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if handle:
                kernel32.CloseHandle(handle)
                return True
            return False
        except Exception:
            return False
    else:
        # Unix-like systems
        try:
            os.kill(pid, 0)  # Signal 0 doesn't kill, just checks
            return True
        except OSError:
            return False


class OrphanGuard:
    """
    Guards against MCP server processes becoming orphans.

    Monitors multiple conditions and terminates gracefully when
    the parent client is detected as gone.
    """

    def __init__(
        self,
        idle_timeout_minutes: int = 30,
        check_interval_seconds: int = 5,
        on_shutdown: Callable | None = None,
    ):
        """
        Initialize the orphan guard.

        Args:
            idle_timeout_minutes: Minutes of inactivity before self-termination.
                                  Set to 0 to disable idle timeout.
            check_interval_seconds: How often to check for orphan conditions.
            on_shutdown: Optional callback to run before shutdown.
        """
        self.idle_timeout = (
            timedelta(minutes=idle_timeout_minutes) if idle_timeout_minutes > 0 else None
        )
        self.check_interval = check_interval_seconds
        self.on_shutdown = on_shutdown

        self.parent_pid = os.getppid()
        self.last_activity = datetime.now()
        self._running = False
        self._thread: threading.Thread | None = None
        self._shutdown_requested = False

        # Track startup time
        self.started_at = datetime.now()

        logger.info(f"🛡️ OrphanGuard initialized - Parent PID: {self.parent_pid}")

    def record_activity(self):
        """Call this when MCP tool is invoked to reset idle timer."""
        self.last_activity = datetime.now()

    def start(self):
        """Start the orphan guard background monitoring."""
        if self._running:
            return

        self._running = True

        # Register cleanup on exit
        atexit.register(self._cleanup)

        # Setup signal handlers
        self._setup_signal_handlers()

        # Start background monitor thread
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

        # Start stdin monitor in separate thread
        stdin_thread = threading.Thread(target=self._monitor_stdin, daemon=True)
        stdin_thread.start()

        logger.info(f"🛡️ OrphanGuard started - monitoring parent PID {self.parent_pid}")

    def stop(self):
        """Stop the orphan guard."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)

    def _setup_signal_handlers(self):
        """Setup handlers for termination signals."""

        def handle_signal(signum, frame):
            logger.info(f"🛡️ Received signal {signum}, initiating graceful shutdown")
            self._initiate_shutdown(f"Received signal {signum}")

        # Handle common termination signals
        if sys.platform != "win32":
            signal.signal(signal.SIGTERM, handle_signal)
            signal.signal(signal.SIGHUP, handle_signal)
        signal.signal(signal.SIGINT, handle_signal)

    def _monitor_stdin(self):
        """Monitor stdin for EOF - indicates parent disconnected."""
        try:
            while self._running:
                # Try to read from stdin (will block)
                # On Windows, stdin.read() on a closed pipe may return empty or raise
                if sys.stdin.closed:
                    logger.info("🛡️ Stdin closed - parent disconnected")
                    self._initiate_shutdown("Stdin closed")
                    return

                # Check if stdin is at EOF without blocking (Windows workaround)
                if sys.platform == "win32":
                    import msvcrt

                    if msvcrt.kbhit():
                        try:
                            char = sys.stdin.read(1)
                            if not char:  # EOF
                                self._initiate_shutdown("Stdin EOF")
                                return
                        except Exception:
                            pass
                    time.sleep(0.5)
                else:
                    # Unix: use select for non-blocking check
                    import select

                    readable, _, _ = select.select([sys.stdin], [], [], 1.0)
                    if readable:
                        try:
                            data = sys.stdin.read(1)
                            if not data:  # EOF
                                self._initiate_shutdown("Stdin EOF")
                                return
                        except Exception:
                            self._initiate_shutdown("Stdin read error")
                            return
        except Exception as e:
            logger.debug(f"Stdin monitor exception: {e}")

    def _monitor_loop(self):
        """Main monitoring loop running in background thread."""
        while self._running and not self._shutdown_requested:
            try:
                # Check 1: Parent process still alive?
                if not is_process_alive(self.parent_pid):
                    logger.warning(f"🛡️ Parent process {self.parent_pid} is gone!")
                    self._initiate_shutdown("Parent process terminated")
                    return

                # Check 2: Idle timeout exceeded?
                if self.idle_timeout:
                    idle_time = datetime.now() - self.last_activity
                    if idle_time > self.idle_timeout:
                        logger.warning(f"🛡️ Idle timeout exceeded ({idle_time})")
                        self._initiate_shutdown(f"Idle timeout ({self.idle_timeout})")
                        return

                # Log status periodically (every 5 minutes)
                uptime = datetime.now() - self.started_at
                if uptime.total_seconds() % 300 < self.check_interval:
                    idle_time = datetime.now() - self.last_activity
                    logger.debug(
                        f"🛡️ Guard status: uptime={uptime}, idle={idle_time}, "
                        f"parent={self.parent_pid} alive={is_process_alive(self.parent_pid)}"
                    )

            except Exception as e:
                logger.error(f"🛡️ Monitor error: {e}")

            time.sleep(self.check_interval)

    def _initiate_shutdown(self, reason: str):
        """Initiate graceful shutdown."""
        if self._shutdown_requested:
            return

        self._shutdown_requested = True
        logger.info(f"🛡️ Initiating shutdown: {reason}")

        # Run shutdown callback if provided
        if self.on_shutdown:
            try:
                self.on_shutdown()
            except Exception as e:
                logger.error(f"Shutdown callback error: {e}")

        self._cleanup()

        # Give a moment for cleanup
        time.sleep(0.5)

        # Exit
        logger.info("🛡️ MCP server terminating")
        os._exit(0)  # Force exit to ensure termination

    def _cleanup(self):
        """Cleanup resources."""
        self._running = False


# Convenience function to add orphan guard to any FastMCP server
def protect_mcp_server(
    mcp_instance,
    idle_timeout_minutes: int = 30,
    check_interval_seconds: int = 5,
):
    """
    Add orphan protection to a FastMCP server instance.

    Args:
        mcp_instance: The FastMCP instance
        idle_timeout_minutes: Minutes before idle shutdown (0 to disable)
        check_interval_seconds: Check interval

    Returns:
        OrphanGuard instance (already started)

    Example:
        from fastmcp import FastMCP
        from mcp_orphan_guard import protect_mcp_server

        mcp = FastMCP("My Server")
        guard = protect_mcp_server(mcp)

        @mcp.tool()
        async def my_tool():
            guard.record_activity()  # Reset idle timer
            ...

        mcp.run()
    """
    guard = OrphanGuard(
        idle_timeout_minutes=idle_timeout_minutes,
        check_interval_seconds=check_interval_seconds,
    )
    guard.start()

    logger.info(
        f"🛡️ MCP server protected - idle timeout: {idle_timeout_minutes}min, "
        f"parent PID: {guard.parent_pid}"
    )

    return guard


# Self-test when run directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print(f"Parent PID: {os.getppid()}")
    print(f"My PID: {os.getpid()}")
    print(f"Parent alive: {is_process_alive(os.getppid())}")

    guard = OrphanGuard(idle_timeout_minutes=1)  # 1 minute for testing
    guard.start()

    print("Guard started. Will exit in 1 minute if idle, or when parent dies.")
    print("Press Ctrl+C to test signal handling.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted!")
