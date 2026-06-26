# Tailscale MCP Integration

**Date:** October 23, 2025  
**Purpose:** Tailscale MCP server integration patterns and examples

---

## 🎯 **Overview**

This document provides comprehensive integration patterns and examples for integrating Tailscale with MCP servers, focusing on the FastMCP framework and portmanteau tools architecture.

---

## 🔧 **MCP Server Integration Patterns**

### **1. FastMCP Integration**

#### **Basic MCP Server Setup**
```python
from fastmcp import FastMCP
from typing import Dict, Any
import httpx

class TailscaleMCPServer:
    def __init__(self, api_key: str, tailnet: str):
        self.api_key = api_key
        self.tailnet = tailnet
        self.mcp = FastMCP("tailscale-mcp")
        self._setup_tools()
    
    def _setup_tools(self):
        """Setup MCP tools for Tailscale operations."""
        
        @self.mcp.tool()
        async def tailscale_device(operation: str, device_id: str = None, **kwargs) -> Dict[str, Any]:
            """
            Tailscale device management operations.
            
            Args:
                operation: The operation to perform (list, get, authorize, revoke, rename, tag)
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
                
                elif operation == "rename" and device_id and "name" in kwargs:
                    result = await self._rename_device(device_id, kwargs["name"])
                    return {"status": "success", "result": result}
                
                elif operation == "tag" and device_id and "tags" in kwargs:
                    result = await self._update_device_tags(device_id, kwargs["tags"])
                    return {"status": "success", "result": result}
                
                else:
                    return {"status": "error", "message": "Invalid operation or missing parameters"}
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        async def tailscale_network(operation: str, **kwargs) -> Dict[str, Any]:
            """
            Tailscale network management operations.
            
            Args:
                operation: The operation to perform (dns_config, acl_config, routes, dns_records)
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
                
                elif operation == "dns_records":
                    records = await self._get_dns_records()
                    return {"status": "success", "data": records}
                
                else:
                    return {"status": "error", "message": "Invalid operation"}
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        async def tailscale_monitor(operation: str, **kwargs) -> Dict[str, Any]:
            """
            Tailscale monitoring operations.
            
            Args:
                operation: The operation to perform (status, metrics, topology, health)
                **kwargs: Additional operation-specific parameters
            """
            try:
                if operation == "status":
                    status = await self._get_network_status()
                    return {"status": "success", "data": status}
                
                elif operation == "metrics":
                    metrics = await self._get_network_metrics()
                    return {"status": "success", "data": metrics}
                
                elif operation == "topology":
                    topology = await self._get_network_topology()
                    return {"status": "success", "data": topology}
                
                elif operation == "health":
                    health = await self._get_network_health()
                    return {"status": "success", "data": health}
                
                else:
                    return {"status": "error", "message": "Invalid operation"}
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
    
    async def _get_devices(self) -> List[Dict[str, Any]]:
        """Get all devices in the tailnet."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.tailscale.com/api/v2/tailnet/{self.tailnet}/devices",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()["devices"]
    
    async def _get_device(self, device_id: str) -> Dict[str, Any]:
        """Get specific device details."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.tailscale.com/api/v2/device/{device_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()
    
    async def _authorize_device(self, device_id: str) -> bool:
        """Authorize a device."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.tailscale.com/api/v2/device/{device_id}/authorized",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"authorized": True}
            )
            return response.status_code == 200
    
    async def _revoke_device(self, device_id: str) -> bool:
        """Revoke a device."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.tailscale.com/api/v2/device/{device_id}/authorized",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"authorized": False}
            )
            return response.status_code == 200
    
    async def _rename_device(self, device_id: str, name: str) -> bool:
        """Rename a device."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.tailscale.com/api/v2/device/{device_id}/name",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"name": name}
            )
            return response.status_code == 200
    
    async def _update_device_tags(self, device_id: str, tags: List[str]) -> bool:
        """Update device tags."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.tailscale.com/api/v2/device/{device_id}/tags",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"tags": tags}
            )
            return response.status_code == 200
    
    async def _get_dns_config(self) -> Dict[str, Any]:
        """Get DNS configuration."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.tailscale.com/api/v2/tailnet/{self.tailnet}/dns/nameservers",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()
    
    async def _get_acl_config(self) -> Dict[str, Any]:
        """Get ACL configuration."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.tailscale.com/api/v2/tailnet/{self.tailnet}/acl",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()
    
    async def _get_routes(self) -> List[Dict[str, Any]]:
        """Get network routes."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.tailscale.com/api/v2/tailnet/{self.tailnet}/routes",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()["routes"]
    
    async def _get_dns_records(self) -> List[Dict[str, Any]]:
        """Get DNS records."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.tailscale.com/api/v2/tailnet/{self.tailnet}/dns/records",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()["records"]
    
    async def _get_network_status(self) -> Dict[str, Any]:
        """Get network status."""
        devices = await self._get_devices()
        return {
            "total_devices": len(devices),
            "online_devices": len([d for d in devices if d.get("online", False)]),
            "offline_devices": len([d for d in devices if not d.get("online", False)]),
            "authorized_devices": len([d for d in devices if d.get("authorized", False)]),
            "unauthorized_devices": len([d for d in devices if not d.get("authorized", False)])
        }
    
    async def _get_network_metrics(self) -> Dict[str, Any]:
        """Get network metrics."""
        devices = await self._get_devices()
        return {
            "device_count": len(devices),
            "online_count": len([d for d in devices if d.get("online", False)]),
            "authorized_count": len([d for d in devices if d.get("authorized", False)]),
            "os_distribution": self._get_os_distribution(devices),
            "user_distribution": self._get_user_distribution(devices)
        }
    
    async def _get_network_topology(self) -> Dict[str, Any]:
        """Get network topology."""
        devices = await self._get_devices()
        return {
            "devices": devices,
            "connections": self._get_device_connections(devices),
            "subnets": self._get_subnets(devices)
        }
    
    async def _get_network_health(self) -> Dict[str, Any]:
        """Get network health."""
        devices = await self._get_devices()
        return {
            "health_score": self._calculate_health_score(devices),
            "issues": self._identify_issues(devices),
            "recommendations": self._get_recommendations(devices)
        }
    
    def _get_os_distribution(self, devices: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get OS distribution."""
        os_dist = {}
        for device in devices:
            os_name = device.get("os", "unknown")
            os_dist[os_name] = os_dist.get(os_name, 0) + 1
        return os_dist
    
    def _get_user_distribution(self, devices: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get user distribution."""
        user_dist = {}
        for device in devices:
            user = device.get("user", "unknown")
            user_dist[user] = user_dist.get(user, 0) + 1
        return user_dist
    
    def _get_device_connections(self, devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get device connections."""
        # Implementation for device connections
        return []
    
    def _get_subnets(self, devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get subnets."""
        # Implementation for subnets
        return []
    
    def _calculate_health_score(self, devices: List[Dict[str, Any]]) -> float:
        """Calculate network health score."""
        if not devices:
            return 0.0
        
        online_count = len([d for d in devices if d.get("online", False)])
        authorized_count = len([d for d in devices if d.get("authorized", False)])
        
        health_score = (online_count + authorized_count) / (len(devices) * 2)
        return round(health_score * 100, 2)
    
    def _identify_issues(self, devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify network issues."""
        issues = []
        
        # Check for unauthorized devices
        unauthorized_devices = [d for d in devices if not d.get("authorized", False)]
        if unauthorized_devices:
            issues.append({
                "type": "unauthorized_devices",
                "count": len(unauthorized_devices),
                "devices": unauthorized_devices
            })
        
        # Check for offline devices
        offline_devices = [d for d in devices if not d.get("online", False)]
        if offline_devices:
            issues.append({
                "type": "offline_devices",
                "count": len(offline_devices),
                "devices": offline_devices
            })
        
        return issues
    
    def _get_recommendations(self, devices: List[Dict[str, Any]]) -> List[str]:
        """Get network recommendations."""
        recommendations = []
        
        # Check for unauthorized devices
        unauthorized_devices = [d for d in devices if not d.get("authorized", False)]
        if unauthorized_devices:
            recommendations.append("Consider authorizing unauthorized devices")
        
        # Check for offline devices
        offline_devices = [d for d in devices if not d.get("online", False)]
        if offline_devices:
            recommendations.append("Check offline devices for connectivity issues")
        
        return recommendations
```

