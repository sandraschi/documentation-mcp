# Tailscale Performance Optimization

**Date:** October 23, 2025  
**Purpose:** Performance optimization patterns and examples for Tailscale integration across all MCP repositories

---

## 🎯 **Overview**

This document provides comprehensive performance optimization patterns, examples, and best practices for optimizing Tailscale integrations across all MCP repositories.

---

## ⚡ **Performance Optimization Fundamentals**

### **1. Performance Metrics**

#### **Performance Metrics Collection**
```python
import time
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PerformanceMetrics:
    response_time: float
    throughput: float
    error_rate: float
    cpu_usage: float
    memory_usage: float
    timestamp: datetime

class PerformanceMonitor:
    def __init__(self):
        self.metrics_history = []
        self.baseline_metrics = None
        self.performance_thresholds = {
            "response_time": 1.0,  # seconds
            "throughput": 1000,    # requests per second
            "error_rate": 0.01,    # 1%
            "cpu_usage": 0.8,      # 80%
            "memory_usage": 0.8    # 80%
        }
    
    def record_metrics(self, metrics: PerformanceMetrics):
        """Record performance metrics."""
        self.metrics_history.append(metrics)
        
        # Keep only last 1000 metrics
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
    
    def get_average_metrics(self, window_size: int = 100) -> PerformanceMetrics:
        """Get average metrics over window."""
        if not self.metrics_history:
            return None
        
        recent_metrics = self.metrics_history[-window_size:]
        
        avg_response_time = sum(m.response_time for m in recent_metrics) / len(recent_metrics)
        avg_throughput = sum(m.throughput for m in recent_metrics) / len(recent_metrics)
        avg_error_rate = sum(m.error_rate for m in recent_metrics) / len(recent_metrics)
        avg_cpu_usage = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
        avg_memory_usage = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        
        return PerformanceMetrics(
            response_time=avg_response_time,
            throughput=avg_throughput,
            error_rate=avg_error_rate,
            cpu_usage=avg_cpu_usage,
            memory_usage=avg_memory_usage,
            timestamp=datetime.now()
        )
    
    def check_performance_thresholds(self, metrics: PerformanceMetrics) -> List[str]:
        """Check if metrics exceed performance thresholds."""
        violations = []
        
        if metrics.response_time > self.performance_thresholds["response_time"]:
            violations.append(f"Response time {metrics.response_time}s exceeds threshold {self.performance_thresholds['response_time']}s")
        
        if metrics.throughput < self.performance_thresholds["throughput"]:
            violations.append(f"Throughput {metrics.throughput} below threshold {self.performance_thresholds['throughput']}")
        
        if metrics.error_rate > self.performance_thresholds["error_rate"]:
            violations.append(f"Error rate {metrics.error_rate} exceeds threshold {self.performance_thresholds['error_rate']}")
        
        if metrics.cpu_usage > self.performance_thresholds["cpu_usage"]:
            violations.append(f"CPU usage {metrics.cpu_usage} exceeds threshold {self.performance_thresholds['cpu_usage']}")
        
        if metrics.memory_usage > self.performance_thresholds["memory_usage"]:
            violations.append(f"Memory usage {metrics.memory_usage} exceeds threshold {self.performance_thresholds['memory_usage']}")
        
        return violations
```

### **2. Performance Profiling**

