# Error Handling Standards

## Overview
Standards for robust error handling, exception management, and error recovery patterns in MCP servers.

## Error Handling Principles

### Core Principles
1. **Fail Fast**: Detect errors early and fail immediately
2. **Graceful Degradation**: Continue operation when possible
3. **Clear Communication**: Provide meaningful error messages
4. **Comprehensive Logging**: Log all errors with context
5. **Recovery Mechanisms**: Implement automatic recovery where feasible

### Mandatory Requirements

#### 1. All Errors Must Be Handled
- **NO empty catch blocks allowed**: Every `except` clause must contain meaningful error handling
- **NO bare `except:` statements**: Always specify exception types or use `except Exception as e:`
- **NO silent failures**: All errors must be logged or handled appropriately

```python
# ❌ WRONG - Empty catch block
try:
    risky_operation()
except:
    pass  # Silent failure - NOT ALLOWED

# ❌ WRONG - Bare except
try:
    risky_operation()
except Exception:
    logger.error("Something went wrong")  # Too vague

# ✅ CORRECT - Specific handling
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value provided: {e}", extra={"operation": "risky_operation"})
    raise ValidationError("Invalid input value", details={"original_error": str(e)})
except ConnectionError as e:
    logger.warning(f"Connection failed, attempting retry: {e}")
    await retry_with_backoff(risky_operation)
except Exception as e:
    logger.critical(f"Unexpected error in risky_operation: {e}", exc_info=True)
    await graceful_shutdown()
```

#### 2. Detailed Error Logging Requirements
- **Context-rich messages**: Include operation name, parameters, user context, timestamps
- **Actionable information**: What failed, why, and potential recovery steps
- **No generic messages**: Avoid "An error occurred" - be specific
- **Correlation IDs**: Include request/operation IDs for tracing

```python
# Comprehensive error logging
logger.error(
    f"Tool execution failed: {tool_name} with params {params}",
    extra={
        "tool_name": tool_name,
        "parameters": params,
        "user_id": user_id,
        "request_id": request_id,
        "execution_time_ms": execution_time,
        "error_type": type(e).__name__,
        "error_message": str(e),
        "stack_trace": traceback.format_exc(),
        "recovery_attempted": recovery_attempted,
        "suggested_actions": ["Check network connectivity", "Verify API credentials"]
    }
)
```

#### 3. No Crashes or Hangs in Edge Cases
- **Resource exhaustion**: Handle memory, disk, and connection limits
- **Infinite loops**: Implement iteration limits and timeouts
- **Deadlocks**: Use timeout decorators and async cancellation
- **Stack overflows**: Implement recursion limits and iterative alternatives

```python
# Resource exhaustion handling
@asynccontextmanager
async def memory_bound_operation(max_memory_mb: int = 100):
    """Ensure operation doesn't exceed memory limits."""
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024

    try:
        yield
    finally:
        current_memory = process.memory_info().rss / 1024 / 1024
        memory_used = current_memory - initial_memory

        if memory_used > max_memory_mb:
            logger.warning(f"High memory usage detected: {memory_used:.1f}MB")
            # Trigger cleanup or scaling

# Infinite loop prevention
async def bounded_retry(operation, max_attempts: int = 5):
    """Prevent infinite retry loops."""
    for attempt in range(max_attempts):
        try:
            return await operation()
        except Exception as e:
            if attempt == max_attempts - 1:
                logger.error(f"Operation failed after {max_attempts} attempts")
                raise
            await asyncio.sleep(min(2 ** attempt, 30))  # Exponential backoff

# Async cancellation handling
async def cancellable_operation(timeout_seconds: int = 30):
    """Handle operation cancellation gracefully."""
    try:
        async with asyncio.timeout(timeout_seconds):
            return await long_running_task()
    except asyncio.CancelledError:
        logger.info("Operation was cancelled, cleaning up resources")
        await cleanup_resources()
        raise
    except asyncio.TimeoutError:
        logger.warning("Operation timed out, initiating recovery")
        await initiate_timeout_recovery()
        raise TimeoutError("Operation exceeded time limit")
```