### **2. Portmanteau Tools Integration**

#### **Portmanteau Tools Pattern**
```python
from fastmcp import FastMCP
from typing import Dict, Any, List

class TailscalePortmanteauTools:
    def __init__(self, api_key: str, tailnet: str):
        self.api_key = api_key
        self.tailnet = tailnet
        self.mcp = FastMCP("tailscale-mcp")
        self._setup_portmanteau_tools()
    
    def _setup_portmanteau_tools(self):
        """Setup portmanteau tools for Tailscale operations."""
        
        @self.mcp.tool()
        async def tailscale_device(operation: str, device_id: str = None, **kwargs) -> Dict[str, Any]:
            """
            Tailscale device management operations.
            
            Args:
                operation: The operation to perform (list, get, authorize, revoke, rename, tag, ssh_access, exit_node, subnet_router)
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
                
                elif operation == "rename" and device_id and "name" in kwargs:
                    result = await self._rename_device(device_id, kwargs["name"])
                    return {"status": "success", "result": result}
                
                elif operation == "tag" and device_id and "tags" in kwargs:
                    result = await self._update_device_tags(device_id, kwargs["tags"])
                    return {"status": "success", "result": result}
                
                elif operation == "ssh_access" and device_id:
                    result = await self._configure_ssh_access(device_id, kwargs.get("enabled", True))
                    return {"status": "success", "result": result}
                
                elif operation == "exit_node" and device_id:
                    result = await self._configure_exit_node(device_id, kwargs.get("enabled", True))
                    return {"status": "success", "result": result}
                
                elif operation == "subnet_router" and device_id:
                    result = await self._configure_subnet_router(device_id, kwargs.get("enabled", True))
                    return {"status": "success", "result": result}
                
                else:
                    return {"status": "error", "message": "Invalid operation or missing parameters"}
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        async def tailscale_network(operation: str, **kwargs) -> Dict[str, Any]:
            """
            Tailscale network management operations.
            
            Args:
                operation: The operation to perform (dns_config, acl_config, routes, dns_records, magic_dns, custom_dns)
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
                
                elif operation == "dns_records":
                    records = await self._get_dns_records()
                    return {"status": "success", "data": records}
                
                elif operation == "magic_dns":
                    result = await self._configure_magic_dns(kwargs.get("enabled", True))
                    return {"status": "success", "result": result}
                
                elif operation == "custom_dns":
                    result = await self._configure_custom_dns(kwargs.get("nameservers", []))
                    return {"status": "success", "result": result}
                
                else:
                    return {"status": "error", "message": "Invalid operation"}
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        async def tailscale_monitor(operation: str, **kwargs) -> Dict[str, Any]:
            """
            Tailscale monitoring operations.
            
            Args:
                operation: The operation to perform (status, metrics, topology, health, grafana_dashboard)
                **kwargs: Additional operation-specific parameters
            """
            try:
                if operation == "status":
                    status = await self._get_network_status()
                    return {"status": "success", "data": status}
                
                elif operation == "metrics":
                    metrics = await self._get_network_metrics()
                    return {"status": "success", "data": metrics}
                
                elif operation == "topology":
                    topology = await self._get_network_topology()
                    return {"status": "success", "data": topology}
                
                elif operation == "health":
                    health = await self._get_network_health()
                    return {"status": "success", "data": health}
                
                elif operation == "grafana_dashboard":
                    dashboard = await self._generate_grafana_dashboard(kwargs.get("dashboard_type", "overview"))
                    return {"status": "success", "data": dashboard}
                
                else:
                    return {"status": "error", "message": "Invalid operation"}
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        async def tailscale_file(operation: str, **kwargs) -> Dict[str, Any]:
            """
            Tailscale file sharing operations.
            
            Args:
                operation: The operation to perform (send, receive, list, status, stats)
                **kwargs: Additional operation-specific parameters
            """
            try:
                if operation == "send":
                    result = await self._send_file(
                        kwargs.get("device_id"),
                        kwargs.get("filename"),
                        kwargs.get("content")
                    )
                    return {"status": "success", "result": result}
                
                elif operation == "receive":
                    result = await self._receive_file(
                        kwargs.get("device_id"),
                        kwargs.get("filename")
                    )
                    return {"status": "success", "result": result}
                
                elif operation == "list":
                    files = await self._list_files(kwargs.get("device_id"))
                    return {"status": "success", "data": files}
                
                elif operation == "status":
                    status = await self._get_file_status(kwargs.get("transfer_id"))
                    return {"status": "success", "data": status}
                
                elif operation == "stats":
                    stats = await self._get_file_stats()
                    return {"status": "success", "data": stats}
                
                else:
                    return {"status": "error", "message": "Invalid operation"}
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        async def tailscale_security(operation: str, **kwargs) -> Dict[str, Any]:
            """
            Tailscale security operations.
            
            Args:
                operation: The operation to perform (scan, compliance, audit, threat_detect, ip_block, quarantine)
                **kwargs: Additional operation-specific parameters
            """
            try:
                if operation == "scan":
                    result = await self._security_scan(kwargs.get("device_id"))
                    return {"status": "success", "result": result}
                
                elif operation == "compliance":
                    result = await self._compliance_check(kwargs.get("device_id"))
                    return {"status": "success", "result": result}
                
                elif operation == "audit":
                    result = await self._security_audit()
                    return {"status": "success", "result": result}
                
                elif operation == "threat_detect":
                    result = await self._threat_detection()
                    return {"status": "success", "result": result}
                
                elif operation == "ip_block":
                    result = await self._block_ip(kwargs.get("ip_address"))
                    return {"status": "success", "result": result}
                
                elif operation == "quarantine":
                    result = await self._quarantine_device(kwargs.get("device_id"))
                    return {"status": "success", "result": result}
                
                else:
                    return {"status": "error", "message": "Invalid operation"}
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
    
    # Implementation methods for all operations
    async def _get_devices(self) -> List[Dict[str, Any]]:
        """Get all devices in the tailnet."""
        # Implementation details
        pass
    
    async def _get_device(self, device_id: str) -> Dict[str, Any]:
        """Get specific device details."""
        # Implementation details
        pass
    
    async def _authorize_device(self, device_id: str) -> bool:
        """Authorize a device."""
        # Implementation details
        pass
    
    async def _revoke_device(self, device_id: str) -> bool:
        """Revoke a device."""
        # Implementation details
        pass
    
    async def _rename_device(self, device_id: str, name: str) -> bool:
        """Rename a device."""
        # Implementation details
        pass
    
    async def _update_device_tags(self, device_id: str, tags: List[str]) -> bool:
        """Update device tags."""
        # Implementation details
        pass
    
    async def _configure_ssh_access(self, device_id: str, enabled: bool) -> bool:
        """Configure SSH access for device."""
        # Implementation details
        pass
    
    async def _configure_exit_node(self, device_id: str, enabled: bool) -> bool:
        """Configure exit node for device."""
        # Implementation details
        pass
    
    async def _configure_subnet_router(self, device_id: str, enabled: bool) -> bool:
        """Configure subnet router for device."""
        # Implementation details
        pass
    
    async def _get_dns_config(self) -> Dict[str, Any]:
        """Get DNS configuration."""
        # Implementation details
        pass
    
    async def _get_acl_config(self) -> Dict[str, Any]:
        """Get ACL configuration."""
        # Implementation details
        pass
    
    async def _get_routes(self) -> List[Dict[str, Any]]:
        """Get network routes."""
        # Implementation details
        pass
    
    async def _get_dns_records(self) -> List[Dict[str, Any]]:
        """Get DNS records."""
        # Implementation details
        pass
    
    async def _configure_magic_dns(self, enabled: bool) -> bool:
        """Configure MagicDNS."""
        # Implementation details
        pass
    
    async def _configure_custom_dns(self, nameservers: List[str]) -> bool:
        """Configure custom DNS."""
        # Implementation details
        pass
    
    async def _get_network_status(self) -> Dict[str, Any]:
        """Get network status."""
        # Implementation details
        pass
    
    async def _get_network_metrics(self) -> Dict[str, Any]:
        """Get network metrics."""
        # Implementation details
        pass
    
    async def _get_network_topology(self) -> Dict[str, Any]:
        """Get network topology."""
        # Implementation details
        pass
    
    async def _get_network_health(self) -> Dict[str, Any]:
        """Get network health."""
        # Implementation details
        pass
    
    async def _generate_grafana_dashboard(self, dashboard_type: str) -> Dict[str, Any]:
        """Generate Grafana dashboard."""
        # Implementation details
        pass
    
    async def _send_file(self, device_id: str, filename: str, content: str) -> bool:
        """Send file via Taildrop."""
        # Implementation details
        pass
    
    async def _receive_file(self, device_id: str, filename: str) -> str:
        """Receive file via Taildrop."""
        # Implementation details
        pass
    
    async def _list_files(self, device_id: str) -> List[Dict[str, Any]]:
        """List files available for transfer."""
        # Implementation details
        pass
    
    async def _get_file_status(self, transfer_id: str) -> Dict[str, Any]:
        """Get file transfer status."""
        # Implementation details
        pass
    
    async def _get_file_stats(self) -> Dict[str, Any]:
        """Get file transfer statistics."""
        # Implementation details
        pass
    
    async def _security_scan(self, device_id: str) -> Dict[str, Any]:
        """Perform security scan on device."""
        # Implementation details
        pass
    
    async def _compliance_check(self, device_id: str) -> Dict[str, Any]:
        """Perform compliance check on device."""
        # Implementation details
        pass
    
    async def _security_audit(self) -> Dict[str, Any]:
        """Perform security audit."""
        # Implementation details
        pass
    
    async def _threat_detection(self) -> Dict[str, Any]:
        """Perform threat detection."""
        # Implementation details
        pass
    
    async def _block_ip(self, ip_address: str) -> bool:
        """Block IP address."""
        # Implementation details
        pass
    
    async def _quarantine_device(self, device_id: str) -> bool:
        """Quarantine device."""
        # Implementation details
        pass
```