#### **Performance Profiler**
```python
import cProfile
import pstats
import io
from functools import wraps

class PerformanceProfiler:
    def __init__(self):
        self.profiles = {}
    
    def profile_function(self, func):
        """Decorator to profile function performance."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()
            
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                profiler.disable()
                
                # Store profile results
                profile_name = f"{func.__name__}_{int(time.time())}"
                self.profiles[profile_name] = profiler
        
        return wrapper
    
    def get_profile_stats(self, profile_name: str) -> Dict[str, Any]:
        """Get profile statistics."""
        if profile_name not in self.profiles:
            return {"error": "Profile not found"}
        
        profiler = self.profiles[profile_name]
        
        # Create string buffer for stats
        stats_buffer = io.StringIO()
        stats = pstats.Stats(profiler, stream=stats_buffer)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 functions
        
        return {
            "profile_name": profile_name,
            "stats": stats_buffer.getvalue(),
            "total_calls": stats.total_calls,
            "total_time": stats.total_tt
        }
    
    def analyze_performance_bottlenecks(self) -> List[Dict[str, Any]]:
        """Analyze performance bottlenecks."""
        bottlenecks = []
        
        for profile_name, profiler in self.profiles.items():
            stats = pstats.Stats(profiler)
            stats.sort_stats('cumulative')
            
            # Get top functions by cumulative time
            top_functions = stats.get_stats_profile().func_profiles
            
            for func_name, func_stats in list(top_functions.items())[:5]:
                if func_stats.cumulative_time > 0.1:  # More than 100ms
                    bottlenecks.append({
                        "profile_name": profile_name,
                        "function": func_name,
                        "cumulative_time": func_stats.cumulative_time,
                        "call_count": func_stats.call_count,
                        "average_time": func_stats.cumulative_time / func_stats.call_count
                    })
        
        return bottlenecks
```

---

## 🚀 **API Performance Optimization**

### **1. Connection Pooling**

#### **Connection Pool Manager**
```python
import httpx
import asyncio
from typing import Optional, Dict, Any

class ConnectionPoolManager:
    def __init__(self, max_connections: int = 20, max_keepalive: int = 10):
        self.max_connections = max_connections
        self.max_keepalive = max_keepalive
        self._client: Optional[httpx.AsyncClient] = None
        self._lock = asyncio.Lock()
    
    async def get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client with connection pooling."""
        if self._client is None:
            async with self._lock:
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

class OptimizedTailscaleAPI:
    def __init__(self, api_key: str, tailnet: str):
        self.api_key = api_key
        self.tailnet = tailnet
        self.connection_pool = ConnectionPoolManager()
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    async def get_devices(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        """Get devices with caching and connection pooling."""
        cache_key = f"devices_{self.tailnet}"
        
        # Check cache first
        if use_cache and cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
        
        # Fetch from API
        client = await self.connection_pool.get_client()
        
        try:
            response = await client.get(
                f"https://api.tailscale.com/api/v2/tailnet/{self.tailnet}/devices",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            
            if response.status_code == 200:
                devices = response.json()["devices"]
                
                # Cache the result
                self.cache[cache_key] = (devices, time.time())
                
                return devices
            else:
                raise Exception(f"API request failed with status {response.status_code}")
        
        except Exception as e:
            # Return cached data if available
            if cache_key in self.cache:
                cached_data, _ = self.cache[cache_key]
                return cached_data
            raise e
    
    async def get_device(self, device_id: str, use_cache: bool = True) -> Dict[str, Any]:
        """Get specific device with caching."""
        cache_key = f"device_{device_id}"
        
        # Check cache first
        if use_cache and cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
        
        # Fetch from API
        client = await self.connection_pool.get_client()
        
        try:
            response = await client.get(
                f"https://api.tailscale.com/api/v2/device/{device_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            
            if response.status_code == 200:
                device = response.json()
                
                # Cache the result
                self.cache[cache_key] = (device, time.time())
                
                return device
            else:
                raise Exception(f"API request failed with status {response.status_code}")
        
        except Exception as e:
            # Return cached data if available
            if cache_key in self.cache:
                cached_data, _ = self.cache[cache_key]
                return cached_data
            raise e
    
    async def close(self):
        """Close connection pool."""
        await self.connection_pool.close()
```

### **2. Batch Operations**

