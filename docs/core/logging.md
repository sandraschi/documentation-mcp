# Logging Standards

## Overview
Comprehensive logging standards for MCP servers, ensuring consistent, structured, and actionable log output across all components.

## Logging Architecture

### Logger Hierarchy
```
mcp_server/
├── server.py           # Server-level logs
├── tools/
│   ├── base_tool.py    # Tool framework logs
│   └── specific_tools/ # Tool-specific logs
├── api/
│   └── endpoints.py    # API request/response logs
├── services/
│   └── external.py     # External service interaction logs
└── utils/
    └── helpers.py      # Utility function logs
```

### Logger Configuration
```python
# src/mcp_server/config/logging.py
import logging
import logging.config
import sys
from pathlib import Path
from typing import Dict, Any


def setup_logging(
    level: str = "INFO",
    log_file: str = None,
    json_format: bool = False
) -> None:
    """Configure logging for the application."""

    # Create formatters
    formatters = {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(module)s %(funcName)s %(lineno)d",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z"
        } if json_format else {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }

    # Create handlers
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "level": level,
            "formatter": "json" if json_format else "standard",
            "stream": "ext://sys.stderr"  # ✅ CRITICAL: MUST BE STDERR FOR MCP
        }
    }

    if log_file:
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": level,
            "formatter": "json" if json_format else "standard",
            "filename": log_file,
            "maxBytes": 10 * 1024 * 1024,  # 10MB
            "backupCount": 5
        }

    # Configure logging
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": formatters,
        "handlers": handlers,
        "root": {
            "level": level,
            "handlers": list(handlers.keys())
        },
        "loggers": {
            "mcp_server": {
                "level": level,
                "handlers": list(handlers.keys()),
                "propagate": False
            },
            "mcp": {
                "level": "WARNING",  # Reduce MCP protocol noise
                "handlers": list(handlers.keys()),
                "propagate": False
            }
        }
    }

    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    return logging.getLogger(f"mcp_server.{name}")
```

## Log Levels and Usage

### Standard Log Levels
```python
import logging

logger = logging.getLogger(__name__)

# DEBUG: Detailed information for debugging
logger.debug("Processing item %s with value %s", item_id, value)

# INFO: General information about application operation
logger.info("Server started successfully on port %d", port)

# WARNING: Something unexpected but not necessarily wrong
logger.warning("Configuration file not found, using defaults")

# ERROR: An error occurred that prevented an operation
logger.error("Failed to connect to database: %s", str(e))

# CRITICAL: A serious error that may prevent the application from continuing
logger.critical("Application shutting down due to unrecoverable error")
```

### Contextual Logging
```python
# src/mcp_server/tools/base_tool.py
import logging
from typing import Dict, Any
from mcp import Context


class BaseTool:
    """Base tool class with standardized logging."""

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    async def execute(self, ctx: Context, **kwargs) -> Dict[str, Any]:
        """Execute tool with comprehensive logging."""
        operation_id = kwargs.get('operation_id', 'unknown')

        self.logger.info(
            "Starting tool execution",
            extra={
                'operation_id': operation_id,
                'tool_name': self.__class__.__name__,
                'parameters': list(kwargs.keys())
            }
        )

        try:
            # Validate input
            self._validate_input(**kwargs)

            # Execute operation
            result = await self._execute_operation(**kwargs)

            self.logger.info(
                "Tool execution completed successfully",
                extra={
                    'operation_id': operation_id,
                    'result_type': type(result).__name__,
                    'execution_time_ms': self._get_execution_time()
                }
            )

            return result

        except Exception as e:
            self.logger.error(
                "Tool execution failed",
                exc_info=True,
                extra={
                    'operation_id': operation_id,
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            )
            raise

    def _validate_input(self, **kwargs) -> None:
        """Validate input parameters."""
        self.logger.debug("Validating input parameters", extra={'param_count': len(kwargs)})

    async def _execute_operation(self, **kwargs) -> Dict[str, Any]:
        """Execute the actual tool operation."""
        raise NotImplementedError

    def _get_execution_time(self) -> float:
        """Get execution time in milliseconds."""
        # Implementation for timing
        return 0.0
```

## Structured Logging

