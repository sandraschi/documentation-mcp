# FileOps-MCP Concurrency Safety Implementation

## 🚨 Critical: FastMCP 3.2+ Universal Connect Pattern

**FileOps-MCP handles file system operations that can be accessed simultaneously from multiple clients (stdio + HTTP).**

---

## 🔒 **Current Issues & Solutions**

### ❌ **Problems Identified**
```python
# PROBLEMATIC: Race condition in file operations
async def write_file(path: str, content: str):
    async with aiofiles.open(path, 'w') as f:
        await f.write(content)  # Multiple clients can corrupt file
```

### ✅ **Safe Implementation**
```python
# SOLUTION: Atomic file operations with locking
async def write_file_safe(path: str, content: str):
    async with self._get_locked_session(path) as session:
        temp_path = f"{path}.tmp.{uuid4()}"
        try:
            async with aiofiles.open(temp_path, 'w') as f:
                await f.write(content)
            
            # Verify write integrity
            async with aiofiles.open(temp_path, 'r') as f:
                written = await f.read()
                if written != content:
                    raise FileOperationError("Write verification failed")
            
            # Atomic replace
            os.replace(temp_path, path)
            
        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise FileOperationError(f"Safe write failed: {e}")
```

---

## 🛠️ **Implementation Plan**

### 1. **Update Base Service Class**
```python
# src/fileops_mcp/services/base_service.py
from contextlib import asynccontextmanager
import asyncio
import uuid
from pathlib import Path

class ConcurrencySafeFileService:
    def __init__(self):
        self._locks = {}  # In-memory lock registry
        self._lock_timeout = 30  # seconds
    
    @asynccontextmanager
    async def _get_file_lock(self, file_path: str):
        """Get exclusive lock for file operations."""
        lock_key = str(Path(file_path).resolve())
        start_time = asyncio.get_event_loop().time()
        
        # Wait for lock with timeout
        while lock_key in self._locks:
            if asyncio.get_event_loop().time() - start_time > self._lock_timeout:
                raise FileOperationError(f"Lock timeout for {file_path}")
            await asyncio.sleep(0.1)
        
        # Acquire lock
        self._locks[lock_key] = asyncio.current_task()
        try:
            yield
        finally:
            self._locks.pop(lock_key, None)
    
    @asynccontextmanager
    async def _get_directory_lock(self, dir_path: str):
        """Get exclusive lock for directory operations."""
        lock_key = f"dir:{str(Path(dir_path).resolve())}"
        start_time = asyncio.get_event_loop().time()
        
        while lock_key in self._locks:
            if asyncio.get_event_loop().time() - start_time > self._lock_timeout:
                raise FileOperationError(f"Directory lock timeout for {dir_path}")
            await asyncio.sleep(0.1)
        
        self._locks[lock_key] = asyncio.current_task()
        try:
            yield
        finally:
            self._locks.pop(lock_key, None)
```

### 2. **Update File Operations**
```python
# src/fileops_mcp/tools/file_operations.py
@mcp.tool()
async def write_file_safe(path: str, content: str, create_dirs: bool = False) -> dict:
    """Write file with atomic operations and concurrency safety."""
    file_service = ConcurrencySafeFileService()
    
    async with file_service._get_file_lock(path):
        # Create directories if needed
        if create_dirs:
            parent_dir = Path(path).parent
            parent_dir.mkdir(parents=True, exist_ok=True)
        
        # Atomic write
        temp_path = f"{path}.tmp.{uuid.uuid4()}"
        try:
            async with aiofiles.open(temp_path, 'w', encoding='utf-8') as f:
                await f.write(content)
            
            # Verify
            async with aiofiles.open(temp_path, 'r', encoding='utf-8') as f:
                verification = await f.read()
                if verification != content:
                    raise FileOperationError("Write verification failed")
            
            # Atomic replace
            os.replace(temp_path, path)
            
            return {
                "success": True,
                "path": path,
                "bytes_written": len(content),
                "atomic": True
            }
            
        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise FileOperationError(f"Safe write failed: {e}")

@mcp.tool()
async def modify_file_safe(path: str, modifications: list[dict]) -> dict:
    """Modify file with concurrency safety."""
    file_service = ConcurrencySafeFileService()
    
    async with file_service._get_file_lock(path):
        # Read current content
        try:
            async with aiofiles.open(path, 'r', encoding='utf-8') as f:
                content = await f.read()
        except FileNotFoundError:
            raise FileOperationError(f"File not found: {path}")
        
        # Apply modifications
        modified_content = content
        changes_made = 0
        
        for mod in modifications:
            old_text = mod.get('old', '')
            new_text = mod.get('new', '')
            options = mod.get('options', {})
            
            if old_text in modified_content:
                if options.get('global', False):
                    modified_content = modified_content.replace(old_text, new_text)
                    changes_made += modified_content.count(old_text)
                else:
                    modified_content = modified_content.replace(old_text, new_text, 1)
                    changes_made += 1
            else:
                logger.warning(f"Text not found in file: {old_text[:50]}...")
        
        # Write back atomically
        if changes_made > 0:
            await write_file_safe(path, modified_content, create_dirs=False)
        
        return {
            "success": True,
            "path": path,
            "changes_made": changes_made,
            "modifications_applied": len(modifications)
        }

@mcp.tool()
async def delete_file_safe(path: str) -> dict:
    """Delete file with concurrency safety."""
    file_service = ConcurrencySafeFileService()
    
    async with file_service._get_file_lock(path):
        try:
            if os.path.exists(path):
                os.unlink(path)
                return {"success": True, "path": path, "deleted": True}
            else:
                return {"success": True, "path": path, "deleted": False}
        except OSError as e:
            raise FileOperationError(f"Delete failed: {e}")
```

