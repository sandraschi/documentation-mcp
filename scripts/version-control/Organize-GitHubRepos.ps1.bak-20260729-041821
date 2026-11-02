<#
.SYNOPSIS
    Organize and manage GitHub repositories for @sandraschi

.DESCRIPTION
    Comprehensive tool for organizing GitHub repositories:
    - List all repositories with stats
    - Categorize repositories (MCP servers, tools, projects)
    - Generate organization plan
    - Create GitHub organization (optional)
    - Transfer repositories to organization (optional)
    - Update repository metadata
    - Generate documentation

.PARAMETER Action
    Action to perform: List, Analyze, Plan, CreateOrg, Transfer, UpdateDocs, SyncLocal, ScanLocal

.PARAMETER Username
    GitHub username (default: sandraschi)

.PARAMETER OrgName
    Organization name (for CreateOrg/Transfer actions)

.PARAMETER Category
    Filter by category: MCP, Tools, Projects, All

.PARAMETER OutputPath
    Path for output files (default: current directory)

.EXAMPLE
    .\Organize-GitHubRepos.ps1 -Action List
    # List all repositories

.EXAMPLE
    .\Organize-GitHubRepos.ps1 -Action Analyze -Category MCP
    # Analyze MCP server repositories

.EXAMPLE
    cd D:\Dev\repos\mcp-central-docs\scripts\version-control
    .\Organize-GitHubRepos.ps1 -Action Plan -OutputPath "D:\Dev\repos\docs"
    # Generate organization plan

.EXAMPLE
    cd D:\Dev\repos\mcp-central-docs\scripts\version-control
    .\Organize-GitHubRepos.ps1 -Action ScanLocal -OutputPath "D:\Dev\repos\docs"
    # Scan local directories for Git/GitHub status
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('List', 'Analyze', 'Plan', 'CreateOrg', 'Transfer', 'UpdateDocs', 'SyncLocal', 'ScanLocal')]
    [string]$Action,
    
    [string]$Username = "sandraschi",
    
    [string]$OrgName = "sandraschi-mcp",
    
    [ValidateSet('MCP', 'Tools', 'Projects', 'All')]
    [string]$Category = "All",
    
    [string]$OutputPath = "."
)

$ErrorActionPreference = "Stop"

# Check for GitHub CLI
function Test-GitHubCLI {
    try {
        $null = gh --version
        return $true
    } catch {
        return $false
    }
}

# Get repositories using GitHub CLI
function Get-GitHubRepositories {
    param([string]$User)
    
    if (-not (Test-GitHubCLI)) {
        Write-Warning "GitHub CLI (gh) not found. Install from: https://cli.github.com/"
        Write-Host "Attempting to use GitHub API directly..." -ForegroundColor Yellow
        
        # Fallback: Use GitHub API (requires token)
        $token = $env:GITHUB_TOKEN
        if (-not $token) {
            throw "GitHub CLI not found and GITHUB_TOKEN not set. Please install gh CLI or set GITHUB_TOKEN environment variable."
        }
        
        $headers = @{
            "Authorization" = "token $token"
            "Accept" = "application/vnd.github.v3+json"
        }
        
        $repos = @()
        $page = 1
        do {
            $response = Invoke-RestMethod -Uri "https://api.github.com/users/$User/repos?per_page=100&page=$page" -Headers $headers
            $repos += $response
            $page++
        } while ($response.Count -eq 100)
        
        return $repos
    }
    
    # Use GitHub CLI
    $json = gh repo list $User --json name,description,isPrivate,isArchived,isFork,url,stargazerCount,primaryLanguage,updatedAt,createdAt,topics --limit 1000
    return $json | ConvertFrom-Json
}

# Categorize repositories
function Get-RepositoryCategory {
    param([object]$Repo)
    
    $name = $Repo.name
    $desc = $Repo.description
    
    # MCP Servers
    if ($name -match "-mcp$|^mcp-|mcp$" -or $desc -match "MCP|Model Context Protocol") {
        return "MCP"
    }
    
    # Tools
    if ($name -match "tool|util|script|helper|manager") {
        return "Tools"
    }
    
    # Projects
    return "Projects"
}

