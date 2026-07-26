import logging
import subprocess

logger = logging.getLogger("docs_mcp.backend.process_manager")


class ProcessManager:
    """Singleton-style manager for tracking and controlling background subprocesses."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.registry = {}
        return cls._instance

    def register(self, key: str, proc: subprocess.Popen):
        """Register a new subprocess."""
        logger.info(f"Registering process {key} (PID: {proc.pid})")
        self.registry[key] = proc

    def list_active(self) -> list[dict]:
        """List and clean dead processes, returning active ones."""
        active_procs = []
        to_remove = []
        for key, proc in self.registry.items():
            if proc.poll() is not None:
                to_remove.append(key)
            else:
                active_procs.append({"id": key, "pid": proc.pid, "status": "running"})

        for key in to_remove:
            logger.debug(f"Cleaning up dead process {key}")
            del self.registry[key]

        return active_procs

    def cleanup_all(self) -> None:
        """Stop all registered processes."""
        keys = list(self.registry.keys())
        for key in keys:
            self.stop_process(proc_id=key)
        logger.info(f"Cleaned up {len(keys)} processes")

    def stop_process(self, proc_id: str | None = None, pid: int | None = None) -> bool:
        """Stop a process by ID or PID using absolute taskkill."""
        target_key = None
        target_pid = None

        if proc_id and proc_id in self.registry:
            target_key = proc_id
            target_pid = self.registry[proc_id].pid
        elif pid:
            for key, p in self.registry.items():
                if p.pid == pid:
                    target_key = key
                    target_pid = pid
                    break

        if target_pid:
            try:
                # Use taskkill for Windows to ensure tree cleanup
                logger.info(f"Stopping process {target_key} (PID: {target_pid})")
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(target_pid)], check=False)  # noqa: S603, S607
                if target_key:
                    del self.registry[target_key]
                return True
            except Exception as e:
                logger.error(f"Failed to stop process {target_pid}: {e}")
                return False

        return False


# Global instance for easy import
process_manager = ProcessManager()