#### 4. Intelligent Timeout Handling
- **Exponential backoff**: Progressive delay increases
- **Jitter**: Randomization to prevent thundering herd
- **Circuit breakers**: Automatic failure detection and recovery
- **User notifications**: Progress updates and timeout warnings

```python
# Intelligent timeout with backoff and notifications
class IntelligentTimeoutHandler:
    """Handle timeouts with backoff logic and user notifications."""

    def __init__(self, max_retries: int = 5, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.retry_count = 0

    async def execute_with_timeout_handling(
        self,
        operation: Callable,
        timeout_seconds: int = 30,
        user_callback: Optional[Callable] = None
    ):
        """Execute operation with intelligent timeout handling."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                # Notify user of retry attempt
                if attempt > 0 and user_callback:
                    await user_callback({
                        "type": "retry_attempt",
                        "attempt": attempt,
                        "max_attempts": self.max_retries,
                        "next_retry_in": self._calculate_delay(attempt)
                    })

                # Execute with timeout
                async with asyncio.timeout(timeout_seconds):
                    result = await operation()
                    self.retry_count = 0  # Reset on success
                    return result

            except asyncio.TimeoutError as e:
                last_exception = e
                delay = self._calculate_delay(attempt)

                logger.warning(
                    f"Operation timed out (attempt {attempt + 1}/{self.max_retries + 1}), "
                    f"retrying in {delay:.1f}s",
                    extra={"attempt": attempt, "timeout_seconds": timeout_seconds}
                )

                if attempt < self.max_retries:
                    await asyncio.sleep(delay)

            except Exception as e:
                # For non-timeout errors, don't retry
                logger.error(f"Non-timeout error, not retrying: {e}")
                raise

        # All retries exhausted
        if user_callback:
            await user_callback({
                "type": "timeout_exhausted",
                "total_attempts": self.max_retries + 1,
                "error": str(last_exception)
            })

        raise TimeoutError(
            f"Operation failed after {self.max_retries + 1} attempts "
            f"(last timeout: {timeout_seconds}s)"
        )

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and jitter."""
        # Exponential backoff: base_delay * (2 ^ attempt)
        delay = self.base_delay * (2 ** attempt)

        # Add jitter: ±25% randomization
        jitter = delay * 0.25 * (2 * random.random() - 1)
        delay += jitter

        # Cap at reasonable maximum (5 minutes)
        return min(delay, 300.0)

# Usage with user notifications
async def notify_user(update: dict):
    """Send progress updates to user interface."""
    if update["type"] == "retry_attempt":
        # Update UI with retry progress
        await update_ui_progress(
            f"Operation timed out, retrying... "
            f"(attempt {update['attempt']}/{update['max_attempts']})"
        )
    elif update["type"] == "timeout_exhausted":
        # Show final error to user
        await show_user_error(
            "Operation failed after multiple attempts",
            details=update["error"]
        )

timeout_handler = IntelligentTimeoutHandler()

# Execute with intelligent timeout handling
result = await timeout_handler.execute_with_timeout_handling(
    my_operation,
    timeout_seconds=60,
    user_callback=notify_user
)
```

## Exception Hierarchy

