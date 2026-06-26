import logging
from collections import deque


class MemoryLogHandler(logging.Handler):
    """In-memory ring buffer for log records, accessible via /api/logs."""

    def __init__(self, capacity: int = 500):
        super().__init__()
        self.buffer = deque(maxlen=capacity)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.buffer.append(msg)
        except Exception:
            self.handleError(record)

    def get_logs(self, limit: int = 100) -> list[str]:
        lines = list(self.buffer)
        return lines[-limit:]


_log_handler: MemoryLogHandler | None = None


def install_log_buffer(level: int = logging.INFO) -> MemoryLogHandler:
    global _log_handler
    if _log_handler is not None:
        return _log_handler

    _log_handler = MemoryLogHandler(capacity=500)
    _log_handler.setLevel(level)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    _log_handler.setFormatter(fmt)

    root = logging.getLogger()
    root.addHandler(_log_handler)
    return _log_handler


def get_log_buffer() -> MemoryLogHandler | None:
    return _log_handler
