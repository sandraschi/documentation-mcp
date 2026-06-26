# Cursor MCP Integration - FastMCP 3.2+ Concurrency Safety

## 🚨 Critical Update Required: Concurrency Safety

**FastMCP 3.2+ Universal Connect Pattern enables simultaneous access from multiple Cursor instances, requiring database and file operation concurrency safety.**

> [!CAUTION]
> **Cursor v3 Parallel Agent Risks**
> With the release of **Cursor v3 (April 2026)**, the IDE now supports **Parallel Agent Execution**. Multiple local and cloud agents can now operate on the same workspace simultaneously. Consequently, the concurrency patterns detailed below (locking, atomic writes, and thread-safe sessions) are no longer "best practices"—they are **mandatory infrastructure** to prevent data corruption and race conditions during multi-agent sessions.


---

## 📋 **Required Updates for Cursor Integration**

### ✅ **Cursor MCP Configuration (settings.json)**
```json
{
  "mcp.mcpServers": {
    "fileops-mcp": {
      "command": "uv run fileops-mcp-server",
      "args": ["--stdio"],
      "env": {
        "MCP_TRANSPORT": "stdio",
        "CONCURRENCY_SAFE": "true",
        "CURSOR_SESSION_ID": "${workspaceFolder}"
      }
    },
    "gitops-mcp": {
      "command": "uv run gitops-mcp-server",
      "args": ["--stdio"],
      "env": {
        "MCP_TRANSPORT": "stdio",
        "GIT_LOCK_TIMEOUT": "30",
        "CONCURRENCY_SAFE": "true",
        "CURSOR_SESSION_ID": "${workspaceFolder}"
      }
    },
    "calibre-mcp": {
      "command": "uv run calibre-mcp",
      "args": ["--stdio"],
      "env": {
        "MCP_TRANSPORT": "stdio",
        "DB_LOCK_TIMEOUT": "15",
        "CONCURRENCY_SAFE": "true"
      }
    }
  }
}
```

---

## 🔒 **Cursor-Specific Concurrency Patterns**

### 1. **Workspace-Aware Session Management**
```typescript
// Cursor extension: src/concurrency-manager.ts
export class CursorConcurrencyManager {
  private workspaceLocks = new Map<string, Set<string>>();
  private operationQueue = new Map<string, Array<() => Promise<any>>>();
  
  constructor(private workspaceId: string) {
    this.workspaceId = workspaceId;
  }
  
  async executeWithLock(
    resourceType: string, 
    resourceId: string, 
    operation: () => Promise<any>
  ): Promise<any> {
    const lockKey = `${this.workspaceId}:${resourceType}:${resourceId}`;
    
    // Check if resource is locked
    if (this.isLocked(lockKey)) {
      return this.queueOperation(lockKey, operation);
    }
    
    // Acquire lock
    this.acquireLock(lockKey);
    
    try {
      return await operation();
    } catch (error) {
      if (this.isConcurrencyError(error)) {
        // Handle concurrency errors
        throw new CursorConcurrencyError(`Concurrent access detected: ${error.message}`);
      }
      throw error;
    } finally {
      this.releaseLock(lockKey);
      this.processQueue(lockKey);
    }
  }
  
  private isConcurrencyError(error: any): boolean {
    const concurrencyPatterns = [
      'Database concurrency error',
      'Resource locked',
      'Lock timeout',
      'Concurrent access detected',
      'Database is locked'
    ];
    
    return concurrencyPatterns.some(pattern => 
      error.message?.includes(pattern) || 
      error.error?.message?.includes(pattern)
    );
  }
}
```

### 2. **File Operation Safety**
```typescript
// Cursor extension: src/file-operations.ts
export class SafeFileOperations {
  constructor(private concurrency: CursorConcurrencyManager) {}
  
  async writeFile(filePath: string, content: string): Promise<void> {
    return this.concurrency.executeWithLock('file', filePath, async () => {
      // Atomic write pattern
      const tempPath = `${filePath}.tmp.${Date.now()}`;
      
      try {
        await vscode.workspace.fs.writeFile(
          vscode.Uri.file(tempPath), 
          Buffer.from(content, 'utf8')
        );
        
        // Atomic replace
        await vscode.workspace.fs.rename(
          vscode.Uri.file(tempPath),
          vscode.Uri.file(filePath)
        );
      } finally {
        // Cleanup temp file
        try {
          await vscode.workspace.fs.delete(vscode.Uri.file(tempPath));
        } catch {}
      }
    });
  }
  
  async modifyFile(filePath: string, modifications: Array<{old: string, new: string}>): Promise<void> {
    return this.concurrency.executeWithLock('file', filePath, async () => {
      const document = await vscode.workspace.openTextDocument(filePath);
      const editor = await vscode.window.showTextDocument(document);
      
      await vscode.workspace.fs.readFile(vscode.Uri.file(filePath)).then(buffer => {
        let content = buffer.toString('utf8');
        
        for (const mod of modifications) {
          content = content.replace(mod.old, mod.new);
        }
        
        return vscode.workspace.fs.writeFile(
          vscode.Uri.file(filePath),
          Buffer.from(content, 'utf8')
        );
      });
    });
  }
}
```

