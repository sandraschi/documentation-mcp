# GitOps-MCP Concurrency Safety Implementation

## 🚨 Critical: FastMCP 3.2+ Universal Connect Pattern

**GitOps-MCP handles Git repository operations that can be accessed simultaneously from multiple clients, potentially corrupting repositories.**

---

## 🔒 **Current Issues & Solutions**

### ❌ **Problems Identified**
```python
# PROBLEMATIC: Race condition in git operations
async def git_commit(repo_path: str, message: str):
    repo = git.Repo(repo_path)
    repo.index.commit(message)  # Multiple clients can corrupt repo state
```

### ✅ **Safe Implementation**
```python
# SOLUTION: Repository locking with atomic operations
async def git_commit_safe(repo_path: str, message: str):
    async with self._get_repo_lock(repo_path) as repo:
        # Check repository state
        if repo.is_dirty(untracked_files=True):
            # Stage changes
            repo.index.add(repo.untracked_files)
            repo.index.add([item.a_path for item in repo.index.diff(None)])
            
            # Commit with retry logic
            try:
                commit = repo.index.commit(message)
                return {"success": True, "commit": commit.hexsha}
            except git.GitError as e:
                if "locked" in str(e).lower():
                    raise GitOperationError(f"Repository locked: {e}")
                raise
        else:
            return {"success": True, "commit": None, "message": "No changes to commit"}
```

---

## 🛠️ **Implementation Plan**

### 1. **Repository Lock Manager**
```python
# src/gitops_mcp/services/repo_lock_manager.py
import asyncio
import time
from pathlib import Path
from typing import Dict, Set
import git
from git.exc import GitCommandError

class RepositoryLockManager:
    def __init__(self):
        self._repo_locks: Dict[str, asyncio.Task] = {}
        self._lock_queue: Dict[str, List[asyncio.Future]] = {}
        self._lock_timeout = 60  # seconds
    
    @asynccontextmanager
    async def get_repo_lock(self, repo_path: str):
        """Get exclusive lock for repository operations."""
        repo_key = str(Path(repo_path).resolve())
        start_time = time.time()
        
        # Wait for existing lock or timeout
        while repo_key in self._repo_locks and (time.time() - start_time) < self._lock_timeout:
            if repo_key not in self._lock_queue:
                self._lock_queue[repo_key] = []
            
            future = asyncio.Future()
            self._lock_queue[repo_key].append(future)
            
            try:
                await future
                break
            except asyncio.CancelledError:
                return
        
        if (time.time() - start_time) >= self._lock_timeout:
            raise GitOperationError(f"Repository lock timeout for {repo_path}")
        
        # Acquire lock
        self._repo_locks[repo_key] = asyncio.current_task()
        
        try:
            yield self._get_repo(repo_path)
        finally:
            # Release lock and process queue
            self._repo_locks.pop(repo_key, None)
            
            if repo_key in self._lock_queue and self._lock_queue[repo_key]:
                next_future = self._lock_queue[repo_key].pop(0)
                if not next_future.done():
                    next_future.set_result(True)
    
    def _get_repo(self, repo_path: str) -> git.Repo:
        """Get Git repository with validation."""
        try:
            repo = git.Repo(repo_path)
            
            # Validate repository state
            if repo.bare:
                raise GitOperationError(f"Repository {repo_path} is bare")
            
            if repo.head.is_detached:
                logger.warning(f"Repository {repo_path} is in detached HEAD state")
            
            return repo
            
        except git.InvalidGitRepositoryError:
            raise GitOperationError(f"Invalid Git repository: {repo_path}")
        except Exception as e:
            raise GitOperationError(f"Failed to open repository {repo_path}: {e}")
```

