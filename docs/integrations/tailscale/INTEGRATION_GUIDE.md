# Tailscale Integration Guide

**Date:** October 23, 2025  
**Purpose:** Integration patterns and examples for Tailscale across all MCP repositories

---

## 🎯 **Overview**

This guide provides comprehensive integration patterns, examples, and best practices for integrating Tailscale with MCP servers and other applications.

---

## 🔧 **Integration Patterns**

### **1. Direct API Integration**

#### **Basic Integration**
```python
import httpx
import asyncio
from typing import List, Dict, Any

class TailscaleIntegration:
    def __init__(self, api_key: str, tailnet: str):
        self.api_key = api_key
        self.tailnet = tailnet
        self.base_url = "https://api.tailscale.com"
    
    async def get_devices(self) -> List[Dict[str, Any]]:
        """Get all devices in the tailnet."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v2/tailnet/{self.tailnet}/devices",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()["devices"]
    
    async def authorize_device(self, device_id: str) -> bool:
        """Authorize a device."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v2/device/{device_id}/authorized",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"authorized": True}
            )
            return response.status_code == 200
```

### **2. MCP Server Integration**

#### **FastMCP Integration**
```python
from fastmcp import FastMCP
from typing import Dict, Any

class TailscaleMCPIntegration:
    def __init__(self, api_key: str, tailnet: str):
        self.api_key = api_key
        self.tailnet = tailnet
        self.mcp = FastMCP("tailscale-mcp")
        self._setup_tools()
    
    def _setup_tools(self):
        """Setup MCP tools."""
        
        @self.mcp.tool()
        async def tailscale_device(operation: str, device_id: str = None, **kwargs) -> Dict[str, Any]:
            """
            Tailscale device management operations.
            
            Args:
                operation: The operation to perform (list, get, authorize, revoke)
                device_id: Device ID for specific operations
                **kwargs: Additional operation-specific parameters
            """
            try:
                if operation == "list":
                    devices = await self._get_devices()
                    return {"status": "success", "data": devices}
                
                elif operation == "get" and device_id:
                    device = await self._get_device(device_id)
                    return {"status": "success", "data": device}
                
                elif operation == "authorize" and device_id:
                    result = await self._authorize_device(device_id)
                    return {"status": "success", "result": result}
                
                elif operation == "revoke" and device_id:
                    result = await self._revoke_device(device_id)
                    return {"status": "success", "result": result}
                
                else:
                    return {"status": "error", "message": "Invalid operation or missing device_id"}
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        async def tailscale_network(operation: str, **kwargs) -> Dict[str, Any]:
            """
            Tailscale network management operations.
            
            Args:
                operation: The operation to perform (dns_config, acl_config, routes)
                **kwargs: Additional operation-specific parameters
            """
            try:
                if operation == "dns_config":
                    config = await self._get_dns_config()
                    return {"status": "success", "data": config}
                
                elif operation == "acl_config":
                    config = await self._get_acl_config()
                    return {"status": "success", "data": config}
                
                elif operation == "routes":
                    routes = await self._get_routes()
                    return {"status": "success", "data": routes}
                
                else:
                    return {"status": "error", "message": "Invalid operation"}
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
    
    async def _get_devices(self) -> List[Dict[str, Any]]:
        """Internal method to get devices."""
        # Implementation details
        pass
    
    async def _get_device(self, device_id: str) -> Dict[str, Any]:
        """Internal method to get specific device."""
        # Implementation details
        pass
    
    async def _authorize_device(self, device_id: str) -> bool:
        """Internal method to authorize device."""
        # Implementation details
        pass
    
    async def _revoke_device(self, device_id: str) -> bool:
        """Internal method to revoke device."""
        # Implementation details
        pass
    
    async def _get_dns_config(self) -> Dict[str, Any]:
        """Internal method to get DNS configuration."""
        # Implementation details
        pass
    
    async def _get_acl_config(self) -> Dict[str, Any]:
        """Internal method to get ACL configuration."""
        # Implementation details
        pass
    
    async def _get_routes(self) -> List[Dict[str, Any]]:
        """Internal method to get routes."""
        # Implementation details
        pass
```

### **3. Webhook Integration**

