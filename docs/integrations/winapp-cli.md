# Microsoft WinApp CLI Integration

## Overview

Microsoft WinApp CLI is a command-line interface for Windows app development that simplifies the process of managing Windows SDKs, packaging, app identity, manifests, certificates, and build tools for any app framework.

**Homepage**: https://github.com/microsoft/winappCli
**Latest Version**: Public Preview (v0.1.1-gui available)
**License**: MIT
**Release Date**: January 22, 2026

## Integration with MCP Ecosystem

WinApp CLI is particularly valuable for MCP servers that need to:

- **Package Windows applications** - Create MSIX packages for deployment
- **Manage app identity** - Add identity for debugging Windows APIs
- **Handle Windows SDKs** - Automated setup and management
- **Support cross-platform development** - Bridge web/native app development

### Relevant MCP Servers

- **advanced-memory-mcp**: Could integrate WinApp CLI for Windows app knowledge management
- **blender-mcp**: For Windows deployment of 3D applications
- **gimp-mcp**: For Windows packaging of image processing tools
- **robotics-mcp**: For Windows deployment of robotics control interfaces
- **virtualization-mcp**: For Windows VM and container app packaging

## Supported Frameworks and Platforms

### Development Frameworks
- **Electron** - Cross-platform desktop apps
- **.NET/Win32** - Native Windows applications
- **CMake** - C/C++ build system
- **Rust** - Systems programming with Windows APIs
- **Dart/Flutter** - Cross-platform UI framework
- **Node.js** - JavaScript/TypeScript applications
- **Python** - Scripting and automation tools

### Target Platforms
- **Windows 10/11** - Primary target platform
- **Windows App SDK** - Modern Windows APIs
- **MSIX Packaging** - Microsoft Store and sideloading
- **Win32 APIs** - Legacy Windows integration

## Installation

### WinGet (Recommended)

```powershell
winget install Microsoft.winappcli --source winget
```

### NPM (for Electron projects)

```bash
npm install @microsoft/winappcli --save-dev
```

### GitHub Actions/Azure DevOps

```yaml
- name: Setup WinApp CLI
  uses: microsoft/setup-WinAppCli@v1
```

### Manual Installation

