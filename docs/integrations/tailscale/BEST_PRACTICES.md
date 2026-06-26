# Tailscale Best Practices

**Date:** October 23, 2025  
**Purpose:** Best practices and patterns for Tailscale integration across all MCP repositories

---

## 🎯 **Overview**

This document provides best practices, patterns, and recommendations for effectively using Tailscale in MCP server development and integration.

---

## 🔐 **Security Best Practices**

### **API Key Management**

#### **Secure Storage**
```python
import os
from cryptography.fernet import Fernet

class SecureAPIKeyManager:
    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)
    
    def encrypt_api_key(self, api_key: str) -> bytes:
        """Encrypt API key for secure storage."""
        return self.cipher.encrypt(api_key.encode())
    
    def decrypt_api_key(self, encrypted_key: bytes) -> str:
        """Decrypt API key for use."""
        return self.cipher.decrypt(encrypted_key).decode()
```

#### **Environment Variables**
```bash
# Use environment variables for API keys
export TAILSCALE_API_KEY="your_api_key_here"
export TAILSCALE_TAILNET="your_tailnet_name"

# Never commit API keys to version control
echo "TAILSCALE_API_KEY=your_api_key_here" >> .env
echo ".env" >> .gitignore
```

#### **API Key Rotation**
```python
import asyncio
from datetime import datetime, timedelta

class APIKeyRotator:
    def __init__(self, api_key: str, rotation_days: int = 90):
        self.api_key = api_key
        self.rotation_days = rotation_days
        self.last_rotation = datetime.now()
    
    async def should_rotate(self) -> bool:
        """Check if API key should be rotated."""
        return (datetime.now() - self.last_rotation).days >= self.rotation_days
    
    async def rotate_api_key(self) -> str:
        """Rotate API key (implement your rotation logic)."""
        # Implement your API key rotation logic
        pass
```

### **Access Control**

#### **Principle of Least Privilege**
```python
# Define minimal required permissions
REQUIRED_PERMISSIONS = [
    "device:read",
    "device:write",
    "acl:read"
]

async def validate_permissions(api_key: str) -> bool:
    """Validate that API key has required permissions."""
    # Implement permission validation logic
    pass
```

#### **ACL Best Practices**
```json
{
  "acl": [
    {
      "action": "accept",
      "src": ["group:admins"],
      "dst": ["*:22", "*:80", "*:443"]
    },
    {
      "action": "accept",
      "src": ["group:users"],
      "dst": ["*:80", "*:443"]
    },
    {
      "action": "accept",
      "src": ["*"],
      "dst": ["*:80"]
    }
  ],
  "groups": {
    "group:admins": ["admin@example.com"],
    "group:users": ["user@example.com"]
  }
}
```

---

## 🏗️ **Architecture Best Practices**

### **Connection Management**

#### **Connection Pooling**
```python
import httpx
import asyncio
from typing import Optional

class TailscaleAPIClient:
    def __init__(self, api_key: str, tailnet: str):
        self.api_key = api_key
        self.tailnet = tailnet
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=20)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
    
    async def get_devices(self) -> List[Dict]:
        """Get devices using connection pool."""
        if not self._client:
            raise RuntimeError("Client not initialized")
        
        response = await self._client.get(
            f"https://api.tailscale.com/api/v2/tailnet/{self.tailnet}/devices",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()["devices"]
```

#### **Retry Logic**
```python
import asyncio
from typing import Callable, Any
import random

class RetryHandler:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with exponential backoff retry."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                    await asyncio.sleep(delay)
                else:
                    raise last_exception
```

### **Error Handling**