### Base Exception Classes
```python
# src/mcp_server/exceptions.py
from typing import Dict, Any, Optional


class MCPError(Exception):
    """Base exception for MCP server errors."""

    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "INTERNAL_ERROR"
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        return {
            "error": {
                "code": self.error_code,
                "message": self.message,
                "details": self.details
            }
        }


class ValidationError(MCPError):
    """Validation error for invalid input data."""
    def __init__(self, field: str, value: Any, reason: str):
        super().__init__(
            f"Validation error for field '{field}': {reason}",
            error_code="VALIDATION_ERROR",
            details={"field": field, "value": value, "reason": reason}
        )


class ResourceNotFoundError(MCPError):
    """Resource not found error."""
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            f"{resource_type} with id '{resource_id}' not found",
            error_code="RESOURCE_NOT_FOUND",
            details={"resource_type": resource_type, "resource_id": resource_id}
        )


class PermissionDeniedError(MCPError):
    """Permission denied error."""
    def __init__(self, action: str, resource: str):
        super().__init__(
            f"Permission denied for action '{action}' on resource '{resource}'",
            error_code="PERMISSION_DENIED",
            details={"action": action, "resource": resource}
        )


class ExternalServiceError(MCPError):
    """Error from external service dependency."""
    def __init__(self, service_name: str, original_error: Exception):
        super().__init__(
            f"External service '{service_name}' error: {str(original_error)}",
            error_code="EXTERNAL_SERVICE_ERROR",
            details={
                "service_name": service_name,
                "original_error": str(original_error),
                "error_type": type(original_error).__name__
            }
        )
```

## Error Handling Patterns

### Tool Error Handling
```python
# src/mcp_server/tools/base_tool.py
from typing import Dict, Any, Optional
from mcp import Context
from ..exceptions import MCPError, ValidationError


class BaseTool:
    """Base class for MCP tools with error handling."""

    async def execute_with_error_handling(
        self,
        ctx: Context,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute tool with comprehensive error handling."""
        try:
            # Validate input
            self.validate_input(**kwargs)

            # Execute tool logic
            result = await self.execute(**kwargs)

            # Validate output
            self.validate_output(result)

            return {
                "success": True,
                "result": result
            }

        except ValidationError as e:
            ctx.logger.warning(f"Validation error in {self.__class__.__name__}: {e}")
            return e.to_dict()

        except PermissionDeniedError as e:
            ctx.logger.error(f"Permission denied in {self.__class__.__name__}: {e}")
            return e.to_dict()

        except ExternalServiceError as e:
            ctx.logger.error(f"External service error in {self.__class__.__name__}: {e}")
            # Attempt recovery for external service errors
            recovery_result = await self.attempt_recovery(e)
            if recovery_result:
                return {
                    "success": True,
                    "result": recovery_result,
                    "recovered": True
                }
            return e.to_dict()

        except Exception as e:
            # Catch-all for unexpected errors
            ctx.logger.error(f"Unexpected error in {self.__class__.__name__}: {e}", exc_info=True)
            return {
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                    "details": {"error_type": type(e).__name__}
                }
            }

    def validate_input(self, **kwargs) -> None:
        """Validate tool input parameters."""
        # Implement validation logic
        pass

    def validate_output(self, result: Any) -> None:
        """Validate tool output."""
        # Implement output validation
        pass

    async def attempt_recovery(self, error: ExternalServiceError) -> Optional[Any]:
        """Attempt to recover from external service errors."""
        # Implement recovery logic (retry, fallback, etc.)
        return None

    async def execute(self, **kwargs) -> Any:
        """Tool execution logic - to be implemented by subclasses."""
        raise NotImplementedError
```

### API Error Handling
```python
# src/mcp_server/api/error_handlers.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from ..exceptions import MCPError


async def mcp_error_handler(request: Request, exc: MCPError):
    """Handle MCP errors in API responses."""
    return JSONResponse(
        status_code=get_status_code(exc.error_code),
        content=exc.to_dict()
    )


async def general_error_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    # Log the error
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Unhandled error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {}
            }
        }
    )


def get_status_code(error_code: str) -> int:
    """Map error codes to HTTP status codes."""
    status_map = {
        "VALIDATION_ERROR": 400,
        "RESOURCE_NOT_FOUND": 404,
        "PERMISSION_DENIED": 403,
        "EXTERNAL_SERVICE_ERROR": 502,
        "INTERNAL_ERROR": 500,
    }
    return status_map.get(error_code, 500)
```

