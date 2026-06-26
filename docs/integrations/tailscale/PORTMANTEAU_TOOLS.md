# Tailscale Portmanteau Tools

**Date:** October 23, 2025  
**Purpose:** Portmanteau tools documentation for Tailscale MCP integration

---

## 🎯 **Overview**

This document provides comprehensive documentation for the Tailscale portmanteau tools architecture, which consolidates multiple related operations into powerful, easy-to-use tools.

---

## 🔧 **Portmanteau Tools Architecture**

### **1. Design Philosophy**

The portmanteau tools pattern consolidates related functionality into single, powerful tools that use an `operation` parameter to specify the action. This approach:

- **Reduces Tool Explosion**: Prevents having dozens of individual tools
- **Improves Usability**: Provides a consistent interface across all operations
- **Enhances Maintainability**: Centralizes related functionality
- **Follows MCP Best Practices**: Aligns with patterns used in other MCP servers

### **2. Tool Structure**

Each portmanteau tool follows this structure:

```python
@mcp.tool()
async def tool_name(operation: str, **kwargs) -> Dict[str, Any]:
    """
    Tool description.
    
    Args:
        operation: The operation to perform
        **kwargs: Additional operation-specific parameters
    """
    try:
        if operation == "operation1":
            # Implementation for operation1
            pass
        elif operation == "operation2":
            # Implementation for operation2
            pass
        else:
            return {"status": "error", "message": "Invalid operation"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

---

## 📊 **Available Portmanteau Tools**

### **1. tailscale_device**

**Purpose**: Device and user management operations

**Operations**:
- `list`: List all devices
- `get`: Get specific device details
- `authorize`: Authorize a device
- `revoke`: Revoke device authorization
- `rename`: Rename a device
- `tag`: Update device tags
- `ssh_access`: Configure SSH access
- `exit_node`: Configure exit node
- `subnet_router`: Configure subnet router

**Example Usage**:
```python
# List all devices
result = await tailscale_device(operation="list")

# Get specific device
result = await tailscale_device(operation="get", device_id="device_123")

# Authorize device
result = await tailscale_device(operation="authorize", device_id="device_123")

# Rename device
result = await tailscale_device(operation="rename", device_id="device_123", name="new_name")

# Update device tags
result = await tailscale_device(operation="tag", device_id="device_123", tags=["tag:server", "tag:production"])
```

### **2. tailscale_network**

**Purpose**: DNS and network management operations

**Operations**:
- `dns_config`: Get DNS configuration
- `acl_config`: Get ACL configuration
- `routes`: Get network routes
- `dns_records`: Get DNS records
- `magic_dns`: Configure MagicDNS
- `custom_dns`: Configure custom DNS

**Example Usage**:
```python
# Get DNS configuration
result = await tailscale_network(operation="dns_config")

# Get ACL configuration
result = await tailscale_network(operation="acl_config")

# Configure MagicDNS
result = await tailscale_network(operation="magic_dns", enabled=True)

# Configure custom DNS
result = await tailscale_network(operation="custom_dns", nameservers=["8.8.8.8", "8.8.4.4"])
```

### **3. tailscale_monitor**

**Purpose**: Monitoring and metrics operations

**Operations**:
- `status`: Get network status
- `metrics`: Get network metrics
- `topology`: Get network topology
- `health`: Get network health
- `grafana_dashboard`: Generate Grafana dashboard

**Example Usage**:
```python
# Get network status
result = await tailscale_monitor(operation="status")

# Get network metrics
result = await tailscale_monitor(operation="metrics")

# Generate Grafana dashboard
result = await tailscale_monitor(operation="grafana_dashboard", dashboard_type="overview")
```

### **4. tailscale_file**

**Purpose**: Taildrop file sharing operations

**Operations**:
- `send`: Send file via Taildrop
- `receive`: Receive file via Taildrop
- `list`: List available files
- `status`: Get transfer status
- `stats`: Get transfer statistics

**Example Usage**:
```python
# Send file
result = await tailscale_file(operation="send", device_id="device_123", filename="example.txt", content="file content")

# Receive file
result = await tailscale_file(operation="receive", device_id="device_123", filename="example.txt")

# List files
result = await tailscale_file(operation="list", device_id="device_123")
```

### **5. tailscale_security**

**Purpose**: Security and compliance operations

**Operations**:
- `scan`: Perform security scan
- `compliance`: Perform compliance check
- `audit`: Perform security audit
- `threat_detect`: Perform threat detection
- `ip_block`: Block IP address
- `quarantine`: Quarantine device

**Example Usage**:
```python
# Perform security scan
result = await tailscale_security(operation="scan", device_id="device_123")

# Perform compliance check
result = await tailscale_security(operation="compliance", device_id="device_123")

# Block IP address
result = await tailscale_security(operation="ip_block", ip_address="192.168.1.100")
```

---

## 🔗 **Integration Patterns**

### **1. Tool Registration**

#### **Basic Tool Registration**
```python
from fastmcp import FastMCP

