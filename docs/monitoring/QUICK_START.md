# Monitoring Quick Start - Add Monitoring to Your MCP Server

> **Fleet stack today:** [MONITORING_CURRENT_SETUP.md](./MONITORING_CURRENT_SETUP.md) — Grafana **12000**, `prometheus.fleet.yml`, host logs via `Invoke-FleetLoggedCommand.ps1`.

**Time Required:** 30-45 minutes  
**Difficulty:** Intermediate  
**Prerequisites:** MCP server with FastMCP 3.1.1++

---

## ðŸŽ¯ What You'll Get

After this guide, your MCP server will have:
- âœ… **Structured logging** with context
- âœ… **Prometheus metrics** for monitoring
- âœ… **Health check endpoint**
- âœ… **Ready for Grafana dashboards**
- âœ… **Loki log aggregation** (optional)

---

## ðŸ“¦ Step 1: Install Dependencies

Add to `requirements.txt`:

```txt
# Logging
structlog>=23.0.0

# Metrics
prometheus-client>=0.19.0

# Optional: Advanced logging
python-json-logger>=2.0.7
```

Install:

```bash
uv sync
# or
pip install -r requirements.txt
```

---

## ðŸ“Š Step 2: Add Structured Logging

### Create `src/{package}/logging_config.py`:

```python
'''Structured logging configuration.'''

import structlog
import logging
import sys
from typing import Any


def configure_logging(debug: bool = False) -> None:
    '''Configure structured logging.
    
    Args:
        debug: Enable debug level logging
    '''
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Configure stdlib logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False
    )


def get_logger(name: str) -> Any:
    '''Get a structured logger.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Structured logger instance
    '''
    return structlog.get_logger(name)
```

### Update your `mcp_server.py`:

```python
from .logging_config import configure_logging, get_logger

# Configure logging at startup
configure_logging(debug=False)  # Set from env var in production
logger = get_logger(__name__)

# Use in your code
logger.info("server_started", version="1.0.0")
logger.error("operation_failed", operation="tool_name", error=str(e))
```

---

## ðŸ“ˆ Step 3: Add Prometheus Metrics

### Create `src/{package}/metrics.py`:

```python
'''Prometheus metrics for monitoring.'''

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from typing import Any
import time


# Define metrics
tool_calls_total = Counter(
    'mcp_tool_calls_total',
    'Total number of tool calls',
    ['tool_name', 'status']  # Labels
)

tool_duration_seconds = Histogram(
    'mcp_tool_duration_seconds',
    'Tool execution duration in seconds',
    ['tool_name']
)

active_connections = Gauge(
    'mcp_active_connections',
    'Number of active MCP connections'
)

errors_total = Counter(
    'mcp_errors_total',
    'Total number of errors',
    ['tool_name', 'error_type']
)


class MetricsCollector:
    '''Collect metrics for tools.'''
    
    @staticmethod
    def record_tool_call(tool_name: str, success: bool) -> None:
        '''Record a tool call.
        
        Args:
            tool_name: Name of the tool
            success: Whether call succeeded
        '''
        status = 'success' if success else 'error'
        tool_calls_total.labels(tool_name=tool_name, status=status).inc()
    
    @staticmethod
    def time_tool_execution(tool_name: str):
        '''Context manager to time tool execution.
        
        Args:
            tool_name: Name of the tool
            
        Example:
            with MetricsCollector.time_tool_execution('my_tool'):
                # Tool execution
                pass
        '''
        return tool_duration_seconds.labels(tool_name=tool_name).time()
    
    @staticmethod
    def record_error(tool_name: str, error_type: str) -> None:
        '''Record an error.
        
        Args:
            tool_name: Name of the tool
            error_type: Type of error
        '''
        errors_total.labels(tool_name=tool_name, error_type=error_type).inc()
    
    @staticmethod
    def get_metrics() -> tuple[str, str]:
        '''Get current metrics in Prometheus format.
        
        Returns:
            Tuple of (metrics_text, content_type)
        '''
        return generate_latest(), CONTENT_TYPE_LATEST


# Global metrics collector instance
metrics = MetricsCollector()
```

### Instrument Your Tools:

