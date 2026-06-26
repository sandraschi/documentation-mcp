# Windsurf MDC MCP Integration - FastMCP 3.2+ Concurrency Safety

## 🚨 Critical Update Required: Concurrency Safety

**FastMCP 3.2+ Universal Connect Pattern enables simultaneous access from multiple Windsurf instances, requiring database and file operation concurrency safety.**

---

## 📋 **Required Updates for Windsurf Integration**

### ✅ **Windsurf MCP Configuration (.windsurfrules/mcp.json)**
```json
{
  "mcpServers": {
    "fileops-mcp": {
      "command": "uv run fileops-mcp-server",
      "args": ["--stdio"],
      "env": {
        "MCP_TRANSPORT": "stdio",
        "CONCURRENCY_SAFE": "true",
        "WINDSURF_SESSION_ID": "${workspaceFolder}",
        "WINDSURF_PROJECT_ID": "${projectName}"
      }
    },
    "gitops-mcp": {
      "command": "uv run gitops-mcp-server",
      "args": ["--stdio"],
      "env": {
        "MCP_TRANSPORT": "stdio",
        "GIT_LOCK_TIMEOUT": "30",
        "CONCURRENCY_SAFE": "true",
        "WINDSURF_SESSION_ID": "${workspaceFolder}"
      }
    },
    "calibre-mcp": {
      "command": "uv run calibre-mcp",
      "args": ["--stdio"],
      "env": {
        "MCP_TRANSPORT": "stdio",
        "DB_LOCK_TIMEOUT": "15",
        "CONCURRENCY_SAFE": "true",
        "WINDSURF_SESSION_ID": "${workspaceFolder}"
      }
    }
  }
}
```

---

## 🔒 **Windsurf-Specific Concurrency Patterns**

### 1. **Project-Aware Session Management**
```typescript
// Windsurf extension: src/windsurf-concurrency.ts
export class WindsurfConcurrencyManager {
  private projectLocks = new Map<string, Set<string>>();
  private operationQueues = new Map<string, Array<QueuedOperation>>();
  private projectId: string;
  
  constructor(projectId: string, workspacePath: string) {
    this.projectId = projectId;
    this.initializeProjectLocks(workspacePath);
  }
  
  async executeWithLock(
    resourceType: string, 
    resourceId: string, 
    operation: () => Promise<any>,
    priority: 'high' | 'normal' | 'low' = 'normal'
  ): Promise<any> {
    const lockKey = `${this.projectId}:${resourceType}:${resourceId}`;
    
    // Check if resource is locked
    if (this.isLocked(lockKey)) {
      return this.queueOperation(lockKey, operation, priority);
    }
    
    // Acquire lock with timeout
    const lockAcquired = await this.acquireLockWithTimeout(lockKey, 30000);
    if (!lockAcquired) {
      throw new WindsurfConcurrencyError(`Failed to acquire lock for ${lockKey}`);
    }
    
    try {
      const result = await operation();
      
      // Broadcast operation completion to other Windsurf instances
      await this.broadcastOperationComplete(lockKey, result);
      
      return result;
    } catch (error) {
      if (this.isConcurrencyError(error)) {
        await this.broadcastOperationError(lockKey, error);
        throw new WindsurfConcurrencyError(`Concurrent access: ${error.message}`);
      }
      throw error;
    } finally {
      this.releaseLock(lockKey);
      this.processQueue(lockKey);
    }
  }
  
  private async acquireLockWithTimeout(lockKey: string, timeout: number): Promise<boolean> {
    const startTime = Date.now();
    
    while (this.isLocked(lockKey) && (Date.now() - startTime) < timeout) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    return !this.isLocked(lockKey);
  }
  
  private async broadcastOperationComplete(lockKey: string, result: any): Promise<void> {
    // Use Windsurf's event system to notify other instances
    WindsurfEvents.emit('operation:complete', {
      lockKey,
      result,
      timestamp: Date.now(),
      projectId: this.projectId
    });
  }
}
```

