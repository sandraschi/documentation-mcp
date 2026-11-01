# Pydantic Settings and .env File Loading Fix

**Critical fix for MCP servers using pydantic-settings with .env files**

---

## ðŸš¨ The Problem

**`pydantic-settings` with `env_file=".env"` does NOT automatically load `.env` files when using `os.getenv()`.**

This is a common gotcha that affects all MCP servers using:
- `pydantic-settings` with `BaseSettings` or `SettingsConfigDict`
- `env_file=".env"` configuration
- `os.getenv()` calls in `from_env()` methods or elsewhere

### Why This Happens

`pydantic-settings` with `env_file=".env"` **only** auto-loads when you instantiate the Pydantic model directly:

```python
# âœ… This works - Pydantic loads .env automatically
config = Settings()

# âŒ This does NOT work - os.getenv() doesn't see .env file
api_key = os.getenv("API_KEY")  # Returns None even if .env has API_KEY=value
```

The `.env` file is **not** automatically loaded into the Python environment. `os.getenv()` only reads from the actual environment variables, not from `.env` files.

---

## âœ… The Solution

**Explicitly load the `.env` file using `python-dotenv` before reading environment variables.**

### Implementation Pattern

Add this to your `config.py` file **at the top**, before any `os.getenv()` calls:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file if it exists
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    # Also try loading from current directory
    load_dotenv()


class MyConfig(BaseSettings):
    """Configuration with .env file support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    api_key: str = Field(..., description="API key")
    tailnet: str = Field(..., description="Tailnet name")
    
    @classmethod
    def from_env(cls) -> "MyConfig":
        """Load configuration from environment variables."""
        # Now os.getenv() will work because .env is loaded
        api_key = os.getenv("API_KEY")
        tailnet = os.getenv("TAILNET")
        
        if not api_key:
            raise ValueError("API_KEY environment variable is required")
        
        return cls(api_key=api_key, tailnet=tailnet)
```

### Alternative: Use Pydantic Directly

If you're using `os.getenv()` unnecessarily, you can simplify by letting Pydantic handle everything:

```python
# âŒ BAD - Manual os.getenv() calls
def create_settings() -> Settings:
    return Settings(
        HOST=os.getenv("HOST", "127.0.0.1"),
        PORT=int(os.getenv("PORT", "8000")),
        # ... more manual calls
    )

# âœ… GOOD - Let Pydantic load from .env automatically
def create_settings() -> Settings:
    # Pydantic will load from .env via model_config
    return Settings()
```

**However**, you still need `load_dotenv()` if:
- You use `os.getenv()` anywhere else in your code
- You have code that runs before Pydantic model instantiation
- You want to ensure `.env` is loaded regardless of how the config is created

---

## ðŸ“‹ Implementation Checklist

For each MCP server repository:

- [ ] **Check if using pydantic-settings**
  - Look for `BaseSettings`, `SettingsConfigDict`, or `env_file=".env"` in config files
  
- [ ] **Check if using os.getenv()**
  - Search for `os.getenv()` calls in config files or server initialization
  
- [ ] **Add load_dotenv() import**
  ```python
  from dotenv import load_dotenv
  ```
  
- [ ] **Add .env loading code**
  ```python
  from pathlib import Path
  
  env_path = Path(__file__).parent.parent.parent / ".env"
  if env_path.exists():
      load_dotenv(env_path)
  else:
      load_dotenv()
  ```
  
- [ ] **Verify python-dotenv is in dependencies**
  - Check `pyproject.toml` or `requirements.txt`
  - Should have: `python-dotenv>=1.0.0`
  
- [ ] **Test configuration loading**
  - Create a `.env` file with test values
  - Verify `os.getenv()` can read them
  - Verify Pydantic models can load them

---

## ðŸ” Affected Repositories

This fix has been applied to:

âœ… **tailscale-mcp** - Fixed in `config.py` and `mcp_server.py`  
âœ… **immichmcp** - Fixed in `config.py` (already had in `server.py`)  
âœ… **beyondcompare-mcp** - Fixed in `config.py` (also simplified `create_settings()`)  
âœ… **advanced-memory-mcp** - Fixed in `config.py`

### Repositories That May Need This Fix

Check all repos that:
- Use `pydantic-settings` with `env_file=".env"`
- Have `from_env()` methods using `os.getenv()`
- Use `os.getenv()` in server initialization code

---

## ðŸ“ Code Examples

### Example 1: Config File with from_env() Method

```python
"""Configuration management."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file if it exists
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()