### Log Context and Correlation
```python
# src/mcp_server/utils/request_context.py
import contextvars
import uuid
from typing import Optional


# Context variables for request correlation
request_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar('request_id', default=None)
user_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar('user_id', default=None)
operation_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar('operation_id', default=None)


class RequestContext:
    """Context manager for request correlation."""

    def __init__(self, request_id: Optional[str] = None, user_id: Optional[str] = None):
        self.request_id = request_id or str(uuid.uuid4())
        self.user_id = user_id
        self.operation_id = str(uuid.uuid4())

    def __enter__(self):
        self._tokens = [
            request_id.set(self.request_id),
            user_id.set(self.user_id),
            operation_id.set(self.operation_id)
        ]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for token in self._tokens:
            token.__class__.reset(token)


def get_correlation_data() -> Dict[str, str]:
    """Get correlation data for logging."""
    return {
        'request_id': request_id.get(),
        'user_id': user_id.get(),
        'operation_id': operation_id.get()
    }


# Custom log formatter with correlation data
class CorrelationFormatter(logging.Formatter):
    """Log formatter that includes correlation data."""

    def format(self, record: logging.LogRecord) -> str:
        # Add correlation data to log record
        correlation = get_correlation_data()
        for key, value in correlation.items():
            if value and not hasattr(record, key):
                setattr(record, key, value)

        # Add to format string
        if hasattr(record, 'request_id'):
            original_format = self._fmt
            self._fmt = f"%(request_id)s - {original_format}"
            try:
                return super().format(record)
            finally:
                self._fmt = original_format
        else:
            return super().format(record)
```

### Structured Log Records
```python
# src/mcp_server/logging/structured.py
import logging
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class StructuredLogRecord:
    """Structured log record with typed fields."""

    event: str
    level: str
    timestamp: str
    message: str
    module: str
    function: str
    line: int

    # Correlation fields
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    operation_id: Optional[str] = None

    # Event-specific fields
    duration_ms: Optional[float] = None
    status_code: Optional[int] = None
    error_type: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None

    # Custom fields
    metadata: Optional[Dict[str, Any]] = None


class StructuredLogger:
    """Logger that creates structured log records."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.name = name

    def _log_structured(
        self,
        level: int,
        event: str,
        message: str,
        **kwargs
    ) -> None:
        """Log a structured event."""
        # Create structured record
        record = StructuredLogRecord(
            event=event,
            level=logging.getLevelName(level),
            timestamp="",  # Will be set by formatter
            message=message,
            module=self.name,
            function="",  # Will be set by logging framework
            line=0,       # Will be set by logging framework
            **kwargs
        )

        # Convert to dict for logging
        log_data = asdict(record)
        log_data['event'] = event

        # Remove None values
        log_data = {k: v for k, v in log_data.items() if v is not None}

        self.logger.log(level, json.dumps(log_data))

    def info_event(self, event: str, message: str, **kwargs) -> None:
        """Log an info-level structured event."""
        self._log_structured(logging.INFO, event, message, **kwargs)

    def error_event(self, event: str, message: str, **kwargs) -> None:
        """Log an error-level structured event."""
        self._log_structured(logging.ERROR, event, message, **kwargs)

    def performance_event(self, operation: str, duration_ms: float, **kwargs) -> None:
        """Log a performance event."""
        self._log_structured(
            logging.INFO,
            "performance",
            f"Operation {operation} completed",
            duration_ms=duration_ms,
            **kwargs
        )

    def api_request(self, method: str, path: str, status_code: int, duration_ms: float) -> None:
        """Log an API request."""
        self._log_structured(
            logging.INFO if status_code < 400 else logging.WARNING,
            "api_request",
            f"{method} {path}",
            status_code=status_code,
            duration_ms=duration_ms
        )

    def tool_execution(self, tool_name: str, success: bool, duration_ms: float, **kwargs) -> None:
        """Log tool execution."""
        level = logging.INFO if success else logging.ERROR
        event = "tool_success" if success else "tool_failure"

        self._log_structured(
            level,
            event,
            f"Tool {tool_name} {'succeeded' if success else 'failed'}",
            duration_ms=duration_ms,
            resource_type="tool",
            resource_id=tool_name,
            **kwargs
        )
```

## Log Analysis and Monitoring

### Log Aggregation
```python
# src/mcp_server/logging/aggregation.py
import logging
import threading
import time
from collections import defaultdict, deque
from typing import Dict, List, Any


class LogAggregator:
    """Aggregate logs for monitoring and analysis."""

    def __init__(self, max_entries: int = 1000):
        self.entries = deque(maxlen=max_entries)
        self.metrics = defaultdict(int)
        self.lock = threading.Lock()

    def add_entry(self, record: logging.LogRecord) -> None:
        """Add a log entry for aggregation."""
        with self.lock:
            # Store entry
            entry = {
                'timestamp': record.created,
                'level': record.levelname,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            }
            self.entries.append(entry)

            # Update metrics
            self.metrics['total_entries'] += 1
            self.metrics[f'level_{record.levelname.lower()}'] += 1
            self.metrics[f'module_{record.module}'] += 1

    def get_recent_entries(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent log entries."""
        with self.lock:
            return list(self.entries)[-limit:]

    def get_error_rate(self, time_window_seconds: int = 300) -> float:
        """Calculate error rate in the given time window."""
        with self.lock:
            cutoff_time = time.time() - time_window_seconds
            recent_entries = [e for e in self.entries if e['timestamp'] > cutoff_time]
            error_entries = [e for e in recent_entries if e['level'] in ['ERROR', 'CRITICAL']]

            if not recent_entries:
                return 0.0

            return len(error_entries) / len(recent_entries)

    def get_metrics(self) -> Dict[str, Any]:
        """Get current log metrics."""
        with self.lock:
            return dict(self.metrics)


# Global aggregator instance
log_aggregator = LogAggregator()


class AggregatingHandler(logging.Handler):
    """Logging handler that feeds into the aggregator."""

    def emit(self, record: logging.LogRecord) -> None:
        """Emit log record to aggregator."""
        log_aggregator.add_entry(record)
```