```python
from .metrics import metrics
from .logging_config import get_logger

logger = get_logger(__name__)


@mcp.tool()
async def my_tool(param: str) -> dict[str, Any]:
    '''My tool with monitoring.'''
    try:
        # Time execution
        with metrics.time_tool_execution('my_tool'):
            # Log start
            logger.info("tool_started", tool="my_tool", param=param)
            
            # Your tool logic
            result = await do_something(param)
            
            # Record success
            metrics.record_tool_call('my_tool', success=True)
            logger.info("tool_completed", tool="my_tool", success=True)
            
            return {"success": True, "data": result}
            
    except Exception as e:
        # Record error
        metrics.record_tool_call('my_tool', success=False)
        metrics.record_error('my_tool', type(e).__name__)
        logger.error("tool_failed", tool="my_tool", error=str(e))
        
        return {"success": False, "error": str(e)}
```

---

## âœ… Step 4: Add Health Check Tool

```python
from .metrics import metrics
from .logging_config import get_logger
import time
import platform

logger = get_logger(__name__)
START_TIME = time.time()


@mcp.tool()
async def health_check() -> dict[str, Any]:
    '''Check server health and status.
    
    Returns comprehensive health information including:
    - Server status
    - Uptime
    - System information
    - Metrics summary
    
    Returns:
        Health check result with system information
        
    Example:
        result = await health_check()
    '''
    uptime_seconds = time.time() - START_TIME
    
    return {
        "success": True,
        "status": "healthy",
        "uptime_seconds": uptime_seconds,
        "uptime_human": format_uptime(uptime_seconds),
        "system": {
            "platform": platform.system(),
            "python_version": platform.python_version()
        },
        "metrics_endpoint": "/metrics"  # If exposing HTTP endpoint
    }


def format_uptime(seconds: float) -> str:
    '''Format uptime in human-readable form.'''
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours}h {minutes}m"
```

---

## ðŸš€ Step 5: Expose Metrics (Optional HTTP Server)

If you want to expose metrics via HTTP:

### Create `src/{package}/metrics_server.py`:

```python
'''HTTP server for Prometheus metrics.'''

from http.server import HTTPServer, BaseHTTPRequestHandler
from .metrics import MetricsCollector
import threading


class MetricsHandler(BaseHTTPRequestHandler):
    '''HTTP handler for metrics endpoint.'''
    
    def do_GET(self):
        '''Handle GET requests.'''
        if self.path == '/metrics':
            metrics_text, content_type = MetricsCollector.get_metrics()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(metrics_text)
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "healthy"}')
        else:
            self.send_response(404)
            self.end_headers()


def start_metrics_server(port: int = 8000):
    '''Start metrics HTTP server in background thread.
    
    Args:
        port: Port to listen on
    '''
    server = HTTPServer(('0.0.0.0', port), MetricsHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server
```

### Start server in `mcp_server.py`:

```python
from .metrics_server import start_metrics_server

# Start metrics server (optional)
if os.getenv("ENABLE_METRICS_SERVER", "false").lower() == "true":
    port = int(os.getenv("METRICS_PORT", "8000"))
    start_metrics_server(port)
    logger.info("metrics_server_started", port=port)
```

---

## ðŸ“Š Step 6: Test Your Monitoring

### Test Structured Logging:

```bash
# Enable debug mode
DEBUG=true uv run {package}

# Check logs format (should be JSON)
# Example output:
# {"event": "tool_started", "tool": "my_tool", "timestamp": "2025-10-24T12:34:56"}
```

### Test Metrics (if HTTP server enabled):

```bash
# Check metrics endpoint
curl http://localhost:8000/metrics

# Check health endpoint
curl http://localhost:8000/health
```

### Test from Claude:

```bash
# Ask Claude to check health
"Check the server health"

# Should return uptime and system info
```

---

## ðŸ“ˆ Step 7: Connect to Grafana (Optional)

### Prerequisites:
- Docker and Docker Compose installed
- Metrics HTTP server enabled

### Quick Grafana Stack:

Download monitoring stack:
```bash
# Copy monitoring configs from central docs
cp -r D:/Dev/repos/mcp-central-docs/monitoring/configs ./monitoring
```

Update `monitoring/prometheus/prometheus.yml`:
```yaml
scrape_configs:
  - job_name: '{your-server-name}'
    static_configs:
      - targets: ['host.docker.internal:8000']
```

Start stack:
```bash
cd monitoring
docker-compose up -d
```

Access Grafana:
- URL: http://localhost:3000
- User: admin
- Pass: admin

