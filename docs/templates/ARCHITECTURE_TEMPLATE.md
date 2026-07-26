# Architecture - {Project Name}

**For:** Developers, Contributors  
**Purpose:** System design and technical architecture documentation  
**Last Updated:** {Date}

---

## ðŸ“ Overview

{High-level system overview - what the project does and how it's structured}

### Key Goals

- {Goal 1}
- {Goal 2}
- {Goal 3}

### Design Principles

- {Principle 1}
- {Principle 2}
- {Principle 3}

---

## ðŸ—ï¸ System Architecture

### High-Level Diagram

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   Claude Desktop    â”‚
â”‚                     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
           â”‚ MCP Protocol
           â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  {Your MCP Server}  â”‚
â”‚                     â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚  FastMCP      â”‚  â”‚
â”‚  â”‚  Framework    â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚          â”‚          â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚  Tool Layer   â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚          â”‚          â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚  Service      â”‚  â”‚
â”‚  â”‚  Layer        â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚          â”‚          â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
           â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  {External System}  â”‚
â”‚  {Application/API}  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸ§© Components

### 1. MCP Server Core

**Location:** `src/{package}/mcp_server.py`

**Purpose:** {Description}

**Key Responsibilities:**
- Tool registration
- Request/response handling
- Error management
- Logging and monitoring

**Dependencies:**
- FastMCP 3.1.1++
- {Other dependencies}

---

### 2. Tool Layer

**Location:** `src/{package}/tools/`

**Purpose:** {Description}

**Organization:**
```
tools/
â”œâ”€â”€ __init__.py          # Tool exports
â”œâ”€â”€ {category1}_tools.py # Category 1 tools
â”œâ”€â”€ {category2}_tools.py # Category 2 tools
â””â”€â”€ portmanteau/         # Portmanteau tools (if applicable)
    â”œâ”€â”€ {category1}.py
    â””â”€â”€ {category2}.py
```

**Key Tools:**
- `{tool1}` - {Description}
- `{tool2}` - {Description}
- `{tool3}` - {Description}

**Tool Pattern:**
```python
@mcp.tool()
async def tool_name(param: str) -> dict[str, Any]:
    '''Comprehensive tool documentation.
    
    Args:
        param: Parameter description
        
    Returns:
        Result dictionary with status and data
    '''
    try:
        result = await service.operation(param)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

---

### 3. Service Layer

**Location:** `src/{package}/services/`

**Purpose:** Business logic and external integration

**Key Services:**
- `{service1}` - {Description}
- `{service2}` - {Description}

**Service Pattern:**
```python
class ServiceName:
    def __init__(self, config: Config):
        self.config = config
        self.client = initialize_client()
    
    async def operation(self, param: str) -> Result:
        # Implementation
        pass
```

---

### 4. Configuration Management

**Location:** `src/{package}/config.py`

**Purpose:** Centralized configuration

**Configuration Sources:**
1. Environment variables
2. Configuration file
3. Default values

**Example:**
```python
@dataclass
class Config:
    api_key: str
    timeout: int = 30
    debug: bool = False
    
    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            api_key=os.getenv("API_KEY"),
            timeout=int(os.getenv("TIMEOUT", "30")),
            debug=os.getenv("DEBUG", "false").lower() == "true"
        )
```

---

### 5. Error Handling

**Location:** `src/{package}/exceptions.py`

**Purpose:** Custom exception hierarchy

**Exception Hierarchy:**
```
BaseException
â””â”€â”€ {Project}Error
    â”œâ”€â”€ ConfigurationError
    â”œâ”€â”€ APIError
    â”‚   â”œâ”€â”€ AuthenticationError
    â”‚   â”œâ”€â”€ RateLimitError
    â”‚   â””â”€â”€ TimeoutError
    â””â”€â”€ ValidationError