#### **Batch Operation Manager**
```python
class BatchOperationManager:
    def __init__(self, tailscale_api):
        self.tailscale_api = tailscale_api
        self.batch_size = 10
        self.batch_delay = 0.1  # 100ms delay between batches
    
    async def batch_authorize_devices(self, device_ids: List[str]) -> Dict[str, Any]:
        """Authorize multiple devices in batches."""
        results = {}
        
        # Process devices in batches
        for i in range(0, len(device_ids), self.batch_size):
            batch = device_ids[i:i + self.batch_size]
            
            # Create tasks for batch
            tasks = [
                self._authorize_device(device_id)
                for device_id in batch
            ]
            
            # Execute batch
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Store results
            for device_id, result in zip(batch, batch_results):
                results[device_id] = result if not isinstance(result, Exception) else False
            
            # Delay between batches to avoid rate limiting
            if i + self.batch_size < len(device_ids):
                await asyncio.sleep(self.batch_delay)
        
        return results
    
    async def batch_update_device_tags(self, device_updates: Dict[str, List[str]]) -> Dict[str, Any]:
        """Update device tags in batches."""
        results = {}
        
        # Process updates in batches
        device_ids = list(device_updates.keys())
        
        for i in range(0, len(device_ids), self.batch_size):
            batch = device_ids[i:i + self.batch_size]
            
            # Create tasks for batch
            tasks = [
                self._update_device_tags(device_id, device_updates[device_id])
                for device_id in batch
            ]
            
            # Execute batch
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Store results
            for device_id, result in zip(batch, batch_results):
                results[device_id] = result if not isinstance(result, Exception) else False
            
            # Delay between batches
            if i + self.batch_size < len(device_ids):
                await asyncio.sleep(self.batch_delay)
        
        return results
    
    async def _authorize_device(self, device_id: str) -> bool:
        """Authorize single device."""
        try:
            result = await self.tailscale_api.authorize_device(device_id)
            return result
        except Exception as e:
            print(f"Error authorizing device {device_id}: {e}")
            return False
    
    async def _update_device_tags(self, device_id: str, tags: List[str]) -> bool:
        """Update device tags."""
        try:
            result = await self.tailscale_api.update_device_tags(device_id, tags)
            return result
        except Exception as e:
            print(f"Error updating tags for device {device_id}: {e}")
            return False
```

---

## 💾 **Memory Optimization**

### **1. Memory Management**

#### **Memory Manager**
```python
import gc
import psutil
import os
from typing import Dict, Any, List

class MemoryManager:
    def __init__(self):
        self.memory_threshold = 0.8  # 80% memory usage threshold
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = time.time()
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage."""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "rss": memory_info.rss / 1024 / 1024,  # MB
            "vms": memory_info.vms / 1024 / 1024,  # MB
            "percent": process.memory_percent(),
            "available": psutil.virtual_memory().available / 1024 / 1024  # MB
        }
    
    def check_memory_threshold(self) -> bool:
        """Check if memory usage exceeds threshold."""
        memory_usage = self.get_memory_usage()
        return memory_usage["percent"] > (self.memory_threshold * 100)
    
    def cleanup_memory(self):
        """Perform memory cleanup."""
        # Force garbage collection
        gc.collect()
        
        # Update last cleanup time
        self.last_cleanup = time.time()
        
        return self.get_memory_usage()
    
    def should_cleanup(self) -> bool:
        """Check if memory cleanup is needed."""
        return (time.time() - self.last_cleanup > self.cleanup_interval or 
                self.check_memory_threshold())
    
    def optimize_memory_usage(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize memory usage of data structures."""
        optimized = {}
        
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 1000:
                # Convert large lists to generators
                optimized[key] = iter(value)
            elif isinstance(value, dict) and len(value) > 100:
                # Recursively optimize nested dictionaries
                optimized[key] = self.optimize_memory_usage(value)
            else:
                optimized[key] = value
        
        return optimized

class MemoryOptimizedTailscaleAPI:
    def __init__(self, api_key: str, tailnet: str):
        self.api_key = api_key
        self.tailnet = tailnet
        self.memory_manager = MemoryManager()
        self.cache = {}
        self.cache_size_limit = 1000  # Maximum cache entries
    
    async def get_devices_optimized(self) -> List[Dict[str, Any]]:
        """Get devices with memory optimization."""
        # Check if memory cleanup is needed
        if self.memory_manager.should_cleanup():
            self.memory_manager.cleanup_memory()
            self._cleanup_cache()
        
        cache_key = f"devices_{self.tailnet}"
        
        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Fetch from API
        devices = await self._fetch_devices()
        
        # Optimize memory usage
        optimized_devices = self.memory_manager.optimize_memory_usage(devices)
        
        # Cache the result
        self.cache[cache_key] = optimized_devices
        
        return optimized_devices
    
    def _cleanup_cache(self):
        """Cleanup cache to free memory."""
        if len(self.cache) > self.cache_size_limit:
            # Remove oldest entries
            entries_to_remove = len(self.cache) - self.cache_size_limit
            cache_keys = list(self.cache.keys())
            
            for i in range(entries_to_extremes):
                del self.cache[cache_keys[i]]
    
    async def _fetch_devices(self) -> List[Dict[str, Any]]:
        """Fetch devices from API."""
        # Implementation for fetching devices
        pass
```