#### **Comprehensive Error Handling**
```python
from enum import Enum
from typing import Dict, Any

class TailscaleErrorType(Enum):
    AUTHENTICATION = "authentication_error"
    PERMISSION = "permission_error"
    NOT_FOUND = "not_found_error"
    RATE_LIMIT = "rate_limit_error"
    NETWORK = "network_error"
    UNKNOWN = "unknown_error"

class TailscaleAPIError(Exception):
    def __init__(self, error_type: TailscaleErrorType, message: str, details: Dict[str, Any] = None):
        self.error_type = error_type
        self.message = message
        self.details = details or {}
        super().__init__(f"{error_type.value}: {message}")

async def handle_api_error(response: httpx.Response) -> None:
    """Handle API errors with proper exception types."""
    if response.status_code == 401:
        raise TailscaleAPIError(
            TailscaleErrorType.AUTHENTICATION,
            "Invalid or missing API key"
        )
    elif response.status_code == 403:
        raise TailscaleAPIError(
            TailscaleErrorType.PERMISSION,
            "Insufficient permissions"
        )
    elif response.status_code == 404:
        raise TailscaleAPIError(
            TailscaleErrorType.NOT_FOUND,
            "Resource not found"
        )
    elif response.status_code == 429:
        raise TailscaleAPIError(
            TailscaleErrorType.RATE_LIMIT,
            "Rate limit exceeded"
        )
    elif response.status_code >= 500:
        raise TailscaleAPIError(
            TailscaleErrorType.NETWORK,
            "Server error"
        )
    else:
        raise TailscaleAPIError(
            TailscaleErrorType.UNKNOWN,
            f"Unknown error: {response.status_code}"
        )
```

---

## 📊 **Performance Best Practices**

### **Caching**

#### **Response Caching**
```python
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class TailscaleCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, tuple[Any, datetime]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl_seconds):
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Set cached value with timestamp."""
        self._cache[key] = (value, datetime.now())
    
    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()

# Usage with caching
async def get_devices_cached(cache: TailscaleCache, client: TailscaleAPIClient) -> List[Dict]:
    """Get devices with caching."""
    cache_key = "devices"
    cached_devices = cache.get(cache_key)
    
    if cached_devices is not None:
        return cached_devices
    
    devices = await client.get_devices()
    cache.set(cache_key, devices)
    return devices
```

### **Batch Operations**

#### **Bulk Device Operations**
```python
async def bulk_authorize_devices(device_ids: List[str], api_key: str) -> Dict[str, bool]:
    """Authorize multiple devices in batch."""
    results = {}
    
    # Process in batches of 10 to avoid rate limits
    batch_size = 10
    for i in range(0, len(device_ids), batch_size):
        batch = device_ids[i:i + batch_size]
        
        tasks = [
            authorize_device(device_id, api_key)
            for device_id in batch
        ]
        
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for device_id, result in zip(batch, batch_results):
            results[device_id] = result if not isinstance(result, Exception) else False
        
        # Rate limit delay between batches
        await asyncio.sleep(1)
    
    return results
```

---

## 🔧 **Integration Best Practices**

### **MCP Server Integration**

#### **Tool Registration Pattern**
```python
from fastmcp import FastMCP
from typing import Dict, Any

class TailscaleMCPTools:
    def __init__(self, api_key: str, tailnet: str):
        self.api_key = api_key
        self.tailnet = tailnet
        self.cache = TailscaleCache()
        self.retry_handler = RetryHandler()
    
    async def list_devices(self, online_only: bool = False) -> Dict[str, Any]:
        """List devices with caching and error handling."""
        try:
            devices = await self.retry_handler.execute_with_retry(
                self._get_devices_cached
            )
            
            if online_only:
                devices = [d for d in devices if d.get("online", False)]
            
            return {
                "status": "success",
                "data": devices,
                "count": len(devices)
            }
        except TailscaleAPIError as e:
            return {
                "status": "error",
                "error_type": e.error_type.value,
                "message": e.message,
                "details": e.details
            }
    
    async def _get_devices_cached(self) -> List[Dict]:
        """Get devices with caching."""
        cache_key = f"devices_{self.tailnet}"
        cached_devices = self.cache.get(cache_key)
        
        if cached_devices is not None:
            return cached_devices
        
        # Fetch from API and cache
        devices = await self._fetch_devices_from_api()
        self.cache.set(cache_key, devices)
        return devices
```

### **Configuration Management**