### 2. **File System Operations with Windsurf Integration**
```typescript
// Windsurf extension: src/windsurf-file-ops.ts
export class WindsurfFileOperations {
  constructor(private concurrency: WindsurfConcurrencyManager) {}
  
  async writeFile(filePath: string, content: string, options?: {
    createDirs?: boolean;
    backup?: boolean;
  }): Promise<void> {
    return this.concurrency.executeWithLock('file', filePath, async () => {
      // Ensure directory exists
      if (options?.createDirs) {
        const dir = path.dirname(filePath);
        await fs.mkdir(dir, { recursive: true });
      }
      
      // Create backup if requested
      if (options?.backup && await fs.access(filePath).then(() => true).catch(() => false)) {
        const backupPath = `${filePath}.backup.${Date.now()}`;
        await fs.copyFile(filePath, backupPath);
      }
      
      // Atomic write using temporary file
      const tempPath = `${filePath}.tmp.${process.pid}.${Date.now()}`;
      
      try {
        await fs.writeFile(tempPath, content, 'utf8');
        
        // Verify write was successful
        const written = await fs.readFile(tempPath, 'utf8');
        if (written !== content) {
          throw new Error('Write verification failed');
        }
        
        // Atomic replace
        await fs.rename(tempPath, filePath);
        
        // Notify Windsurf of file change
        WindsurfEvents.emit('file:changed', {
          path: filePath,
          type: 'write',
          timestamp: Date.now()
        });
        
      } finally {
        // Cleanup temp file
        await fs.unlink(tempPath).catch(() => {});
      }
    }, 'high'); // File operations are high priority
  }
  
  async modifyFile(filePath: string, modifications: Array<{
    search: string | RegExp;
    replace: string;
    options?: { global?: boolean; caseSensitive?: boolean }
  }>): Promise<void> {
    return this.concurrency.executeWithLock('file', filePath, async () => {
      let content = await fs.readFile(filePath, 'utf8');
      let modified = false;
      
      for (const mod of modifications) {
        const search = typeof mod.search === 'string' ? mod.search : mod.search.source;
        const flags = mod.options?.caseSensitive ? 'g' : 'gi';
        const regex = new RegExp(search, flags);
        
        if (regex.test(content)) {
          content = content.replace(regex, mod.replace);
          modified = true;
        }
      }
      
      if (modified) {
        await this.writeFile(filePath, content);
        
        WindsurfEvents.emit('file:modified', {
          path: filePath,
          modifications: modifications.length,
          timestamp: Date.now()
        });
      }
    }, 'normal');
  }
}
```

### 3. **Git Operations with Windsurf Project Context**
```typescript
// Windsurf extension: src/windsurf-git-ops.ts
export class WindsurfGitOperations {
  constructor(private concurrency: WindsurfConcurrencyManager) {}
  
  async commitWithLock(
    repoPath: string, 
    message: string, 
    options?: {
      files?: string[];
      createBranch?: string;
      amend?: boolean;
    }
  ): Promise<string> {
    return this.concurrency.executeWithLock('git', repoPath, async () => {
      const git = simpleGit(repoPath);
      
      // Check repository state
      const status = await git.status();
      
      if (status.conflicted.length > 0) {
        throw new WindsurfGitError('Repository has conflicts - resolve before committing');
      }
      
      // Create branch if requested
      if (options?.createBranch) {
        try {
          await git.checkoutLocalBranch(options.createBranch);
        } catch (error) {
          await git.checkoutLocalBranch('-b', options.createBranch);
        }
      }
      
      // Stage files
      if (options?.files) {
        await git.add(options.files);
      } else {
        await git.add('.');
      }
      
      // Commit with retry logic
      try {
        const commitOptions = options?.amend ? ['--amend'] : [];
        const result = await git.commit(message, commitOptions);
        
        // Notify Windsurf of commit
        WindsurfEvents.emit('git:committed', {
          repoPath,
          commit: result.commit,
          branch: status.current,
          timestamp: Date.now()
        });
        
        return result.commit;
        
      } catch (error) {
        if (error.message.includes('Git repository is locked')) {
          // Wait and retry
          await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000));
          const retryResult = await git.commit(message, options?.amend ? ['--amend'] : []);
          return retryResult.commit;
        }
        throw error;
      }
    }, 'high'); // Git operations are high priority
  }
  
  async mergeWithLock(
    repoPath: string, 
    branch: string, 
    options?: {
      noCommit?: boolean;
      strategy?: 'ours' | 'theirs' | 'union';
    }
  ): Promise<void> {
    return this.concurrency.executeWithLock('git', repoPath, async () => {
      const git = simpleGit(repoPath);
      
      try {
        const mergeOptions = [];
        if (options?.noCommit) mergeOptions.push('--no-commit');
        if (options?.strategy) mergeOptions.push(`--strategy=${options.strategy}`);
        
        await git.merge([branch, ...mergeOptions]);
        
        WindsurfEvents.emit('git:merged', {
          repoPath,
          branch,
          timestamp: Date.now()
        });
        
      } catch (error) {
        if (error.message.includes('conflict')) {
          WindsurfEvents.emit('git:conflicts', {
            repoPath,
            branch,
            conflicts: await this.getConflicts(repoPath),
            timestamp: Date.now()
          });
        }
        throw error;
      }
    }, 'high');
  }
}
```

