# Tailscale Monitoring Integration

**Date:** October 23, 2025  
**Purpose:** Monitoring integration patterns and examples for Tailscale MCP

---

## 🎯 **Overview**

This document provides comprehensive monitoring integration patterns and examples for Tailscale MCP servers, covering Prometheus metrics, Grafana dashboards, structured logging, and health monitoring.

---

## 📊 **Monitoring Architecture**

### **1. Monitoring Stack Components**

The Tailscale monitoring integration includes:

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Loki**: Log aggregation and analysis
- **Promtail**: Log collection and shipping
- **Structured Logging**: JSON-formatted logs for analysis

### **2. Monitoring Data Flow**

```
Tailscale MCP Server → Prometheus Metrics → Grafana Dashboards
                   → Structured Logs → Loki → Grafana Logs
                   → Health Checks → Monitoring Alerts
```

---

## 🔧 **Prometheus Metrics Integration**

### **1. Metrics Collection**

#### **Basic Metrics Setup**
```python
from prometheus_client import Counter, Histogram, Gauge, Info, start_http_server
import time

class TailscaleMetrics:
    def __init__(self):
        # Device metrics
        self.devices_total = Gauge('tailscale_devices_total', 'Total number of devices')
        self.devices_online = Gauge('tailscale_devices_online', 'Number of online devices')
        self.devices_offline = Gauge('tailscale_devices_offline', 'Number of offline devices')
        self.devices_authorized = Gauge('tailscale_devices_authorized', 'Number of authorized devices')
        self.devices_unauthorized = Gauge('tailscale_devices_unauthorized', 'Number of unauthorized devices')
        
        # API metrics
        self.api_requests_total = Counter('tailscale_api_requests_total', 'Total API requests', ['method', 'endpoint'])
        self.api_request_duration = Histogram('tailscale_api_request_duration_seconds', 'API request duration')
        self.api_errors_total = Counter('tailscale_api_errors_total', 'Total API errors', ['error_type'])
        
        # Network metrics
        self.network_health_score = Gauge('tailscale_network_health_score', 'Network health score')
        self.network_latency = Histogram('tailscale_network_latency_seconds', 'Network latency')
        self.network_bandwidth = Gauge('tailscale_network_bandwidth_bytes', 'Network bandwidth usage')
        
        # Application metrics
        self.app_info = Info('tailscale_mcp_info', 'Application information')
        self.app_uptime = Gauge('tailscale_mcp_uptime_seconds', 'Application uptime')
    
    def setup_metrics(self, port: int = 9091):
        """Setup Prometheus metrics server."""
        start_http_server(port)
        
        # Set application info
        self.app_info.info({
            'version': '2.0.0',
            'name': 'tailscale-mcp-server'
        })
    
    def update_device_metrics(self, devices: List[Dict[str, Any]]):
        """Update device metrics."""
        total_devices = len(devices)
        online_devices = len([d for d in devices if d.get("online", False)])
        offline_devices = total_devices - online_devices
        authorized_devices = len([d for d in devices if d.get("authorized", False)])
        unauthorized_devices = total_devices - authorized_devices
        
        self.devices_total.set(total_devices)
        self.devices_online.set(online_devices)
        self.devices_offline.set(offline_devices)
        self.devices_authorized.set(authorized_devices)
        self.devices_unauthorized.set(unauthorized_devices)
    
    def update_network_metrics(self, health_score: float, latency: float, bandwidth: float):
        """Update network metrics."""
        self.network_health_score.set(health_score)
        self.network_latency.observe(latency)
        self.network_bandwidth.set(bandwidth)
    
    def record_api_request(self, method: str, endpoint: str, duration: float, success: bool):
        """Record API request metrics."""
        self.api_requests_total.labels(method=method, endpoint=endpoint).inc()
        self.api_request_duration.observe(duration)
        
        if not success:
            self.api_errors_total.labels(error_type="api_error").inc()
```

### **2. Metrics Collection Workflow**