# List repositories
function Show-RepositoryList {
    param([array]$Repos, [string]$FilterCategory)
    
    Write-Host "`n" -NoNewline
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "GitHub Repositories - @$Username" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host ""
    
    $categories = @{
        "MCP" = @()
        "Tools" = @()
        "Projects" = @()
    }
    
    foreach ($repo in $Repos) {
        $cat = Get-RepositoryCategory -Repo $repo
        $categories[$cat] += $repo
    }
    
    $total = $Repos.Count
    Write-Host "Total Repositories: $total" -ForegroundColor Green
    Write-Host "  MCP Servers: $($categories['MCP'].Count)" -ForegroundColor Yellow
    Write-Host "  Tools: $($categories['Tools'].Count)" -ForegroundColor Yellow
    Write-Host "  Projects: $($categories['Projects'].Count)" -ForegroundColor Yellow
    Write-Host ""
    
    $displayCategories = if ($FilterCategory -eq "All") { @("MCP", "Tools", "Projects") } else { @($FilterCategory) }
    
    foreach ($cat in $displayCategories) {
        if ($categories[$cat].Count -eq 0) { continue }
        
        Write-Host "`n[$cat] Repositories" -ForegroundColor Cyan
        Write-Host ("-" * 80) -ForegroundColor DarkGray
        
        
        foreach ($repo in $categories[$cat] | Sort-Object name) {
            $lang = if ($repo.primaryLanguage) { $repo.primaryLanguage.name } else { "N/A" }
            $stars = $repo.stargazerCount
            $private = if ($repo.isPrivate) { "[Private]" } else { "[Public]" }
            $archived = if ($repo.isArchived) { "[Archived]" } else { "" }
            
            Write-Host ("  {0,-35} {1,-15} â­{2,-5} {3} {4}" -f $repo.name, $lang, $stars, $private, $archived)
            if ($repo.description) {
                Write-Host ("    {0}" -f $repo.description) -ForegroundColor DarkGray
            }
        }
    }
}

# Analyze repositories
function Analyze-Repositories {
    param([array]$Repos)
    
    Write-Host "`n" -NoNewline
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "Repository Analysis" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host ""
    
    $stats = @{
        Total = $Repos.Count
        Public = ($Repos | Where-Object { -not $_.isPrivate }).Count
        Private = ($Repos | Where-Object { $_.isPrivate }).Count
        Archived = ($Repos | Where-Object { $_.isArchived }).Count
        Forks = ($Repos | Where-Object { $_.isFork }).Count
        TotalStars = ($Repos | Measure-Object -Property stargazerCount -Sum).Sum
    }
    
    $categories = @{
        "MCP" = @()
        "Tools" = @()
        "Projects" = @()
    }
    
    foreach ($repo in $Repos) {
        $cat = Get-RepositoryCategory -Repo $repo
        $categories[$cat] += $repo
    }
    
    Write-Host "Statistics:" -ForegroundColor Green
    Write-Host ("  Total Repositories: {0}" -f $stats.Total)
    Write-Host ("  Public: {0}" -f $stats.Public)
    Write-Host ("  Private: {0}" -f $stats.Private)
    Write-Host ("  Archived: {0}" -f $stats.Archived)
    Write-Host ("  Forks: {0}" -f $stats.Forks)
    Write-Host ("  Total Stars: {0}" -f $stats.TotalStars)
    Write-Host ""
    
    Write-Host "By Category:" -ForegroundColor Green
    foreach ($cat in $categories.Keys) {
        Write-Host ("  {0}: {1}" -f $cat, $categories[$cat].Count)
    }
    Write-Host ""
    
    Write-Host "Top Repositories by Stars:" -ForegroundColor Green
    $topRepos = $Repos | Sort-Object stargazerCount -Descending | Select-Object -First 10
    foreach ($repo in $topRepos) {
        Write-Host ("  â­{0,-5} {1}" -f $repo.stargazerCount, $repo.name)
    }
}