#### **Webhook Handler**
```python
from fastapi import FastAPI, Request
import json
from typing import Dict, Any

app = FastAPI()

class TailscaleWebhookHandler:
    def __init__(self):
        self.event_handlers = {}
    
    def register_handler(self, event_type: str, handler: callable):
        """Register event handler."""
        self.event_handlers[event_type] = handler
    
    async def handle_webhook(self, request: Request) -> Dict[str, Any]:
        """Handle incoming webhook."""
        try:
            payload = await request.json()
            event_type = payload.get("event_type")
            
            if event_type in self.event_handlers:
                await self.event_handlers[event_type](payload)
                return {"status": "success", "message": "Webhook processed"}
            else:
                return {"status": "error", "message": f"Unknown event type: {event_type}"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Initialize webhook handler
webhook_handler = TailscaleWebhookHandler()

# Register event handlers
async def handle_device_authorized(payload: Dict[str, Any]):
    """Handle device authorized event."""
    device_id = payload.get("device_id")
    print(f"Device {device_id} has been authorized")

async def handle_device_revoked(payload: Dict[str, Any]):
    """Handle device revoked event."""
    device_id = payload.get("device_id")
    print(f"Device {device_id} has been revoked")

webhook_handler.register_handler("device.authorized", handle_device_authorized)
webhook_handler.register_handler("device.revoked", handle_device_revoked)

@app.post("/webhook/tailscale")
async def tailscale_webhook(request: Request):
    """Tailscale webhook endpoint."""
    return await webhook_handler.handle_webhook(request)
```

---

## 🔗 **Integration Examples**

### **1. Device Management Integration**

#### **Device Lifecycle Management**
```python
class DeviceLifecycleManager:
    def __init__(self, tailscale_api: TailscaleIntegration):
        self.tailscale_api = tailscale_api
    
    async def onboard_new_device(self, device_info: Dict[str, Any]) -> Dict[str, Any]:
        """Onboard a new device."""
        try:
            # Get device details
            device = await self.tailscale_api.get_device(device_info["device_id"])
            
            # Check if device needs authorization
            if not device.get("authorized", False):
                await self.tailscale_api.authorize_device(device_info["device_id"])
            
            # Apply tags
            if device_info.get("tags"):
                await self.tailscale_api.update_device_tags(
                    device_info["device_id"], 
                    device_info["tags"]
                )
            
            # Configure ACL if needed
            if device_info.get("acl_config"):
                await self.tailscale_api.update_acl(device_info["acl_config"])
            
            return {
                "status": "success",
                "message": f"Device {device_info['device_id']} onboarded successfully"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to onboard device: {str(e)}"
            }
    
    async def offboard_device(self, device_id: str) -> Dict[str, Any]:
        """Offboard a device."""
        try:
            # Revoke device
            await self.tailscale_api.revoke_device(device_id)
            
            # Remove from ACL
            await self.tailscale_api.remove_device_from_acl(device_id)
            
            return {
                "status": "success",
                "message": f"Device {device_id} offboarded successfully"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to offboard device: {str(e)}"
            }
```

### **2. Network Security Integration**

#### **Security Policy Enforcement**
```python
class SecurityPolicyEnforcer:
    def __init__(self, tailscale_api: TailscaleIntegration):
        self.tailscale_api = tailscale_api
    
    async def enforce_security_policy(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        """Enforce security policy."""
        try:
            # Get current ACL configuration
            current_acl = await self.tailscale_api.get_acl_config()
            
            # Apply security policy
            updated_acl = self._apply_security_policy(current_acl, policy)
            
            # Update ACL configuration
            await self.tailscale_api.update_acl_config(updated_acl)
            
            # Log security policy enforcement
            await self._log_security_event("policy_enforced", policy)
            
            return {
                "status": "success",
                "message": "Security policy enforced successfully"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to enforce security policy: {str(e)}"
            }
    
    def _apply_security_policy(self, current_acl: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
        """Apply security policy to ACL configuration."""
        # Implementation details for policy application
        pass
    
    async def _log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security event."""
        # Implementation details for security event logging
        pass
```

### **3. Monitoring Integration**

#### **Network Monitoring**
```python
class NetworkMonitor:
    def __init__(self, tailscale_api: TailscaleIntegration):
        self.tailscale_api = tailscale_api
        self.metrics_collector = MetricsCollector()
    
    async def collect_network_metrics(self) -> Dict[str, Any]:
        """Collect network metrics."""
        try:
            # Get device information
            devices = await self.tailscale_api.get_devices()
            
            # Collect metrics
            metrics = {
                "total_devices": len(devices),
                "online_devices": len([d for d in devices if d.get("online", False)]),
                "offline_devices": len([d for d in devices if not d.get("online", False)]),
                "authorized_devices": len([d for d in devices if d.get("authorized", False)]),
                "unauthorized_devices": len([d for d in devices if not d.get("authorized", False)])
            }
            
            # Send metrics to monitoring system
            await self.metrics_collector.send_metrics(metrics)
            
            return {
                "status": "success",
                "metrics": metrics
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to collect network metrics: {str(e)}"
            }
    
    async def detect_anomalies(self) -> Dict[str, Any]:
        """Detect network anomalies."""
        try:
            # Get current network state
            devices = await self.tailscale_api.get_devices()
            
            # Detect anomalies
            anomalies = []
            
            # Check for unauthorized devices
            unauthorized_devices = [d for d in devices if not d.get("authorized", False)]
            if unauthorized_devices:
                anomalies.append({
                    "type": "unauthorized_devices",
                    "count": len(unauthorized_devices),
                    "devices": unauthorized_devices
                })
            
            # Check for offline devices
            offline_devices = [d for d in devices if not d.get("online", False)]
            if offline_devices:
                anomalies.append({
                    "type": "offline_devices",
                    "count": len(offline_devices),
                    "devices": offline_devices
                })
            
            return {
                "status": "success",
                "anomalies": anomalies
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to detect anomalies: {str(e)}"
            }

class MetricsCollector:
    async def send_metrics(self, metrics: Dict[str, Any]):
        """Send metrics to monitoring system."""
        # Implementation details for metrics collection
        pass
```

