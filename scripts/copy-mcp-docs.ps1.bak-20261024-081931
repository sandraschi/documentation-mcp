# Copy MCP Server Documentation Script

# Main MCP Servers
$mcpServers = @(
    "advanced-memory-mcp",
    "avatarmcp", 
    "blender-mcp",
    "calibremcp",
    "database-operations-mcp",
    "davinci-resolve-mcp",
    "dockermcp",
    "filesystem-mcp",
    "gimp-mcp",
    "handbrakemcp",
    "immichmcp",
    "notepadpp-mcp",
    "obsidianmcp",
    "obs-studio-mcp",
    "oscmcp",
    "plexmcp",
    "pywinauto-mcp",
    "qbtmcp",
    "reaper-mcp",
    "ring-mcp",
    "rustdeskmcp",
    "suno-mcp",
    "system-admin-mcp",
    "tailscale-mcp",
    "tapo-camera-mcp",
    "unity3d-mcp",
    "virtualdj-mcp",
    "virtualization-mcp",
    "vrchat-mcp",
    "vroidstudio-mcp",
    "web-development-mcp",
    "windows-operations-mcp",
    "winrar-mcp"
)

# Other Projects (non-MCP)
$otherProjects = @(
    "anthropic-skills",
    "autohotkey-test",
    "backup-scripts",
    "basic-memory",
    "claude-config-mcp",
    "ednaficator",
    "fastsearch-mcp",
    "fullstack-demo",
    "fullstack-demo-backup",
    "gtfs-mcp",
    "hasleo-backup-mcp",
    "komga",
    "llm-txt-mcp",
    "local-llm-mcp",
    "mcp-collection",
    "mcp-commons",
    "mcp-config-backup",
    "mcp-filesystem",
    "mcp-hello-world-server",
    "mcp-server-template",
    "mcp-studio",
    "MCP-SuperAssistant",
    "mcp-test-app-server",
    "mcp-test-suite",
    "mcp-wrapper-poc",
    "mini-testapp",
    "miniclaude",
    "myscripts",
    "mywienerlinien",
    "nest-protect-mcp",
    "notion-mcp",
    "pdf-export-backup",
    "robotics",
    "scrapes",
    "scripts",
    "temp",
    "templates",
    "tools",
    "unitree-robotics",
    "Unity_TransparentWindowManager",
    "uv-install",
    "windsurf-automation",
    "zed"
)

# Create directories for MCP servers
foreach ($server in $mcpServers) {
    $dir = "D:\Dev\repos\mcp-central-docs\projects\mcp-servers\$server"
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
    }
    
    # Copy README.md
    $readme = "D:\Dev\repos\$server\README.md"
    if (Test-Path $readme) {
        Copy-Item $readme "$dir\README.md" -Force
        Write-Host "Copied README.md for $server"
    }
    
    # Copy CHANGELOG.md
    $changelog = "D:\Dev\repos\$server\CHANGELOG.md"
    if (Test-Path $changelog) {
        Copy-Item $changelog "$dir\CHANGELOG.md" -Force
        Write-Host "Copied CHANGELOG.md for $server"
    }
}

# Create directories for other projects
foreach ($project in $otherProjects) {
    $dir = "D:\Dev\repos\mcp-central-docs\projects\other-projects\$project"
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
    }
    
    # Copy README.md
    $readme = "D:\Dev\repos\$project\README.md"
    if (Test-Path $readme) {
        Copy-Item $readme "$dir\README.md" -Force
        Write-Host "Copied README.md for $project"
    }
    
    # Copy CHANGELOG.md
    $changelog = "D:\Dev\repos\$project\CHANGELOG.md"
    if (Test-Path $changelog) {
        Copy-Item $changelog "$dir\CHANGELOG.md" -Force
        Write-Host "Copied CHANGELOG.md for $project"
    }
}

Write-Host "Documentation copy completed!"
