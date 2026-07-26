# health-mcp

**Status:** Alpha (scaffolded)
**Ports:** MCP HTTP 10902

Multi-source health data fusion MCP server. Ingests from Visual State Machines
(devices-mcp camera watchers), Apple Health exports, and manual entries.

## Features
- SQLite store for health records, VSM events, meals
- Apple Health XML export parser
- VSM event consumer from devices-mcp (scale, dog bowl, fridge, bedroom)
- Trend analysis (avg, min, max, direction over days window)
- Prefab UI dashboard card
- Dual transport stdio + HTTP

## Tools
- `health_data` — log_record, query, trend, import_apple_health, get_stats, log_vsm_event
- `show_health_dashboard` — rich summary card

## Links
- [GitHub](https://github.com/sandraschi/health-mcp)
- [VSM pattern](https://github.com/sandraschi/mcp-central-docs/blob/main/patterns/visual-state-machines.md)