---

## 🎯 **Windsurf Extension Integration**

### 1. **Extension Setup with Concurrency**
```typescript
// extension.ts
export async function activate(context: vscode.ExtensionContext) {
  const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
  if (!workspaceFolder) {
    return;
  }
  
  const projectId = await getProjectId(workspaceFolder.uri.fsPath);
  const concurrency = new WindsurfConcurrencyManager(projectId, workspaceFolder.uri.fsPath);
  const fileOps = new WindsurfFileOperations(concurrency);
  const gitOps = new WindsurfGitOperations(concurrency);
  const mcpWrapper = new WindsurfMCPWrapper(concurrency);
  
  // Register Windsurf-specific commands
  const commands = [
    vscode.commands.registerCommand('windsurf.safeWriteFile', async (uri, content) => {
      return fileOps.writeFile(uri.fsPath, content, { createDirs: true, backup: true });
    }),
    vscode.commands.registerCommand('windsurf.safeCommit', async (message) => {
      const workspacePath = workspaceFolder.uri.fsPath;
      return gitOps.commitWithLock(workspacePath, message);
    }),
    vscode.commands.registerCommand('windsurf.mcpCall', async (toolName, params) => {
      return mcpWrapper.callTool(toolName, params);
    })
  ];
  
  // Set up event listeners
  setupEventListeners(concurrency);
  
  commands.forEach(cmd => context.subscriptions.push(cmd));
}

function setupEventListeners(concurrency: WindsurfConcurrencyManager) {
  // Listen for operations from other Windsurf instances
  WindsurfEvents.on('operation:complete', (event) => {
    console.log(`Operation completed in project ${event.projectId}:`, event.lockKey);
  });
  
  WindsurfEvents.on('git:committed', (event) => {
    // Refresh git status in UI
    vscode.commands.executeCommand('git.refresh');
  });
  
  WindsurfEvents.on('file:changed', (event) => {
    // Refresh file explorer if needed
    if (event.path) {
      const uri = vscode.Uri.file(event.path);
      vscode.workspace.fs.stat(uri).then(() => {
        vscode.commands.executeCommand('workbench.files.action.refresh');
      });
    }
  });
}
```

### 2. **Windsurf MCP Tool Wrapper**
```typescript
// src/windsurf-mcp-wrapper.ts
export class WindsurfMCPWrapper {
  constructor(private concurrency: WindsurfConcurrencyManager) {}
  
  async callTool(toolName: string, params: any): Promise<any> {
    const resourceInfo = this.analyzeToolResource(toolName, params);
    
    if (resourceInfo.needsLock) {
      return this.concurrency.executeWithLock(
        resourceInfo.type,
        resourceInfo.id,
        async () => this.executeMCPTool(toolName, params),
        resourceInfo.priority
      );
    }
    
    return this.executeMCPTool(toolName, params);
  }
  
  private analyzeToolResource(toolName: string, params: any): {
    needsLock: boolean;
    type: string;
    id: string;
    priority: 'high' | 'normal' | 'low';
  } {
    // Analyze tool to determine if locking is needed
    const writeOperations = ['write_file', 'modify_file', 'delete_file', 'git_commit', 'git_merge'];
    const databaseOperations = ['create_book', 'update_book', 'delete_book'];
    
    if (writeOperations.includes(toolName) && params.path) {
      return { needsLock: true, type: 'file', id: params.path, priority: 'high' };
    }
    
    if (databaseOperations.includes(toolName) && params.id) {
      return { needsLock: true, type: 'database', id: String(params.id), priority: 'normal' };
    }
    
    if (toolName.startsWith('git_') && params.repo_path) {
      return { needsLock: true, type: 'git', id: params.repo_path, priority: 'high' };
    }
    
    return { needsLock: false, type: 'none', id: '', priority: 'normal' };
  }
  
  private async executeMCPTool(toolName: string, params: any): Promise<any> {
    try {
      const result = await vscode.commands.executeCommand('mcp.callTool', toolName, params);
      
      // Check for concurrency errors
      if (result?.error?.code === 423) {
        throw new WindsurfConcurrencyError('Resource locked - try again');
      }
      
      if (result?.error?.message?.includes('concurrency')) {
        throw new WindsurfConcurrencyError('Concurrent access detected');
      }
      
      return result;
    } catch (error) {
      if (this.isRetryableError(error)) {
        return this.retryWithBackoff(toolName, params);
      }
      throw error;
    }
  }
  
  private isRetryableError(error: any): boolean {
    const retryablePatterns = [
      'Resource locked',
      'Database is locked',
      'Git repository is locked',
      'Concurrent access detected'
    ];
    
    return retryablePatterns.some(pattern => 
      error.message?.includes(pattern) || 
      error.error?.message?.includes(pattern)
    );
  }
}
```