---

## 🔌 **Third-Party Integrations**

### **1. Slack Integration**

#### **Slack Notifications**
```python
import aiohttp
from typing import Dict, Any

class SlackIntegration:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def send_notification(self, message: str, channel: str = None) -> Dict[str, Any]:
        """Send notification to Slack."""
        try:
            payload = {
                "text": message,
                "channel": channel
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 200:
                        return {"status": "success", "message": "Notification sent"}
                    else:
                        return {"status": "error", "message": f"Failed to send notification: {response.status}"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def send_device_alert(self, device_id: str, event_type: str) -> Dict[str, Any]:
        """Send device alert to Slack."""
        message = f"🚨 Tailscale Device Alert: {event_type} for device {device_id}"
        return await self.send_notification(message)

# Usage
slack_integration = SlackIntegration("https://hooks.slack.com/services/your/webhook/url")

# Send device authorization notification
await slack_integration.send_device_alert("device_123", "authorized")
```

### **2. Discord Integration**

#### **Discord Bot Integration**
```python
import discord
from discord.ext import commands

class TailscaleDiscordBot(commands.Bot):
    def __init__(self, tailscale_api: TailscaleIntegration):
        super().__init__(command_prefix='!')
        self.tailscale_api = tailscale_api
    
    @commands.command(name='devices')
    async def list_devices(self, ctx):
        """List all Tailscale devices."""
        try:
            devices = await self.tailscale_api.get_devices()
            
            embed = discord.Embed(
                title="Tailscale Devices",
                description=f"Total devices: {len(devices)}",
                color=0x00ff00
            )
            
            for device in devices[:10]:  # Limit to 10 devices
                status = "🟢 Online" if device.get("online", False) else "🔴 Offline"
                authorized = "✅ Authorized" if device.get("authorized", False) else "❌ Unauthorized"
                
                embed.add_field(
                    name=device.get("name", "Unknown"),
                    value=f"{status} | {authorized}",
                    inline=False
                )
            
            await ctx.send(embed=embed)
        
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")
    
    @commands.command(name='authorize')
    async def authorize_device(self, ctx, device_id: str):
        """Authorize a Tailscale device."""
        try:
            result = await self.tailscale_api.authorize_device(device_id)
            
            if result:
                await ctx.send(f"✅ Device {device_id} authorized successfully")
            else:
                await ctx.send(f"❌ Failed to authorize device {device_id}")
        
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

# Usage
bot = TailscaleDiscordBot(tailscale_api)
bot.run('your_discord_bot_token')
```

### **3. PagerDuty Integration**

#### **PagerDuty Alerts**
```python
import aiohttp
from typing import Dict, Any

class PagerDutyIntegration:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://events.pagerduty.com/v2"
    
    async def create_incident(self, summary: str, severity: str = "critical") -> Dict[str, Any]:
        """Create PagerDuty incident."""
        try:
            payload = {
                "routing_key": self.api_key,
                "event_action": "trigger",
                "payload": {
                    "summary": summary,
                    "severity": severity,
                    "source": "tailscale-mcp",
                    "component": "network"
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/enqueue", json=payload) as response:
                    if response.status == 202:
                        return {"status": "success", "message": "Incident created"}
                    else:
                        return {"status": "error", "message": f"Failed to create incident: {response.status}"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def resolve_incident(self, dedup_key: str) -> Dict[str, Any]:
        """Resolve PagerDuty incident."""
        try:
            payload = {
                "routing_key": self.api_key,
                "event_action": "resolve",
                "dedup_key": dedup_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/enqueue", json=payload) as response:
                    if response.status == 202:
                        return {"status": "success", "message": "Incident resolved"}
                    else:
                        return {"status": "error", "message": f"Failed to resolve incident: {response.status}"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Usage
pagerduty_integration = PagerDutyIntegration("your_pagerduty_api_key")

# Create incident for unauthorized device
await pagerduty_integration.create_incident("Unauthorized device detected on Tailscale network")
```