1. Download from [GitHub Releases](https://github.com/microsoft/WinAppCli/releases/latest)
2. Extract to a directory in PATH
3. Verify installation: `winapp --help`

### CI/CD Integration

For automated pipelines:

```yaml
# GitHub Actions
- name: Setup Windows App Development CLI
  uses: microsoft/setup-WinAppCli@v1

# Azure DevOps
- task: Microsoft.setup-winapp-cli.setup-winapp-cli.SetupWinAppCli@1
```

## Core Commands and Usage

### Project Initialization

```bash
# Initialize project with Windows SDK
winapp init

# Restore packages and dependencies
winapp restore

# Update to latest SDK versions
winapp update
```

### App Packaging

```bash
# Create MSIX package from directory
winapp package MyApp/ --output MyApp.msix

# Package with specific options
winapp package MyApp/ --output MyApp.msix --publisher "CN=MyCompany"
```

### Debug Identity Management

```bash
# Add temporary identity for debugging
winapp create-debug-identity --name "MyApp.Debug"

# For Electron apps specifically
npx winapp node add-electron-debug-identity

# Remove debug identity
npx winapp node clear-electron-debug-identity
```

### Manifest Management

```bash
# Generate AppxManifest.xml
winapp manifest generate --name "MyApp" --version "1.0.0"

# Validate manifest
winapp manifest validate AppxManifest.xml
```

### Certificate Management

```bash
# Generate development certificate
winapp cert generate --subject "CN=MyCompany"

# Install certificate to local machine store
winapp cert install MyCert.pfx
```

### Signing

```bash
# Sign MSIX package
winapp sign MyApp.msix --cert MyCert.pfx

# Sign executable
winapp sign MyApp.exe --cert MyCert.pfx
```

## MCP Tool Integration Examples

### Basic App Packaging Tool

```python
# Example MCP tool for Windows app packaging
@winapp_mcp.tool()
async def package_windows_app(
    source_path: str,
    output_name: str,
    publisher: str = None,
    version: str = "1.0.0"
) -> dict:
    """
    Package a Windows application using WinApp CLI.

    Args:
        source_path: Path to application source directory
        output_name: Name for the output MSIX file
        publisher: Publisher certificate subject (optional)
        version: Application version

    Returns:
        Packaging result with paths and status
    """
    try:
        # Generate manifest
        manifest_cmd = [
            "winapp", "manifest", "generate",
            "--name", output_name,
            "--version", version
        ]
        if publisher:
            manifest_cmd.extend(["--publisher", publisher])

        result = await run_subprocess(manifest_cmd, cwd=source_path)

        # Create package
        package_cmd = [
            "winapp", "package", source_path,
            "--output", f"{output_name}.msix"
        ]

        result = await run_subprocess(package_cmd)

        return {
            "success": True,
            "package_path": f"{output_name}.msix",
            "manifest_path": f"{source_path}/AppxManifest.xml"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

### Electron App Development Tool

```python
# MCP tool for Electron Windows development
@electron_mcp.tool()
async def setup_electron_windows(
    project_path: str,
    enable_debug_identity: bool = True,
    create_addon: bool = False
) -> dict:
    """
    Setup Electron app for Windows development with WinApp CLI.

    Args:
        project_path: Path to Electron project
        enable_debug_identity: Add debug identity for Windows APIs
        create_addon: Generate native addon template

    Returns:
        Setup results and generated files
    """
    results = {}

    try:
        # Initialize Windows SDK
        init_result = await run_subprocess(["winapp", "init"], cwd=project_path)
        results["init"] = init_result

        if enable_debug_identity:
            # Add debug identity for Electron
            debug_result = await run_subprocess(
                ["npx", "winapp", "node", "add-electron-debug-identity"],
                cwd=project_path
            )
            results["debug_identity"] = debug_result

        if create_addon:
            # Create C# addon template
            addon_result = await run_subprocess(
                ["npx", "winapp", "node", "create-addon", "--language", "csharp"],
                cwd=project_path
            )
            results["addon"] = addon_result

        return {
            "success": True,
            "results": results,
            "project_path": project_path
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

### CI/CD Pipeline Integration

```python
# MCP tool for automated Windows app builds
@ci_cd_mcp.tool()
async def build_windows_app_pipeline(
    repo_url: str,
    framework: str = "electron",
    output_format: str = "msix"
) -> dict:
    """
    Complete CI/CD pipeline for Windows app using WinApp CLI.

    Args:
        repo_url: Git repository URL
        framework: App framework (electron, dotnet, rust, etc.)
        output_format: Output format (msix, exe, etc.)

    Returns:
        Build results and artifacts
    """
    # Clone repository
    clone_result = await run_subprocess(["git", "clone", repo_url])

    # Setup WinApp CLI
    setup_result = await run_subprocess(["winget", "install", "Microsoft.winappcli"])

    # Initialize project
    init_result = await run_subprocess(["winapp", "init"])

    # Framework-specific setup
    if framework == "electron":
        await run_subprocess(["npm", "install"])
        await run_subprocess(["npx", "winapp", "node", "add-electron-debug-identity"])

    # Build and package
    build_result = await run_subprocess(["winapp", "package", ".", f"--output app.{output_format}"])

    return {
        "success": True,
        "artifacts": [f"app.{output_format}"],
        "framework": framework,
        "build_steps": ["clone", "setup", "init", "build", "package"]
    }
```

## Advanced Usage Patterns

### Multi-Framework Development

```bash
# Setup for different frameworks
winapp init --framework electron
winapp init --framework dotnet
winapp init --framework rust
```

### Custom Manifest Generation

```bash
# Generate manifest with custom capabilities
winapp manifest generate \
    --name "MyApp" \
    --capabilities "internetClient,documentsLibrary" \
    --protocol "myapp" \
    --file-type ".myext"
```

### Certificate Chain Management

```bash
# Create certificate chain for production
winapp cert generate --subject "CN=MyCompany" --chain
winapp cert export --format p12 --password "securepass"
```

### Batch Processing

```bash
# Package multiple apps
for app in apps/*/; do
    winapp package "$app" --output "${app%/}.msix"
done
```

## Integration with Development Workflows

### VS Code/Cursor Integration

Create tasks.json for automated workflows:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "WinApp: Initialize Project",
            "type": "shell",
            "command": "winapp",
            "args": ["init"],
            "group": "build"
        },
        {
            "label": "WinApp: Package App",
            "type": "shell",
            "command": "winapp",
            "args": ["package", ".", "--output", "app.msix"],
            "group": "build"
        },
        {
            "label": "WinApp: Add Debug Identity",
            "type": "shell",
            "command": "npx",
            "args": ["winapp", "node", "add-electron-debug-identity"],
            "group": "test"
        }
    ]
}
```

### GitHub Actions Workflow

```yaml
name: Windows App Build