### Async Error Handling
```python
# src/mcp_server/utils/async_error_handling.py
import asyncio
import logging
from typing import Callable, Any, Optional
from functools import wraps


def handle_async_errors(logger: Optional[logging.Logger] = None):
    """Decorator for handling errors in async functions."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)

            try:
                return await func(*args, **kwargs)
            except asyncio.CancelledError:
                logger.info(f"Operation cancelled: {func.__name__}")
                raise
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                raise
        return wrapper
    return decorator


class AsyncErrorHandler:
    """Context manager for handling async operation errors."""

    def __init__(self, operation_name: str, logger: Optional[logging.Logger] = None):
        self.operation_name = operation_name
        self.logger = logger or logging.getLogger(__name__)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(
                f"Error in async operation '{self.operation_name}': {exc_val}",
                exc_info=(exc_type, exc_val, exc_tb)
            )
            # Could implement recovery logic here
            return False  # Don't suppress the exception
        return False


# Usage examples
@handle_async_errors()
async def async_operation():
    """Async operation with automatic error handling."""
    # Operation logic
    pass

async def complex_operation():
    """Complex operation with context manager."""
    async with AsyncErrorHandler("complex_operation"):
        # Complex logic that might fail
        pass
```

## Recovery Mechanisms

### Circuit Breaker Pattern
```python
# src/mcp_server/utils/circuit_breaker.py
import time
import logging
from enum import Enum
from typing import Callable, Any


class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"         # Failing, requests rejected
    HALF_OPEN = "half_open"  # Testing recovery


class CircuitBreaker:
    """Circuit breaker for external service calls."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: Exception = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

        self.logger = logging.getLogger(__name__)

    def __call__(self, func: Callable) -> Callable:
        async def wrapper(*args, **kwargs) -> Any:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                    self.logger.info("Circuit breaker entering half-open state")
                else:
                    raise Exception("Circuit breaker is OPEN")

            try:
                result = await func(*args, **kwargs)
                self._on_success()
                return result
            except self.expected_exception as e:
                self._on_failure()
                raise e

        return wrapper

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery."""
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.recovery_timeout

    def _on_success(self):
        """Handle successful operation."""
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.logger.info("Circuit breaker reset to closed state")

    def _on_failure(self):
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.logger.warning(f"Circuit breaker opened after {self.failure_count} failures")


# Usage
circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

@circuit_breaker
async def call_external_service():
    """Call external service with circuit breaker protection."""
    # Service call logic
    pass
```

### Retry Mechanisms
```python
# src/mcp_server/utils/retry.py
import asyncio
import logging
import random
from typing import Callable, Any, Optional


class RetryConfig:
    """Configuration for retry behavior."""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        jitter: bool = True
    ):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter


async def retry_async(
    func: Callable,
    config: RetryConfig = None,
    exceptions: tuple = (Exception,),
    logger: Optional[logging.Logger] = None
) -> Any:
    """Retry an async function with exponential backoff."""
    if config is None:
        config = RetryConfig()
    if logger is None:
        logger = logging.getLogger(__name__)

    last_exception = None

    for attempt in range(config.max_attempts):
        try:
            return await func()
        except exceptions as e:
            last_exception = e

            if attempt < config.max_attempts - 1:
                delay = min(
                    config.initial_delay * (config.backoff_factor ** attempt),
                    config.max_delay
                )

                if config.jitter:
                    delay *= (0.5 + random.random() * 0.5)  # Add jitter

                logger.warning(
                    f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {e}"
                )
                await asyncio.sleep(delay)
            else:
                logger.error(
                    f"All {config.max_attempts} attempts failed: {e}"
                )

    raise last_exception


# Usage
async def unreliable_operation():
    """Example operation that might fail."""
    # Operation logic
    pass

# Retry with default config
result = await retry_async(unreliable_operation)

# Retry with custom config
config = RetryConfig(max_attempts=5, initial_delay=2.0)
result = await retry_async(unreliable_operation, config)
```