---

## 📊 **Windsurf-Specific Features**

### 1. **Project-Based Isolation**
```typescript
// Different projects should not interfere with each other
class ProjectIsolationManager {
  private projectManagers = new Map<string, WindsurfConcurrencyManager>();
  
  getManager(projectId: string): WindsurfConcurrencyManager {
    if (!this.projectManagers.has(projectId)) {
      const workspacePath = this.getProjectWorkspace(projectId);
      this.projectManagers.set(projectId, new WindsurfConcurrencyManager(projectId, workspacePath));
    }
    return this.projectManagers.get(projectId)!;
  }
  
  async executeInProject(
    projectId: string,
    toolName: string,
    params: any
  ): Promise<any> {
    const manager = this.getManager(projectId);
    const wrapper = new WindsurfMCPWrapper(manager);
    return wrapper.callTool(toolName, params);
  }
}
```

### 2. **Real-time Collaboration**
```typescript
// Handle multiple developers in same project
class CollaborationManager {
  private activeUsers = new Map<string, UserSession>();
  
  async handleUserOperation(userId: string, projectId: string, operation: MCPRequest): Promise<any> {
    const conflicts = await this.detectUserConflicts(userId, projectId, operation);
    
    if (conflicts.length > 0) {
      const conflictMessage = `Operation conflicts with users: ${conflicts.join(', ')}. Please wait or contact them.`;
      WindsurfEvents.emit('collaboration:conflict', {
        userId,
        projectId,
        conflicts,
        message: conflictMessage
      });
      
      throw new WindsurfCollaborationError(conflictMessage);
    }
    
    const userSession = this.getUserSession(userId);
    return userSession.executeOperation(operation);
  }
  
  private async detectUserConflicts(userId: string, projectId: string, operation: MCPRequest): Promise<string[]> {
    const conflicts: string[] = [];
    const resourceInfo = this.analyzeOperationResources(operation);
    
    for (const [otherUserId, session] of this.activeUsers) {
      if (otherUserId === userId) continue;
      
      const userConflicts = await session.checkConflicts(resourceInfo);
      if (userConflicts.length > 0) {
        conflicts.push(otherUserId);
      }
    }
    
    return conflicts;
  }
}
```

---

## 🧪 **Testing in Windsurf Environment**

### 1. **Unit Tests**
```typescript
// test/windsurf-concurrency.test.ts
import * as assert from 'assert';
import { WindsurfConcurrencyManager } from '../src/windsurf-concurrency';

suite('Windsurf Concurrency Tests', () => {
  test('project isolation', async () => {
    const manager1 = new WindsurfConcurrencyManager('project1', '/path/to/project1');
    const manager2 = new WindsurfConcurrencyManager('project2', '/path/to/project2');
    
    // Operations on different projects should not interfere
    const results = await Promise.all([
      manager1.executeWithLock('file', 'file1.txt', () => Promise.resolve('project1-result')),
      manager2.executeWithLock('file', 'file1.txt', () => Promise.resolve('project2-result'))
    ]);
    
    assert.strictEqual(results[0], 'project1-result');
    assert.strictEqual(results[1], 'project2-result');
  });
  
  test('priority queue ordering', async () => {
    const manager = new WindsurfConcurrencyManager('test-project', '/test/path');
    
    // Queue operations with different priorities
    const results = await Promise.all([
      manager.executeWithLock('file', 'test.txt', () => Promise.resolve('low'), 'low'),
      manager.executeWithLock('file', 'test.txt', () => Promise.resolve('high'), 'high'),
      manager.executeWithLock('file', 'test.txt', () => Promise.resolve('normal'), 'normal')
    ]);
    
    // High priority should execute first
    assert.strictEqual(results[1], 'high');
  });
});
```

