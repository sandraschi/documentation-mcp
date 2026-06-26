# MCP Server Monitoring Guide

**Last Updated:** 2025-12-04

Monitoring and observability for MCP servers.

---

## 📊 Metrics

### Prometheus Integration

```python
from prometheus_client import Counter, Histogram

tool_calls = Counter('mcp_tool_calls_total', 'Total tool calls', ['tool_name'])
tool_duration = Histogram('mcp_tool_duration_seconds', 'Tool execution time')
```

---

## 📝 Logging

Use structured logging for better observability.

---

## 🚨 Alerting

Configure alerts for critical issues.

---

→ Complete monitoring stack: [../../monitoring/README.md](../../monitoring/README.md)