### Log Rotation and Retention
```python
# src/mcp_server/config/logging.py (continued)
from logging.handlers import TimedRotatingFileHandler


def setup_production_logging(log_dir: str = "logs") -> None:
    """Set up production logging with rotation."""

    # Ensure log directory exists
    Path(log_dir).mkdir(exist_ok=True)

    # Create rotating file handler
    file_handler = TimedRotatingFileHandler(
        filename=f"{log_dir}/mcp_server.log",
        when="midnight",      # Rotate at midnight
        interval=1,           # Every 1 interval (day)
        backupCount=30        # Keep 30 days of logs
    )

    # Set formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(request_id)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(AggregatingHandler())

    # Set appropriate level
    root_logger.setLevel(logging.INFO)
```

## Performance Logging

### Timing and Profiling
```python
# src/mcp_server/utils/performance.py
import time
import logging
import functools
from typing import Callable, Any
from contextlib import contextmanager


@contextmanager
def log_performance(operation: str, logger: Optional[logging.Logger] = None):
    """Context manager for performance logging."""
    if logger is None:
        logger = logging.getLogger(__name__)

    start_time = time.perf_counter()

    try:
        yield
    finally:
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000

        logger.info(
            f"Performance: {operation}",
            extra={
                'operation': operation,
                'duration_ms': duration_ms,
                'performance': True
            }
        )


def log_execution_time(logger: Optional[logging.Logger] = None):
    """Decorator for logging execution time."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            async with log_performance(f"{func.__module__}.{func.__name__}", logger):
                return await func(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            with log_performance(f"{func.__module__}.{func.__name__}", logger):
                return func(*args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
```

## Security Logging

### Sensitive Data Handling
```python
# src/mcp_server/logging/security.py
import logging
import re
from typing import Dict, Any


class SecurityLogger:
    """Logger for security-related events."""

    SENSITIVE_PATTERNS = [
        r'password["\s]*:[\s]*["\']([^"\']+)["\']',
        r'api_key["\s]*:[\s]*["\']([^"\']+)["\']',
        r'token["\s]*:[\s]*["\']([^"\']+)["\']',
        r'secret["\s]*:[\s]*["\']([^"\']+)["\']',
    ]

    def __init__(self):
        self.logger = logging.getLogger("security")

    def sanitize_message(self, message: str) -> str:
        """Remove sensitive data from log messages."""
        sanitized = message
        for pattern in self.SENSITIVE_PATTERNS:
            sanitized = re.sub(pattern, r'\1["***REDACTED***"]', sanitized, flags=re.IGNORECASE)
        return sanitized

    def log_auth_event(self, event: str, user_id: str = None, **kwargs) -> None:
        """Log authentication events."""
        self.logger.info(
            f"Auth event: {event}",
            extra={
                'event_type': 'authentication',
                'user_id': user_id,
                **kwargs
            }
        )

    def log_access_event(self, resource: str, action: str, user_id: str = None, **kwargs) -> None:
        """Log resource access events."""
        self.logger.info(
            f"Access: {action} on {resource}",
            extra={
                'event_type': 'access',
                'resource': resource,
                'action': action,
                'user_id': user_id,
                **kwargs
            }
        )

    def log_security_event(self, event: str, severity: str = "medium", **kwargs) -> None:
        """Log security events."""
        level = {
            "low": logging.INFO,
            "medium": logging.WARNING,
            "high": logging.ERROR,
            "critical": logging.CRITICAL
        }.get(severity, logging.WARNING)

        self.logger.log(
            level,
            f"Security event: {event}",
            extra={
                'event_type': 'security',
                'severity': severity,
                **kwargs
            }
        )


# Global security logger
security_logger = SecurityLogger()
```

## Next Steps
After logging implementation, proceed to:
1. [Monitoring Standards](./monitoring.md)
2. [Performance Standards](./performance.md)
3. [Security Standards](./security.md)