---

## 🔄 **Caching Strategies**

### **1. Multi-Level Caching**

#### **Cache Manager**
```python
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self):
        self.memory_cache = {}
        self.disk_cache = {}
        self.cache_ttl = 300  # 5 minutes
        self.max_memory_cache_size = 1000
        self.max_disk_cache_size = 10000
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        # Check memory cache first
        if key in self.memory_cache:
            value, timestamp = self.memory_cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                return value
            else:
                # Remove expired entry
                del self.memory_cache[key]
        
        # Check disk cache
        if key in self.disk_cache:
            value, timestamp = self.disk_cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                # Move to memory cache
                self._set_memory_cache(key, value)
                return value
            else:
                # Remove expired entry
                del self.disk_cache[key]
        
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache."""
        # Set in memory cache
        self._set_memory_cache(key, value)
        
        # Set in disk cache if memory cache is full
        if len(self.memory_cache) > self.max_memory_cache_size:
            self._set_disk_cache(key, value)
    
    def _set_memory_cache(self, key: str, value: Any):
        """Set value in memory cache."""
        self.memory_cache[key] = (value, datetime.now())
        
        # Cleanup if cache is full
        if len(self.memory_cache) > self.max_memory_cache_size:
            # Remove oldest entries
            oldest_key = min(self.memory_cache.keys(), 
                           key=lambda k: self.memory_cache[k][1])
            del self.memory_cache[oldest_key]
    
    def _set_disk_cache(self, key: str, value: Any):
        """Set value in disk cache."""
        self.disk_cache[key] = (value, datetime.now())
        
        # Cleanup if cache is full
        if len(self.disk_cache) > self.max_disk_cache_size:
            # Remove oldest entries
            oldest_key = min(self.disk_cache.keys(), 
                           key=lambda k: self.disk_cache[k][1])
            del self.disk_cache[oldest_key]
    
    def clear(self):
        """Clear all caches."""
        self.memory_cache.clear()
        self.disk_cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "memory_cache_size": len(self.memory_cache),
            "disk_cache_size": len(self.disk_cache),
            "total_cache_size": len(self.memory_cache) + len(self.disk_cache),
            "cache_hit_ratio": self._calculate_hit_ratio()
        }
    
    def _calculate_hit_ratio(self) -> float:
        """Calculate cache hit ratio."""
        # Implementation for hit ratio calculation
        return 0.0

class CachedTailscaleAPI:
    def __init__(self, api_key: str, tailnet: str):
        self.api_key = api_key
        self.tailnet = tailnet
        self.cache_manager = CacheManager()
        self.cache_stats = {
            "hits": 0,
            "misses": 0
        }
    
    async def get_devices_cached(self) -> List[Dict[str, Any]]:
        """Get devices with caching."""
        cache_key = f"devices_{self.tailnet}"
        
        # Check cache first
        cached_devices = self.cache_manager.get(cache_key)
        if cached_devices is not None:
            self.cache_stats["hits"] += 1
            return cached_devices
        
        # Cache miss - fetch from API
        self.cache_stats["misses"] += 1
        devices = await self._fetch_devices()
        
        # Cache the result
        self.cache_manager.set(cache_key, devices)
        
        return devices
    
    async def get_device_cached(self, device_id: str) -> Dict[str, Any]:
        """Get device with caching."""
        cache_key = f"device_{device_id}"
        
        # Check cache first
        cached_device = self.cache_manager.get(cache_key)
        if cached_device is not None:
            self.cache_stats["hits"] += 1
            return cached_device
        
        # Cache miss - fetch from API
        self.cache_stats["misses"] += 1
        device = await self._fetch_device(device_id)
        
        # Cache the result
        self.cache_manager.set(cache_key, device)
        
        return device
    
    async def _fetch_devices(self) -> List[Dict[str, Any]]:
        """Fetch devices from API."""
        # Implementation for fetching devices
        pass
    
    async def _fetch_device(self, device_id: str) -> Dict[str, Any]:
        """Fetch device from API."""
        # Implementation for fetching device
        pass
    
    def get_cache_performance(self) -> Dict[str, Any]:
        """Get cache performance metrics."""
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_ratio = self.cache_stats["hits"] / total_requests if total_requests > 0 else 0
        
        return {
            "cache_hits": self.cache_stats["hits"],
            "cache_misses": self.cache_stats["misses"],
            "hit_ratio": hit_ratio,
            "cache_stats": self.cache_manager.get_cache_stats()
        }
```