## Error Response Standards

### MCP Error Responses
```python
# Standardized MCP error response format
def create_error_response(
    error_code: str,
    message: str,
    details: Dict[str, Any] = None,
    recoverable: bool = False,
    retry_after: Optional[int] = None
) -> Dict[str, Any]:
    """Create standardized error response."""
    response = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
            "timestamp": int(time.time()),
        }
    }

    if details:
        response["error"]["details"] = details

    if recoverable:
        response["error"]["recoverable"] = True

    if retry_after:
        response["error"]["retry_after"] = retry_after

    return response


# Usage in tools
async def failing_tool(ctx: Context) -> Dict[str, Any]:
    """Tool that demonstrates proper error responses."""
    try:
        # Tool logic that might fail
        result = await risky_operation()
        return {"success": True, "result": result}
    except TemporaryFailureError as e:
        # Recoverable error
        return create_error_response(
            "TEMPORARY_FAILURE",
            str(e),
            recoverable=True,
            retry_after=30
        )
    except PermanentFailureError as e:
        # Non-recoverable error
        return create_error_response(
            "PERMANENT_FAILURE",
            str(e),
            details={"reason": "configuration_error"}
        )
```

## Log Rotation and Analysis Tools

### Log Rotation Standards

#### Automatic Log Rotation Configuration
```python
# src/mcp_server/config/logging.py (continued)
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os


def setup_production_logging(
    log_dir: str = "logs",
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 30
) -> None:
    """Set up production logging with automatic rotation."""

    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Size-based rotation (when file exceeds max_file_size)
    size_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "mcp_server.log"),
        maxBytes=max_file_size,
        backupCount=backup_count,
        encoding='utf-8'
    )

    # Time-based rotation (daily rotation)
    time_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, "mcp_server_daily.log"),
        when="midnight",      # Rotate at midnight
        interval=1,           # Every 1 interval (day)
        backupCount=30,       # Keep 30 days
        encoding='utf-8'
    )

    # Error-only log (separate high-priority log)
    error_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "mcp_errors.log"),
        maxBytes=max_file_size,
        backupCount=backup_count,
        encoding='utf-8',
        level=logging.ERROR
    )

    # Configure formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(request_id)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    json_formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
        '"logger": "%(name)s", "request_id": "%(request_id)s", '
        '"message": "%(message)s"}',
        datefmt='%Y-%m-%dT%H:%M:%SZ'
    )

    # Apply formatters
    size_handler.setFormatter(detailed_formatter)
    time_handler.setFormatter(detailed_formatter)
    error_handler.setFormatter(json_formatter)

    # Get root logger and add handlers
    root_logger = logging.getLogger()
    root_logger.addHandler(size_handler)
    root_logger.addHandler(time_handler)
    root_logger.addHandler(error_handler)

    # Set appropriate level
    root_logger.setLevel(logging.INFO)

    logger.info("Production logging configured with automatic rotation")


def cleanup_old_logs(log_dir: str = "logs", max_age_days: int = 90) -> None:
    """Clean up log files older than specified days."""
    import glob
    from datetime import datetime, timedelta

    cutoff_date = datetime.now() - timedelta(days=max_age_days)

    # Find all log files
    log_pattern = os.path.join(log_dir, "*.log*")
    log_files = glob.glob(log_pattern)

    cleaned_count = 0
    for log_file in log_files:
        try:
            # Check file modification time
            file_mtime = datetime.fromtimestamp(os.path.getmtime(log_file))

            if file_mtime < cutoff_date:
                os.remove(log_file)
                cleaned_count += 1
                logger.info(f"Removed old log file: {log_file}")

        except OSError as e:
            logger.warning(f"Failed to remove log file {log_file}: {e}")

    if cleaned_count > 0:
        logger.info(f"Cleaned up {cleaned_count} old log files")
```

