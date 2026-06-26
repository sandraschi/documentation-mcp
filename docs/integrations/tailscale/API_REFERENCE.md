# Tailscale API Reference

**Date:** October 23, 2025  
**Purpose:** Comprehensive Tailscale API reference for all MCP repositories

---

## 🎯 **Overview**

This document provides comprehensive documentation for the Tailscale API, covering all endpoints, authentication, and usage patterns relevant to MCP server development.

---

## 🔐 **Authentication**

### **API Key Authentication**
```python
import httpx

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
```

### **Environment Variables**
```bash
TAILSCALE_API_KEY=your_api_key_here
TAILSCALE_TAILNET=your_tailnet_name
```

---

## 📡 **Core API Endpoints**

### **Devices**

#### **List Devices**
```http
GET /api/v2/device
```

**Parameters:**
- `fields`: Comma-separated list of fields to include
- `limit`: Maximum number of devices to return

**Response:**
```json
{
  "devices": [
    {
      "id": "device_id",
      "name": "device_name",
      "user": "user@example.com",
      "addresses": ["100.64.0.1"],
      "hostname": "device-hostname",
      "os": "linux",
      "created": "2023-01-01T00:00:00Z",
      "lastSeen": "2023-01-01T12:00:00Z",
      "online": true,
      "authorized": true,
      "tags": ["tag:server", "tag:production"]
    }
  ]
}
```

#### **Get Device Details**
```http
GET /api/v2/device/{device_id}
```

#### **Authorize Device**
```http
POST /api/v2/device/{device_id}/authorized
```

**Request Body:**
```json
{
  "authorized": true
}
```

#### **Update Device Tags**
```http
POST /api/v2/device/{device_id}/tags
```

**Request Body:**
```json
{
  "tags": ["tag:server", "tag:production"]
}
```

### **Users**

#### **List Users**
```http
GET /api/v2/user
```

**Response:**
```json
{
  "users": [
    {
      "id": "user_id",
      "loginName": "user@example.com",
      "displayName": "User Name",
      "profilePicURL": "https://example.com/avatar.jpg",
      "created": "2023-01-01T00:00:00Z"
    }
  ]
}
```

#### **Create User**
```http
POST /api/v2/user
```

**Request Body:**
```json
{
  "loginName": "user@example.com",
  "displayName": "User Name"
}
```

### **Access Control Lists (ACLs)**

#### **Get ACL**
```http
GET /api/v2/tailnet/{tailnet}/acl
```

**Response:**
```json
{
  "acl": [
    {
      "action": "accept",
      "src": ["*"],
      "dst": ["*:*"]
    }
  ],
  "groups": {
    "group:admins": ["user@example.com"]
  },
  "hosts": {
    "server": "100.64.0.1"
  },
  "tests": []
}
```

#### **Update ACL**
```http
POST /api/v2/tailnet/{tailnet}/acl
```

**Request Body:**
```json
{
  "acl": [
    {
      "action": "accept",
      "src": ["group:admins"],
      "dst": ["*:22"]
    }
  ]
}
```

### **DNS**

#### **Get DNS Configuration**
```http
GET /api/v2/tailnet/{tailnet}/dns/nameservers
```

#### **Update DNS Configuration**
```http
POST /api/v2/tailnet/{tailnet}/dns/nameservers
```

**Request Body:**
```json
{
  "nameservers": ["8.8.8.8", "8.8.4.4"]
}
```

#### **Get DNS Records**
```http
GET /api/v2/tailnet/{tailnet}/dns/records
```

#### **Create DNS Record**
```http
POST /api/v2/tailnet/{tailnet}/dns/records
```

**Request Body:**
```json
{
  "name": "example",
  "type": "A",
  "value": "100.64.0.1"
}
```

### **Taildrop (File Sharing)**

#### **List Files**
```http
GET /api/v2/tailnet/{tailnet}/files
```

#### **Send File**
```http
POST /api/v2/tailnet/{tailnet}/files/{device_id}
```

**Request Body:**
```json
{
  "filename": "example.txt",
  "content": "file content here"
}
```

#### **Receive File**
```http
GET /api/v2/tailnet/{tailnet}/files/{device_id}/{filename}
```

---

## 🔧 **Common Usage Patterns**