class ServerConfig(BaseSettings):
    """Server configuration."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    api_key: str = Field(..., description="API key")
    server_url: str = Field(..., description="Server URL")
    
    @classmethod
    def from_env(cls) -> "ServerConfig":
        """Load from environment variables."""
        # Now works because .env is loaded
        api_key = os.getenv("API_KEY")
        server_url = os.getenv("SERVER_URL", "http://localhost:8000")
        
        if not api_key:
            raise ValueError("API_KEY is required")
        
        return cls(api_key=api_key, server_url=server_url)
```

### Example 2: Server Initialization

```python
"""MCP Server."""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
import structlog
from fastmcp import FastMCP

# Load .env file if it exists (after imports to avoid E402)
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

from .config import ServerConfig
from .tools import register_tools

logger = structlog.get_logger(__name__)


class MCPServer:
    """MCP Server implementation."""
    
    def __init__(self):
        """Initialize server."""
        # Now os.getenv() works because .env is loaded
        self.api_key = os.getenv("API_KEY")
        self.server_url = os.getenv("SERVER_URL")
        
        if not self.api_key:
            logger.error("API_KEY not found in environment")
        
        self.mcp = FastMCP("My MCP Server")
        register_tools(self.mcp)
```

### Example 3: Simplified Pydantic-Only Approach

```python
"""Configuration - Let Pydantic handle everything."""

from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load .env file if it exists
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()


class Settings(BaseModel):
    """Application settings."""
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }
    
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    API_KEY: str = Field(...)


def create_settings() -> Settings:
    """Create settings instance.
    
    Pydantic will automatically load from .env file via model_config.
    """
    return Settings()  # No manual os.getenv() needed!
```

---

## ðŸ§ª Testing

### Test 1: Verify .env Loading

```python
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env
env_path = Path(".env")
load_dotenv(env_path)

# Verify
assert os.getenv("API_KEY") is not None, "API_KEY not loaded from .env"
print("âœ… .env file loading works")
```

### Test 2: Verify Config Loading

```python
from my_package.config import MyConfig

# This should work if .env is loaded
config = MyConfig.from_env()
assert config.api_key is not None
print("âœ… Config loads from .env successfully")
```

### Test 3: Verify Pydantic Direct Loading

```python
from my_package.config import Settings

# This should work if .env is loaded
settings = Settings()
assert settings.API_KEY is not None
print("âœ… Pydantic loads from .env successfully")
```

---

## ðŸ”— Related Documentation

- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [FastMCP 3.1.1++ Migration Guide](../FASTMCP_3.1.1+_MIGRATION.md)
- [MCP Standards](../../STANDARDS.md)

---

## ðŸ“Œ Key Takeaways

1. **`pydantic-settings` with `env_file=".env"` does NOT automatically load `.env` files into the environment**
2. **`os.getenv()` only reads from actual environment variables, not `.env` files**
3. **Always add explicit `load_dotenv()` calls when using `os.getenv()`**
4. **Place `load_dotenv()` at the top of config files, before any `os.getenv()` calls**
5. **Check both project root and current directory for `.env` file**
6. **Ensure `python-dotenv>=1.0.0` is in dependencies**

---

## ðŸš€ Propagation

This fix should be applied to **all MCP server repositories** that:
- Use `pydantic-settings` with `.env` files
- Use `os.getenv()` in configuration or server initialization code

**Status**: âœ… Documented and ready for propagation to all repos

---

**Last Updated**: 2025-11-24  
**Version**: 1.0  
**Status**: Active Standard