### Log Analysis Tools

#### Error Pattern Detection
```python
# src/mcp_server/analysis/error_analyzer.py
import re
import logging
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class ErrorAnalyzer:
    """Analyze log files for error patterns and trends."""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.logger = logging.getLogger(__name__)

    def analyze_recent_errors(self, hours: int = 24) -> Dict[str, any]:
        """Analyze error patterns in recent logs."""
        cutoff_time = datetime.now() - timedelta(hours=hours)

        error_patterns = defaultdict(int)
        error_trends = []
        error_details = []

        # Read error log file
        error_log_path = os.path.join(self.log_dir, "mcp_errors.log")

        try:
            with open(error_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        # Parse JSON log entry
                        import json
                        entry = json.loads(line.strip())

                        entry_time = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))

                        if entry_time > cutoff_time:
                            error_type = self._categorize_error(entry)
                            error_patterns[error_type] += 1

                            error_details.append({
                                'timestamp': entry_time,
                                'type': error_type,
                                'message': entry['message'],
                                'logger': entry['logger']
                            })

                    except (json.JSONDecodeError, KeyError):
                        # Try to parse as plain text log
                        if 'ERROR' in line or 'CRITICAL' in line:
                            timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                            if timestamp_match:
                                entry_time = datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M:%S')
                                if entry_time > cutoff_time:
                                    error_type = self._categorize_text_error(line)
                                    error_patterns[error_type] += 1

        except FileNotFoundError:
            self.logger.warning(f"Error log file not found: {error_log_path}")

        # Analyze trends
        error_trends = self._calculate_error_trends(error_details, hours)

        return {
            'time_range': f"Last {hours} hours",
            'total_errors': sum(error_patterns.values()),
            'error_patterns': dict(error_patterns),
            'error_trends': error_trends,
            'top_errors': sorted(error_patterns.items(), key=lambda x: x[1], reverse=True)[:10],
            'error_rate_per_hour': sum(error_patterns.values()) / hours
        }

    def _categorize_error(self, entry: Dict) -> str:
        """Categorize error from structured log entry."""
        message = entry.get('message', '').lower()

        if 'timeout' in message:
            return 'timeout'
        elif 'connection' in message or 'network' in message:
            return 'connection'
        elif 'validation' in message or 'invalid' in message:
            return 'validation'
        elif 'permission' in message or 'unauthorized' in message:
            return 'permission'
        elif 'memory' in message or 'out of memory' in message:
            return 'resource'
        else:
            return 'other'

    def _categorize_text_error(self, line: str) -> str:
        """Categorize error from plain text log line."""
        line_lower = line.lower()

        if 'timeout' in line_lower:
            return 'timeout'
        elif 'connection' in line_lower or 'network' in line_lower:
            return 'connection'
        elif 'validation' in line_lower or 'invalid' in line_lower:
            return 'validation'
        elif 'permission' in line_lower or 'unauthorized' in line_lower:
            return 'permission'
        elif 'memory' in line_lower:
            return 'resource'
        else:
            return 'other'

    def _calculate_error_trends(self, errors: List[Dict], hours: int) -> List[Dict]:
        """Calculate error trends over time."""
        if not errors:
            return []

        # Group errors by hour
        hourly_errors = defaultdict(int)

        for error in errors:
            hour_key = error['timestamp'].strftime('%Y-%m-%d %H:00')
            hourly_errors[hour_key] += 1

        # Convert to trend data
        trends = []
        for hour, count in sorted(hourly_errors.items()):
            trends.append({
                'hour': hour,
                'error_count': count
            })

        return trends

    def generate_error_report(self, hours: int = 24) -> str:
        """Generate human-readable error report."""
        analysis = self.analyze_recent_errors(hours)

        report = f"""
Error Analysis Report - Last {hours} hours
========================================

Total Errors: {analysis['total_errors']}
Error Rate: {analysis['error_rate_per_hour']:.2f} errors/hour

Top Error Categories:
"""

        for error_type, count in analysis['top_errors'][:5]:
            percentage = (count / analysis['total_errors'] * 100) if analysis['total_errors'] > 0 else 0
            report += f"- {error_type}: {count} ({percentage:.1f}%)\n"

        if analysis['error_trends']:
            report += "\nError Trends (by hour):\n"
            for trend in analysis['error_trends'][-10:]:  # Last 10 hours
                report += f"- {trend['hour']}: {trend['error_count']} errors\n"

        return report


# CLI tool for error analysis
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MCP Error Log Analyzer")
    parser.add_argument("--hours", type=int, default=24, help="Analysis time window in hours")
    parser.add_argument("--log-dir", default="logs", help="Log directory path")

    args = parser.parse_args()

    analyzer = ErrorAnalyzer(args.log_dir)
    report = analyzer.generate_error_report(args.hours)

    print(report)

    # Save detailed analysis
    analysis = analyzer.analyze_recent_errors(args.hours)
    with open("error_analysis.json", "w") as f:
        import json
        json.dump(analysis, f, indent=2, default=str)

    print("Detailed analysis saved to error_analysis.json")
```

