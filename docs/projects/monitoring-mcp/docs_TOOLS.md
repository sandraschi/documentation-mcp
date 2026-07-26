# MCP Tool Reference

All tools follow the **portmanteau pattern**: a single `@mcp.tool()` with an `operation` parameter
that selects the sub-operation. This keeps the tool list manageable.

## `grafana_management`

| Operation | Description | Status |
|-----------|-------------|--------|
| `list_dashboards` | List all dashboards with metadata | Implemented |
| `get_dashboard` | Retrieve dashboard by UID | Implemented |
| `create_dashboard` | Create new dashboard from JSON | Implemented |
| `update_dashboard` | Modify existing dashboard | Implemented |
| `delete_dashboard` | Remove dashboard by UID | Implemented |
| `search_dashboards` | Filter dashboards by title/tag | Implemented |
| `list_datasources` | List configured Grafana datasources | Implemented |
| `query_datasource` | Run query against a datasource | Implemented |
| `analyze_dashboard` | Dashboard structure analysis + scoring | Implemented |
| `create_panel` | Add panel to dashboard | Not yet implemented |
| `update_panel` | Modify panel config | Not yet implemented |
| `create_alert` | Set up alerting rules | Not yet implemented |
| `export_dashboard` | Export as JSON | Not yet implemented |
| `import_dashboard` | Import from JSON | Not yet implemented |
| `list_folders` | List dashboard folders | Not yet implemented |
| `create_folder` | Create dashboard folder | Not yet implemented |
| `get_dashboard_permissions` | View permissions | Not yet implemented |

## `prometheus_monitoring`

| Operation | Description | Status |
|-----------|-------------|--------|
| `query_metrics` | Instant PromQL query | Implemented |
| `query_range` | Range PromQL query with time window | Implemented |
| `list_targets` | List scrape targets + health | Implemented |
| `get_target_health` | Health summary with up/down counts | Implemented |
| `list_rules` | Alerting + recording rules | Implemented |
| `list_alerts` | Active alerts with state summary | Implemented |
| `get_build_info` | Prometheus version | Implemented |
| `analyze_metrics` | Detect anomalous patterns in results | Implemented |
| `optimize_queries` | PromQL performance suggestions | Implemented |
| `get_rule_groups` | Rule group configs | Not yet implemented |
| `create_alert_rule` | Create new rule | Not yet implemented |
| `update_alert_rule` | Modify existing rule | Not yet implemented |
| `delete_alert_rule` | Remove rule | Not yet implemented |
| `get_alert_details` | Single alert detail | Not yet implemented |
| `silence_alert` | Suppress alert notifications | Not yet implemented |
| `list_silences` | Active silences | Not yet implemented |
| `expire_silence` | Remove silence | Not yet implemented |
| `get_config` | Prometheus runtime config | Not yet implemented |
| `get_flags` | CLI flags | Not yet implemented |

## `loki_logging`

| Operation | Description | Status |
|-----------|-------------|--------|
| `query_logs` | Instant LogQL query | Implemented |
| `query_range` | Range LogQL with time window | Implemented |
| `tail_logs` | Stream recent logs (limited) | Implemented |
| `get_labels` | List available log labels | Implemented |
| `get_label_values` | Values for a specific label | Implemented |
| `get_series` | Series matching stream selectors | Implemented |
| `analyze_logs` | Pattern recognition in log sample | Implemented |
| `detect_anomalies` | Error rate, connection, timestamp checks | Implemented |
| `search_errors` | Find ERROR/Exception/Failed patterns | Implemented |
| `trace_requests` | Find request/correlation IDs in logs | Implemented |
| `create_alert_rule` | Log-based alerting | Not yet implemented |
| `list_alerts` | Active log alerts | Not yet implemented |
| `optimize_queries` | LogQL perf suggestions | Not yet implemented |
| `export_logs` | Export in various formats | Not yet implemented |
| `compare_timeframes` | Diff log patterns between periods | Not yet implemented |
| `generate_report` | Comprehensive analysis report | Not yet implemented |

## `cross_system_correlation`

| Operation | Description | Status |
|-----------|-------------|--------|
| `correlate_incident` | Cross-reference metrics + logs for an incident | Implemented |
| `find_root_cause` | Heuristic root cause from error metrics + logs | Implemented |
| `performance_correlation` | Link latency metrics with perf-related logs | Implemented |
| `error_correlation` | Cluster errors by type and affected service | Implemented |
| `health_assessment` | Combined health score from all systems | Implemented |
| `anomaly_correlation` | Connect metric anomalies with log patterns | Not yet implemented |
| `service_dependency_map` | Map service relationships | Not yet implemented |
| `impact_analysis` | Analyse change/incident impact | Not yet implemented |
| `predictive_insights` | Trend-based predictions | Not yet implemented |
| `bottleneck_detection` | Identify system bottlenecks | Not yet implemented |

## `monitoring_status`

| Operation | Description | Status |
|-----------|-------------|--------|
| `system_health` | Overall health across all components | Implemented |
| `connectivity_test` | Test reachability of each system | Implemented |
| `configuration_validation` | Validate URLs, datasources, labels | Implemented |
| `performance_metrics` | Prometheus engine query stats | Implemented |
| `data_flow_status` | Check datasource links in Grafana | Implemented |
| `alert_status` | Active firing alerts + rule count | Implemented |
| `storage_status` | Storage health/capacity | Not yet implemented |
| `backup_status` | Backup/data retention | Not yet implemented |
| `security_status` | Security health check | Not yet implemented |
| `capacity_planning` | Growth trends | Not yet implemented |