#### **Automated Metrics Collection**
```python
import asyncio
from datetime import datetime

class MetricsCollector:
    def __init__(self, tailscale_api, metrics: TailscaleMetrics):
        self.tailscale_api = tailscale_api
        self.metrics = metrics
        self.running = False
    
    async def start_collection(self, interval: int = 60):
        """Start automated metrics collection."""
        self.running = True
        
        while self.running:
            try:
                await self.collect_metrics()
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error collecting metrics: {e}")
                await asyncio.sleep(interval)
    
    async def stop_collection(self):
        """Stop metrics collection."""
        self.running = False
    
    async def collect_metrics(self):
        """Collect all metrics."""
        try:
            # Collect device metrics
            devices = await self.tailscale_api.get_devices()
            self.metrics.update_device_metrics(devices)
            
            # Collect network metrics
            health_score = await self.calculate_health_score(devices)
            latency = await self.measure_latency()
            bandwidth = await self.measure_bandwidth()
            
            self.metrics.update_network_metrics(health_score, latency, bandwidth)
            
            print(f"Metrics collected at {datetime.now()}")
        
        except Exception as e:
            print(f"Error collecting metrics: {e}")
    
    async def calculate_health_score(self, devices: List[Dict[str, Any]]) -> float:
        """Calculate network health score."""
        if not devices:
            return 0.0
        
        online_count = len([d for d in devices if d.get("online", False)])
        authorized_count = len([d for d in devices if d.get("authorized", False)])
        
        health_score = (online_count + authorized_count) / (len(devices) * 2)
        return round(health_score * 100, 2)
    
    async def measure_latency(self) -> float:
        """Measure network latency."""
        # Implementation for latency measurement
        return 0.0
    
    async def measure_bandwidth(self) -> float:
        """Measure network bandwidth."""
        # Implementation for bandwidth measurement
        return 0.0
```

---

## 📈 **Grafana Dashboard Integration**

### **1. Dashboard Generation**

#### **Dynamic Dashboard Creation**
```python
import json
from typing import Dict, Any, List

class GrafanaDashboardGenerator:
    def __init__(self):
        self.dashboard_templates = {}
    
    def generate_dashboard(self, dashboard_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Grafana dashboard based on type."""
        if dashboard_type == "overview":
            return self._generate_overview_dashboard(data)
        elif dashboard_type == "device_activity":
            return self._generate_device_activity_dashboard(data)
        elif dashboard_type == "network_health":
            return self._generate_network_health_dashboard(data)
        elif dashboard_type == "comprehensive":
            return self._generate_comprehensive_dashboard(data)
        else:
            raise ValueError(f"Unknown dashboard type: {dashboard_type}")
    
    def _generate_overview_dashboard(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overview dashboard."""
        return {
            "dashboard": {
                "title": "Tailscale MCP Overview",
                "panels": [
                    {
                        "title": "Device Status",
                        "type": "stat",
                        "targets": [
                            {
                                "expr": "tailscale_devices_total",
                                "legendFormat": "Total Devices"
                            },
                            {
                                "expr": "tailscale_devices_online",
                                "legendFormat": "Online Devices"
                            },
                            {
                                "expr": "tailscale_devices_authorized",
                                "legendFormat": "Authorized Devices"
                            }
                        ]
                    },
                    {
                        "title": "Network Health",
                        "type": "gauge",
                        "targets": [
                            {
                                "expr": "tailscale_network_health_score",
                                "legendFormat": "Health Score"
                            }
                        ]
                    },
                    {
                        "title": "API Requests",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "rate(tailscale_api_requests_total[5m])",
                                "legendFormat": "{{method}} {{endpoint}}"
                            }
                        ]
                    }
                ]
            }
        }
    
    def _generate_device_activity_dashboard(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate device activity dashboard."""
        return {
            "dashboard": {
                "title": "Tailscale Device Activity",
                "panels": [
                    {
                        "title": "Device Online Status",
                        "type": "table",
                        "targets": [
                            {
                                "expr": "tailscale_devices_online",
                                "legendFormat": "Online Devices"
                            },
                            {
                                "expr": "tailscale_devices_offline",
                                "legendFormat": "Offline Devices"
                            }
                        ]
                    },
                    {
                        "title": "Device Authorization Status",
                        "type": "piechart",
                        "targets": [
                            {
                                "expr": "tailscale_devices_authorized",
                                "legendFormat": "Authorized"
                            },
                            {
                                "expr": "tailscale_devices_unauthorized",
                                "legendFormat": "Unauthorized"
                            }
                        ]
                    }
                ]
            }
        }
    
    def _generate_network_health_dashboard(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate network health dashboard."""
        return {
            "dashboard": {
                "title": "Tailscale Network Health",
                "panels": [
                    {
                        "title": "Health Score Trend",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "tailscale_network_health_score",
                                "legendFormat": "Health Score"
                            }
                        ]
                    },
                    {
                        "title": "Network Latency",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "tailscale_network_latency_seconds",
                                "legendFormat": "Latency"
                            }
                        ]
                    },
                    {
                        "title": "Bandwidth Usage",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "tailscale_network_bandwidth_bytes",
                                "legendFormat": "Bandwidth"
                            }
                        ]
                    }
                ]
            }
        }
    
    def _generate_comprehensive_dashboard(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive dashboard."""
        overview = self._generate_overview_dashboard(data)
        device_activity = self._generate_device_activity_dashboard(data)
        network_health = self._generate_network_health_dashboard(data)
        
        # Combine all panels
        all_panels = []
        all_panels.extend(overview["dashboard"]["panels"])
        all_panels.extend(device_activity["dashboard"]["panels"])
        all_panels.extend(network_health["dashboard"]["panels"])
        
        return {
            "dashboard": {
                "title": "Tailscale MCP Comprehensive Monitoring",
                "panels": all_panels
            }
        }
```