### 2. **Safe Git Operations**
```python
# src/gitops_mcp/services/safe_git_operations.py
from contextlib import asynccontextmanager
import asyncio
import tempfile
import os
from git import Repo, GitCommandError

class SafeGitOperations:
    def __init__(self):
        self.lock_manager = RepositoryLockManager()
    
    @asynccontextmanager
    async def _get_repo_lock(self, repo_path: str):
        """Repository lock context manager."""
        async with self.lock_manager.get_repo_lock(repo_path) as repo:
            yield repo
    
    async def commit_safe(self, repo_path: str, message: str, files: list = None) -> dict:
        """Safe commit with repository locking."""
        async with self._get_repo_lock(repo_path) as repo:
            try:
                # Check for conflicts first
                if repo.is_dirty(untracked_files=True):
                    # Stage files
                    if files:
                        repo.index.add(files)
                    else:
                        repo.index.add(repo.untracked_files)
                        repo.index.add([item.a_path for item in repo.index.diff(None)])
                    
                    # Create commit
                    commit = repo.index.commit(message)
                    
                    return {
                        "success": True,
                        "commit": commit.hexsha,
                        "message": message,
                        "files_changed": len(repo.index.diff("HEAD~1")) if repo.head.commit else 0
                    }
                else:
                    return {
                        "success": True,
                        "commit": None,
                        "message": "No changes to commit",
                        "files_changed": 0
                    }
                    
            except GitCommandError as e:
                if "locked" in str(e).lower():
                    raise GitOperationError(f"Repository locked during commit: {e}")
                raise GitOperationError(f"Commit failed: {e}")
    
    async def merge_safe(self, repo_path: str, branch: str, strategy: str = "recursive") -> dict:
        """Safe merge with repository locking."""
        async with self._get_repo_lock(repo_path) as repo:
            try:
                # Check current branch
                current_branch = repo.active_branch.name
                
                # Check if branch exists
                if branch not in repo.heads:
                    raise GitOperationError(f"Branch {branch} does not exist")
                
                # Check for conflicts before merge
                try:
                    repo.git.merge("--no-commit", "--no-ff", branch)
                    
                    # Check for conflicts
                    if repo.is_dirty(untracked_files=True):
                        unmerged = repo.index.unmerged_files()
                        if unmerged:
                            # Abort merge and report conflicts
                            repo.git.merge("--abort")
                            return {
                                "success": False,
                                "error": "merge_conflicts",
                                "conflicts": unmerged,
                                "message": f"Merge conflicts in {len(unmerged)} files"
                            }
                    
                    # Complete merge
                    commit = repo.index.commit(f"Merge {branch} into {current_branch}")
                    
                    return {
                        "success": True,
                        "commit": commit.hexsha,
                        "merged_branch": branch,
                        "current_branch": current_branch,
                        "message": f"Merged {branch} into {current_branch}"
                    }
                    
                except GitCommandError as e:
                    # Abort merge on error
                    try:
                        repo.git.merge("--abort")
                    except:
                        pass
                    raise GitOperationError(f"Merge failed: {e}")
                    
            except GitCommandError as e:
                raise GitOperationError(f"Merge operation failed: {e}")
    
    async def push_safe(self, repo_path: str, remote: str = "origin", branch: str = None) -> dict:
        """Safe push with repository locking."""
        async with self._get_repo_lock(repo_path) as repo:
            try:
                if branch is None:
                    branch = repo.active_branch.name
                
                # Check if remote exists
                if remote not in repo.remotes:
                    raise GitOperationError(f"Remote {remote} not found")
                
                # Push with retry logic
                try:
                    result = repo.remotes[remote].push(branch)
                    
                    return {
                        "success": True,
                        "remote": remote,
                        "branch": branch,
                        "pushed_refs": [ref.name for ref in result],
                        "message": f"Pushed {branch} to {remote}"
                    }
                    
                except GitCommandError as e:
                    if "locked" in str(e).lower() or "busy" in str(e).lower():
                        # Wait and retry
                        await asyncio.sleep(2)
                        result = repo.remotes[remote].push(branch)
                        return {
                            "success": True,
                            "remote": remote,
                            "branch": branch,
                            "pushed_refs": [ref.name for ref in result],
                            "message": f"Pushed {branch} to {remote} (retry)"
                        }
                    raise GitOperationError(f"Push failed: {e}")
                    
            except GitCommandError as e:
                raise GitOperationError(f"Push operation failed: {e}")
    
    async def create_branch_safe(self, repo_path: str, branch_name: str, base_branch: str = None) -> dict:
        """Safe branch creation with repository locking."""
        async with self._get_repo_lock(repo_path) as repo:
            try:
                # Determine base branch
                if base_branch is None:
                    base_branch = repo.active_branch.name
                
                # Check if branch already exists
                if branch_name in repo.heads:
                    return {
                        "success": False,
                        "error": "branch_exists",
                        "message": f"Branch {branch_name} already exists"
                    }
                
                # Create new branch
                new_branch = repo.create_head(branch_name, repo.heads[base_branch])
                new_branch.checkout()
                
                return {
                    "success": True,
                    "branch": branch_name,
                    "base_branch": base_branch,
                    "current_branch": branch_name,
                    "message": f"Created branch {branch_name} from {base_branch}"
                }
                
            except GitCommandError as e:
                raise GitOperationError(f"Branch creation failed: {e}")
```