class TailscalePortmanteauTools:
    def __init__(self, api_key: str, tailnet: str):
        self.api_key = api_key
        self.tailnet = tailnet
        self.mcp = FastMCP("tailscale-mcp")
        self._setup_tools()
    
    def _setup_tools(self):
        """Setup all portmanteau tools."""
        
        @self.mcp.tool()
        async def tailscale_device(operation: str, **kwargs) -> Dict[str, Any]:
            """Device management operations."""
            # Implementation
            pass
        
        @self.mcp.tool()
        async def tailscale_network(operation: str, **kwargs) -> Dict[str, Any]:
            """Network management operations."""
            # Implementation
            pass
        
        @self.mcp.tool()
        async def tailscale_monitor(operation: str, **kwargs) -> Dict[str, Any]:
            """Monitoring operations."""
            # Implementation
            pass
        
        @self.mcp.tool()
        async def tailscale_file(operation: str, **kwargs) -> Dict[str, Any]:
            """File sharing operations."""
            # Implementation
            pass
        
        @self.mcp.tool()
        async def tailscale_security(operation: str, **kwargs) -> Dict[str, Any]:
            """Security operations."""
            # Implementation
            pass
```

### **2. Operation Routing**

#### **Operation Router Pattern**
```python
class OperationRouter:
    def __init__(self):
        self.operations = {}
    
    def register_operation(self, tool_name: str, operation: str, handler: callable):
        """Register operation handler."""
        if tool_name not in self.operations:
            self.operations[tool_name] = {}
        self.operations[tool_name][operation] = handler
    
    async def route_operation(self, tool_name: str, operation: str, **kwargs) -> Dict[str, Any]:
        """Route operation to appropriate handler."""
        if tool_name not in self.operations:
            return {"status": "error", "message": f"Unknown tool: {tool_name}"}
        
        if operation not in self.operations[tool_name]:
            return {"status": "error", "message": f"Unknown operation: {operation}"}
        
        try:
            handler = self.operations[tool_name][operation]
            result = await handler(**kwargs)
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Usage
router = OperationRouter()

# Register operations
router.register_operation("tailscale_device", "list", list_devices_handler)
router.register_operation("tailscale_device", "get", get_device_handler)
router.register_operation("tailscale_device", "authorize", authorize_device_handler)

# Route operations
result = await router.route_operation("tailscale_device", "list")
```

### **3. Parameter Validation**

#### **Parameter Validator Pattern**
```python
from pydantic import BaseModel, validator
from typing import Dict, Any, List, Optional

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

# Usage
validator = TailscaleDeviceValidator()

try:
    validated_params = validator(**parameters)
    # Use validated parameters
except Exception as e:
    return {"status": "error", "message": str(e)}
```

---

## 📊 **Tool Usage Examples**

### **1. Device Management Workflow**

```python
async def device_management_workflow():
    """Example device management workflow."""
    
    # List all devices
    devices_result = await tailscale_device(operation="list")
    if devices_result["status"] != "success":
        return {"status": "error", "message": "Failed to list devices"}
    
    devices = devices_result["data"]
    
    # Check for unauthorized devices
    unauthorized_devices = [d for d in devices if not d.get("authorized", False)]
    
    for device in unauthorized_devices:
        # Authorize device
        auth_result = await tailscale_device(
            operation="authorize",
            device_id=device["id"]
        )
        
        if auth_result["status"] == "success":
            print(f"Authorized device: {device['name']}")
        else:
            print(f"Failed to authorize device: {device['name']}")
    
    # Apply tags to devices
    for device in devices:
        if device.get("os") == "linux":
            tag_result = await tailscale_device(
                operation="tag",
                device_id=device["id"],
                tags=["tag:linux", "tag:server"]
            )
            
            if tag_result["status"] == "success":
                print(f"Applied tags to device: {device['name']}")
    
    return {"status": "success", "message": "Device management workflow completed"}
```

### **2. Network Monitoring Workflow**

```python
async def network_monitoring_workflow():
    """Example network monitoring workflow."""
    
    # Get network status
    status_result = await tailscale_monitor(operation="status")
    if status_result["status"] != "success":
        return {"status": "error", "message": "Failed to get network status"}
    
    status = status_result["data"]
    print(f"Network Status: {status['total_devices']} total devices, {status['online_devices']} online")
    
    # Get network metrics
    metrics_result = await tailscale_monitor(operation="metrics")
    if metrics_result["status"] != "success":
        return {"status": "error", "message": "Failed to get network metrics"}
    
    metrics = metrics_result["data"]
    print(f"Network Metrics: {metrics['device_count']} devices, {metrics['online_count']} online")
    
    # Get network health
    health_result = await tailscale_monitor(operation="health")
    if health_result["status"] != "success":
        return {"status": "error", "message": "Failed to get network health"}
    
    health = health_result["data"]
    print(f"Network Health Score: {health['health_score']}")
    
    # Generate Grafana dashboard
    dashboard_result = await tailscale_monitor(
        operation="grafana_dashboard",
        dashboard_type="comprehensive"
    )
    
    if dashboard_result["status"] == "success":
        print("Grafana dashboard generated successfully")
    
    return {"status": "success", "message": "Network monitoring workflow completed"}