### **2. Dashboard Deployment**

#### **Dashboard Deployment to Grafana**
```python
import aiohttp
from typing import Dict, Any

class GrafanaDashboardDeployer:
    def __init__(self, grafana_url: str, api_key: str):
        self.grafana_url = grafana_url
        self.api_key = api_key
    
    async def deploy_dashboard(self, dashboard: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy dashboard to Grafana."""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "dashboard": dashboard["dashboard"],
                    "overwrite": True
                }
                
                async with session.post(
                    f"{self.grafana_url}/api/dashboards/db",
                    headers=headers,
                    json=payload
                ) as response:
                    
                    if response.status == 200:
                        return {"status": "success", "message": "Dashboard deployed successfully"}
                    else:
                        error_text = await response.text()
                        return {"status": "error", "message": f"Failed to deploy dashboard: {error_text}"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def list_dashboards(self) -> List[Dict[str, Any]]:
        """List all dashboards in Grafana."""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                async with session.get(
                    f"{self.grafana_url}/api/search?type=dash-db",
                    headers=headers
                ) as response:
                    
                    if response.status == 200:
                        return await response.json()
                    else:
                        return []
        
        except Exception as e:
            print(f"Error listing dashboards: {e}")
            return []
```

---

## 📝 **Structured Logging Integration**

### **1. Structured Logging Setup**

#### **Structured Logging Configuration**
```python
import structlog
import logging
from pathlib import Path

class StructuredLoggingSetup:
    def __init__(self, log_file: str = "logs/tailscale-mcp.log"):
        self.log_file = log_file
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup structured logging."""
        # Create logs directory if it doesn't exist
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Configure structlog for JSON output to file
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
        
        # Setup file handler for structured logs
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        
        # Setup console handler for human-readable logs
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        )
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
    
    def get_logger(self, name: str):
        """Get structured logger."""
        return structlog.get_logger(name)
```

### **2. Logging Integration**

#### **Application Logging**
```python
class TailscaleMCPLogger:
    def __init__(self, logger_name: str = "tailscale-mcp"):
        self.logger = structlog.get_logger(logger_name)
    
    def log_device_event(self, event_type: str, device_id: str, details: Dict[str, Any]):
        """Log device event."""
        self.logger.info(
            "device_event",
            event_type=event_type,
            device_id=device_id,
            details=details
        )
    
    def log_api_call(self, method: str, endpoint: str, status_code: int, duration: float):
        """Log API call."""
        self.logger.info(
            "api_call",
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            duration=duration
        )
    
    def log_network_event(self, event_type: str, details: Dict[str, Any]):
        """Log network event."""
        self.logger.info(
            "network_event",
            event_type=event_type,
            details=details
        )
    
    def log_error(self, error_type: str, error_message: str, context: Dict[str, Any]):
        """Log error."""
        self.logger.error(
            "error",
            error_type=error_type,
            error_message=error_message,
            context=context
        )
    
    def log_metrics_collection(self, metrics_type: str, count: int, duration: float):
        """Log metrics collection."""
        self.logger.info(
            "metrics_collection",
            metrics_type=metrics_type,
            count=count,
            duration=duration
        )
```

---

## 🏥 **Health Monitoring Integration**

### **1. Health Check Implementation**