---

## 📊 **Performance Monitoring**

### **1. Performance Dashboard**

#### **Performance Dashboard Generator**
```python
class PerformanceDashboardGenerator:
    def __init__(self, performance_monitor: PerformanceMonitor):
        self.performance_monitor = performance_monitor
    
    def generate_performance_dashboard(self) -> Dict[str, Any]:
        """Generate performance dashboard."""
        # Get current metrics
        current_metrics = self.performance_monitor.get_average_metrics()
        
        # Get performance trends
        performance_trends = self._analyze_performance_trends()
        
        # Generate dashboard
        dashboard = {
            "title": "Tailscale Performance Dashboard",
            "timestamp": datetime.now().isoformat(),
            "current_metrics": {
                "response_time": current_metrics.response_time,
                "throughput": current_metrics.throughput,
                "error_rate": current_metrics.error_rate,
                "cpu_usage": current_metrics.cpu_usage,
                "memory_usage": current_metrics.memory_usage
            },
            "performance_trends": performance_trends,
            "recommendations": self._generate_performance_recommendations(current_metrics),
            "alerts": self._generate_performance_alerts(current_metrics)
        }
        
        return dashboard
    
    def _analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends."""
        # Implementation for performance trend analysis
        return {
            "response_time_trend": "stable",
            "throughput_trend": "increasing",
            "error_rate_trend": "decreasing",
            "cpu_usage_trend": "stable",
            "memory_usage_trend": "stable"
        }
    
    def _generate_performance_recommendations(self, metrics: PerformanceMetrics) -> List[str]:
        """Generate performance recommendations."""
        recommendations = []
        
        if metrics.response_time > 1.0:
            recommendations.append("Consider optimizing API response time")
        
        if metrics.throughput < 1000:
            recommendations.append("Consider scaling to increase throughput")
        
        if metrics.error_rate > 0.01:
            recommendations.append("Investigate and fix error sources")
        
        if metrics.cpu_usage > 0.8:
            recommendations.append("Consider optimizing CPU usage")
        
        if metrics.memory_usage > 0.8:
            recommendations.append("Consider optimizing memory usage")
        
        return recommendations
    
    def _generate_performance_alerts(self, metrics: PerformanceMetrics) -> List[Dict[str, Any]]:
        """Generate performance alerts."""
        alerts = []
        
        violations = self.performance_monitor.check_performance_thresholds(metrics)
        
        for violation in violations:
            alerts.append({
                "type": "performance_violation",
                "message": violation,
                "severity": "warning",
                "timestamp": datetime.now().isoformat()
            })
        
        return alerts
```

---

## 📚 **Summary**

The Tailscale performance optimization guide provides comprehensive patterns for:

- **Performance Metrics**: Collection and monitoring of performance metrics
- **API Performance Optimization**: Connection pooling and batch operations
- **Memory Optimization**: Memory management and optimization strategies
- **Caching Strategies**: Multi-level caching and cache management
- **Performance Monitoring**: Performance dashboards and alerting

Following these performance optimization patterns ensures optimal performance and scalability for Tailscale integrations across all MCP repositories.

---

**Status**: ✅ Active  
**Last Updated**: October 23, 2025  
**Version**: 1.0.0  
**Purpose**: Performance optimization patterns and examples for Tailscale integration across all MCP repositories