# Generate organization plan
function New-OrganizationPlan {
    param([array]$Repos, [string]$OutputDir)
    
    $planPath = Join-Path $OutputDir "GITHUB_ORGANIZATION_PLAN.md"
    
    $categories = @{
        "MCP" = @()
        "Tools" = @()
        "Projects" = @()
    }
    
    foreach ($repo in $Repos) {
        $cat = Get-RepositoryCategory -Repo $repo
        $categories[$cat] += $repo
    }
    
    $content = @"
# GitHub Organization Plan - @$Username

**Generated:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Total Repositories:** $($Repos.Count)

## ðŸ“Š Current State

- **Total Repositories:** $($Repos.Count)
- **MCP Servers:** $($categories['MCP'].Count)
- **Tools:** $($categories['Tools'].Count)
- **Projects:** $($categories['Projects'].Count)

## ðŸŽ¯ Organization Strategy

### Option 1: Create GitHub Organization for MCP Servers

**Organization Name:** `sandraschi-mcp` or `sandraschi-mcp-servers`

**Benefits:**
- Better organization and discoverability
- Shared team management
- Centralized documentation
- Easier maintenance

**Repositories to Transfer:**
$($categories['MCP'] | ForEach-Object { "- [$($_.name)]($($_.url))" } | Out-String)

### Option 2: Keep Personal, Organize with Topics

**Benefits:**
- No transfer needed
- Use GitHub topics for organization
- Easier to manage

**Recommended Topics:**
- `mcp-server` - All MCP servers
- `python` - Python projects
- `automation` - Automation tools
- `windows` - Windows-specific tools

## ðŸ“‹ Repository Categories

### MCP Servers ($($categories['MCP'].Count))

$($categories['MCP'] | ForEach-Object { 
    $lang = if ($_.primaryLanguage) { $_.primaryLanguage.name } else { "N/A" }
    "- **[$($_.name)]($($_.url))** - $($_.description) (â­$($_.stargazerCount), $lang)"
} | Out-String)

### Tools ($($categories['Tools'].Count))

$($categories['Tools'] | ForEach-Object { 
    $lang = if ($_.primaryLanguage) { $_.primaryLanguage.name } else { "N/A" }
    "- **[$($_.name)]($($_.url))** - $($_.description) (â­$($_.stargazerCount), $lang)"
} | Out-String)

### Projects ($($categories['Projects'].Count))

$($categories['Projects'] | ForEach-Object { 
    $lang = if ($_.primaryLanguage) { $_.primaryLanguage.name } else { "N/A" }
    "- **[$($_.name)]($($_.url))** - $($_.description) (â­$($_.stargazerCount), $lang)"
} | Out-String)

## ðŸš€ Recommended Actions

1. **Create GitHub Organization** (if transferring MCP servers)
   ```powershell
   cd D:\Dev\repos\mcp-central-docs\scripts\version-control
   .\Organize-GitHubRepos.ps1 -Action CreateOrg -OrgName "sandraschi-mcp"
   ```

2. **Add Topics to Repositories**
   ```powershell
   # Example: Add topic to MCP server
   gh repo edit $Username/repo-name --add-topic "mcp-server"
   ```

3. **Update Repository Descriptions**
   - Ensure all MCP servers have "MCP server" in description
   - Add consistent formatting

4. **Create Organization README**
   - If creating organization, add README.md to organization profile

## ðŸ“ Next Steps

1. Review this plan
2. Decide on organization strategy
3. Execute organization actions
4. Update documentation

---
*Generated by Organize-GitHubRepos.ps1*
"@
    
    $content | Out-File -FilePath $planPath -Encoding UTF8
    Write-Host "Organization plan saved to: $planPath" -ForegroundColor Green
}

# Check if directory is a git repository
function Test-GitRepository {
    param([string]$Path)
    
    $gitPath = Join-Path $Path ".git"
    return (Test-Path $gitPath)
}

# Get git remote URL
function Get-GitRemote {
    param([string]$Path)
    
    if (-not (Test-GitRepository -Path $Path)) {
        return $null
    }
    
    try {
        Push-Location $Path
        $remote = git remote get-url origin 2>$null
        Pop-Location
        return $remote
    } catch {
        Pop-Location
        return $null
    }
}

