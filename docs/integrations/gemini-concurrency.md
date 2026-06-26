# Gemini.md MCP Integration - FastMCP 3.2+ Concurrency Safety

## 🚨 Critical Update Required: Concurrency Safety

**FastMCP 3.2+ Universal Connect Pattern enables simultaneous access from multiple clients, requiring database and file operation concurrency safety.**

---

## 📋 **Required Updates for Gemini.md Integration**

### ✅ **FastMCP 3.2+ Compatibility**
```json
{
  "mcp_servers": {
    "fileops-mcp": {
      "command": "uv run fileops-mcp-server",
      "args": ["--stdio"],
      "env": {
        "MCP_TRANSPORT": "stdio",
        "CONCURRENCY_SAFE": "true"
      }
    },
    "gitops-mcp": {
      "command": "uv run gitops-mcp-server", 
      "args": ["--stdio"],
      "env": {
        "MCP_TRANSPORT": "stdio",
        "GIT_LOCK_TIMEOUT": "30",
        "CONCURRENCY_SAFE": "true"
      }
    }
  }
}
```

### 🔒 **Concurrency Safety Requirements**

#### Database Operations
```javascript
// Gemini.md tool calls must handle concurrency
const safeDatabaseOperation = async (tool, params) => {
  try {
    const result = await tool(params);
    // Check for concurrency errors
    if (result.error?.code === 423) {
      // Resource locked - retry with backoff
      return await retryWithBackoff(tool, params);
    }
    return result;
  } catch (error) {
    if (error.message.includes('concurrency')) {
      // Handle concurrent access
      throw new Error(`Concurrent access detected: ${error.message}`);
    }
    throw error;
  }
};
```

#### File Operations  
```javascript
// Atomic file operations required
const safeFileOperation = async (operation, path, content) => {
  // Use atomic patterns
  const tempPath = `${path}.tmp.${Date.now()}`;
  try {
    await operation(tempPath, content);
    await fs.rename(tempPath, path);
  } finally {
    // Cleanup temp file
    await fs.unlink(tempPath).catch(() => {});
  }
};
```

---

## 🛠️ **Gemini.md Specific Patterns**

### 1. **Multi-Client Awareness**
```javascript
// Gemini.md can have multiple simultaneous sessions
class GeminiMCPManager {
  constructor() {
    this.activeOperations = new Map(); // Track ongoing operations
    this.locks = new Map(); // Resource locks
  }
  
  async executeTool(toolName, params) {
    const lockKey = this.getLockKey(toolName, params);
    
    // Wait for lock if resource is busy
    if (this.locks.has(lockKey)) {
      await this.waitForLock(lockKey);
    }
    
    this.locks.set(lockKey, true);
    try {
      return await this.mcpClient.callTool(toolName, params);
    } finally {
      this.locks.delete(lockKey);
    }
  }
}
```

### 2. **Error Handling for Concurrency**
```javascript
const handleConcurrencyErrors = (error) => {
  const concurrencyErrors = [
    'Database concurrency error',
    'Resource locked',
    'Lock timeout',
    'Concurrent access detected'
  ];
  
  if (concurrencyErrors.some(pattern => error.message.includes(pattern))) {
    return {
      retry: true,
      backoff: Math.random() * 1000, // Random backoff
      error: 'Concurrent access - retrying'
    };
  }
  
  return { retry: false, error };
};
```

### 3. **Batch Operations Safety**
```javascript
// Execute multiple operations atomically
const executeBatchSafely = async (operations) => {
  const results = [];
  const rollbackOps = [];
  
  try {
    for (const op of operations) {
      const result = await executeTool(op.tool, op.params);
      results.push(result);
      
      // Store rollback info if needed
      if (op.rollback) {
        rollbackOps.push(op.rollback(result));
      }
    }
    
    return { success: true, results };
  } catch (error) {
    // Rollback on failure
    for (const rollback of rollbackOps.reverse()) {
      try {
        await executeTool(rollback.tool, rollback.params);
      } catch (rollbackError) {
        console.error('Rollback failed:', rollbackError);
      }
    }
    
    throw error;
  }
};
```

---

## 📊 **Performance Considerations**

### Connection Pooling
```javascript
// Gemini.md should respect MCP server limits
const mcpConfig = {
  maxConcurrentConnections: 5, // Don't overwhelm servers
  connectionTimeout: 30000,
  retryAttempts: 3,
  retryDelay: 1000
};
```

### Rate Limiting
```javascript
class RateLimiter {
  constructor(maxPerSecond = 10) {
    this.maxPerSecond = maxPerSecond;
    this.requests = [];
  }
  
  async waitIfNecessary() {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < 1000);
    
    if (this.requests.length >= this.maxPerSecond) {
      const delay = 1000 - (now - this.requests[0]);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
    
    this.requests.push(now);
  }
}
```

---

## 🎯 **Gemini.md Integration Checklist**

### ✅ **Configuration Updates**
- [ ] Add `CONCURRENCY_SAFE=true` to all MCP server environments
- [ ] Configure appropriate timeouts for lock operations
- [ ] Set connection limits to prevent server overload

### ✅ **Code Updates**
- [ ] Implement retry logic for 423 (locked) errors
- [ ] Add atomic file operation patterns
- [ ] Use batch operations for multi-step changes
- [ ] Handle concurrent access errors gracefully

### ✅ **Testing**
- [ ] Test with 5+ simultaneous Gemini.md sessions
- [ ] Verify no data corruption under load
- [ ] Test error recovery and rollback
- [ ] Validate performance under concurrency

---

## 🔧 **Migration Guide**

### Step 1: Update Configuration
```json
// Before
{
  "mcp_servers": {
    "fileops-mcp": {
      "command": "uv run fileops-mcp-server"
    }
  }
}

// After  
{
  "mcp_servers": {
    "fileops-mcp": {
      "command": "uv run fileops-mcp-server",
      "env": {
        "CONCURRENCY_SAFE": "true",
        "MAX_CONCURRENT_OPS": "5"
      }
    }
  }
}
```

### Step 2: Update Client Code
```javascript
// Add concurrency handling
const mcpClient = new MCPClient({
  concurrencyControl: true,
  maxRetries: 3,
  lockTimeout: 30000
});
```

### Step 3: Test Integration
```javascript
// Test concurrent operations
const testConcurrency = async () => {
  const promises = Array(5).fill().map(() => 
    mcpClient.callTool('write_file', {path: 'test.txt', content: 'test'})
  );
  
  const results = await Promise.allSettled(promises);
  console.log('Concurrency test results:', results);
};
```

---

## 📚 **Additional Resources**

- **FastMCP 3.2+ Concurrency Standards**: `mcp-central-docs/standards/fastmcp-3.2-concurrency.md`
- **Testing Patterns**: `mcp-central-docs/patterns/concurrency-testing.md`
- **Error Handling**: `mcp-central-docs/patterns/error-recovery.md`

---

**⚠️ ACTION REQUIRED: Update all Gemini.md MCP integrations to support FastMCP 3.2+ concurrency safety before deployment.**