---

## 🔗 **Integration Examples**

### **1. Device Management Integration**

#### **Device Lifecycle Management**
```python
class DeviceLifecycleManager:
    def __init__(self, tailscale_mcp: TailscaleMCPServer):
        self.tailscale_mcp = tailscale_mcp
    
    async def onboard_new_device(self, device_info: Dict[str, Any]) -> Dict[str, Any]:
        """Onboard a new device."""
        try:
            # Get device details
            device_result = await self.tailscale_mcp.mcp.tools["tailscale_device"](
                operation="get",
                device_id=device_info["device_id"]
            )
            
            if device_result["status"] != "success":
                return {"status": "error", "message": "Failed to get device details"}
            
            device = device_result["data"]
            
            # Check if device needs authorization
            if not device.get("authorized", False):
                auth_result = await self.tailscale_mcp.mcp.tools["tailscale_device"](
                    operation="authorize",
                    device_id=device_info["device_id"]
                )
                
                if auth_result["status"] != "success":
                    return {"status": "error", "message": "Failed to authorize device"}
            
            # Apply tags
            if device_info.get("tags"):
                tag_result = await self.tailscale_mcp.mcp.tools["tailscale_device"](
                    operation="tag",
                    device_id=device_info["device_id"],
                    tags=device_info["tags"]
                )
                
                if tag_result["status"] != "success":
                    return {"status": "error", "message": "Failed to apply tags"}
            
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
            revoke_result = await self.tailscale_mcp.mcp.tools["tailscale_device"](
                operation="revoke",
                device_id=device_id
            )
            
            if revoke_result["status"] != "success":
                return {"status": "error", "message": "Failed to revoke device"}
            
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

### **2. Network Monitoring Integration**

#### **Network Monitoring Dashboard**
```python
class NetworkMonitoringDashboard:
    def __init__(self, tailscale_mcp: TailscaleMCPServer):
        self.tailscale_mcp = tailscale_mcp
    
    async def generate_dashboard(self) -> Dict[str, Any]:
        """Generate network monitoring dashboard."""
        try:
            # Get network status
            status_result = await self.tailscale_mcp.mcp.tools["tailscale_monitor"](
                operation="status"
            )
            
            if status_result["status"] != "success":
                return {"status": "error", "message": "Failed to get network status"}
            
            # Get network metrics
            metrics_result = await self.tailscale_mcp.mcp.tools["tailscale_monitor"](
                operation="metrics"
            )
            
            if metrics_result["status"] != "success":
                return {"status": "error", "message": "Failed to get network metrics"}
            
            # Get network health
            health_result = await self.tailscale_mcp.mcp.tools["tailscale_monitor"](
                operation="health"
            )
            
            if health_result["status"] != "success":
                return {"status": "error", "message": "Failed to get network health"}
            
            # Generate Grafana dashboard
            dashboard_result = await self.tailscale_mcp.mcp.tools["tailscale_monitor"](
                operation="grafana_dashboard",
                dashboard_type="comprehensive"
            )
            
            if dashboard_result["status"] != "success":
                return {"status": "error", "message": "Failed to generate Grafana dashboard"}
            
            return {
                "status": "success",
                "data": {
                    "status": status_result["data"],
                    "metrics": metrics_result["data"],
                    "health": health_result["data"],
                    "dashboard": dashboard_result["data"]
                }
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to generate dashboard: {str(e)}"
            }