```

---

## ðŸ“Š Data Flow

### Request Flow

```
1. Claude Desktop â†’ MCP Protocol Request
2. FastMCP â†’ Route to Tool
3. Tool â†’ Validate Parameters
4. Tool â†’ Call Service Layer
5. Service â†’ External System (if needed)
6. Service â†’ Return Result
7. Tool â†’ Format Response
8. FastMCP â†’ MCP Protocol Response
9. Claude Desktop â†’ Display Result
```

### Error Flow

```
1. Error Occurs in Service/Tool
2. Exception Raised
3. Caught by Tool Error Handler
4. Logged to Structured Logger
5. Formatted Error Response
6. Returned to Claude Desktop
```

---

## ðŸ”Œ Integration Points

### External Systems

| System | Integration Type | Purpose |
|--------|-----------------|---------|
| {System 1} | REST API | {Purpose} |
| {System 2} | SDK | {Purpose} |
| {System 3} | CLI | {Purpose} |

### Integration Patterns

**Pattern 1: REST API Integration**
```python
async def call_api(endpoint: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/{endpoint}")
        response.raise_for_status()
        return response.json()
```

**Pattern 2: SDK Integration**
```python
from external_sdk import Client

client = Client(api_key=config.api_key)
result = await client.operation(params)
```

---

## ðŸ” Security Architecture

### Authentication

- {Authentication method}
- {Key storage approach}
- {Token refresh strategy}

### Authorization

- {Authorization model}
- {Permission checks}

### Data Security

- {Sensitive data handling}
- {Encryption approach}
- {Logging security}

---

## ðŸ“ˆ Monitoring & Observability

### Logging

**Structured Logging:**
```python
logger.info(
    "operation_completed",
    operation="tool_name",
    duration=1.23,
    success=True
)
```

### Metrics

- Request count
- Request duration
- Error rate
- {Custom metrics}

### Health Checks

```python
@mcp.tool()
async def health_check() -> dict[str, Any]:
    '''System health check.'''
    return {
        "status": "healthy",
        "version": VERSION,
        "uptime": get_uptime()
    }
```

---

## ðŸ”„ State Management

### Session State

- {How session state is managed}
- {State persistence approach}

### Cache Strategy

- {Caching approach}
- {Cache invalidation}
- {TTL configuration}

---

## ðŸš€ Deployment Architecture

### Development

```
Developer Machine
â”œâ”€â”€ Source Code
â”œâ”€â”€ Local FastMCP Server
â””â”€â”€ Claude Desktop (Development)
```

### Production

```
User Machine
â”œâ”€â”€ Installed MCPB Package
â”œâ”€â”€ FastMCP Server (via uv/pip)
â””â”€â”€ Claude Desktop (Production)
```

---

## ðŸ”§ Extension Points

### Adding New Tools

1. Create tool function in `tools/`
2. Register with `@mcp.tool()` decorator
3. Add comprehensive docstring
4. Add to `__init__.py` exports
5. Update documentation

### Adding New Services

1. Create service class in `services/`
2. Implement async methods
3. Add error handling
4. Add tests
5. Update architecture docs

### Adding New Integrations

1. Create integration module
2. Implement client wrapper
3. Add authentication
4. Add error handling
5. Add monitoring
6. Document integration

---

## ðŸ“‹ Dependency Graph

```
mcp_server.py
â”œâ”€â”€ FastMCP (external)
â”œâ”€â”€ tools/
â”‚   â”œâ”€â”€ {category1}_tools.py
â”‚   â”‚   â””â”€â”€ services/{service1}.py
â”‚   â””â”€â”€ {category2}_tools.py
â”‚       â””â”€â”€ services/{service2}.py
â””â”€â”€ config.py
```

---

## ðŸ§ª Testing Architecture

### Test Structure

```
tests/
â”œâ”€â”€ unit/              # Unit tests
â”‚   â”œâ”€â”€ test_tools/
â”‚   â””â”€â”€ test_services/
â”œâ”€â”€ integration/       # Integration tests
â”‚   â””â”€â”€ test_api/
â””â”€â”€ fixtures/          # Test fixtures
    â””â”€â”€ mock_data.py
```

### Test Strategy

- **Unit Tests:** Test individual components
- **Integration Tests:** Test external integrations
- **Mocking:** Mock external systems for reliability

---

## ðŸŽ¯ Performance Considerations

### Bottlenecks

- {Known bottleneck 1}
- {Known bottleneck 2}

### Optimization Strategies

- {Strategy 1}
- {Strategy 2}

### Scalability

- {Scalability approach}
- {Resource limits}

---

## ðŸ“š Further Reading

- [Tool Reference](tools-reference.md) - Complete API documentation
- [Integration Guide](integration-guide.md) - Setup and configuration
- [FastMCP Documentation](https://fastmcp.wiki/) - Framework documentation
- [MCP Protocol Specification](https://modelcontextprotocol.io/) - Protocol details

---

**Architecture Version:** 1.0  
**Last Reviewed:** {Date}  
**Next Review:** {Date}


