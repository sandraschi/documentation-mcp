# Pydantic Integration Guide

**Timestamp**: 2026-01-23
**Status**: Core Standard

## Overview

Pydantic is the most widely used data validation library for Python. In the MCP (Model Context Protocol) ecosystem, it serves as the backbone for type safety, schema generation, and configuration management.

## Role in MCP & MyHomeServer

1.  **Tool Input Schemas**: FastMCP uses Pydantic models to automatically generate the JSON Schema that LLMs use to understand how to call tools.
2.  **Configuration**: Via `pydantic-settings`, it manages `.env` files and system environment variables with strict typing.
3.  **Data Serialization**: Ensures that data returned from sensors (Tapo, Netatmo) matches the expected format before reaching the frontend.

## Core Concepts

### 1. Data Models (`BaseModel`)
Define the structure of your data. Pydantic enforces these types at runtime.

```python
from pydantic import BaseModel, Field
from typing import Optional

class DeviceStatus(BaseModel):
    id: str
    name: str
    is_online: bool
    battery_level: Optional[int] = Field(None, ge=0, le=100)
```

### 2. Configuration (`BaseSettings`)
Professional environment variable management.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    DEBUG: bool = False
    
    model_config = {
        "env_file": ".env"
    }
```

### 3. Field Validation
Use `Field` to add constraints and metadata.

*   `ge`: Greater than or equal
*   `le`: Less than or equal
*   `description`: Used for LLM tool descriptions

## Standards for this Repo

*   **Always use Pydantic v2**: Target `pydantic>=2.0.0`.
*   **Docstrings matter**: FastMCP extracts tool documentation from the Pydantic model docstrings.
*   **Type Hints**: Use `Optional`, `List`, `Dict` from `typing` for compatibility.

## Troubleshooting

*   **ValidationError**: Occurs when raw data (e.g., from a camera API) doesn't match your model. Always wrap external API calls in `try/except ValidationError`.
*   **Serialization**: Use `.model_dump()` to convert a model to a dictionary, or `.model_dump_json()` for strings.