### **Device Management**
```python
async def list_devices(api_key: str, tailnet: str) -> List[Dict]:
    """List all devices in the tailnet."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.tailscale.com/api/v2/tailnet/{tailnet}/devices",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        return response.json()["devices"]

async def authorize_device(api_key: str, device_id: str) -> bool:
    """Authorize a device."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.tailscale.com/api/v2/device/{device_id}/authorized",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"authorized": True}
        )
        return response.status_code == 200
```

### **ACL Management**
```python
async def get_acl(api_key: str, tailnet: str) -> Dict:
    """Get current ACL configuration."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.tailscale.com/api/v2/tailnet/{tailnet}/acl",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        return response.json()

async def update_acl(api_key: str, tailnet: str, acl_config: Dict) -> bool:
    """Update ACL configuration."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.tailscale.com/api/v2/tailnet/{tailnet}/acl",
            headers={"Authorization": f"Bearer {api_key}"},
            json=acl_config
        )
        return response.status_code == 200
```

### **DNS Management**
```python
async def get_dns_records(api_key: str, tailnet: str) -> List[Dict]:
    """Get DNS records."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.tailscale.com/api/v2/tailnet/{tailnet}/dns/records",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        return response.json()["records"]

async def create_dns_record(api_key: str, tailnet: str, name: str, 
                          record_type: str, value: str) -> bool:
    """Create a DNS record."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.tailscale.com/api/v2/tailnet/{tailnet}/dns/records",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "name": name,
                "type": record_type,
                "value": value
            }
        )
        return response.status_code == 200
```

---

## 📊 **Rate Limiting**

### **Rate Limits**
- **Standard API**: 100 requests per minute
- **Bulk Operations**: 10 requests per minute
- **Authentication**: 20 requests per minute

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

### **Handling Rate Limits**
```python
import asyncio
from datetime import datetime

async def make_request_with_retry(client, url, headers, max_retries=3):
    """Make request with rate limit retry logic."""
    for attempt in range(max_retries):
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 429:  # Rate limited
                retry_after = int(response.headers.get("Retry-After", 60))
                await asyncio.sleep(retry_after)
                continue
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(2 ** attempt)
```

---

## 🚨 **Error Handling**

### **Common Error Codes**
- **400 Bad Request**: Invalid request parameters
- **401 Unauthorized**: Invalid or missing API key
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

### **Error Response Format**
```json
{
  "error": {
    "code": "invalid_request",
    "message": "Invalid request parameters",
    "details": {
      "field": "device_id",
      "reason": "Device not found"
    }
  }
}
```

### **Error Handling Pattern**
```python
async def handle_api_response(response: httpx.Response) -> Dict:
    """Handle API response with proper error handling."""
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise ValueError("Invalid API key")
    elif response.status_code == 403:
        raise PermissionError("Insufficient permissions")
    elif response.status_code == 404:
        raise ValueError("Resource not found")
    elif response.status_code == 429:
        raise ValueError("Rate limit exceeded")
    else:
        raise RuntimeError(f"API error: {response.status_code}")
```

---

## 🔍 **Advanced Features**

### **Webhooks**
```python
async def create_webhook(api_key: str, tailnet: str, url: str, 
                        events: List[str]) -> Dict:
    """Create a webhook for events."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.tailscale.com/api/v2/tailnet/{tailnet}/webhooks",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "url": url,
                "events": events
            }
        )
        return response.json()
```

### **Bulk Operations**
```python
async def bulk_authorize_devices(api_key: str, device_ids: List[str]) -> Dict:
    """Authorize multiple devices in bulk."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.tailscale.com/api/v2/device/bulk/authorize",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"device_ids": device_ids}
        )
        return response.json()
```

---

## 📚 **Additional Resources**

### **Official Documentation**
- [Tailscale API Documentation](https://tailscale.com/kb/1247/api)
- [Tailscale CLI Reference](https://tailscale.com/kb/1240/tailscale-cli)
- [Tailscale Admin Console](https://login.tailscale.com/admin)

### **Community Resources**
- [Tailscale GitHub](https://github.com/tailscale/tailscale)
- [Tailscale Community Forum](https://github.com/tailscale/tailscale/discussions)
- [Tailscale Blog](https://tailscale.com/blog/)

---

**Status**: ✅ Active  
**Last Updated**: October 23, 2025  
**Version**: 1.0.0  
**Purpose**: Comprehensive Tailscale API reference for MCP development