on: [push, pull_request]

jobs:
  build:
    runs-on: windows-latest

    steps:
    - uses: actions/checkout@v4

    - name: Setup WinApp CLI
      uses: microsoft/setup-WinAppCli@v1

    - name: Initialize Project
      run: winapp init

    - name: Build App
      run: npm run build  # or dotnet build, cargo build, etc.

    - name: Package App
      run: winapp package . --output app.msix

    - name: Upload Artifact
      uses: actions/upload-artifact@v4
      with:
        name: windows-app
        path: app.msix
```

## Troubleshooting

### Common Issues

1. **"winapp command not found"**
   - Ensure WinApp CLI is installed and in PATH
   - Try `winget install Microsoft.winappcli` or manual installation

2. **"Failed to initialize Windows SDK"**
   - Ensure Windows 10/11 with developer mode enabled
   - Check Windows SDK installation
   - Run as administrator for system changes

3. **"Manifest validation failed"**
   - Check AppxManifest.xml syntax
   - Verify package identity format
   - Ensure capabilities are properly declared

4. **"Certificate not trusted"**
   - Install certificate to Trusted Root store
   - Use `winapp cert install --store root`
   - For development, use self-signed certificates

5. **"MSIX packaging failed"**
   - Ensure all required files are present
   - Check file paths in manifest
   - Verify publisher certificate is valid

### Debug Mode Issues

```bash
# Enable detailed logging
winapp --verbose package . --output app.msix

# Check Windows Event Viewer
# Application and Services Logs > Microsoft > Windows > AppxPackaging

# Validate manifest manually
winapp manifest validate AppxManifest.xml
```

### Performance Optimization

- **Incremental builds**: Use `winapp restore` instead of full `init`
- **Parallel packaging**: Package independent components separately
- **Cache certificates**: Reuse development certificates across builds
- **Selective updates**: Use `winapp update --component sdk` for targeted updates

## Technical Architecture

### Components

- **CLI Core**: Cross-platform .NET command-line application
- **Windows SDK Integration**: Automated setup and management
- **MSIX Packaging Engine**: Native Windows packaging technology
- **Certificate Management**: Windows Certificate Store integration
- **Manifest Generator**: XML-based app manifest creation

### Security Model

- **Code Signing**: Enforces signed packages for deployment
- **Certificate Validation**: Verifies certificate chains and trust
- **App Identity**: Isolated app execution with identity-based security
- **Capability Declaration**: Explicit permission model for Windows APIs

### File Structure

```
project/
├── AppxManifest.xml          # Generated app manifest
├── app.msix                  # Packaged application
├── certificates/             # Development certificates
│   ├── debug.pfx
│   └── release.pfx
└── build/                    # Build artifacts
    ├── assets/
    └── resources/