# Check if remote is GitHub
function Test-GitHubRemote {
    param([string]$RemoteUrl)
    
    if ([string]::IsNullOrEmpty($RemoteUrl)) {
        return $false
    }
    
    return $RemoteUrl -match "github\.com"
}

# Scan local directories for Git/GitHub status
function Scan-LocalDirectories {
    param([string]$LocalPath, [array]$GitHubRepos)
    
    Write-Host "`n" -NoNewline
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "Local Directory Git/GitHub Status Scan" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Scanning: $LocalPath" -ForegroundColor Yellow
    Write-Host ""
    
    if (-not (Test-Path $LocalPath)) {
        Write-Warning "Local path does not exist: $LocalPath"
        return
    }
    
    $directories = Get-ChildItem -Path $LocalPath -Directory | Where-Object {
        # Skip hidden/system directories
        -not $_.Name.StartsWith('.') -and
        -not $_.Name.StartsWith('$')
    }
    
    $results = @{
        HasGit = @()
        HasGitHub = @()
        NoGit = @()
        GitHubNotLocal = @()
        LocalNotGitHub = @()
    }
    
    $githubRepoNames = if ($GitHubRepos) { $GitHubRepos | Select-Object -ExpandProperty name } else { @() }
    
    Write-Host "Scanning $($directories.Count) directories..." -ForegroundColor Yellow
    Write-Host ""
    
    foreach ($dir in $directories) {
        $dirPath = $dir.FullName
        $dirName = $dir.Name
        
        $isGit = Test-GitRepository -Path $dirPath
        $remote = if ($isGit) { Get-GitRemote -Path $dirPath } else { $null }
        $isGitHub = Test-GitHubRemote -RemoteUrl $remote
        
        $status = @{
            Name = $dirName
            Path = $dirPath
            HasGit = $isGit
            HasGitHub = $isGitHub
            Remote = $remote
            OnGitHub = $githubRepoNames -contains $dirName
        }
        
        if ($isGitHub) {
            $results.HasGitHub += $status
        } elseif ($isGit) {
            $results.HasGit += $status
        } else {
            $results.NoGit += $status
        }
        
        if ($isGitHub -and -not ($githubRepoNames -contains $dirName)) {
            $results.LocalNotGitHub += $status
        }
    }
    
    # Find GitHub repos not in local
    if ($GitHubRepos) {
        $localDirNames = $directories | Select-Object -ExpandProperty Name
        $results.GitHubNotLocal = $githubRepoNames | Where-Object { $localDirNames -notcontains $_ }
    }
    
    # Display results
    Write-Host "ðŸ“Š Summary" -ForegroundColor Green
    Write-Host ("  Total Directories: {0}" -f $directories.Count)
    Write-Host ("  âœ… Has Git + GitHub: {0}" -f $results.HasGitHub.Count) -ForegroundColor Green
    Write-Host ("  âš ï¸  Has Git (no GitHub): {0}" -f $results.HasGit.Count) -ForegroundColor Yellow
    Write-Host ("  âŒ No Git: {0}" -f $results.NoGit.Count) -ForegroundColor Red
    Write-Host ""
    
    # Has Git + GitHub
    if ($results.HasGitHub.Count -gt 0) {
        Write-Host "âœ… Has Git + GitHub Remote ($($results.HasGitHub.Count))" -ForegroundColor Green
        Write-Host ("-" * 80) -ForegroundColor DarkGray
        foreach ($item in $results.HasGitHub | Sort-Object Name) {
            $onGitHub = if ($item.OnGitHub) { "âœ“" } else { "âœ-" }
            Write-Host ("  {0,-35} {1} {2}" -f $item.Name, $onGitHub, $item.Remote) -ForegroundColor White
        }
        Write-Host ""
    }
    
    # Has Git but no GitHub
    if ($results.HasGit.Count -gt 0) {
        Write-Host "âš ï¸  Has Git but No GitHub Remote ($($results.HasGit.Count))" -ForegroundColor Yellow
        Write-Host ("-" * 80) -ForegroundColor DarkGray
        foreach ($item in $results.HasGit | Sort-Object Name) {
            $remote = if ($item.Remote) { $item.Remote } else { "(no remote)" }
            Write-Host ("  {0,-35} {1}" -f $item.Name, $remote) -ForegroundColor Yellow
        }
        Write-Host ""
    }
    
    # No Git
    if ($results.NoGit.Count -gt 0) {
        Write-Host "âŒ No Git Repository ($($results.NoGit.Count))" -ForegroundColor Red
        Write-Host ("-" * 80) -ForegroundColor DarkGray
        foreach ($item in $results.NoGit | Sort-Object Name) {
            Write-Host ("  {0}" -f $item.Name) -ForegroundColor DarkGray
        }
        Write-Host ""
    }
    
    # Local repos not on GitHub
    if ($results.LocalNotGitHub.Count -gt 0) {
        Write-Host "ðŸ“¤ Local Git Repos Not on GitHub ($($results.LocalNotGitHub.Count))" -ForegroundColor Cyan
        Write-Host ("-" * 80) -ForegroundColor DarkGray
        foreach ($item in $results.LocalNotGitHub | Sort-Object Name) {
            Write-Host ("  {0,-35} {1}" -f $item.Name, $item.Remote) -ForegroundColor Cyan
        }
        Write-Host ""
    }
    
    # GitHub repos not local
    if ($results.GitHubNotLocal.Count -gt 0) {
        Write-Host "ðŸ“¥ GitHub Repos Not in Local ($($results.GitHubNotLocal.Count))" -ForegroundColor Magenta
        Write-Host ("-" * 80) -ForegroundColor DarkGray
        foreach ($repo in $results.GitHubNotLocal) {
            Write-Host ("  {0}" -f $repo) -ForegroundColor Magenta
        }
        Write-Host ""
    }
    
    return $results
}

