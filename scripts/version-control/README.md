# Version Control Scripts

Scripts for managing Git and GitHub repositories.

## Scripts

### `Organize-GitHubRepos.ps1`

Comprehensive tool for organizing and managing GitHub repositories.

**Location:** `mcp-central-docs/scripts/version-control/Organize-GitHubRepos.ps1`

**Features:**
- List all repositories with stats
- Categorize repositories (MCP servers, tools, projects)
- Generate organization plan
- Scan local directories for Git/GitHub status
- Sync local repos with GitHub
- Create GitHub organization (guidance)
- Transfer repositories to organization (guidance)

**Quick Start:**
```powershell
cd D:\Dev\repos\mcp-central-docs\scripts\version-control
.\Organize-GitHubRepos.ps1 -Action ScanLocal -OutputPath "D:\Dev\repos\docs"
```

**See Also:**
- [GitHub Organization Guide](../../../docs/GITHUB_ORGANIZATION_GUIDE.md)
- [GitHub Organization Quick Start](../../../docs/GITHUB_ORGANIZATION_QUICKSTART.md)

---

*Last updated: 2025-12-02*