Add your metrics:
1. Go to Data Sources
2. Add Prometheus (http://prometheus:9090)
3. Create dashboard
4. Add panels with queries like:
   - `rate(mcp_tool_calls_total[5m])`
   - `mcp_tool_duration_seconds`

---

## ðŸŽ¯ What to Monitor

### Essential Metrics:

**Tool Performance:**
```promql
# Requests per second
rate(mcp_tool_calls_total[5m])

# Error rate
rate(mcp_tool_calls_total{status="error"}[5m])

# Tool duration (p95)
histogram_quantile(0.95, mcp_tool_duration_seconds)
```

**Server Health:**
```promql
# Active connections
mcp_active_connections

# Total errors
sum(rate(mcp_errors_total[5m])) by (error_type)
```

### Logs to Monitor:

- Tool execution times
- Error messages
- Configuration changes
- Authentication failures

---

## ðŸš¨ Alerting (Optional)

### Example Prometheus Alerts:

```yaml
groups:
  - name: mcp_server_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(mcp_tool_calls_total{status="error"}[5m]) > 0.1
        for: 5m
        annotations:
          summary: "High error rate detected"
          
      - alert: SlowToolExecution
        expr: histogram_quantile(0.95, mcp_tool_duration_seconds) > 10
        for: 5m
        annotations:
          summary: "Tool execution is slow"
```

---

## âœ… Checklist

- [ ] Installed structlog and prometheus-client
- [ ] Configured structured logging
- [ ] Added metrics collection
- [ ] Instrumented tools
- [ ] Added health_check tool
- [ ] Tested logging output
- [ ] Tested metrics (if HTTP server)
- [ ] Verified Claude can call health_check
- [ ] Optional: Connected to Grafana
- [ ] Optional: Set up alerts

---

## ðŸ” Troubleshooting

### Logs Not JSON Format

**Problem:** Logs are plain text  
**Solution:** Check structlog configuration uses `JSONRenderer()`

### Metrics Not Updating

**Problem:** Metrics endpoint shows old data  
**Solution:** Ensure metrics are being recorded in tool code

### HTTP Server Not Starting

**Problem:** Port already in use  
**Solution:** Change `METRICS_PORT` environment variable

### Claude Can't Call Health Check

**Problem:** Tool not registered  
**Solution:** Ensure `@mcp.tool()` decorator is present

---

## ðŸ“š Next Steps

### Further Enhancements:

1. **Custom Metrics** - Add business-specific metrics
2. **Log Correlation** - Add trace IDs across tools
3. **Dashboards** - Create Grafana dashboards
4. **Alerts** - Set up Prometheus alerts
5. **Loki Integration** - Centralized log aggregation

### Advanced Topics:

- [Unified Monitoring Stack](UNIFIED_MONITORING_STACK.md)
- [Grafana Dashboards](Grafana.md)
- [Prometheus Configuration](Prometheus.md)
- [Loki Setup](Loki.md)

---

## ðŸ“ Example: Complete Monitored Tool

```python
from .metrics import metrics
from .logging_config import get_logger
from typing import Literal, Any

logger = get_logger(__name__)


@mcp.tool()
async def item_management(
    action: Literal["create", "read", "update", "delete"],
    identifier: str | None = None,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    '''Complete item management with monitoring.
    
    SUPPORTED OPERATIONS:
    - create: Create new item
    - read: Retrieve item
    - update: Modify item
    - delete: Remove item
    
    Args:
        action: Operation to perform
        identifier: Item identifier
        data: Item data (for create/update)
        
    Returns:
        Operation result
    '''
    tool_name = "item_management"
    
    try:
        # Log and time execution
        with metrics.time_tool_execution(tool_name):
            logger.info(
                "tool_started",
                tool=tool_name,
                action=action,
                identifier=identifier
            )
            
            # Route to handler
            if action == "create":
                result = await handle_create(identifier, data)
            elif action == "read":
                result = await handle_read(identifier)
            elif action == "update":
                result = await handle_update(identifier, data)
            elif action == "delete":
                result = await handle_delete(identifier)
            
            # Record success
            metrics.record_tool_call(tool_name, success=True)
            logger.info(
                "tool_completed",
                tool=tool_name,
                action=action,
                success=True
            )
            
            return result
            
    except Exception as e:
        # Record error with details
        metrics.record_tool_call(tool_name, success=False)
        metrics.record_error(tool_name, type(e).__name__)
        logger.error(
            "tool_failed",
            tool=tool_name,
            action=action,
            error=str(e),
            exc_info=True
        )
        
        return {
            "success": False,
            "error": str(e),
            "action": action
        }
```

---

**Guide Version:** 1.0  
**Last Updated:** 2025-10-24  
**Tested With:** FastMCP 3.1.1++, Python 3.10+


