# Zed Extension Template for MCP Servers

**Template for adding Zed IDE extensions to MCP servers**

This template provides a standardized way to add Zed IDE extension support to any MCP server. Even if your MCP server is experimental or "wild", having a Zed extension makes it discoverable and usable within Zed's AI assistant.

## 🚀 Quick Start

### For Individual Repos

1. **Copy template files** to your MCP repo root:
   ```bash
   cp extension.toml Cargo.toml src/lib.rs build.ps1 /path/to/your-mcp-repo/
   ```

2. **Customize placeholders**:
   - `{{PROJECT_SLUG}}` → your-repo-name
   - `{{PROJECT_NAME}}` → YourProjectName
   - `{{DISPLAY_NAME}}` → "Your Tools Display Name"
   - `{{PROJECT_DESCRIPTION}}` → "Description of your MCP server"

3. **Build and test**:
   ```powershell
   .\build.ps1
   # Then install in Zed: Extensions → Install Dev Extension
   ```

### Automated Rollout (Multiple Repos)

Use the deployment script to add Zed extensions to multiple MCP repos:

```powershell
# Deploy to specific repos
.\deploy-to-mcp-repos.ps1 -Repos "unity3d-mcp", "advanced-memory-mcp"

# Deploy to all configured repos
.\deploy-to-mcp-repos.ps1

# Test mode (no git operations)
.\deploy-to-mcp-repos.ps1 -TestOnly
```

## 🎯 Benefits of Zed Extensions

### Even for "Wild" MCP Servers

- **Standardized Interface**: Consistent discovery in Zed's AI assistant
- **Sandbox Security**: Extensions run in isolated Wasm environment
- **Easy Testing**: Users can try experimental tools without complex setup
- **Community Exposure**: Makes your tools discoverable in Zed ecosystem
- **Future-Proof**: Works with Zed's evolving extension API

### Technical Advantages

- **Cross-Platform**: Single extension works on macOS, Linux, Windows
- **Performance**: Native-speed execution with minimal overhead
- **Memory Safe**: Rust's ownership system prevents crashes
- **Version Independent**: Extensions work across Zed versions

## 📋 Configured MCP Servers

The deployment script includes configurations for these MCP servers:

| Repository | Display Name | Description |
|------------|--------------|-------------|
| `unity3d-mcp` | Unity Development Tools | Unity game development and asset pipeline |
| `advanced-memory-mcp` | Knowledge Base Tools | Personal knowledge graph and research management |
| `blender-mcp` | Blender 3D Tools | 3D modeling, animation, and rendering |
| `gimp-mcp` | GIMP Image Tools | Professional image editing and manipulation |
| `resonite-mcp` | Resonite VR Tools | Social VR world creation and scripting |
| `vrchat-mcp` | VRChat Development | VRChat world and avatar development |
| `plex-mcp` | Plex Media Tools | Media library management and playback control |
| `calibre-mcp` | Calibre Library Tools | Ebook library organization and conversion |
| `filesystem-mcp` | File System Tools | Advanced file and directory management |
| `ocr-mcp` | Document OCR Tools | Multi-engine OCR and document analysis |

## 🔧 Customization

### Adding New MCP Servers

Edit the `$MCP_CONFIGS` hashtable in `deploy-to-mcp-repos.ps1`:

```powershell
"MCP_CONFIGS = @{
    'your-mcp-repo' = @{
        name = 'Your MCP Server'
        description = 'What your server does'
        display_name = 'Tools Display Name'
    }
}
```

### Modifying Templates

- **extension.toml**: Zed extension manifest
- **Cargo.toml**: Rust project configuration
- **src/lib.rs**: Bridge logic (rarely needs changes)
- **build.ps1**: Build automation script

## 🧪 Testing

### Local Testing

1. Build extension: `.\build.ps1`
2. Install in Zed: `Cmd+Shift+P` → "zed: extensions" → "Install Dev Extension"
3. Check AI assistant panel for your server
4. Test tool calls work correctly

### CI/CD Testing

The template includes GitHub Actions for automated building:

```yaml
- run: cargo build --release --target wasm32-wasip1
```

## 🤝 Contributing to Zed

Once your extensions work locally:

1. **Fork** `zed-industries/extensions`
2. **Add submodule**: `git submodule add https://github.com/yourusername/your-mcp-repo extensions/your-extension`
3. **Submit PR** with documentation
4. **Community review** and Zed team audit

## 📚 Resources

- [Zed Extension Documentation](https://github.com/zed-industries/zed/tree/main/docs)
- [MCP Specification](https://modelcontextprotocol.io/specification)
- [Zed MCP Extensions Guide](../../mcp-central-docs/integrations/zed/ZED_MCP_EXTENSIONS_GUIDE.md)

---

**Template for**: Zed IDE MCP extension rollout
**Purpose**: Democratize MCP server access through Zed's AI assistant
**Impact**: 30+ MCP servers discoverable in Zed IDE

*Even "wild" MCP servers deserve Zed extensions - standardized discovery with sandboxed security.*