```

---

## 📊 **MCP Tool Registration**

### **1. Tool Registration Pattern**

#### **Dynamic Tool Registration**
```python
class DynamicToolRegistry:
    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self.registered_tools = {}
    
    def register_tool(self, tool_name: str, tool_func: callable):
        """Register a tool dynamically."""
        self.mcp.tool(name=tool_name)(tool_func)
        self.registered_tools[tool_name] = tool_func
    
    def unregister_tool(self, tool_name: str):
        """Unregister a tool."""
        if tool_name in self.registered_tools:
            del self.registered_tools[tool_name]
    
    def list_registered_tools(self) -> List[str]:
        """List all registered tools."""
        return list(self.registered_tools.keys())
```

### **2. Tool Validation**

#### **Tool Parameter Validation**
```python
from pydantic import BaseModel, validator
from typing import Dict, Any, List, Optional

class ToolParameterValidator:
    def __init__(self):
        self.validators = {}
    
    def register_validator(self, tool_name: str, validator_class: BaseModel):
        """Register parameter validator for a tool."""
        self.validators[tool_name] = validator_class
    
    def validate_parameters(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate tool parameters."""
        if tool_name not in self.validators:
            return {"valid": True, "message": "No validator registered"}
        
        try:
            validator = self.validators[tool_name](**parameters)
            return {"valid": True, "data": validator.dict()}
        except Exception as e:
            return {"valid": False, "message": str(e)}

# Example validator
class TailscaleDeviceValidator(BaseModel):
    operation: str
    device_id: Optional[str] = None
    name: Optional[str] = None
    tags: Optional[List[str]] = None
    
    @validator('operation')
    def validate_operation(cls, v):
        valid_operations = ["list", "get", "authorize", "revoke", "rename", "tag"]
        if v not in valid_operations:
            raise ValueError(f"Invalid operation. Must be one of: {valid_operations}")
        return v
    
    @validator('device_id')
    def validate_device_id(cls, v):
        if v and len(v) < 5:
            raise ValueError("Device ID must be at least 5 characters")
        return v
    
    @validator('name')
    def validate_name(cls, v):
        if v and len(v) < 2:
            raise ValueError("Device name must be at least 2 characters")
        return v
    
    @validator('tags')
    def validate_tags(cls, v):
        if v:
            for tag in v:
                if not tag.startswith("tag:"):
                    raise ValueError("Tags must start with 'tag:'")
        return v
```

---

## 🚀 **Deployment Integration**

### **1. Docker Integration**

#### **Dockerfile for MCP Server**
```dockerfile
FROM python:3.11-slim

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ /app/
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "-m", "tailscalemcp"]
```

#### **Docker Compose for MCP Server**
```yaml
version: '3.8'

services:
  tailscale-mcp:
    build: .
    environment:
      - TAILSCALE_API_KEY=${TAILSCALE_API_KEY}
      - TAILSCALE_TAILNET=${TAILSCALE_TAILNET}
      - LOG_LEVEL=INFO
    ports:
      - "8000:8000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - monitoring
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

This MCP integration guide provides comprehensive patterns for:

- **FastMCP Integration**: Basic and advanced MCP server setup
- **Portmanteau Tools Integration**: Consolidated tool architecture
- **Device Management Integration**: Device lifecycle management
- **Network Monitoring Integration**: Monitoring dashboard generation
- **Tool Registration**: Dynamic tool registration and validation
- **Deployment Integration**: Docker and Kubernetes deployment patterns

These patterns ensure robust, scalable, and maintainable Tailscale MCP integrations across all repositories.

---

**Status**: ✅ Active  
**Last Updated**: October 23, 2025  
**Version**: 1.0.0  
**Purpose**: MCP integration patterns and examples for Tailscale
