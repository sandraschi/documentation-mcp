# Tailscale Troubleshooting Guide

**Date:** October 23, 2025  
**Purpose:** Common issues and solutions for Tailscale integration across all MCP repositories

---

## 🎯 **Overview**

This guide provides comprehensive troubleshooting information for common issues encountered when integrating Tailscale with MCP servers and other applications.

---

## 🔐 **Authentication Issues**

### **Problem: Invalid API Key**

#### **Symptoms**
- HTTP 401 Unauthorized errors
- "Invalid or missing API key" messages
- Authentication failures

#### **Solutions**

1. **Verify API Key Format**
```python
import re

def validate_api_key(api_key: str) -> bool:
    """Validate Tailscale API key format."""
    # Tailscale API keys are typically 32+ characters
    if not api_key or len(api_key) < 20:
        return False
    
    # Check for valid characters
    if not re.match(r'^[a-zA-Z0-9_-]+$', api_key):
        return False
    
    return True

# Usage
api_key = os.getenv("TAILSCALE_API_KEY")
if not validate_api_key(api_key):
    print("Invalid API key format")
```

2. **Check API Key Permissions**
```python
async def check_api_key_permissions(api_key: str) -> Dict[str, Any]:
    """Check API key permissions."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.tailscale.com/api/v2/user/me",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            
            if response.status_code == 200:
                return {"status": "success", "permissions": "valid"}
            else:
                return {"status": "error", "message": "Invalid API key"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

3. **Regenerate API Key**
```bash
# Generate new API key in Tailscale admin console
# https://login.tailscale.com/admin/settings/keys
```

### **Problem: API Key Expired**

#### **Symptoms**
- HTTP 401 Unauthorized errors after working
- "Token expired" messages
- Authentication failures after period of working

#### **Solutions**

1. **Check API Key Expiration**
```python
async def check_api_key_expiration(api_key: str) -> Dict[str, Any]:
    """Check if API key is expired."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.tailscale.com/api/v2/user/me",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            
            if response.status_code == 401:
                return {"status": "expired", "message": "API key expired"}
            elif response.status_code == 200:
                return {"status": "valid", "message": "API key is valid"}
            else:
                return {"status": "error", "message": f"Unexpected status: {response.status_code}"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

2. **Implement API Key Rotation**
```python
class APIKeyRotator:
    def __init__(self, primary_key: str, backup_key: str = None):
        self.primary_key = primary_key
        self.backup_key = backup_key
        self.current_key = primary_key
    
    async def rotate_if_needed(self) -> str:
        """Rotate API key if needed."""
        if await self._is_key_expired(self.current_key):
            if self.backup_key:
                self.current_key = self.backup_key
                return self.current_key
            else:
                raise ValueError("API key expired and no backup key available")
        
        return self.current_key
    
    async def _is_key_expired(self, api_key: str) -> bool:
        """Check if API key is expired."""
        result = await check_api_key_expiration(api_key)
        return result["status"] == "expired"
```

---

## 🌐 **Network Connectivity Issues**

### **Problem: Cannot Connect to Tailscale API**

#### **Symptoms**
- Connection timeouts
- DNS resolution failures
- Network unreachable errors

#### **Solutions**

1. **Check Network Connectivity**
```python
import asyncio
import httpx

async def check_network_connectivity() -> Dict[str, Any]:
    """Check network connectivity to Tailscale API."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://api.tailscale.com/health")
            
            if response.status_code == 200:
                return {"status": "success", "message": "Network connectivity OK"}
            else:
                return {"status": "error", "message": f"API returned status {response.status_code}"}
    
    except httpx.TimeoutException:
        return {"status": "error", "message": "Connection timeout"}
    except httpx.ConnectError:
        return {"status": "error", "message": "Connection failed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

2. **Implement Retry Logic**
```python
import asyncio
from typing import Callable, Any

class NetworkRetryHandler:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with network retry logic."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt)
                    await asyncio.sleep(delay)
                else:
                    raise last_exception
            except Exception as e:
                raise e
```

3. **Check Proxy Settings**
```python
import os

def check_proxy_settings() -> Dict[str, Any]:
    """Check proxy settings that might affect API calls."""
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
    proxy_settings = {}
    
    for var in proxy_vars:
        if var in os.environ:
            proxy_settings[var] = os.environ[var]
    
    return {
        "status": "success" if proxy_settings else "info",
        "message": "Proxy settings found" if proxy_settings else "No proxy settings",
        "proxy_settings": proxy_settings
    }
```

### **Problem: Rate Limiting**

#### **Symptoms**
- HTTP 429 Too Many Requests errors
- Rate limit exceeded messages
- API calls failing with rate limit errors

#### **Solutions**

1. **Implement Rate Limit Handling**
```python
import asyncio
from datetime import datetime, timedelta

class RateLimitHandler:
    def __init__(self, max_requests_per_minute: int = 100):
        self.max_requests_per_minute = max_requests_per_minute
        self.request_times = []
    
    async def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        now = datetime.now()
        
        # Remove old requests
        self.request_times = [
            req_time for req_time in self.request_times
            if now - req_time < timedelta(minutes=1)
        ]
        
        # Check if we need to wait
        if len(self.request_times) >= self.max_requests_per_minute:
            oldest_request = min(self.request_times)
            wait_time = (oldest_request + timedelta(minutes=1) - now).total_seconds()
            
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        # Record this request
        self.request_times.append(now)
```

2. **Exponential Backoff**
```python
import random

class ExponentialBackoff:
    def __init__(self, base_delay: float = 1.0, max_delay: float = 60.0):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.attempt = 0
    
    async def wait(self):
        """Wait with exponential backoff."""
        delay = min(
            self.base_delay * (2 ** self.attempt) + random.uniform(0, 1),
            self.max_delay
        )
        await asyncio.sleep(delay)
        self.attempt += 1
    
    def reset(self):
        """Reset attempt counter."""
        self.attempt = 0
```

---

## 📊 **Data Issues**

### **Problem: Invalid Response Data**

#### **Symptoms**
- JSON parsing errors
- Missing expected fields
- Data type mismatches

#### **Solutions**

1. **Validate Response Data**
```python
from typing import Dict, Any, List
import jsonschema

def validate_device_response(data: Dict[str, Any]) -> bool:
    """Validate device response data."""
    schema = {
        "type": "object",
        "properties": {
            "devices": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "user": {"type": "string"},
                        "addresses": {"type": "array"},
                        "online": {"type": "boolean"},
                        "authorized": {"type": "boolean"}
                    },
                    "required": ["id", "name", "user"]
                }
            }
        },
        "required": ["devices"]
    }
    
    try:
        jsonschema.validate(data, schema)
        return True
    except jsonschema.ValidationError:
        return False
```

2. **Handle Missing Fields**
```python
def safe_get_device_field(device: Dict[str, Any], field: str, default: Any = None) -> Any:
    """Safely get device field with default value."""
    return device.get(field, default)

# Usage
device = {"id": "device_123", "name": "test_device"}
user = safe_get_device_field(device, "user", "unknown")
online = safe_get_device_field(device, "online", False)
```

3. **Data Type Conversion**
```python
def convert_device_data(device: Dict[str, Any]) -> Dict[str, Any]:
    """Convert device data to expected types."""
    return {
        "id": str(device.get("id", "")),
        "name": str(device.get("name", "")),
        "user": str(device.get("user", "")),
        "addresses": list(device.get("addresses", [])),
        "online": bool(device.get("online", False)),
        "authorized": bool(device.get("authorized", False)),
        "created": device.get("created"),
        "lastSeen": device.get("lastSeen")
    }
```

### **Problem: Data Inconsistency**

#### **Symptoms**
- Inconsistent data between API calls
- Stale data being returned
- Data not updating as expected

#### **Solutions**

1. **Implement Data Caching with TTL**
```python
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class DataCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, tuple[Any, datetime]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached data if not expired."""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl_seconds):
                return data
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, data: Any) -> None:
        """Set cached data with timestamp."""
        self._cache[key] = (data, datetime.now())
    
    def clear(self) -> None:
        """Clear all cached data."""
        self._cache.clear()
    
    def is_expired(self, key: str) -> bool:
        """Check if cached data is expired."""
        if key in self._cache:
            _, timestamp = self._cache[key]
            return datetime.now() - timestamp >= timedelta(seconds=self.ttl_seconds)
        return True
```

2. **Data Validation and Sanitization**
```python
def sanitize_device_data(device: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize device data to ensure consistency."""
    return {
        "id": device.get("id", "").strip(),
        "name": device.get("name", "").strip(),
        "user": device.get("user", "").strip(),
        "addresses": [addr.strip() for addr in device.get("addresses", []) if addr],
        "hostname": device.get("hostname", "").strip(),
        "os": device.get("os", "").strip(),
        "online": bool(device.get("online", False)),
        "authorized": bool(device.get("authorized", False)),
        "created": device.get("created"),
        "lastSeen": device.get("lastSeen"),
        "tags": [tag.strip() for tag in device.get("tags", []) if tag]
    }
```

---

## 🔧 **Configuration Issues**

### **Problem: Invalid Configuration**

#### **Symptoms**
- Configuration validation errors
- Missing required configuration
- Invalid configuration values

#### **Solutions**

1. **Configuration Validation**
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
    
    @validator('max_retries')
    def validate_max_retries(cls, v):
        if v < 0 or v > 10:
            raise ValueError('Max retries must be between 0 and 10')
        return v
    
    @validator('cache_ttl')
    def validate_cache_ttl(cls, v):
        if v < 0 or v > 3600:
            raise ValueError('Cache TTL must be between 0 and 3600 seconds')
        return v

# Usage
try:
    config = TailscaleConfig(
        api_key=os.getenv("TAILSCALE_API_KEY"),
        tailnet=os.getenv("TAILSCALE_TAILNET")
    )
except ValueError as e:
    print(f"Configuration error: {e}")
```

2. **Configuration Loading**
```python
import os
from typing import Dict, Any

def load_configuration() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    config = {}
    
    # Required configuration
    required_vars = ["TAILSCALE_API_KEY", "TAILSCALE_TAILNET"]
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            raise ValueError(f"Required environment variable {var} not set")
        config[var.lower()] = value
    
    # Optional configuration with defaults
    optional_vars = {
        "TAILSCALE_BASE_URL": "https://api.tailscale.com",
        "TAILSCALE_TIMEOUT": "30",
        "TAILSCALE_MAX_RETRIES": "3",
        "TAILSCALE_CACHE_TTL": "300"
    }
    
    for var, default in optional_vars.items():
        config[var.lower()] = os.getenv(var, default)
    
    return config
```

### **Problem: Environment Variable Issues**

#### **Symptoms**
- Environment variables not found
- Incorrect environment variable values
- Environment variable format issues

#### **Solutions**

1. **Environment Variable Validation**
```python
import os
from typing import Dict, Any

def validate_environment() -> Dict[str, Any]:
    """Validate environment variables."""
    errors = []
    warnings = []
    
    # Check required variables
    required_vars = {
        "TAILSCALE_API_KEY": "Tailscale API key",
        "TAILSCALE_TAILNET": "Tailnet name"
    }
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            errors.append(f"Missing required environment variable: {var} ({description})")
        elif len(value) < 10:
            warnings.append(f"Environment variable {var} seems too short")
    
    # Check optional variables
    optional_vars = {
        "TAILSCALE_BASE_URL": "https://api.tailscale.com",
        "TAILSCALE_TIMEOUT": "30",
        "TAILSCALE_MAX_RETRIES": "3"
    }
    
    for var, default in optional_vars.items():
        value = os.getenv(var, default)
        if not value:
            warnings.append(f"Environment variable {var} not set, using default: {default}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
```

2. **Environment Variable Loading**
```python
def load_env_file(env_file: str = ".env") -> Dict[str, str]:
    """Load environment variables from .env file."""
    env_vars = {}
    
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    
    return env_vars
```

---

## 🚨 **Error Handling Issues**

### **Problem: Unhandled Exceptions**

#### **Symptoms**
- Application crashes
- Unhandled exception errors
- Unexpected behavior

#### **Solutions**

1. **Comprehensive Error Handling**
```python
from typing import Dict, Any
import traceback

class TailscaleErrorHandler:
    def __init__(self):
        self.error_counts = {}
    
    async def handle_api_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle API errors comprehensively."""
        error_type = type(error).__name__
        error_message = str(error)
        
        # Count error occurrences
        error_key = f"{error_type}:{context}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        # Log error details
        error_details = {
            "error_type": error_type,
            "error_message": error_message,
            "context": context,
            "traceback": traceback.format_exc(),
            "count": self.error_counts[error_key]
        }
        
        # Return structured error response
        return {
            "status": "error",
            "error_type": error_type,
            "message": error_message,
            "context": context,
            "details": error_details
        }
    
    def get_error_stats(self) -> Dict[str, int]:
        """Get error statistics."""
        return self.error_counts.copy()
```

2. **Graceful Degradation**
```python
class GracefulDegradation:
    def __init__(self, fallback_data: Dict[str, Any] = None):
        self.fallback_data = fallback_data or {}
    
    async def execute_with_fallback(self, func: callable, *args, **kwargs) -> Dict[str, Any]:
        """Execute function with graceful degradation."""
        try:
            result = await func(*args, **kwargs)
            return {"status": "success", "data": result}
        
        except Exception as e:
            # Log error but don't crash
            print(f"Error in {func.__name__}: {e}")
            
            # Return fallback data if available
            if self.fallback_data:
                return {
                    "status": "fallback",
                    "data": self.fallback_data,
                    "error": str(e)
                }
            else:
                return {
                    "status": "error",
                    "message": str(e)
                }
```

---

## 📊 **Performance Issues**

### **Problem: Slow API Responses**

#### **Symptoms**
- Long response times
- Timeout errors
- Poor user experience

#### **Solutions**

1. **Response Time Monitoring**
```python
import time
from typing import Callable, Any

class PerformanceMonitor:
    def __init__(self):
        self.response_times = []
    
    async def monitor_response_time(self, func: Callable, *args, **kwargs) -> Any:
        """Monitor response time of function."""
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            response_time = time.time() - start_time
            
            self.response_times.append(response_time)
            
            # Log slow responses
            if response_time > 5.0:  # 5 seconds threshold
                print(f"Slow response detected: {func.__name__} took {response_time:.2f}s")
            
            return result
        
        except Exception as e:
            response_time = time.time() - start_time
            print(f"Error in {func.__name__} after {response_time:.2f}s: {e}")
            raise e
    
    def get_average_response_time(self) -> float:
        """Get average response time."""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    def get_slow_responses(self, threshold: float = 5.0) -> int:
        """Get count of slow responses."""
        return len([rt for rt in self.response_times if rt > threshold])
```

2. **Connection Pooling**
```python
import httpx
from typing import Optional

class ConnectionPoolManager:
    def __init__(self, max_connections: int = 20, max_keepalive: int = 10):
        self.max_connections = max_connections
        self.max_keepalive = max_keepalive
        self._client: Optional[httpx.AsyncClient] = None
    
    async def get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client with connection pooling."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                limits=httpx.Limits(
                    max_keepalive_connections=self.max_keepalive,
                    max_connections=self.max_connections
                ),
                timeout=30.0
            )
        return self._client
    
    async def close(self):
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
```

---

## 📚 **Summary**

This troubleshooting guide covers common issues and solutions for:

- **Authentication Issues**: API key problems and solutions
- **Network Connectivity Issues**: Connection and rate limiting problems
- **Data Issues**: Invalid data and inconsistency problems
- **Configuration Issues**: Configuration validation and environment variable problems
- **Error Handling Issues**: Exception handling and graceful degradation
- **Performance Issues**: Slow responses and connection pooling

Following these troubleshooting patterns will help resolve common issues and improve the reliability of Tailscale integrations across all MCP repositories.

---

**Status**: ✅ Active  
**Last Updated**: October 23, 2025  
**Version**: 1.0.0  
**Purpose**: Troubleshooting guide for Tailscale integration across all MCP repositories
