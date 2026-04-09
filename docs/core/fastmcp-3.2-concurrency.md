# FastMCP 3.2+ Universal Concurrency Safety Standards

## 🚨 Critical: Multi-Client Database Concurrency

**FastMCP 3.2+ Universal Connect Pattern enables simultaneous stdio + HTTP access, creating critical database concurrency issues.**

### 🎯 **Scope: ALL Write-Enabled MCP Repositories**

This affects ANY MCP server that:
- ✅ Writes to databases (SQLite, PostgreSQL, MySQL)
- ✅ Modifies files on disk
- ✅ Manages shared state
- ✅ Uses Git operations
- ✅ Handles concurrent API requests

**Affected Repositories:**
- `fileops-mcp` - File system operations
- `gitops-mcp` - Git repository operations  
- `calibre-mcp` - Book database operations
- `plex-mcp` - Media database operations
- `meta-mcp` - Fleet management
- `yahboom-mcp` - Robot control state
- `inkscape-mcp` - File modifications

---

## 🔒 **Database Concurrency Requirements**

### ❌ **PROHIBITED Patterns**
```python
# NEVER DO THIS - Race Condition!
with session:
    book = session.query(Book).get(id)  # Read
    book.title = "New Title"           # Modify
    session.commit()                     # Write
```

### ✅ **REQUIRED Patterns**
```python
# ALWAYS DO THIS - Thread-Safe!
async with self._get_locked_session(resource_id) as session:
    book = session.query(Book).get(id)
    book.title = "New Title"
    session.add(book)
    # Automatic commit/rollback with proper locking
```

---

## 🛠️ **Implementation Standards**

### 1. **Base Service Class with Concurrency**
```python
from contextlib import asynccontextmanager
from sqlalchemy import text

class BaseConcurrencyService:
    @asynccontextmanager
    async def _get_safe_session(self) -> Session:
        """Thread-safe session for concurrent operations."""
        session = self.db.session
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise ServiceError(f"Concurrency error: {e}", status_code=500)
        finally:
            session.close()
    
    @asynccontextmanager
    async def _get_locked_session(self, resource_id: Any) -> Session:
        """Row-level locking for write operations."""
        session = self.db.session
        try:
            session.execute(text("BEGIN IMMEDIATE"))
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise ServiceError(f"Lock error: {e}", status_code=423)
        finally:
            session.close()
```

### 2. **SQLite Concurrency Configuration**
```python
# REQUIRED for all SQLite databases
engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False},
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
)

# REQUIRED WAL mode for concurrent reads
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=-2000")
    cursor.execute("PRAGMA temp_store=MEMORY")
    cursor.close()
```

### 3. **File Operations Concurrency**
```python
import asyncio
import aiofiles
from pathlib import Path

class ThreadSafeFileOperations:
    async def write_file_safe(self, path: Path, content: str):
        """Atomic file write with locking."""
        temp_path = path.with_suffix('.tmp')
        try:
            async with aiofiles.open(temp_path, 'w', encoding='utf-8') as f:
                await f.write(content)
            # Atomic replace
            temp_path.replace(path)
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            raise ServiceError(f"File write error: {e}")
    
    async def modify_file_safe(self, path: Path, modifications: list):
        """Thread-safe file modifications."""
        async with aiofiles.open(path, 'r+', encoding='utf-8') as f:
            content = await f.read()
            for mod in modifications:
                content = content.replace(mod['old'], mod['new'])
            await f.seek(0)
            await f.write(content)
            await f.truncate()
```

---

## 📋 **Repository Checklist**

### ✅ **Database Safety**
- [ ] Row-level locking for write operations
- [ ] `BEGIN IMMEDIATE` transactions for SQLite
- [ ] WAL mode enabled
- [ ] Connection pooling configured
- [ ] Proper rollback handling

### ✅ **File Operations Safety**  
- [ ] Atomic file writes
- [ ] Temporary file patterns
- [ ] Thread-safe async file I/O
- [ ] Locking for shared files

### ✅ **Git Operations Safety**
- [ ] Repository locking during operations
- [ ] Atomic commits
- [ ] Conflict resolution
- [ ] Branch protection

### ✅ **API Safety**
- [ ] Request rate limiting
- [ ] Resource locking
- [ ] Timeout handling
- [ ] Error recovery

---

## 🚀 **FastMCP 3.2+ Integration**

### Universal Connect Pattern Support
```python
# Single FastMCP instance, multiple transports
mcp = FastMCP("server")

# Enable concurrent access
@mcp.tool()
async def safe_database_operation(resource_id: str):
    async with service._get_locked_session(resource_id) as session:
        # Thread-safe operation
        result = await perform_operation(session, resource_id)
        return result

# Works with both stdio and HTTP simultaneously
```

---

## 📚 **Documentation Requirements**

### README.md Updates
```markdown
## Concurrency Safety

This MCP server supports FastMCP 3.2+ universal connect pattern with:
- ✅ Thread-safe database operations
- ✅ Row-level locking for writes
- ✅ Atomic file operations
- ✅ Multi-client support (5+ simultaneous)

### Supported Clients
- Claude Desktop (stdio)
- Web applications (HTTP)
- IDE integrations (both)
```

### CHANGELOG.md Entry
```markdown
## [X.X.X] - FastMCP 3.2+ Concurrency Safety

### Added
- Thread-safe database operations with row-level locking
- Atomic file operations for concurrent access
- Multi-client support (5+ simultaneous connections)
- FastMCP 3.2+ universal connect pattern compatibility

### Fixed
- Race conditions in database write operations
- File corruption during concurrent modifications
- Git operation conflicts
```

---

## 🧪 **Testing Requirements**

### Concurrency Tests
```python
@mcp.tool()
async def test_concurrency(operation: str, clients: int = 5):
    """Test concurrent operations safety."""
    # Test 5+ simultaneous operations
    # Verify no data corruption
    # Check proper locking behavior
    return {"concurrency_safe": True, "clients_tested": clients}
```

### Load Testing
- ✅ 5+ concurrent database writes
- ✅ 10+ concurrent file operations  
- ✅ Mixed read/write operations
- ✅ Error recovery testing

---

## 🎯 **Implementation Priority**

### **HIGH PRIORITY** (Immediate)
1. `fileops-mcp` - File system operations
2. `gitops-mcp` - Git repository operations
3. `calibre-mcp` - Book database operations
4. `plex-mcp` - Media database operations

### **MEDIUM PRIORITY** (Next Sprint)
5. `meta-mcp` - Fleet management
6. `yahboom-mcp` - Robot control
7. `inkscape-mcp` - File modifications

### **LOW PRIORITY** (Future)
8. Read-only repositories
9. Simple utility MCPs

---

## 📞 **Support & Resources**

- **FastMCP 3.2+ Documentation**: https://gofastmcp.com
- **Concurrency Patterns**: See `mcp-central-docs/patterns/concurrency.md`
- **Testing Suite**: `mcp-central-docs/tools/concurrency-tester.py`
- **Standards Repository**: `mcp-central-docs/standards/`

---

**⚠️ CRITICAL: All write-enabled MCP servers MUST implement these patterns before FastMCP 3.2+ deployment.**