### 2. **Integration Tests**
```typescript
// test/windsurf-integration.test.ts
suite('Windsurf Integration Tests', () => {
  test('multi-windsurf instance safety', async () => {
    // Simulate multiple Windsurf instances working on same project
    const instances = Array(3).fill(null).map((_, i) => 
      new WindsurfMCPWrapper(
        new WindsurfConcurrencyManager('shared-project', '/shared/path')
      )
    );
    
    const operations = instances.map((instance, i) => 
      instance.callTool('write_file', {path: `shared${i}.txt`, content: `content${i}`})
    );
    
    const results = await Promise.allSettled(operations);
    
    // All should succeed without conflicts
    results.forEach((result, i) => {
      assert.strictEqual(result.status, 'fulfilled', `Instance ${i} failed`);
    });
  });
  
  test('git operation safety', async () => {
    const gitOps = new WindsurfGitOperations(
      new WindsurfConcurrencyManager('test-project', '/test/repo')
    );
    
    // Simulate concurrent git operations
    const operations = [
      gitOps.commitWithLock('/test/repo', 'Commit 1'),
      gitOps.commitWithLock('/test/repo', 'Commit 2'),
      gitOps.commitWithLock('/test/repo', 'Commit 3')
    ];
    
    const results = await Promise.allSettled(operations);
    
    // Should handle gracefully (some may queue)
    const successful = results.filter(r => r.status === 'fulfilled');
    assert.ok(successful.length > 0, 'At least one git operation should succeed');
  });
});
```

---

## 📋 **Windsurf Migration Checklist**

### ✅ **Configuration Updates**
- [ ] Add `CONCURRENCY_SAFE=true` to all MCP server environments
- [ ] Set `WINDSURF_SESSION_ID=${workspaceFolder}` for workspace isolation
- [ ] Set `WINDSURF_PROJECT_ID=${projectName}` for project isolation
- [ ] Configure appropriate lock timeouts

### ✅ **Extension Updates**
- [ ] Implement `WindsurfConcurrencyManager`
- [ ] Add project-based isolation
- [ ] Create safe file and git operation wrappers
- [ ] Add retry logic with exponential backoff
- [ ] Implement event broadcasting for collaboration

### ✅ **Testing**
- [ ] Test with multiple Windsurf instances
- [ ] Verify project isolation
- [ ] Test concurrent file operations
- [ ] Validate git operation safety
- [ ] Test collaboration features

---

## 🔧 **Troubleshooting**

### Common Windsurf Issues
```typescript
const handleWindsurfError = (error: any): string => {
  if (error.message.includes('Database is locked')) {
    return 'Database busy - another Windsurf instance is working. Please wait a moment.';
  }
  
  if (error.message.includes('Git repository is locked')) {
    return 'Another git operation is in progress - please wait for it to complete.';
  }
  
  if (error.message.includes('Concurrent access detected')) {
    return 'Another user is modifying this resource - please wait.';
  }
  
  if (error.message.includes('Failed to acquire lock')) {
    return 'Resource is busy - try again in a few moments.';
  }
  
  return error.message;
};
```

---

## 📚 **Additional Resources**

- **FastMCP 3.2+ Concurrency Standards**: `mcp-central-docs/standards/fastmcp-3.2-concurrency.md`
- **Windsurf Extension Development**: https://www.windsurf.ai/docs
- **Testing Patterns**: `mcp-central-docs/patterns/windsurf-testing.md`

---

**⚠️ ACTION REQUIRED: Update all Windsurf MCP integrations to support FastMCP 3.2+ concurrency safety before next release.**