# Sync local repos with GitHub
function Sync-LocalRepositories {
    param([array]$Repos, [string]$LocalPath)
    
    Write-Host "`n" -NoNewline
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "Syncing Local Repositories" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host ""
    
    if (-not (Test-Path $LocalPath)) {
        Write-Warning "Local path does not exist: $LocalPath"
        return
    }
    
    # First scan local directories
    $scanResults = Scan-LocalDirectories -LocalPath $LocalPath -GitHubRepos $Repos
    
    # Then show sync comparison
    $localDirs = Get-ChildItem -Path $LocalPath -Directory | Select-Object -ExpandProperty Name
    $githubRepos = $Repos | Select-Object -ExpandProperty name
    
    Write-Host "`n" -NoNewline
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "Sync Comparison" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "Local repositories found: $($localDirs.Count)" -ForegroundColor Yellow
    Write-Host "GitHub repositories: $($githubRepos.Count)" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "Repositories in GitHub but not local:" -ForegroundColor Green
    $missing = $githubRepos | Where-Object { $localDirs -notcontains $_ }
    if ($missing.Count -eq 0) {
        Write-Host "  (none)" -ForegroundColor DarkGray
    } else {
        foreach ($repo in $missing) {
            Write-Host "  - $repo" -ForegroundColor Yellow
        }
    }
    
    Write-Host "`nRepositories local but not on GitHub:" -ForegroundColor Green
    $extra = $localDirs | Where-Object { $githubRepos -notcontains $_ }
    if ($extra.Count -eq 0) {
        Write-Host "  (none)" -ForegroundColor DarkGray
    } else {
        foreach ($repo in $extra) {
            Write-Host "  - $repo" -ForegroundColor Yellow
        }
    }
}