---

## 📊 **Data Integration**

### **1. Database Integration**

#### **PostgreSQL Integration**
```python
import asyncpg
from typing import List, Dict, Any

class TailscaleDatabaseIntegration:
    def __init__(self, database_url: str):
        self.database_url = database_url
    
    async def store_device_data(self, devices: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Store device data in database."""
        try:
            conn = await asyncpg.connect(self.database_url)
            
            for device in devices:
                await conn.execute(
                    """
                    INSERT INTO tailscale_devices 
                    (device_id, name, user, addresses, hostname, os, created, last_seen, online, authorized, tags)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                    ON CONFLICT (device_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    user = EXCLUDED.user,
                    addresses = EXCLUDED.addresses,
                    hostname = EXCLUDED.hostname,
                    os = EXCLUDED.os,
                    last_seen = EXCLUDED.last_seen,
                    online = EXCLUDED.online,
                    authorized = EXCLUDED.authorized,
                    tags = EXCLUDED.tags
                    """,
                    device.get("id"),
                    device.get("name"),
                    device.get("user"),
                    device.get("addresses", []),
                    device.get("hostname"),
                    device.get("os"),
                    device.get("created"),
                    device.get("lastSeen"),
                    device.get("online", False),
                    device.get("authorized", False),
                    device.get("tags", [])
                )
            
            await conn.close()
            
            return {
                "status": "success",
                "message": f"Stored {len(devices)} devices in database"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to store device data: {str(e)}"
            }
    
    async def get_device_history(self, device_id: str) -> List[Dict[str, Any]]:
        """Get device history from database."""
        try:
            conn = await asyncpg.connect(self.database_url)
            
            rows = await conn.fetch(
                """
                SELECT * FROM tailscale_devices 
                WHERE device_id = $1 
                ORDER BY last_seen DESC
                """,
                device_id
            )
            
            await conn.close()
            
            return [dict(row) for row in rows]
        
        except Exception as e:
            return []
```

### **2. Log Integration**

#### **Structured Logging**
```python
import structlog
import json
from typing import Dict, Any

class TailscaleLogIntegration:
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.logger = structlog.get_logger(__name__)
    
    async def log_device_event(self, event_type: str, device_id: str, details: Dict[str, Any]):
        """Log device event."""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "device_id": device_id,
                "details": details
            }
            
            self.logger.info("device_event", **log_entry)
            
            # Write to file
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        
        except Exception as e:
            self.logger.error("Failed to log device event", error=str(e))
    
    async def log_network_event(self, event_type: str, details: Dict[str, Any]):
        """Log network event."""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "details": details
            }
            
            self.logger.info("network_event", **log_entry)
            
            # Write to file
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        
        except Exception as e:
            self.logger.error("Failed to log network event", error=str(e))
```

---

## 🚀 **Deployment Integration**

### **1. Docker Integration**

#### **Docker Compose with Tailscale**
```yaml
version: '3.8'

services:
  tailscale-mcp:
    build: .
    environment:
      - TAILSCALE_API_KEY=${TAILSCALE_API_KEY}
      - TAILSCALE_TAILNET=${TAILSCALE_TAILNET}
    networks:
      - tailscale-network
      - monitoring-network
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    networks:
      - monitoring-network
  
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    networks:
      - monitoring-network

networks:
  tailscale-network:
    driver: bridge
  monitoring-network:
    driver: bridge
```

### **2. Kubernetes Integration**

#### **Kubernetes Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tailscale-mcp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tailscale-mcp
  template:
    metadata:
      labels:
        app: tailscale-mcp
    spec:
      containers:
      - name: tailscale-mcp
        image: tailscale-mcp:latest
        env:
        - name: TAILSCALE_API_KEY
          valueFrom:
            secretKeyRef:
              name: tailscale-secrets
              key: api-key
        - name: TAILSCALE_TAILNET
          valueFrom:
            configMapKeyRef:
              name: tailscale-config
              key: tailnet
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## 📚 **Summary**

This integration guide provides comprehensive patterns for:

- **Direct API Integration**: Basic and advanced API usage patterns
- **MCP Server Integration**: FastMCP tool registration and management
- **Webhook Integration**: Event handling and webhook processing
- **Third-Party Integrations**: Slack, Discord, PagerDuty integrations
- **Data Integration**: Database and logging integration
- **Deployment Integration**: Docker and Kubernetes deployment patterns

These patterns ensure robust, scalable, and maintainable Tailscale integrations across all MCP repositories.

---

**Status**: ✅ Active  
**Last Updated**: October 23, 2025  
**Version**: 1.0.0  
**Purpose**: Integration patterns and examples for Tailscale across all MCP repositories