### 3. **Directory Operations**
```python
# src/fileops_mcp/tools/directory_operations.py
@mcp.tool()
async def create_directory_safe(path: str, parents: bool = True) -> dict:
    """Create directory with concurrency safety."""
    file_service = ConcurrencySafeFileService()
    
    async with file_service._get_directory_lock(path):
        try:
            Path(path).mkdir(parents=parents, exist_ok=True)
            return {
                "success": True,
                "path": path,
                "created": True,
                "parents": parents
            }
        except OSError as e:
            raise DirectoryOperationError(f"Directory creation failed: {e}")

@mcp.tool()
async def delete_directory_safe(path: str, recursive: bool = False) -> dict:
    """Delete directory with concurrency safety."""
    file_service = ConcurrencySafeFileService()
    
    async with file_service._get_directory_lock(path):
        try:
            if not os.path.exists(path):
                return {"success": True, "path": path, "deleted": False}
            
            if recursive:
                import shutil
                shutil.rmtree(path)
            else:
                os.rmdir(path)
            
            return {"success": True, "path": path, "deleted": True}
        except OSError as e:
            raise DirectoryOperationError(f"Directory deletion failed: {e}")
```

---

## 🧪 **Testing Implementation**

### 1. **Concurrency Tests**
```python
# tests/test_concurrency.py
import asyncio
import tempfile
import os
from fileops_mcp.services.base_service import ConcurrencySafeFileService

class TestConcurrency:
    async def test_concurrent_file_writes(self):
        """Test multiple clients writing to same file."""
        service = ConcurrencySafeFileService()
        temp_file = tempfile.mktemp()
        
        async def write_content(client_id: int):
            content = f"Client {client_id} content"
            return await write_file_safe(temp_file, content)
        
        # Run 5 concurrent writes
        tasks = [write_content(i) for i in range(5)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify file integrity
        if os.path.exists(temp_file):
            async with aiofiles.open(temp_file, 'r') as f:
                final_content = await f.read()
            os.unlink(temp_file)
        
        # Should have exactly one client's content
        assert any(f"Client {i} content" in final_content for i in range(5))
        assert len([r for r in results if isinstance(r, Exception)]) == 0
    
    async def test_concurrent_file_modifications(self):
        """Test multiple clients modifying same file."""
        service = ConcurrencySafeFileService()
        temp_file = tempfile.mktemp()
        
        # Create initial file
        await write_file_safe(temp_file, "Initial content")
        
        async def modify_file(client_id: int):
            mods = [{"old": "Initial content", "new": f"Modified by client {client_id}"}]
            return await modify_file_safe(temp_file, mods)
        
        # Run concurrent modifications
        tasks = [modify_file(i) for i in range(3)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify final state
        async with aiofiles.open(temp_file, 'r') as f:
            final_content = await f.read()
        os.unlink(temp_file)
        
        # Should have exactly one modification
        assert any(f"Modified by client {i}" in final_content for i in range(3))
```

---

## 📋 **Migration Checklist**

### ✅ **Code Updates**
- [ ] Implement `ConcurrencySafeFileService` base class
- [ ] Update all file operation tools with locking
- [ ] Add atomic write patterns
- [ ] Implement proper error handling and cleanup
- [ ] Add verification steps for critical operations

### ✅ **Configuration**
- [ ] Add `CONCURRENCY_SAFE=true` environment variable
- [ ] Set appropriate lock timeouts
- [ ] Configure logging for concurrency issues

### ✅ **Testing**
- [ ] Add concurrency tests to test suite
- [ ] Test with 5+ simultaneous operations
- [ ] Verify file integrity under load
- [ ] Test error recovery scenarios

---

## 🚀 **FastMCP 3.2+ Integration**

### Universal Connect Pattern Support
```python
# Works with both stdio and HTTP simultaneously
mcp = FastMCP("fileops-mcp")

@mcp.tool()
async def atomic_file_operation(path: str, operation: str, **kwargs):
    """Thread-safe file operation for universal access."""
    file_service = ConcurrencySafeFileService()
    
    async with file_service._get_file_lock(path):
        if operation == "write":
            return await write_file_safe(path, kwargs.get("content", ""))
        elif operation == "modify":
            return await modify_file_safe(path, kwargs.get("modifications", []))
        elif operation == "delete":
            return await delete_file_safe(path)
        else:
            raise ValueError(f"Unknown operation: {operation}")
```

---

## 📊 **Performance Considerations**

- **Lock Timeout**: 30 seconds (configurable)
- **Atomic Operations**: Temporary file pattern
- **Memory Usage**: In-memory lock registry
- **Scalability**: Supports 10+ concurrent operations

---

## 📞 **Support & Resources**

- **FastMCP 3.2+ Standards**: `mcp-central-docs/standards/fastmcp-3.2-concurrency.md`
- **Testing Suite**: `tests/test_concurrency.py`
- **Error Patterns**: `src/fileops_mcp/exceptions.py`

---

**⚠️ CRITICAL: FileOps-MCP must implement these concurrency patterns before FastMCP 3.2+ deployment to prevent file corruption.**