### 3. **Git Operations Safety**
```typescript
// Cursor extension: src/git-operations.ts
export class SafeGitOperations {
  constructor(private concurrency: CursorConcurrencyManager) {}
  
  async commitWithLock(repoPath: string, message: string, files?: string[]): Promise<void> {
    return this.concurrency.executeWithLock('git', repoPath, async () => {
      const git = simpleGit(repoPath);
      
      // Ensure we're on the right branch and no conflicts
      const status = await git.status();
      if (status.conflicted.length > 0) {
        throw new Error('Repository has conflicts - resolve before committing');
      }
      
      // Stage files
      if (files) {
        await git.add(files);
      } else {
        await git.add('.');
      }
      
      // Commit with retry logic
      try {
        await git.commit(message);
      } catch (error) {
        if (error.message.includes('Git repository is locked')) {
          // Wait and retry
          await new Promise(resolve => setTimeout(resolve, 1000));
          await git.commit(message);
        } else {
          throw error;
        }
      }
    });
  }
}
```

---

## 🎯 **Cursor Extension Integration**

### 1. **Extension Activation**
```typescript
// extension.ts
export async function activate(context: vscode.ExtensionContext) {
  const workspaceId = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || 'default';
  const concurrency = new CursorConcurrencyManager(workspaceId);
  const fileOps = new SafeFileOperations(concurrency);
  const gitOps = new SafeGitOperations(concurrency);
  
  // Register commands with concurrency safety
  const commands = [
    vscode.commands.registerCommand('mcp.safeWriteFile', async (uri, content) => {
      return fileOps.writeFile(uri.fsPath, content);
    }),
    vscode.commands.registerCommand('mcp.safeCommit', async (message) => {
      const workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
      if (workspacePath) {
        return gitOps.commitWithLock(workspacePath, message);
      }
    })
  ];
  
  commands.forEach(cmd => context.subscriptions.push(cmd));
}
```

### 2. **MCP Tool Wrappers**
```typescript
// src/mcp-wrapper.ts
export class MCPToolWrapper {
  constructor(private concurrency: CursorConcurrencyManager) {}
  
  async callTool(toolName: string, params: any): Promise<any> {
    const resourceType = this.getResourceType(toolName);
    const resourceId = this.getResourceId(params);
    
    if (resourceType && resourceId) {
      return this.concurrency.executeWithLock(resourceType, resourceId, async () => {
        return this.executeMCPTool(toolName, params);
      });
    }
    
    return this.executeMCPTool(toolName, params);
  }
  
  private async executeMCPTool(toolName: string, params: any): Promise<any> {
    try {
      const result = await vscode.commands.executeCommand('mcp.callTool', toolName, params);
      
      // Check for concurrency errors
      if (result?.error?.code === 423) {
        throw new CursorConcurrencyError('Resource locked - try again');
      }
      
      return result;
    } catch (error) {
      if (this.isConcurrencyError(error)) {
        // Retry with exponential backoff
        return this.retryWithBackoff(toolName, params);
      }
      throw error;
    }
  }
  
  private async retryWithBackoff(toolName: string, params: any, attempt = 1): Promise<any> {
    if (attempt > 3) {
      throw new Error('Max retry attempts exceeded for concurrent operation');
    }
    
    const delay = Math.min(1000 * Math.pow(2, attempt), 5000);
    await new Promise(resolve => setTimeout(resolve, delay));
    
    try {
      return await this.executeMCPTool(toolName, params);
    } catch (error) {
      if (this.isConcurrencyError(error)) {
        return this.retryWithBackoff(toolName, params, attempt + 1);
      }
      throw error;
    }
  }
}
```

---

## 📊 **Cursor-Specific Considerations**

### 1. **Multi-Workspace Support**
```typescript
// Handle multiple Cursor workspaces
class MultiWorkspaceManager {
  private managers = new Map<string, CursorConcurrencyManager>();
  
  getManager(workspaceId: string): CursorConcurrencyManager {
    if (!this.managers.has(workspaceId)) {
      this.managers.set(workspaceId, new CursorConcurrencyManager(workspaceId));
    }
    return this.managers.get(workspaceId)!;
  }
  
  async executeInWorkspace(
    workspaceId: string, 
    resourceType: string, 
    resourceId: string, 
    operation: () => Promise<any>
  ): Promise<any> {
    const manager = this.getManager(workspaceId);
    return manager.executeWithLock(resourceType, resourceId, operation);
  }
}
```