#### **Health Check System**
```python
from datetime import datetime, timedelta
from typing import Dict, Any, List

class HealthCheckSystem:
    def __init__(self):
        self.health_checks = {}
        self.health_status = {}
        self.last_check = {}
    
    def register_health_check(self, name: str, check_func: callable, interval: int = 60):
        """Register health check."""
        self.health_checks[name] = {
            "function": check_func,
            "interval": interval,
            "last_run": None,
            "status": "unknown"
        }
    
    async def run_health_checks(self) -> Dict[str, Any]:
        """Run all health checks."""
        results = {}
        
        for name, check_info in self.health_checks.items():
            try:
                # Check if enough time has passed since last run
                if (check_info["last_run"] and 
                    datetime.now() - check_info["last_run"] < timedelta(seconds=check_info["interval"])):
                    results[name] = self.health_status.get(name, {"status": "unknown"})
                    continue
                
                # Run health check
                result = await check_info["function"]()
                
                # Update status
                self.health_status[name] = result
                check_info["last_run"] = datetime.now()
                check_info["status"] = result["status"]
                
                results[name] = result
            
            except Exception as e:
                error_result = {
                    "status": "error",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                self.health_status[name] = error_result
                results[name] = error_result
        
        return results
    
    async def get_overall_health(self) -> Dict[str, Any]:
        """Get overall health status."""
        await self.run_health_checks()
        
        # Calculate overall health
        healthy_checks = 0
        total_checks = len(self.health_checks)
        
        for status in self.health_status.values():
            if status.get("status") == "healthy":
                healthy_checks += 1
        
        health_percentage = (healthy_checks / total_checks) * 100 if total_checks > 0 else 0
        
        return {
            "overall_status": "healthy" if health_percentage >= 80 else "degraded" if health_percentage >= 50 else "unhealthy",
            "health_percentage": health_percentage,
            "healthy_checks": healthy_checks,
            "total_checks": total_checks,
            "checks": self.health_status
        }

# Health check implementations
async def check_tailscale_api_health() -> Dict[str, Any]:
    """Check Tailscale API health."""
    try:
        # Implementation for API health check
        return {
            "status": "healthy",
            "message": "API is responding",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"API health check failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

async def check_database_health() -> Dict[str, Any]:
    """Check database health."""
    try:
        # Implementation for database health check
        return {
            "status": "healthy",
            "message": "Database is responding",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Database health check failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

async def check_metrics_collection_health() -> Dict[str, Any]:
    """Check metrics collection health."""
    try:
        # Implementation for metrics collection health check
        return {
            "status": "healthy",
            "message": "Metrics collection is working",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Metrics collection health check failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
```

### **2. Health Monitoring Integration**

#### **Health Monitoring in MCP Server**
```python
class TailscaleMCPHealthMonitor:
    def __init__(self, tailscale_api, metrics_collector):
        self.tailscale_api = tailscale_api
        self.metrics_collector = metrics_collector
        self.health_system = HealthCheckSystem()
        self._setup_health_checks()
    
    def _setup_health_checks(self):
        """Setup health checks."""
        self.health_system.register_health_check(
            "tailscale_api",
            check_tailscale_api_health,
            interval=30
        )
        
        self.health_system.register_health_check(
            "metrics_collection",
            check_metrics_collection_health,
            interval=60
        )
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get health status."""
        return await self.health_system.get_overall_health()
    
    async def start_health_monitoring(self):
        """Start health monitoring."""
        while True:
            try:
                health_status = await self.get_health_status()
                
                # Log health status
                if health_status["overall_status"] != "healthy":
                    print(f"Health status: {health_status['overall_status']} ({health_status['health_percentage']}%)")
                
                await asyncio.sleep(60)  # Check every minute
            
            except Exception as e:
                print(f"Error in health monitoring: {e}")
                await asyncio.sleep(60)
```

---

## 📚 **Summary**

The Tailscale monitoring integration provides:

- **Prometheus Metrics**: Comprehensive metrics collection and export
- **Grafana Dashboards**: Dynamic dashboard generation and deployment
- **Structured Logging**: JSON-formatted logs for analysis
- **Health Monitoring**: Automated health checks and monitoring
- **Integration Patterns**: Reusable patterns for monitoring setup

This monitoring integration ensures comprehensive observability and monitoring for Tailscale MCP servers across all repositories.

---

**Status**: ✅ Active  
**Last Updated**: October 23, 2025  
**Version**: 1.0.0  
**Purpose**: Monitoring integration patterns and examples for Tailscale MCP