```

### **3. Security Workflow**

```python
async def security_workflow():
    """Example security workflow."""
    
    # Get all devices
    devices_result = await tailscale_device(operation="list")
    if devices_result["status"] != "success":
        return {"status": "error", "message": "Failed to list devices"}
    
    devices = devices_result["data"]
    
    # Perform security scan on each device
    for device in devices:
        scan_result = await tailscale_security(
            operation="scan",
            device_id=device["id"]
        )
        
        if scan_result["status"] == "success":
            print(f"Security scan completed for device: {device['name']}")
        else:
            print(f"Security scan failed for device: {device['name']}")
    
    # Perform compliance check
    compliance_result = await tailscale_security(operation="compliance")
    if compliance_result["status"] == "success":
        print("Compliance check completed")
    
    # Perform security audit
    audit_result = await tailscale_security(operation="audit")
    if audit_result["status"] == "success":
        print("Security audit completed")
    
    return {"status": "success", "message": "Security workflow completed"}
```

---

## 🔧 **Advanced Patterns**

### **1. Tool Composition**

#### **Composing Multiple Tools**
```python
class TailscaleWorkflowComposer:
    def __init__(self, tailscale_tools):
        self.tailscale_tools = tailscale_tools
    
    async def compose_device_workflow(self, device_id: str) -> Dict[str, Any]:
        """Compose device workflow using multiple tools."""
        try:
            # Get device details
            device_result = await self.tailscale_tools.tailscale_device(
                operation="get",
                device_id=device_id
            )
            
            if device_result["status"] != "success":
                return {"status": "error", "message": "Failed to get device details"}
            
            device = device_result["data"]
            
            # Perform security scan
            scan_result = await self.tailscale_tools.tailscale_security(
                operation="scan",
                device_id=device_id
            )
            
            # Get network status
            status_result = await self.tailscale_tools.tailscale_monitor(operation="status")
            
            return {
                "status": "success",
                "data": {
                    "device": device,
                    "security_scan": scan_result,
                    "network_status": status_result
                }
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
```

### **2. Tool Chaining**

#### **Chaining Tool Operations**
```python
class TailscaleToolChain:
    def __init__(self, tailscale_tools):
        self.tailscale_tools = tailscale_tools
        self.chain = []
    
    def add_operation(self, tool_name: str, operation: str, **kwargs):
        """Add operation to chain."""
        self.chain.append({
            "tool_name": tool_name,
            "operation": operation,
            "parameters": kwargs
        })
        return self
    
    async def execute_chain(self) -> List[Dict[str, Any]]:
        """Execute all operations in chain."""
        results = []
        
        for operation in self.chain:
            try:
                tool_name = operation["tool_name"]
                op = operation["operation"]
                params = operation["parameters"]
                
                if tool_name == "tailscale_device":
                    result = await self.tailscale_tools.tailscale_device(op, **params)
                elif tool_name == "tailscale_network":
                    result = await self.tailscale_tools.tailscale_network(op, **params)
                elif tool_name == "tailscale_monitor":
                    result = await self.tailscale_tools.tailscale_monitor(op, **params)
                elif tool_name == "tailscale_file":
                    result = await self.tailscale_tools.tailscale_file(op, **params)
                elif tool_name == "tailscale_security":
                    result = await self.tailscale_tools.tailscale_security(op, **params)
                else:
                    result = {"status": "error", "message": f"Unknown tool: {tool_name}"}
                
                results.append(result)
                
                # Stop chain if operation fails
                if result["status"] != "success":
                    break
            
            except Exception as e:
                results.append({"status": "error", "message": str(e)})
                break
        
        return results

# Usage
chain = TailscaleToolChain(tailscale_tools)
results = await chain.add_operation("tailscale_device", "list") \
                     .add_operation("tailscale_monitor", "status") \
                     .add_operation("tailscale_security", "audit") \
                     .execute_chain()
```

---

## 📚 **Summary**

The Tailscale portmanteau tools architecture provides:

- **Consolidated Functionality**: Multiple operations in single tools
- **Consistent Interface**: Uniform parameter structure across all tools
- **Improved Usability**: Easy-to-use tool interface
- **Enhanced Maintainability**: Centralized related functionality
- **MCP Best Practices**: Follows established MCP patterns

This architecture ensures robust, scalable, and maintainable Tailscale MCP integrations across all repositories.

---

**Status**: ✅ Active  
**Last Updated**: October 23, 2025  
**Version**: 1.0.0  
**Purpose**: Portmanteau tools documentation for Tailscale MCP integration