# Main execution
try {
    Write-Host "GitHub Repository Organizer" -ForegroundColor Cyan
    Write-Host "Username: @$Username" -ForegroundColor Gray
    Write-Host ""
    
    if ($Action -ne "CreateOrg" -and $Action -ne "Transfer" -and $Action -ne "ScanLocal") {
        Write-Host "Fetching repositories from GitHub..." -ForegroundColor Yellow
        $repos = Get-GitHubRepositories -User $Username
        
        if ($Category -ne "All") {
            $repos = $repos | Where-Object { (Get-RepositoryCategory -Repo $_) -eq $Category }
        }
    } elseif ($Action -eq "ScanLocal") {
        # For ScanLocal, we still want GitHub repos for comparison
        Write-Host "Fetching repositories from GitHub for comparison..." -ForegroundColor Yellow
        try {
            $repos = Get-GitHubRepositories -User $Username
        } catch {
            Write-Warning "Could not fetch GitHub repositories: $_"
            Write-Host "Continuing with local scan only..." -ForegroundColor Yellow
            $repos = @()
        }
    }
    
    switch ($Action) {
        "List" {
            Show-RepositoryList -Repos $repos -FilterCategory $Category
        }
        "Analyze" {
            Analyze-Repositories -Repos $repos
        }
        "Plan" {
            New-OrganizationPlan -Repos $repos -OutputDir $OutputPath
        }
        "CreateOrg" {
            Write-Host "Creating GitHub organization: $OrgName" -ForegroundColor Yellow
            Write-Host "Note: This requires manual creation via GitHub web interface" -ForegroundColor Yellow
            Write-Host "Visit: https://github.com/organizations/new" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "After creating, you can transfer repositories using:" -ForegroundColor Green
            Write-Host "  gh repo transfer $Username/REPO-NAME --target-org $OrgName" -ForegroundColor White
        }
        "Transfer" {
            Write-Host "Transfer repositories to organization: $OrgName" -ForegroundColor Yellow
            Write-Host "This action requires manual confirmation for each repository." -ForegroundColor Yellow
            Write-Host ""
            Write-Host "To transfer a repository:" -ForegroundColor Green
            Write-Host "  gh repo transfer $Username/REPO-NAME --target-org $OrgName" -ForegroundColor White
        }
        "UpdateDocs" {
            $docPath = Join-Path $OutputPath "sandraschi_github_repositories.md"
            Write-Host "Updating documentation: $docPath" -ForegroundColor Yellow
            # Implementation for updating docs
        }
        "SyncLocal" {
            $localPath = "D:\Dev\repos"
            Sync-LocalRepositories -Repos $repos -LocalPath $localPath
        }
        "ScanLocal" {
            $localPath = "D:\Dev\repos"
            $scanResults = Scan-LocalDirectories -LocalPath $localPath -GitHubRepos $repos
            
            # Optionally save results to file
            if ($OutputPath) {
                $reportPath = Join-Path $OutputPath "LOCAL_GIT_STATUS_REPORT.md"
                $report = @"
# Local Git/GitHub Status Report

**Generated:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Scan Path:** $localPath

## Summary

- **Total Directories:** $($scanResults.HasGitHub.Count + $scanResults.HasGit.Count + $scanResults.NoGit.Count)
- **âœ… Has Git + GitHub:** $($scanResults.HasGitHub.Count)
- **âš ï¸ Has Git (no GitHub):** $($scanResults.HasGit.Count)
- **âŒ No Git:** $($scanResults.NoGit.Count)

## âœ… Has Git + GitHub Remote

$($scanResults.HasGitHub | ForEach-Object { "- **$($_.Name)** - $($_.Remote)" } | Out-String)

## âš ï¸ Has Git but No GitHub Remote

$($scanResults.HasGit | ForEach-Object { 
    $remote = if ($_.Remote) { $_.Remote } else { "(no remote)" }
    "- **$($_.Name)** - $remote"
} | Out-String)

## âŒ No Git Repository

$($scanResults.NoGit | ForEach-Object { "- **$($_.Name)**" } | Out-String)

## ðŸ“¤ Local Git Repos Not on GitHub

$($scanResults.LocalNotGitHub | ForEach-Object { "- **$($_.Name)** - $($_.Remote)" } | Out-String)

## ðŸ“¥ GitHub Repos Not in Local

$($scanResults.GitHubNotLocal | ForEach-Object { "- **$_**" } | Out-String)

---
*Generated by Organize-GitHubRepos.ps1*
"@
                $report | Out-File -FilePath $reportPath -Encoding UTF8
                Write-Host "`nReport saved to: $reportPath" -ForegroundColor Green
            }
        }
    }
    
    Write-Host "`nDone!" -ForegroundColor Green
} catch {
    Write-Error "Error: $_"
    exit 1
}