```

## Version Compatibility

- **Windows**: 10 version 1903+ (19H1) or Windows 11
- **Windows App SDK**: 1.0+ (automatically managed)
- **.NET**: 6.0+ for CLI itself
- **Node.js**: 16+ for Electron integration
- **Visual Studio**: 2019+ for development
- **MSIX**: Windows 10 1709+ support

## Ecosystem Integration

### Related Tools

- **Windows App SDK**: Modern Windows development platform
- **MSIX Packaging Tool**: Advanced packaging features
- **Windows Terminal**: Enhanced command-line experience
- **Visual Studio**: Full IDE integration
- **WinUI**: Modern UI framework for Windows

### MCP Server Synergies

- **Package management**: Integrate with existing package tools
- **Certificate lifecycle**: Automate cert management across projects
- **Build orchestration**: Coordinate with other build tools
- **Deployment automation**: Streamline Windows app distribution

## Development and Contribution

### Building from Source

```bash
# Clone repository
git clone https://github.com/microsoft/winappCli.git
cd winappCli

# Build CLI
.\scripts\build-cli.ps1

# Build GUI (experimental)
.\scripts\build-gui.ps1
```

### Extending WinApp CLI

The CLI supports plugins and extensions:

```csharp
// Example plugin interface
public interface IWinAppPlugin
{
    string Name { get; }
    Task ExecuteAsync(string[] args);
}
```

### Testing

```bash
# Run unit tests
dotnet test

# Run integration tests
.\scripts\run-integration-tests.ps1

# Test packaging scenarios
.\scripts\test-packaging.ps1
```

## Future Roadmap

### Planned Features

- **Enhanced Node.js Support**: Improved Electron and NW.js integration
- **Python Packaging**: Native Python app packaging support
- **Cross-platform Development**: macOS and Linux target support
- **Advanced Security**: Hardware-backed certificates and secure boot
- **AI Integration**: Windows AI API integration for intelligent apps
- **Cloud Integration**: Azure DevOps and GitHub integration improvements

### Experimental Features

- **GUI Application**: Drag-and-drop interface for CLI operations
- **Visual Studio Extension**: IDE integration for seamless development
- **Container Support**: Windows containers and WSL integration
- **Remote Development**: SSH-based remote Windows development

## Support and Resources

### Official Resources

- **GitHub Repository**: https://github.com/microsoft/winappCli
- **Documentation**: https://github.com/microsoft/winappCli/tree/main/docs
- **Issues**: https://github.com/microsoft/winappCli/issues
- **Discussions**: https://github.com/microsoft/winappCli/discussions

### Community Support

- **Microsoft Developer Forums**: Windows App Development
- **Stack Overflow**: Tag `windows-app-sdk` or `msix`
- **Reddit**: r/windowsdev, r/UWP

### Getting Help

1. Check existing issues on GitHub
2. Review documentation and samples
3. Create detailed issue with reproduction steps
4. Include environment information (Windows version, framework, etc.)

## Migration from Legacy Tools

### From Desktop App Converter

```bash
# Old method (deprecated)
DesktopAppConverter.exe -Installer "setup.exe" -Destination "output" -PackageName "MyApp"

# New WinApp CLI method
winapp package setup.exe --output MyApp.msix --installer
```

### From MakeAppx.exe

```bash
# Old method
MakeAppx.exe pack -d "input" -p "app.msix"

# New WinApp CLI method
winapp package input/ --output app.msix
```

### From SignTool.exe

```bash
# Old method
signtool.exe sign /f cert.pfx /p password app.msix

# New WinApp CLI method
winapp sign app.msix --cert cert.pfx
```

---

*Last updated: January 2026*
*WinApp CLI version: Public Preview*
*Windows App SDK: Latest available*