#### **Configuration Validation**
```python
from pydantic import BaseModel, validator
from typing import Optional

class TailscaleConfig(BaseModel):
    api_key: str
    tailnet: str
    base_url: str = "https://api.tailscale.com"
    timeout: int = 30
    max_retries: int = 3
    cache_ttl: int = 300
    
    @validator('api_key')
    def validate_api_key(cls, v):
        if not v or len(v) < 20:
            raise ValueError('API key must be at least 20 characters')
        return v
    
    @validator('tailnet')
    def validate_tailnet(cls, v):
        if not v or '.' not in v:
            raise ValueError('Tailnet must be a valid domain')
        return v
    
    @validator('timeout')
    def validate_timeout(cls, v):
        if v < 1 or v > 300:
            raise ValueError('Timeout must be between 1 and 300 seconds')
        return v

# Usage
config = TailscaleConfig(
    api_key=os.getenv("TAILSCALE_API_KEY"),
    tailnet=os.getenv("TAILSCALE_TAILNET")
)
```

---

## 📈 **Monitoring and Observability**

### **Logging**

#### **Structured Logging**
```python
import structlog
import logging

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.LoggerFactory(),
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

async def log_api_call(endpoint: str, method: str, status_code: int, duration: float):
    """Log API calls with structured logging."""
    logger.info(
        "api_call",
        endpoint=endpoint,
        method=method,
        status_code=status_code,
        duration=duration
    )
```

### **Metrics**

#### **Performance Metrics**
```python
import time
from prometheus_client import Counter, Histogram, Gauge

# Metrics
api_requests_total = Counter('tailscale_api_requests_total', 'Total API requests', ['method', 'endpoint'])
api_request_duration = Histogram('tailscale_api_request_duration_seconds', 'API request duration')
active_devices = Gauge('tailscale_active_devices', 'Number of active devices')

async def track_api_call(endpoint: str, method: str):
    """Track API call metrics."""
    start_time = time.time()
    
    try:
        # Make API call
        result = await make_api_call(endpoint, method)
        
        # Record metrics
        api_requests_total.labels(method=method, endpoint=endpoint).inc()
        api_request_duration.observe(time.time() - start_time)
        
        return result
    except Exception as e:
        # Record error metrics
        api_requests_total.labels(method=method, endpoint=endpoint).inc()
        raise e
```

---

## 🚀 **Deployment Best Practices**

### **Docker Integration**

#### **Dockerfile Best Practices**
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

#### **Docker Compose**
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

### **Environment Configuration**

#### **Production Configuration**
```bash
# Production environment variables
TAILSCALE_API_KEY=your_production_api_key
TAILSCALE_TAILNET=your_production_tailnet
LOG_LEVEL=INFO
CACHE_TTL=300
MAX_RETRIES=3
TIMEOUT=30
```

---

## 📚 **Testing Best Practices**

### **Unit Testing**

#### **Mock API Responses**
```python
import pytest
from unittest.mock import AsyncMock, patch
import httpx

@pytest.mark.asyncio
async def test_list_devices():
    """Test device listing with mocked API response."""
    mock_response = AsyncMock()
    mock_response.json.return_value = {
        "devices": [
            {
                "id": "test_device",
                "name": "test_device",
                "online": True
            }
        ]
    }
    
    with patch('httpx.AsyncClient.get', return_value=mock_response):
        client = TailscaleAPIClient("test_key", "test_tailnet")
        devices = await client.get_devices()
        
        assert len(devices) == 1
        assert devices[0]["id"] == "test_device"
```

### **Integration Testing**

#### **Test with Real API**
```python
@pytest.mark.integration
async def test_real_api_integration():
    """Test with real Tailscale API (requires test API key)."""
    api_key = os.getenv("TEST_TAILSCALE_API_KEY")
    tailnet = os.getenv("TEST_TAILSCALE_TAILNET")
    
    if not api_key or not tailnet:
        pytest.skip("Test API credentials not provided")
    
    client = TailscaleAPIClient(api_key, tailnet)
    devices = await client.get_devices()
    
    assert isinstance(devices, list)
    # Add more assertions based on expected behavior
```

---

## 🎯 **Summary**

These best practices ensure:

- **Security**: Proper API key management and access control
- **Performance**: Efficient connection management and caching
- **Reliability**: Robust error handling and retry logic
- **Observability**: Comprehensive logging and monitoring
- **Maintainability**: Clean architecture and testing practices

Following these practices will result in robust, secure, and performant Tailscale integrations across all MCP repositories.

---

**Status**: ✅ Active  
**Last Updated**: October 23, 2025  
**Version**: 1.0.0  
**Purpose**: Best practices for Tailscale integration in MCP development