### 2. **Real-time Collaboration**
```typescript
// Handle multiple users in same workspace
class CollaborationManager {
  private userSessions = new Map<string, UserSession>();
  
  async handleUserOperation(userId: string, operation: MCPRequest): Promise<any> {
    const session = this.getUserSession(userId);
    
    // Check for conflicts with other users
    const conflicts = this.detectConflicts(operation);
    if (conflicts.length > 0) {
      throw new Error(`Operation conflicts with users: ${conflicts.join(', ')}`);
    }
    
    return session.executeWithLock(operation);
  }
  
  private detectConflicts(operation: MCPRequest): string[] {
    // Implement conflict detection logic
    return [];
  }
}
```

---

## 🧪 **Testing in Cursor Environment**

### 1. **Unit Tests**
```typescript
// test/concurrency.test.ts
import * as assert from 'assert';
import { CursorConcurrencyManager } from '../src/concurrency-manager';

suite('Cursor Concurrency Tests', () => {
  test('concurrent file operations', async () => {
    const manager = new CursorConcurrencyManager('test-workspace');
    const results = await Promise.all([
      manager.executeWithLock('file', 'test.txt', () => Promise.resolve('result1')),
      manager.executeWithLock('file', 'test.txt', () => Promise.resolve('result2'))
    ]);
    
    assert.strictEqual(results.length, 2);
  });
  
  test('database lock timeout', async () => {
    const manager = new CursorConcurrencyManager('test-workspace');
    
    // Simulate long-running operation
    const longOp = manager.executeWithLock('db', 'table1', async () => {
      await new Promise(resolve => setTimeout(resolve, 2000));
      return 'done';
    });
    
    // Second operation should queue
    const shortOp = manager.executeWithLock('db', 'table1', () => Promise.resolve('quick'));
    
    const results = await Promise.all([longOp, shortOp]);
    assert.strictEqual(results[1], 'quick');
  });
});
```

### 2. **Integration Tests**
```typescript
// test/integration.test.ts
suite('Cursor MCP Integration', () => {
  test('multi-cursor instance safety', async () => {
    // Simulate multiple Cursor instances
    const instances = Array(3).fill(null).map(() => new MCPToolWrapper(
      new CursorConcurrencyManager('shared-workspace')
    ));
    
    const operations = instances.map((instance, i) => 
      instance.callTool('write_file', {path: `test${i}.txt`, content: `content${i}`})
    );
    
    const results = await Promise.allSettled(operations);
    
    // All should succeed without conflicts
    results.forEach(result => {
      assert.strictEqual(result.status, 'fulfilled');
    });
  });
});
```

---

## 📋 **Cursor Migration Checklist**

### ✅ **Configuration Updates**
- [ ] Add `CONCURRENCY_SAFE=true` to all MCP server environments
- [ ] Set `CURSOR_SESSION_ID=${workspaceFolder}` for workspace isolation
- [ ] Configure appropriate lock timeouts

### ✅ **Extension Updates**
- [ ] Implement `CursorConcurrencyManager`
- [ ] Add atomic file operations
- [ ] Create safe git operation wrappers
- [ ] Add retry logic for 423 errors

### ✅ **Testing**
- [ ] Test with multiple Cursor windows
- [ ] Verify workspace isolation
- [ ] Test concurrent file operations
- [ ] Validate git operation safety

---

## 🔧 **Troubleshooting**

### Common Issues
```typescript
// Handle common concurrency errors
const handleCursorError = (error: any): string => {
  if (error.message.includes('Database is locked')) {
    return 'Database busy - please wait a moment and try again';
  }
  
  if (error.message.includes('Git repository is locked')) {
    return 'Another git operation is in progress - please wait';
  }
  
  if (error.message.includes('Concurrent access detected')) {
    return 'Another user is modifying this resource - please wait';
  }
  
  return error.message;
};
```

---

## 📚 **Additional Resources**

- **FastMCP 3.2+ Concurrency Standards**: `mcp-central-docs/standards/fastmcp-3.2-concurrency.md`
- **Cursor Extension Development**: https://code.visualstudio.com/api
- **Testing Patterns**: `mcp-central-docs/patterns/cursor-testing.md`

---

**⚠️ ACTION REQUIRED: Update all Cursor MCP integrations to support FastMCP 3.2+ concurrency safety before next release.**