#### Log Monitoring Dashboard
```python
# src/mcp_server/monitoring/log_dashboard.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
from .error_analyzer import ErrorAnalyzer
from ..metrics import metrics


app = FastAPI(title="MCP Log Monitoring Dashboard")


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the log monitoring dashboard."""
    analyzer = ErrorAnalyzer()

    # Get current error analysis
    analysis = analyzer.analyze_recent_errors(hours=24)

    # Generate HTML dashboard
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MCP Error Monitoring Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .metric {{ background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .error {{ color: red; }}
            .warning {{ color: orange; }}
            .success {{ color: green; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>MCP Server Error Monitoring Dashboard</h1>

        <div class="metric">
            <h2>Overall Metrics (Last 24 hours)</h2>
            <p><strong>Total Errors:</strong> <span class="error">{analysis['total_errors']}</span></p>
            <p><strong>Error Rate:</strong> {analysis['error_rate_per_hour']:.2f} errors/hour</p>
        </div>

        <div class="metric">
            <h2>Error Categories</h2>
            <table>
                <tr><th>Category</th><th>Count</th><th>Percentage</th></tr>
                {"".join(f"<tr><td>{cat}</td><td>{count}</td><td>{count/analysis['total_errors']*100:.1f}%</td></tr>"
                        for cat, count in analysis['top_errors'][:10])}
            </table>
        </div>

        <div class="metric">
            <h2>Error Trends (Last 10 hours)</h2>
            <table>
                <tr><th>Hour</th><th>Error Count</th></tr>
                {"".join(f"<tr><td>{trend['hour']}</td><td>{trend['error_count']}</td></tr>"
                        for trend in analysis['error_trends'][-10:])}
            </table>
        </div>

        <div class="metric">
            <h2>System Health</h2>
            <p><strong>Health Status:</strong>
                <span class="{'success' if metrics.health_status._value == 1 else 'error'}">
                    {'Healthy' if metrics.health_status._value == 1 else 'Unhealthy'}
                </span>
            </p>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html)


@app.get("/api/errors/analysis")
async def get_error_analysis(hours: int = 24):
    """API endpoint for error analysis data."""
    analyzer = ErrorAnalyzer()
    return analyzer.analyze_recent_errors(hours)


@app.get("/api/errors/report")
async def get_error_report(hours: int = 24):
    """API endpoint for error report."""
    analyzer = ErrorAnalyzer()
    return {"report": analyzer.generate_error_report(hours)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
```

## Next Steps
After error handling implementation, proceed to:
1. [Logging Standards](./logging.md)
2. [Monitoring Standards](./monitoring.md)
3. [Performance Standards](./performance.md)