### 3. **Update MCP Tools**
```python
# src/gitops_mcp/tools/safe_git_tools.py
from gitops_mcp.services.safe_git_operations import SafeGitOperations

@mcp.tool()
async def git_commit_safe(repo_path: str, message: str, files: list = None) -> dict:
    """Commit changes with repository locking and safety checks."""
    git_ops = SafeGitOperations()
    
    try:
        result = await git_ops.commit_safe(repo_path, message, files)
        return result
    except GitOperationError as e:
        return {
            "success": False,
            "error": "git_operation_failed",
            "message": str(e)
        }

@mcp.tool()
async def git_merge_safe(repo_path: str, branch: str, strategy: str = "recursive") -> dict:
    """Merge branch with repository locking and conflict detection."""
    git_ops = SafeGitOperations()
    
    try:
        result = await git_ops.merge_safe(repo_path, branch, strategy)
        return result
    except GitOperationError as e:
        return {
            "success": False,
            "error": "git_operation_failed",
            "message": str(e)
        }

@mcp.tool()
async def git_push_safe(repo_path: str, remote: str = "origin", branch: str = None) -> dict:
    """Push changes with repository locking and retry logic."""
    git_ops = SafeGitOperations()
    
    try:
        result = await git_ops.push_safe(repo_path, remote, branch)
        return result
    except GitOperationError as e:
        return {
            "success": False,
            "error": "git_operation_failed",
            "message": str(e)
        }

@mcp.tool()
async def git_create_branch_safe(repo_path: str, branch_name: str, base_branch: str = None) -> dict:
    """Create branch with repository locking."""
    git_ops = SafeGitOperations()
    
    try:
        result = await git_ops.create_branch_safe(repo_path, branch_name, base_branch)
        return result
    except GitOperationError as e:
        return {
            "success": False,
            "error": "git_operation_failed",
            "message": str(e)
        }
```

---

## 🧪 **Testing Implementation**

