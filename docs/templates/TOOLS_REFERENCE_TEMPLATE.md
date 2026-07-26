# Tool Reference - {Project Name}

**For:** Developers, Advanced Users  
**Purpose:** Complete API documentation for all tools  
**Last Updated:** {Date}

---

## 📚 Tool Index

| Tool | Category | Description |
|------|----------|-------------|
| [{tool1}](#tool1) | {Category} | {Brief description} |
| [{tool2}](#tool2) | {Category} | {Brief description} |
| [{tool3}](#tool3) | {Category} | {Brief description} |

**Total Tools:** {count}  
**Tool Mode:** {Production/Testing/Portmanteau}

---

## 🎯 Tool Categories

### {Category 1}
- [{tool1}](#tool1) - {Description}
- [{tool2}](#tool2) - {Description}

### {Category 2}
- [{tool3}](#tool3) - {Description}
- [{tool4}](#tool4) - {Description}

---

## 📖 Tool Documentation

### {tool1}

**Category:** {Category}  
**Complexity:** {Simple/Medium/Complex}  
**Async:** Yes

#### Description

{Comprehensive description of what the tool does and when to use it}

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `param1` | `str` | ✅ Yes | - | {Description} |
| `param2` | `int` | ⬜ No | `10` | {Description} |
| `param3` | `bool` | ⬜ No | `false` | {Description} |

#### Returns

**Type:** `dict[str, Any]`

**Success Response:**
```json
{
  "success": true,
  "data": {
    "field1": "value",
    "field2": 123
  },
  "message": "Operation completed successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message here",
  "error_code": "ERROR_CODE"
}
```

#### Examples

**Example 1: Basic Usage**

```bash
# Ask Claude:
"{Natural language query that uses this tool}"

# What happens:
# 1. Claude calls tool1(param1="value")
# 2. Tool processes request
# 3. Returns result
```

**Example Response:**
```json
{
  "success": true,
  "data": {"result": "example output"}
}
```

**Example 2: Advanced Usage**

```bash
# Ask Claude:
"{More complex query}"

# With specific parameters:
# param1="advanced", param2=20, param3=true
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "result": "advanced output",
    "metadata": {"count": 20}
  }
}
```

#### Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `INVALID_INPUT` | Invalid parameter value | Check parameter format and constraints |
| `NOT_FOUND` | Resource not found | Verify resource exists |
| `TIMEOUT` | Operation timed out | Increase timeout or retry |

#### Notes

- ⚠️ {Important note 1}
- 💡 {Tip or best practice}
- 🔒 {Security consideration}

#### Related Tools

- [{tool2}](#tool2) - {How they relate}
- [{tool3}](#tool3) - {How they relate}

---

### {tool2}

**Category:** {Category}  
**Complexity:** {Simple/Medium/Complex}  
**Async:** Yes

#### Description

{Comprehensive description}

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `action` | `Literal["op1", "op2", "op3"]` | ✅ Yes | - | Operation to perform |
| `identifier` | `str` | ⬜ No | `None` | Resource identifier |
| `options` | `dict` | ⬜ No | `{}` | Additional options |

**Action Values:**
- `"op1"` - {Description of operation 1}
- `"op2"` - {Description of operation 2}
- `"op3"` - {Description of operation 3}

#### Returns

**Type:** `dict[str, Any]`

Returns operation-specific results. See individual operation documentation below.

#### Operations

##### Operation: `op1`

**Purpose:** {What this operation does}

**Required Parameters:**
- `action`: `"op1"`
- `identifier`: Required for this operation

**Example:**
```bash
# Ask Claude:
"{Query that triggers op1}"
```

**Response:**
```json
{
  "success": true,
  "operation": "op1",
  "data": {"result": "op1 output"}
}
```

##### Operation: `op2`

**Purpose:** {What this operation does}

**Required Parameters:**
- `action`: `"op2"`
- `options`: Recommended for this operation

**Example:**
```bash
# Ask Claude:
"{Query that triggers op2}"
```

**Response:**
```json
{
  "success": true,
  "operation": "op2",
  "data": {"result": "op2 output"}
}
```

##### Operation: `op3`

**Purpose:** {What this operation does}

**Required Parameters:**
- `action`: `"op3"`

**Example:**
```bash
# Ask Claude:
"{Query that triggers op3}"
```

**Response:**
```json
{
  "success": true,
  "operation": "op3",
  "data": {"result": "op3 output"}
}
```

#### Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `INVALID_OPERATION` | Invalid action specified | Use one of: op1, op2, op3 |
| `MISSING_PARAM` | Required parameter missing | Check operation requirements |

#### Notes

- 💡 This is a **portmanteau tool** - it consolidates multiple operations
- 🔍 Claude discovers all operations automatically via `Literal` types
- ⚡ Use specific operations for better performance

#### Related Tools

- See individual operations above for related functionality

---

## 🔍 Tool Discovery

### How Claude Discovers Tools

Claude Desktop automatically discovers all available tools and their parameters through the MCP protocol. The tool list and parameter types are provided at startup.

### Literal Types for Operations

For portmanteau tools with action parameters, we use `Literal` types:

```python
action: Literal["op1", "op2", "op3"]
```

This creates an enum in the JSON schema, allowing Claude to discover all available operations without needing separate documentation.

### Tool Modes

**Production Mode:** (Default)
- Consolidated portmanteau tools
- Clean, organized tool list
- Recommended for end users

**Testing Mode:** (Development)
- Individual tools exposed
- Useful for testing and development
- Enable via environment variable

---

## 📝 Usage Patterns

### Simple Operations

For straightforward tasks, use direct tool calls:

```bash
# Direct, single-purpose operation
Ask Claude: "{Simple query}"
```

### Complex Workflows

For multi-step operations, chain tool calls:

```bash
# Step 1
Ask Claude: "{Query for step 1}"

# Step 2 (using results from step 1)
Ask Claude: "{Query for step 2 with context}"

# Step 3
Ask Claude: "{Final query}"
```

### Batch Operations

For multiple similar operations:

```bash
# Process multiple items
Ask Claude: "{Query to process items A, B, C}"

# Claude will automatically:
# 1. Call tool for item A
# 2. Call tool for item B
# 3. Call tool for item C
# 4. Aggregate results
```

---

## ⚡ Performance Tips

### Optimization Strategies

1. **Use Specific Parameters**
   - More specific → Faster results
   - Example: Use `identifier="exact-match"` instead of searching

2. **Batch When Possible**
   - Single call for multiple items
   - Reduces overhead

3. **Cache Results**
   - Tools may cache frequently accessed data
   - Subsequent calls are faster

### Rate Limits

| Operation | Limit | Period |
|-----------|-------|--------|
| {Operation 1} | {count} requests | {period} |
| {Operation 2} | {count} requests | {period} |

---

## 🔒 Security Considerations

### Authentication

All tools require valid API keys configured in Claude Desktop settings.

### Authorization

Tools respect the permissions of the configured API key:
- Read operations: Require read permissions
- Write operations: Require write permissions
- Admin operations: Require admin permissions

### Data Privacy

- Tools do not store sensitive data
- API keys are managed by Claude Desktop
- Logs may contain operation details (no sensitive data)

---

## 🧪 Testing

### Manual Testing

```bash
# 1. Enable debug mode
# Set DEBUG=true in Claude Desktop config

# 2. Test each tool
# Ask Claude to use specific tools

# 3. Check logs
# Review Claude Desktop logs for errors
```

### Automated Testing

```bash
# Run test suite
uv run pytest tests/test_tools/

# Test specific tool
uv run pytest tests/test_tools/test_{tool_name}.py -v

# With coverage
uv run pytest --cov=src/{package}/tools
```

---

## 📚 Further Reading

- [Integration Guide](integration-guide.md) - Setup and configuration
- [Architecture](architecture.md) - System design
- [Examples](examples/) - Usage examples
- [Troubleshooting](troubleshooting.md) - Common issues

---

## 🔄 Version History

### Current Version

**Version:** {version}  
**Release Date:** {date}  
**Changes:** See [CHANGELOG.md](../CHANGELOG.md)

### API Stability

- ✅ **Stable:** Core tools and parameters
- ⚠️ **Beta:** New experimental features
- 🔧 **Deprecated:** Tools scheduled for removal (see notes)

---

**Reference Version:** 1.0  
**Last Updated:** {Date}  
**Next Review:** {Date}