### 1. **Concurrency Tests**
```python
# tests/test_git_concurrency.py
import asyncio
import tempfile
import shutil
from pathlib import Path
from gitops_mcp.services.safe_git_operations import SafeGitOperations

class TestGitConcurrency:
    def setup_repo(self):
        """Create test repository."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_path = Path(self.temp_dir) / "test_repo"
        self.repo_path.mkdir()
        
        # Initialize git repo
        repo = git.Repo.init(self.repo_path)
        
        # Configure git
        with repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")
        
        # Create initial commit
        test_file = self.repo_path / "test.txt"
        test_file.write_text("Initial content")
        repo.index.add([str(test_file)])
        repo.index.commit("Initial commit")
        
        return str(self.repo_path)
    
    def teardown_repo(self):
        """Clean up test repository."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    async def test_concurrent_commits(self):
        """Test multiple clients committing to same repository."""
        repo_path = self.setup_repo()
        git_ops = SafeGitOperations()
        
        async def commit_changes(client_id: int):
            # Create different files for each client
            test_file = Path(repo_path) / f"client_{client_id}.txt"
            test_file.write_text(f"Content from client {client_id}")
            
            return await git_ops.commit_safe(
                repo_path, 
                f"Commit from client {client_id}",
                [str(test_file)]
            )
        
        # Run 5 concurrent commits
        tasks = [commit_changes(i) for i in range(5)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify all commits succeeded
        successful = [r for r in results if isinstance(r, dict) and r.get("success")]
        assert len(successful) == 5
        
        # Verify repository integrity
        repo = git.Repo(repo_path)
        commits = list(repo.iter_commits())
        assert len(commits) == 6  # Initial + 5 client commits
        
        self.teardown_repo()
    
    async def test_concurrent_branch_operations(self):
        """Test concurrent branch creation and operations."""
        repo_path = self.setup_repo()
        git_ops = SafeGitOperations()
        
        async def create_branch(client_id: int):
            return await git_ops.create_branch_safe(
                repo_path,
                f"feature-{client_id}",
                "main"
            )
        
        # Run concurrent branch creation
        tasks = [create_branch(i) for i in range(3)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify all branches created successfully
        successful = [r for r in results if isinstance(r, dict) and r.get("success")]
        assert len(successful) == 3
        
        self.teardown_repo()
```

---

## 📋 **Migration Checklist**

### ✅ **Code Updates**
- [ ] Implement `RepositoryLockManager` class
- [ ] Create `SafeGitOperations` service
- [ ] Update all git tools with locking
- [ ] Add proper error handling and cleanup
- [ ] Implement retry logic for lock contention

### ✅ **Configuration**
- [ ] Add `CONCURRENCY_SAFE=true` environment variable
- [ ] Set appropriate repository lock timeouts
- [ ] Configure git user settings for automation

### ✅ **Testing**
- [ ] Add concurrency tests to test suite
- [ ] Test with 5+ simultaneous git operations
- [ ] Verify repository integrity under load
- [ ] Test conflict detection and resolution

---

## 🚀 **FastMCP 3.2+ Integration**

### Universal Connect Pattern Support
```python
# Works with both stdio and HTTP simultaneously
mcp = FastMCP("gitops-mcp")

@mcp.tool()
async def safe_git_operation(repo_path: str, operation: str, **kwargs):
    """Thread-safe git operation for universal access."""
    git_ops = SafeGitOperations()
    
    if operation == "commit":
        return await git_ops.commit_safe(repo_path, kwargs.get("message"), kwargs.get("files"))
    elif operation == "merge":
        return await git_ops.merge_safe(repo_path, kwargs.get("branch"), kwargs.get("strategy"))
    elif operation == "push":
        return await git_ops.push_safe(repo_path, kwargs.get("remote"), kwargs.get("branch"))
    else:
        raise ValueError(f"Unknown git operation: {operation}")
```

---

## 📊 **Performance Considerations**

- **Lock Timeout**: 60 seconds (configurable)
- **Queue Processing**: FIFO order for waiting operations
- **Repository Validation**: State checks before operations
- **Conflict Detection**: Pre-merge conflict checking

---

## 📞 **Support & Resources**

- **FastMCP 3.2+ Standards**: `mcp-central-docs/standards/fastmcp-3.2-concurrency.md`
- **Testing Suite**: `tests/test_git_concurrency.py`
- **GitPython Documentation**: https://gitpython.readthedocs.io

---

**⚠️ CRITICAL: GitOps-MCP must implement these repository locking patterns before FastMCP 3.2+ deployment to prevent repository corruption.**
